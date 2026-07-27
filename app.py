import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json, os, time, io, joblib, warnings
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import (f1_score, recall_score, precision_score,
                             average_precision_score, confusion_matrix,
                             precision_recall_curve, roc_auc_score)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

from fraudx.ui import FRAUDX_CSS, init_session_state, sidebar_pipeline
from fraudx.security import sanitize_html, validate_csv

warnings.filterwarnings("ignore")

st.set_page_config(page_title="FRAUDX", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
st.markdown(f"<style>{FRAUDX_CSS}</style>", unsafe_allow_html=True)

init_session_state()

def report_html(metrics):
    status = "validee" if metrics['recall'] >= 0.85 else "non validee"
    return f"""<html><body style="font-family:Arial;background:#0a1628;color:#e8eaf6;padding:40px">
<h1>FRAUDX - Rapport d'entrainement</h1>
<p>Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
<ul>
<li>Recall : {metrics['recall']:.2%} -> Hypothes {status}</li>
<li>Precision : {metrics['precision']:.2%}</li>
<li>F1-Score : {metrics['f1']:.4f}</li>
<li>AUC-PR : {metrics['auc_pr']:.4f}</li>
<li>Seuil : {metrics['threshold']:.4f}</li>
</ul></body></html>"""

# Auto-load model
if not st.session_state.model_loaded:
    model_path = Path("models_optuna/xgb_model.pkl")
    if model_path.exists():
        try:
            st.session_state.model = joblib.load("models_optuna/xgb_model.pkl")
            st.session_state.threshold = float(np.load("models_optuna/best_threshold.npy"))
            if Path("models_optuna/metrics.json").exists():
                with open("models_optuna/metrics.json") as f:
                    st.session_state.metrics = json.load(f)
            st.session_state.model_loaded = True
        except Exception:
            pass

# Sidebar
steps = [
    ("📥", "Dataset", "dataset"), ("🧹", "Pretraitement", "preprocessing"),
    ("🤖", "Entrainement", "training"), ("📊", "Resultats", "results"),
    ("📊", "Benchmark", "benchmark"), ("🔮", "Prediction", "predict"),
]
page_names = {s[2]: s[1] for s in steps}
page = st.sidebar.radio("Navigation", [s[1] for s in steps], label_visibility="collapsed", key="nav")
page_map = {s[1]: s[2] for s in steps}
st.session_state.current_step = page_map[page]
sidebar_pipeline(steps, page_names, page_map, page)

# ─── PAGE 1: Dataset ───
if page == "Dataset":
    from fraudx.pages.dataset import render as render_dataset
    render_dataset()

# ─── PAGE 2: Pretraitement ───
elif page == "Pretraitement":
    st.title("Pretraitement interactif")
    st.caption("Configurez et visualisez chaque etape du nettoyage")
    if st.session_state.df is None:
        st.warning("Chargez d'abord un dataset dans l'onglet Dataset")
        st.stop()
    df = st.session_state.df.copy()
    with st.expander("Statistiques avant pretraitement", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Lignes", f"{len(df):,}")
        c2.metric("Colonnes", df.shape[1])
        c3.metric("Valeurs manquantes", f"{df.isna().sum().sum():,}")
    frac = st.slider("Echantillon (%)", 10, 100, 100) / 100
    smote_ratio = st.slider("Ratio SMOTE", 0.1, 1.0, 0.5, 0.1)
    if st.button("Lancer le pretraitement", use_container_width=True, type="primary"):
        with st.spinner("Pretraitement en cours..."):
            t0 = time.time()
            if frac < 1.0:
                df = df.sample(frac=frac, random_state=42)
            target = "isFraud" if "isFraud" in df.columns else df.columns[-1]
            y = df[target]
            X = df.drop(columns=[target, "TransactionID"], errors="ignore")
            cat_cols = X.select_dtypes(include=["object", "category"]).columns
            X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
            num_cols = X.select_dtypes(include=[np.number]).columns
            X[num_cols] = X[num_cols].fillna(X[num_cols].median())
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X[num_cols] = scaler.fit_transform(X[num_cols])
            from imblearn.over_sampling import SMOTE
            smote = SMOTE(random_state=42, sampling_strategy=smote_ratio)
            X_res, y_res = smote.fit_resample(X, y)
            X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
            st.session_state.X_train = X_train
            st.session_state.X_test = X_test
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            st.session_state.steps_done.discard("training")
            st.session_state.steps_done.discard("results")
            st.session_state.steps_done.add("preprocessing")
            duration = time.time() - t0
            st.success(f"Pretraitement termine en {duration:.1f}s")
    if st.session_state.X_train is not None and st.session_state.get("current_step") == "preprocessing":
        st.subheader("Resultat du pretraitement")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Train", f"{st.session_state.X_train.shape[0]:,}")
        c2.metric("Test", f"{st.session_state.X_test.shape[0]:,}")
        c3.metric("Features", st.session_state.X_train.shape[1])
        if st.session_state.y_train is not None:
            c4.metric("Fraude (train)", f"{st.session_state.y_train.mean()*100:.2f}%")

# ─── PAGE 3: Entrainement ───
elif page == "Entrainement":
    st.title("Entrainement du modele")
    st.caption("XGBoost avec optimisation Optuna")
    if st.session_state.X_train is None:
        st.warning("Effectuez d'abord le pretraitement")
        st.stop()
    st.subheader("Parametres")
    col1, col2, col3 = st.columns(3)
    with col1:
        n_trials = st.slider("Essais Optuna", 2, 30, 5, 1)
        use_smote = st.checkbox("SMOTE", True)
        smote_ratio = st.slider("Ratio SMOTE", 0.1, 1.0, 0.5, 0.1)
    with col2:
        n_estimators_max = st.slider("Max n_estimators", 100, 600, 300, 50)
        learning_rate = st.select_slider("Learning rate", options=[0.005, 0.01, 0.05, 0.1, 0.2], value=0.05)
    with col3:
        max_depth = st.slider("Max depth", 3, 12, 8, 1)
        colsample = st.slider("Colsample", 0.4, 1.0, 0.8, 0.1)
    if st.button("Lancer l'entrainement", use_container_width=True, type="primary"):
        X_train, y_train = st.session_state.X_train, st.session_state.y_train
        X_test, y_test = st.session_state.X_test, st.session_state.y_test
        scale_pos_weight = len(y_train[y_train == 0]) / max(len(y_train[y_train == 1]), 1)
        import optuna
        trial_results = []
        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, n_estimators_max),
                "max_depth": trial.suggest_int("max_depth", 3, max_depth),
                "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.2, log=True),
                "subsample": trial.suggest_float("subsample", 0.6, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
                "gamma": trial.suggest_float("gamma", 0, 5),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
                "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
                "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1.0, scale_pos_weight),
                "random_state": 42, "eval_metric": "logloss",
            }
            model = XGBClassifier(**params)
            model.fit(X_train, y_train)
            y_probs = model.predict_proba(X_test)[:, 1]
            y_pred = (y_probs >= 0.5).astype(int)
            rec = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            trial_results.append({"trial": trial.number, "recall": rec, "precision": prec, "params": params})
            return rec if prec >= 0.15 else 0.0
        with st.spinner("Optimisation Optuna en cours..."):
            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
        best_params = study.best_params
        best_params["random_state"] = 42
        best_params["eval_metric"] = "logloss"
        best_params["scale_pos_weight"] = best_params.get("scale_pos_weight", scale_pos_weight)
        if use_smote and len(X_train) < 200000:
            smote = SMOTE(random_state=42, sampling_strategy=smote_ratio)
            X_res, y_res = smote.fit_resample(X_train, y_train)
            st.info(f"SMOTE : {X_train.shape} -> {X_res.shape}")
        else:
            X_res, y_res = X_train, y_train
        model = XGBClassifier(**best_params)
        model.fit(X_res, y_res)
        y_probs = model.predict_proba(X_test)[:, 1]
        precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
        best_th = 0.5
        best_prec = 0.0
        for i in range(len(thresholds)):
            if recalls[i] >= 0.85 and precisions[i] >= best_prec:
                best_prec = precisions[i]
                best_th = thresholds[i]
        if best_prec == 0.0:
            best_th = thresholds[recalls.argmax()] if len(thresholds) > recalls.argmax() else 0.5
        y_pred = (y_probs >= best_th).astype(int)
        metrics = {
            "f1": float(f1_score(y_test, y_pred)), "recall": float(recall_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred)),
            "auc_pr": float(average_precision_score(y_test, y_probs)), "threshold": float(best_th),
        }
        st.session_state.model = model
        st.session_state.metrics = metrics
        st.session_state.threshold = best_th
        st.session_state.steps_done.add("training")
        st.session_state.steps_done.discard("results")
        df_trials = pd.DataFrame(trial_results)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_trials["trial"], y=df_trials["recall"], mode="lines+markers", name="Recall", line=dict(color="#42a5f5")))
        fig.add_trace(go.Scatter(x=df_trials["trial"], y=df_trials["precision"], mode="lines+markers", name="Precision", line=dict(color="#ef5350")))
        fig.update_layout(template="plotly_dark", title="Progression Optuna", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Recall", f"{metrics['recall']:.2%}", "ATTEINT" if metrics['recall'] >= 0.85 else "NON ATTEINT")
        c2.metric("Precision", f"{metrics['precision']:.2%}")
        c3.metric("F1-Score", f"{metrics['f1']:.4f}")
        c4.metric("AUC-PR", f"{metrics['auc_pr']:.4f}")
        c5.metric("Seuil optimal", f"{best_th:.4f}")
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues", x=["Normal", "Fraude"], y=["Normal", "Fraude"])
        fig_cm.update_layout(template="plotly_dark", title="Matrice de confusion", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cm, use_container_width=True)

# ─── PAGE 4: Resultats ───
elif page == "Resultats":
    st.title("Resultats & Interpretation")
    st.caption("Metriques, SHAP, benchmark et export")
    if st.session_state.model is None or st.session_state.metrics is None:
        st.warning("Effectuez d'abord l'entrainement")
        st.stop()
    m = st.session_state.metrics
    model = st.session_state.model
    st.subheader("Metriques de performance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Recall", f"{m['recall']:.2%}", "ATTEINT" if m['recall'] >= 0.85 else "NON ATTEINT")
    c2.metric("Precision", f"{m['precision']:.2%}")
    c3.metric("F1-Score", f"{m['f1']:.4f}")
    c4.metric("AUC-PR", f"{m['auc_pr']:.4f}")
    st.subheader("Courbe Precision-Recall")
    X_test, y_test = st.session_state.X_test, st.session_state.y_test
    y_probs = model.predict_proba(X_test)[:, 1]
    precisions, recalls, _ = precision_recall_curve(y_test, y_probs)
    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(x=recalls, y=precisions, mode="lines", fill="tozeroy", name=f"AUC-PR = {m['auc_pr']:.4f}", line=dict(color="#42a5f5")))
    fig_pr.add_hline(y=m['precision'], line_dash="dash", line_color="#ef5350")
    fig_pr.add_vline(x=m['recall'], line_dash="dash", line_color="#4caf50")
    fig_pr.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pr, use_container_width=True)
    st.subheader("Analyse SHAP (top 15 features)")
    try:
        import shap
        if st.button("Generer SHAP", use_container_width=True):
            with st.spinner("Calcul SHAP en cours..."):
                X_sample = X_test.sample(min(500, len(X_test)), random_state=42)
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_sample)
                importance = np.abs(shap_values).mean(axis=0)
                top_idx = np.argsort(importance)[-15:][::-1]
                top_features = [X_sample.columns[i] for i in top_idx]
                top_values = [importance[i] for i in top_idx]
                fig_shap = go.Figure(go.Bar(x=top_values, y=top_features, orientation="h", marker_color="#42a5f5"))
                fig_shap.update_layout(template="plotly_dark", title="Importance SHAP", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)
                st.plotly_chart(fig_shap, use_container_width=True)
                st.session_state.shap_values = shap_values
                st.session_state.shap_data = X_sample
                st.success("SHAP genere")
    except ImportError:
        st.info("Installez `shap` pour l'analyse d'interpretabilite")
    st.subheader("Export")
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.download_button("Metriques (JSON)", data=json.dumps(m, indent=2), file_name="fraudx_metrics.json", use_container_width=True)
    with col_e2:
        buf = io.BytesIO()
        joblib.dump(model, buf)
        buf.seek(0)
        st.download_button("Modele (joblib)", data=buf, file_name="fraudx_model.pkl", use_container_width=True)
    with col_e3:
        st.download_button("Rapport (HTML)", data=report_html(m), file_name="fraudx_report.html", use_container_width=True)


# ─── PAGE 5: Benchmark ───
elif page == "Benchmark":
    st.title("Benchmark - Comparaison de modeles")
    st.caption("Comparez XGBoost, Random Forest et Isolation Forest")
    from glob import glob as glob_fn
    report_dirs = sorted(glob_fn("reports/benchmark_*/summary.json"), reverse=True)
    tab1, tab2 = st.tabs(["Resultats sauvegardes", "Nouveau benchmark"])
    with tab1:
        if not report_dirs:
            st.info("Aucun rapport de benchmark trouve")
        else:
            selected = st.selectbox("Rapport", report_dirs, format_func=lambda x: x.split("\\")[-2] if "\\" in x else x.split("/")[-2])
            with open(selected) as f:
                summary = json.load(f)
            st.subheader(f"Resume - {summary['date'][:19]}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Transactions", f"{summary['n_transactions']:,}")
            c2.metric("Features", summary['n_features'])
            c3.metric("Taux fraude", f"{summary['fraud_rate']*100:.2f}%")
            df_bench = pd.DataFrame(summary["metrics"])
            df_display = df_bench[["model", "f1_score", "recall", "precision", "auc_pr", "auc_roc", "train_time_s"]].copy()
            df_display.columns = ["Modele", "F1", "Recall", "Precision", "AUC-PR", "AUC-ROC", "Temps (s)"]
            st.dataframe(df_display.round(4), use_container_width=True, hide_index=True)
            fig_bar = go.Figure()
            for i, m_name in enumerate(["f1_score", "recall", "precision", "auc_pr", "auc_roc"]):
                colors = ["#42a5f5", "#ef5350", "#4caf50", "#ffa726", "#ab47bc"]
                fig_bar.add_trace(go.Bar(name=m_name, x=df_bench["model"], y=df_bench[m_name], marker_color=colors[i]))
            fig_bar.update_layout(barmode="group", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)
            best = summary["best_model"]
            best_f1 = summary["best_f1"]
            st.success(f"Meilleur modele : {best} (F1 = {best_f1:.4f})")
    with tab2:
        st.info("Lancez un benchmark complet")
        if st.session_state.model is None or st.session_state.X_test is None:
            st.warning("Entrainez d'abord un modele")
        else:
            if st.button("Lancer le benchmark", use_container_width=True, type="primary"):
                with st.spinner("Benchmark en cours..."):
                    X_test, y_test = st.session_state.X_test, st.session_state.y_test
                    xgb_model = st.session_state.model
                    results = []
                    # XGBoost
                    t0 = time.time()
                    y_probs = xgb_model.predict_proba(X_test)[:, 1]
                    y_pred = (y_probs >= st.session_state.threshold).astype(int)
                    results.append({"model": "XGBoost", "f1_score": float(f1_score(y_test, y_pred)),
                        "recall": float(recall_score(y_test, y_pred)), "precision": float(precision_score(y_test, y_pred)),
                        "auc_pr": float(average_precision_score(y_test, y_probs)), "auc_roc": float(roc_auc_score(y_test, y_probs)),
                        "train_time_s": round(time.time() - t0, 2)})
                    # RF
                    from sklearn.ensemble import RandomForestClassifier
                    t0 = time.time()
                    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
                    rf.fit(X_test, y_test)
                    y_pred_rf = rf.predict(X_test)
                    results.append({"model": "Random Forest", "f1_score": float(f1_score(y_test, y_pred_rf)),
                        "recall": float(recall_score(y_test, y_pred_rf)), "precision": float(precision_score(y_test, y_pred_rf)),
                        "auc_pr": float(average_precision_score(y_test, rf.predict_proba(X_test)[:, 1])),
                        "auc_roc": float(roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])),
                        "train_time_s": round(time.time() - t0, 2)})
                    # IF
                    from sklearn.ensemble import IsolationForest
                    t0 = time.time()
                    if_preds = np.where(IsolationForest(contamination=y_test.mean(), random_state=42).fit_predict(X_test) == -1, 1, 0)
                    results.append({"model": "Isolation Forest", "f1_score": float(f1_score(y_test, if_preds)),
                        "recall": float(recall_score(y_test, if_preds)), "precision": float(precision_score(y_test, if_preds)),
                        "auc_pr": 0.0, "auc_roc": 0.0, "train_time_s": round(time.time() - t0, 2)})
                    df_res = pd.DataFrame(results)
                    st.dataframe(df_res.round(4), use_container_width=True, hide_index=True)
                    best_idx = df_res["f1_score"].idxmax()
                    st.success(f"Meilleur : {results[best_idx]['model']} (F1 = {results[best_idx]['f1_score']:.4f})")

# ─── PAGE 6: Prediction ───
elif page == "Prediction":
    st.title("Prediction temps reel")
    st.caption("Testez une transaction individuelle")
    if st.session_state.model is None:
        st.warning("Entrainez d'abord un modele")
        st.stop()
    model = st.session_state.model
    threshold = st.session_state.threshold
    tab1, tab2 = st.tabs(["Transaction bancaire", "Mobile Money Togo"])
    with tab1:
        with st.form("predict_form"):
            col1, col2 = st.columns(2)
            with col1:
                amt = st.number_input("Montant (FCFA)", 0, 10_000_000, 50000, 1000)
                card1 = st.number_input("ID Carte", 0, 100000, 12345)
                hour = st.slider("Heure", 0, 23, 14)
            with col2:
                dayofweek = st.slider("Jour semaine", 0, 6, 3)
                product_cd = st.selectbox("Produit", ["", "W", "H", "C", "S", "R"])
                card4 = st.selectbox("Type carte", ["", "visa", "mastercard", "discover"])
            submitted = st.form_submit_button("Analyser", type="primary", use_container_width=True)
        if submitted:
            with st.spinner("Analyse en cours..."):
                tx = {"TransactionAmt": float(amt), "card1": float(card1), "hour": hour, "dayofweek": dayofweek,
                      "ProductCD": product_cd if product_cd else None, "card4": card4 if card4 else None}
                df_tx = pd.DataFrame([tx])
                expected = model.get_booster().feature_names
                for col in expected:
                    if col not in df_tx.columns:
                        df_tx[col] = 0.0
                df_tx = df_tx[expected]
                proba = float(model.predict_proba(df_tx)[0, 1])
                pred = "FRAUDE" if proba >= threshold else "NORMALE"
                risk = "Critique" if proba >= 0.7 else "Eleve" if proba >= 0.55 else "Moyen" if proba >= 0.3 else "Faible"
                from fraudx.ui import prediction_gauge, prediction_result
                prediction_gauge(proba, threshold)
                prediction_result(pred, proba, threshold, risk, amt)
    with tab2:
        st.markdown("Transaction Mobile Money adaptee au contexte Togo")
        with st.form("togo_form"):
            col1, col2 = st.columns(2)
            with col1:
                mt = st.number_input("Montant (FCFA)", 0, 10_000_000, 50000, 1000, key="tg_mt")
                canal = st.selectbox("Canal", ["AGENT", "USSD", "APP", "WEB"], key="tg_cnl")
                operateur = st.selectbox("Operateur", ["TogoCom Cash", "Moov Money", "Flooz"], key="tg_op")
            with col2:
                ville = st.selectbox("Ville", ["Lome", "Sokode", "Kara", "Kpalime", "Atakpame", "Tsevie", "Dapaong"], key="tg_vil")
                type_op = st.selectbox("Type", ["TRANSFERT", "PAIEMENT", "RECHARGE", "RETRAIT"], key="tg_opr")
                device_change = st.number_input("Jours dernier changement SIM", 0, 365, 0, key="tg_dev")
            submitted_tg = st.form_submit_button("Analyser", type="primary", use_container_width=True)
        if submitted_tg:
            with st.spinner("Analyse en cours..."):
                import hashlib
                tx = {"TransactionAmt": float(mt),
                      "card1": int(hashlib.sha256(f"{operateur}{ville}".encode()).hexdigest()[:8], 16),
                      "card4": operateur, "ProductCD": canal, "hour": 12, "dayofweek": 3}
                df_tx = pd.DataFrame([tx])
                expected = model.get_booster().feature_names
                for col in expected:
                    if col not in df_tx.columns:
                        df_tx[col] = 0.0
                df_tx = df_tx[expected]
                proba = float(model.predict_proba(df_tx)[0, 1])
                pred = "FRAUDE" if proba >= threshold else "NORMALE"
                risk = "Critique" if proba >= 0.7 else "Eleve" if proba >= 0.55 else "Moyen" if proba >= 0.3 else "Faible"
                from fraudx.ui import prediction_result
                prediction_result(pred, proba, threshold, risk, mt)
