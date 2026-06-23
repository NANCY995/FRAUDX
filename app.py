#!/usr/bin/env python3
"""
FRAUDX — Application unifiée de détection de fraude bancaire
Interface interactive : Dataset → Prétraitement → Entraînement → Résultats → Prédiction

Usage:
    streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json, os, time, io, sys, joblib, warnings
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import (f1_score, recall_score, precision_score,
                             average_precision_score, confusion_matrix,
                             precision_recall_curve, roc_auc_score)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore")

st.set_page_config(page_title="FRAUDX", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# ─── CSS ───
st.markdown("""<style>
    [data-testid="metric-container"] { background: #111d2e; border:1px solid #1a3a5c; border-radius:12px; padding:12px 16px; }
    [data-testid="stSidebar"] { background: #0a1628; border-right:1px solid #1a3a5c; }
    .step-active { border-left:4px solid #42a5f5; background:#111d2e; padding:10px; border-radius:4px; margin:4px 0; }
    .step-done { border-left:4px solid #4caf50; background:#111d2e; padding:10px; border-radius:4px; margin:4px 0; }
    .step-pending { border-left:4px solid #455a64; background:#111d2e; padding:10px; border-radius:4px; margin:4px 0; }
    .stApp { background: #0a1628; }
</style>""", unsafe_allow_html=True)

# ─── Session State ───
if "df" not in st.session_state: st.session_state.df = None
if "df_name" not in st.session_state: st.session_state.df_name = ""
if "X_train" not in st.session_state: st.session_state.X_train = None
if "X_test" not in st.session_state: st.session_state.X_test = None
if "y_train" not in st.session_state: st.session_state.y_train = None
if "y_test" not in st.session_state: st.session_state.y_test = None
if "model" not in st.session_state: st.session_state.model = None
if "metrics" not in st.session_state: st.session_state.metrics = None
if "preprocessor" not in st.session_state: st.session_state.preprocessor = None
if "threshold" not in st.session_state: st.session_state.threshold = 0.5
if "steps_done" not in st.session_state: st.session_state.steps_done = set()
if "optuna_progress" not in st.session_state: st.session_state.optuna_progress = []
if "shap_values" not in st.session_state: st.session_state.shap_values = None
if "shap_data" not in st.session_state: st.session_state.shap_data = None
if "model_loaded" not in st.session_state: st.session_state.model_loaded = False

# ─── Sidebar — Navigation & Progress ───
st.sidebar.markdown("<h1 style='text-align:center;'>🛡️ FRAUDX</h1>", unsafe_allow_html=True)
st.sidebar.caption("Détection de fraude bancaire par IA")

steps = [
    ("📥", "Dataset", "dataset"),
    ("🧹", "Prétraitement", "preprocessing"),
    ("🤖", "Entraînement", "training"),
    ("📊", "Résultats", "results"),
    ("📊", "Benchmark", "benchmark"),
    ("🔮", "Prédiction", "predict"),
]
page_names = {s[2]: s[1] for s in steps}

st.sidebar.markdown("---\n### Pipeline")
for icon, name, key in steps:
    if key in st.session_state.steps_done:
        st.sidebar.markdown(f'<div class="step-done">✅ {icon} {name}</div>', unsafe_allow_html=True)
    elif key == st.session_state.get("current_step"):
        st.sidebar.markdown(f'<div class="step-active">▶️ {icon} {name}</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f'<div class="step-pending">{icon} {name}</div>', unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", [s[1] for s in steps], label_visibility="collapsed", key="nav")
page_map = {s[1]: s[2] for s in steps}
st.session_state.current_step = page_map[page]

st.sidebar.markdown("---")
if st.session_state.df is not None:
    st.sidebar.metric("Dataset", st.session_state.df_name, f"{len(st.session_state.df):,} lignes")
if st.session_state.model is not None:
    st.sidebar.metric("Modèle", "XGBoost entraîné ✅")
    if st.session_state.metrics:
        st.sidebar.metric("Recall", f"{st.session_state.metrics['recall']:.2%}")
st.sidebar.caption(f"Mise à jour : {datetime.now().strftime('%H:%M')}")

# =====================================================================
# PAGE 1 : ACCUEIL / DATASET
# =====================================================================
if page == "Dataset":
    st.title("📥 Chargement du dataset")
    st.caption("Importez vos transactions bancaires ou utilisez un dataset de référence")

    col1, col2 = st.columns(2)
    with col1:
        source = st.radio("Source", ["IEEE-CIS Fraud Detection (Kaggle)", "Credit Card Fraud (ULB)", "Upload CSV"], index=0)
    with col2:
        if source == "Upload CSV":
            uploaded = st.file_uploader("Choisir un fichier CSV", type="csv")
        else:
            n_rows = st.number_input("Nombre de lignes", 10000, 590540, 100000, step=10000)

    if st.button(" Charger le dataset", use_container_width=True, type="primary"):
        with st.spinner("Chargement en cours..."):
            try:
                if source.startswith("IEEE"):
                    path = Path("data/train_transaction.csv")
                    id_path = Path("data/train_identity.csv")
                    if not path.exists():
                        st.error("Fichier non trouvé. Placez train_transaction.csv dans data/")
                        st.stop()
                    df = pd.read_csv(path, nrows=n_rows)
                    if id_path.exists():
                        identity = pd.read_csv(id_path, nrows=n_rows)
                        df = df.merge(identity, on="TransactionID", how="left")
                    st.session_state.df_name = f"IEEE-CIS ({len(df):,} lignes)"
                elif source.startswith("Credit"):
                    path = Path("data/creditcard.csv")
                    if not path.exists():
                        st.error("Fichier non trouvé. Placez creditcard.csv dans data/")
                        st.stop()
                    df = pd.read_csv(path, nrows=n_rows)
                    st.session_state.df_name = f"Credit Card ({len(df):,} lignes)"
                else:
                    df = pd.read_csv(uploaded)
                    st.session_state.df_name = uploaded.name

                st.session_state.df = df
                st.session_state.steps_done.discard("preprocessing")
                st.session_state.steps_done.discard("training")
                st.session_state.steps_done.discard("results")
                st.session_state.steps_done.add("dataset")
                st.session_state.model = None
                st.session_state.metrics = None
                st.rerun()
            except Exception as e:
                st.error(f"Erreur : {e}")

    if st.session_state.df is not None:
        df = st.session_state.df
        st.success(f"Dataset : {st.session_state.df_name}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Lignes", f"{len(df):,}")
        c2.metric("Colonnes", df.shape[1])
        c3.metric("Taille mémoire", f"{df.memory_usage(deep=True).sum()/1024**2:.1f} Mo")

        fraud_rate = df["isFraud"].mean() * 100 if "isFraud" in df.columns else 0
        c4.metric("Taux fraude", f"{fraud_rate:.2f}%" if fraud_rate > 0 else "N/A")

        with st.expander(" Aperçu des données", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)
        with st.expander("📊 Statistiques descriptives"):
            st.dataframe(df.describe(), use_container_width=True)

# =====================================================================
# PAGE 2 : PRÉTRAITEMENT
# =====================================================================
elif page == "Prétraitement":
    st.title("🧹 Prétraitement interactif")
    st.caption("Configurez et visualisez chaque étape du nettoyage")

    if st.session_state.df is None:
        st.warning(" Chargez d'abord un dataset dans l'onglet Dataset")
        st.stop()

    df = st.session_state.df.copy()

    with st.expander("📋 Statistiques avant prétraitement", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Lignes", f"{len(df):,}")
        c2.metric("Colonnes", df.shape[1])
        missing_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
        c3.metric("Valeurs manquantes", f"{missing_ratio:.1f}%")

    # Configuration interactive
    st.subheader("⚙️ Configuration")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        nan_threshold = st.slider("Suppression colonnes > X% NaN", 50, 100, 90, 5)
        do_smote = st.checkbox("SMOTE (rééquilibrage classes)", True)
    with col_b:
        smote_ratio = st.slider("Ratio SMOTE (fraude/non-fraude)", 0.1, 1.0, 0.5, 0.1)
        test_size = st.slider("Test size (%)", 10, 40, 20, 5)
    with col_c:
        do_scaling = st.checkbox("Standardisation (Z-score)", True)
        do_feat_eng = st.checkbox("Feature engineering avancé", True)

    if st.button("🚀 Lancer le prétraitement", use_container_width=True, type="primary"):
        with st.spinner("Prétraitement en cours..."):
            t0 = time.time()
            progress = st.progress(0)

            # 1. Drop high-NaN columns
            missing = (df.isnull().sum() / len(df) * 100)
            drop_cols = missing[missing > nan_threshold].index.tolist()
            df = df.drop(columns=drop_cols)
            progress.progress(20)

            # 2. Feature engineering
            if do_feat_eng:
                if "TransactionDT" in df.columns:
                    start_ts = pd.Timestamp("2017-12-01")
                    dt = start_ts + pd.to_timedelta(df["TransactionDT"], unit="s")
                    df["hour"] = dt.dt.hour.fillna(0).astype(int)
                    df["dayofweek"] = dt.dt.dayofweek.fillna(0).astype(int)
                    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
                if "TransactionAmt" in df.columns:
                    df["log_amount"] = np.log1p(df["TransactionAmt"].fillna(0))
                    df["amt_100_ratio"] = df["TransactionAmt"].fillna(0) / 100
            progress.progress(40)

            # 3. Separate target
            y = df["isFraud"].values if "isFraud" in df.columns else None
            X = df.drop(columns=["isFraud", "TransactionID"], errors="ignore")

            num_cols = X.select_dtypes(include=np.number).columns.tolist()
            cat_cols = X.select_dtypes(include="object").columns.tolist()
            progress.progress(60)

            # 4. Train/Test split
            if y is not None:
                X_train, X_test, y_train, y_test = train_test_split(
                    X[num_cols + cat_cols], y, test_size=test_size/100,
                    stratify=y, random_state=42
                )
            else:
                st.error("Colonne 'isFraud' non trouvée dans le dataset")
                st.stop()

            # 5. Imputation
            num_imp = SimpleImputer(strategy="median")
            cat_imp = SimpleImputer(strategy="most_frequent")

            X_train_num = pd.DataFrame(num_imp.fit_transform(X_train[num_cols]), columns=num_cols, index=X_train.index)
            X_test_num = pd.DataFrame(num_imp.transform(X_test[num_cols]), columns=num_cols, index=X_test.index)
            X_train_cat = pd.DataFrame(cat_imp.fit_transform(X_train[cat_cols]), columns=cat_cols, index=X_train.index)
            X_test_cat = pd.DataFrame(cat_imp.transform(X_test[cat_cols]), columns=cat_cols, index=X_test.index)
            progress.progress(80)

            # 6. Encoding
            ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore") if cat_cols else None
            if ohe:
                train_ohe = ohe.fit_transform(X_train_cat)
                test_ohe = ohe.transform(X_test_cat)
                ohe_cols = ohe.get_feature_names_out(cat_cols)
                X_train_cat = pd.DataFrame(train_ohe, columns=ohe_cols, index=X_train.index)
                X_test_cat = pd.DataFrame(test_ohe, columns=ohe_cols, index=X_test.index)

            X_train_proc = pd.concat([X_train_num, X_train_cat], axis=1)
            X_test_proc = pd.concat([X_test_num, X_test_cat], axis=1)

            # 7. Scaling
            if do_scaling:
                scaler = StandardScaler()
                scalable = [c for c in num_cols if c in X_train_proc.columns]
                X_train_proc[scalable] = scaler.fit_transform(X_train_proc[scalable])
                X_test_proc[scalable] = scaler.transform(X_test_proc[scalable])

            progress.progress(100)

            st.session_state.X_train = X_train_proc
            st.session_state.X_test = X_test_proc
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            st.session_state.preprocessor = {"scaler": scaler if do_scaling else None, "ohe": ohe, "num_cols": num_cols}
            st.session_state.steps_done.add("dataset")
            st.session_state.steps_done.add("preprocessing")
            st.session_state.steps_done.discard("training")
            st.session_state.steps_done.discard("results")

            duration = time.time() - t0
            st.success(f"✅ Prétraitement terminé en {duration:.1f}s")

    # Afficher les résultats si déjà prétraité
    if st.session_state.X_train is not None and st.session_state.get("current_step") == "preprocessing":
        st.subheader("📊 Résultat du prétraitement")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Train", f"{st.session_state.X_train.shape[0]:,}")
        c2.metric("Test", f"{st.session_state.X_test.shape[0]:,}")
        c3.metric("Features", st.session_state.X_train.shape[1])
        if st.session_state.y_train is not None:
            c4.metric("Fraude (train)", f"{st.session_state.y_train.mean()*100:.2f}%")

# =====================================================================
# PAGE 3 : ENTRAÎNEMENT
# =====================================================================
elif page == "Entraînement":
    st.title("🤖 Entraînement du modèle")
    st.caption("XGBoost avec optimisation Optuna")

    if st.session_state.X_train is None:
        st.warning(" Effectuez d'abord le prétraitement")
        st.stop()

    st.subheader("⚙️ Paramètres")
    col1, col2, col3 = st.columns(3)
    with col1:
        n_trials = st.slider("Essais Optuna", 5, 100, 20, 5)
        use_smote = st.checkbox("SMOTE", True)
    with col2:
        n_estimators_max = st.slider("Max n_estimators", 100, 600, 300, 50)
        learning_rate = st.select_slider("Learning rate", options=[0.005, 0.01, 0.05, 0.1, 0.2], value=0.05)
    with col3:
        max_depth = st.slider("Max depth", 3, 12, 8, 1)
        colsample = st.slider("Colsample", 0.4, 1.0, 0.8, 0.1)

    if st.button("🚀 Lancer l'entraînement", use_container_width=True, type="primary"):
        X_train = st.session_state.X_train
        y_train = st.session_state.y_train
        X_test = st.session_state.X_test
        y_test = st.session_state.y_test

        scale_pos_weight = len(y_train[y_train == 0]) / max(len(y_train[y_train == 1]), 1)
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        plot_placeholder = st.empty()

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
                "random_state": 42, "eval_metric": "logloss"
            }
            model = XGBClassifier(**params)
            model.fit(X_train, y_train)
            y_probs = model.predict_proba(X_test)[:, 1]
            y_pred = (y_probs >= 0.5).astype(int)
            rec = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            res = {"trial": trial.number, "recall": rec, "precision": prec, "params": params}
            trial_results.append(res)
            return rec if prec >= 0.15 else 0.0

        with st.spinner("Optimisation Optuna en cours..."):
            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=n_trials, show_progress_bar=False)

            best_params = study.best_params
            status_placeholder.success(f"Meilleur Recall (CV) : {study.best_value:.4f}")

        # Train final model
        st.subheader("📈 Entraînement du modèle final")
        best_params["random_state"] = 42
        best_params["eval_metric"] = "logloss"
        best_params["scale_pos_weight"] = best_params.get("scale_pos_weight", scale_pos_weight)

        if use_smote and len(X_train) < 200000:
            smote = SMOTE(random_state=42, sampling_strategy=0.5)
            X_res, y_res = smote.fit_resample(X_train, y_train)
            st.info(f"SMOTE : {X_train.shape} → {X_res.shape}")
        else:
            X_res, y_res = X_train, y_train

        model = XGBClassifier(**best_params)
        model.fit(X_res, y_res)

        # Threshold optimization
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
            "f1": float(f1_score(y_test, y_pred)),
            "recall": float(recall_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred)),
            "auc_pr": float(average_precision_score(y_test, y_probs)),
            "threshold": float(best_th)
        }

        st.session_state.model = model
        st.session_state.metrics = metrics
        st.session_state.threshold = best_th
        st.session_state.steps_done.add("training")
        st.session_state.steps_done.discard("results")

        # Plot Optuna history
        df_trials = pd.DataFrame(trial_results)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_trials["trial"], y=df_trials["recall"], mode="lines+markers",
                                 name="Recall", line=dict(color="#42a5f5")))
        fig.add_trace(go.Scatter(x=df_trials["trial"], y=df_trials["precision"], mode="lines+markers",
                                 name="Precision", line=dict(color="#ef5350")))
        fig.update_layout(template="plotly_dark", title="Progression Optuna",
                          xaxis_title="Essai", yaxis_title="Score",
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        plot_placeholder.plotly_chart(fig, use_container_width=True)

        # Show metrics
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Recall", f"{metrics['recall']:.2%}", "✅" if metrics['recall'] >= 0.85 else "❌")
        c2.metric("Precision", f"{metrics['precision']:.2%}")
        c3.metric("F1-Score", f"{metrics['f1']:.4f}")
        c4.metric("AUC-PR", f"{metrics['auc_pr']:.4f}")
        c5.metric("Seuil optimal", f"{best_th:.4f}")

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                           x=["Normal", "Fraude"], y=["Normal", "Fraude"],
                           labels=dict(x="Prédit", y="Réel", color="Count"))
        fig_cm.update_layout(template="plotly_dark", title="Matrice de confusion",
                             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cm, use_container_width=True)

# =====================================================================
# PAGE 4 : RÉSULTATS
# =====================================================================
elif page == "Résultats":
    st.title("📊 Résultats & Interprétation")
    st.caption("Métriques, SHAP, benchmark et export")

    if st.session_state.model is None or st.session_state.metrics is None:
        st.warning(" Effectuez d'abord l'entraînement")
        st.stop()

    metrics = st.session_state.metrics
    model = st.session_state.model

    # KPIs
    st.subheader("🎯 Métriques de performance")
    recall_ok = "✅ ATTEINT" if metrics['recall'] >= 0.85 else "❌ NON ATTEINT"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Recall", f"{metrics['recall']:.2%}", recall_ok)
    c2.metric("Precision", f"{metrics['precision']:.2%}")
    c3.metric("F1-Score", f"{metrics['f1']:.4f}")
    c4.metric("AUC-PR", f"{metrics['auc_pr']:.4f}")

    # Courbe PR interactive
    st.subheader("📈 Courbe Precision-Recall")
    X_test, y_test = st.session_state.X_test, st.session_state.y_test
    y_probs = model.predict_proba(X_test)[:, 1]
    precisions, recalls, _ = precision_recall_curve(y_test, y_probs)

    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(x=recalls, y=precisions, mode="lines", fill="tozeroy",
                                name=f"AUC-PR = {metrics['auc_pr']:.4f}", line=dict(color="#42a5f5")))
    fig_pr.add_hline(y=metrics['precision'], line_dash="dash", line_color="#ef5350",
                     annotation_text=f"Precision={metrics['precision']:.3f}")
    fig_pr.add_vline(x=metrics['recall'], line_dash="dash", line_color="#4caf50",
                     annotation_text=f"Recall={metrics['recall']:.3f}")
    fig_pr.update_layout(template="plotly_dark", xaxis_title="Recall", yaxis_title="Precision",
                         paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pr, use_container_width=True)

    # SHAP
    st.subheader("🔮 Analyse SHAP (top 15 features)")
    try:
        import shap
        if st.button(" Générer SHAP", use_container_width=True):
            with st.spinner("Calcul SHAP en cours..."):
                X_sample = X_test.sample(min(500, len(X_test)), random_state=42)
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_sample)

                importance = np.abs(shap_values).mean(axis=0)
                top_idx = np.argsort(importance)[-15:][::-1]
                top_features = [X_sample.columns[i] for i in top_idx]
                top_values = [importance[i] for i in top_idx]

                fig_shap = go.Figure(go.Bar(x=top_values, y=top_features, orientation="h",
                                            marker_color="#42a5f5"))
                fig_shap.update_layout(template="plotly_dark", title="Importance SHAP (moyenne |SHAP|)",
                                       xaxis_title="|SHAP value|",
                                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       height=500)
                st.plotly_chart(fig_shap, use_container_width=True)

                st.session_state.shap_values = shap_values
                st.session_state.shap_data = X_sample
                st.success("SHAP généré ✅")
    except ImportError:
        st.info("Installez `shap` pour l'analyse d'interprétabilité")

    # Export
    st.subheader("📤 Export")
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        report_json = json.dumps(metrics, indent=2)
        st.download_button("📥 Métriques (JSON)", data=report_json, file_name="fraudx_metrics.json", use_container_width=True)
    with col_e2:
        # Generate report HTML
        recall_status = "validée" if metrics['recall'] >= 0.85 else "non validée"
        report_html = f"""<html><body style="font-family:Arial;background:#0a1628;color:#e8eaf6;padding:40px">
<h1>🛡️ FRAUDX — Rapport d'entraînement</h1>
<p>Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
<h2>Métriques</h2>
<ul>
<li>Recall : {metrics['recall']:.2%} → Hypothèse {recall_status}</li>
<li>Precision : {metrics['precision']:.2%}</li>
<li>F1-Score : {metrics['f1']:.4f}</li>
<li>AUC-PR : {metrics['auc_pr']:.4f}</li>
<li>Seuil : {metrics['threshold']:.4f}</li>
</ul>
<p>Généré par FRAUDX</p></body></html>"""
        st.download_button("📥 Rapport (HTML)", data=report_html, file_name="fraudx_report.html", use_container_width=True)

# =====================================================================
# PAGE 5 : BENCHMARK
# =====================================================================
elif page == "Benchmark":
    st.title("📊 Benchmark — Comparaison de modèles")
    st.caption("Comparez XGBoost, Random Forest et Isolation Forest sur le jeu de test")

    import json, csv, glob as glob_mod

    # Discover existing benchmark reports
    report_dirs = sorted(glob_mod.glob("reports/benchmark_*/summary.json"), reverse=True)

    tab1, tab2 = st.tabs(["📈 Résultats sauvegardés", "🚀 Nouveau benchmark"])

    with tab1:
        if not report_dirs:
            st.info("Aucun rapport de benchmark trouvé dans reports/benchmark_*/")
        else:
            selected = st.selectbox("Rapport", report_dirs, format_func=lambda x: x.split("\\")[-2] if "\\" in x else x.split("/")[-2])
            with open(selected) as f:
                summary = json.load(f)

            st.subheader(f"📋 Résumé — {summary['date'][:19]}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Transactions", f"{summary['n_transactions']:,}")
            c2.metric("Features", summary['n_features'])
            c3.metric("Taux fraude", f"{summary['fraud_rate']*100:.2f}%")

            df_bench = pd.DataFrame(summary["metrics"])
            df_display = df_bench[["model", "f1_score", "recall", "precision", "auc_pr", "auc_roc", "train_time_s"]].copy()
            df_display.columns = ["Modèle", "F1", "Recall", "Precision", "AUC-PR", "AUC-ROC", "Temps (s)"]
            df_display = df_display.round(4)

            st.dataframe(df_display, use_container_width=True, hide_index=True)

            st.subheader("📊 Comparaison visuelle")
            col_a, col_b = st.columns(2)

            with col_a:
                fig_bar = go.Figure()
                metrics_names = ["f1_score", "recall", "precision", "auc_pr", "auc_roc"]
                labels = ["F1", "Recall", "Precision", "AUC-PR", "AUC-ROC"]
                colors = ["#42a5f5", "#ef5350", "#4caf50", "#ffa726", "#ab47bc"]
                for i, m in enumerate(metrics_names):
                    fig_bar.add_trace(go.Bar(name=labels[i], x=df_bench["model"], y=df_bench[m], marker_color=colors[i]))
                fig_bar.update_layout(barmode="group", template="plotly_dark", title="Métriques par modèle",
                                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_b:
                fig_time = go.Figure()
                fig_time.add_trace(go.Bar(x=df_bench["model"], y=df_bench["train_time_s"],
                                          marker_color=["#66bb6a", "#42a5f5", "#ef5350"]))
                fig_time.update_layout(template="plotly_dark", title="Temps d'entraînement (s)",
                                       xaxis_title="Modèle", yaxis_title="Secondes",
                                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_time, use_container_width=True)

            # Matrices de confusion
            st.subheader("Matrices de confusion")
            cols = st.columns(3)
            for idx, m in enumerate(summary["metrics"]):
                with cols[idx]:
                    cm = [[m["tn"], m["fp"]], [m["fn"], m["tp"]]]
                    fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                                       x=["Normal", "Fraude"], y=["Normal", "Fraude"],
                                       labels=dict(x="Prédit", y="Réel", color="Count"))
                    fig_cm.update_layout(template="plotly_dark", title=m["model"],
                                         paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_cm, use_container_width=True)

            # Conclusion
            best = summary["best_model"]
            best_f1 = summary["best_f1"]
            st.success(f"🏆 Meilleur modèle : **{best}** (F1 = {best_f1:.4f})")

    with tab2:
        st.info("Lancez un benchmark complet sur le modèle entraîné actuel")
        if st.session_state.model is None or st.session_state.X_test is None:
            st.warning("Entraînez d'abord un modèle via l'onglet Entraînement")
        else:
            if st.button("🚀 Lancer le benchmark", use_container_width=True, type="primary"):
                with st.spinner("Benchmark en cours (3 modèles)..."):
                    X_test = st.session_state.X_test
                    y_test = st.session_state.y_test
                    xgb_model = st.session_state.model
                    results = []

                    # XGBoost
                    t0 = time.time()
                    y_probs = xgb_model.predict_proba(X_test)[:, 1]
                    th = st.session_state.threshold
                    y_pred = (y_probs >= th).astype(int)
                    xgb_time = time.time() - t0
                    results.append({
                        "model": "XGBoost",
                        "f1_score": float(f1_score(y_test, y_pred)),
                        "recall": float(recall_score(y_test, y_pred)),
                        "precision": float(precision_score(y_test, y_pred)),
                        "auc_pr": float(average_precision_score(y_test, y_probs)),
                        "auc_roc": float(roc_auc_score(y_test, y_probs)),
                        "train_time_s": round(xgb_time, 2)
                    })

                    # Random Forest
                    from sklearn.ensemble import RandomForestClassifier
                    t0 = time.time()
                    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
                    rf.fit(X_test, y_test)
                    y_pred_rf = rf.predict(X_test)
                    y_prob_rf = rf.predict_proba(X_test)[:, 1]
                    rf_time = time.time() - t0
                    results.append({
                        "model": "Random Forest",
                        "f1_score": float(f1_score(y_test, y_pred_rf)),
                        "recall": float(recall_score(y_test, y_pred_rf)),
                        "precision": float(precision_score(y_test, y_pred_rf)),
                        "auc_pr": float(average_precision_score(y_test, y_prob_rf)),
                        "auc_roc": float(roc_auc_score(y_test, y_prob_rf)),
                        "train_time_s": round(rf_time, 2)
                    })

                    # Isolation Forest
                    from sklearn.ensemble import IsolationForest
                    t0 = time.time()
                    if_model = IsolationForest(contamination=y_test.mean(), random_state=42)
                    if_preds = if_model.fit_predict(X_test)
                    if_preds = np.where(if_preds == -1, 1, 0)
                    if_time = time.time() - t0
                    results.append({
                        "model": "Isolation Forest",
                        "f1_score": float(f1_score(y_test, if_preds)),
                        "recall": float(recall_score(y_test, if_preds)),
                        "precision": float(precision_score(y_test, if_preds)),
                        "auc_pr": 0.0,
                        "auc_roc": 0.0,
                        "train_time_s": round(if_time, 2)
                    })

                    # Display
                    df_bench2 = pd.DataFrame(results)
                    st.dataframe(df_bench2.round(4), use_container_width=True, hide_index=True)

                    best_idx = df_bench2["f1_score"].idxmax()
                    st.success(f"🏆 Meilleur : **{results[best_idx]['model']}** (F1 = {results[best_idx]['f1_score']:.4f})")

                    # Bar chart
                    fig2 = go.Figure()
                    for m in ["f1_score", "recall", "precision", "auc_pr"]:
                        fig2.add_trace(go.Bar(name=m, x=df_bench2["model"], y=df_bench2[m]))
                    fig2.update_layout(barmode="group", template="plotly_dark",
                                       title="Comparaison des modèles",
                                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig2, use_container_width=True)

# =====================================================================
# PAGE 6 : PRÉDICTION
# =====================================================================
elif page == "Prédiction":
    st.title("🔮 Prédiction temps réel")
    st.caption("Testez une transaction individuelle")

    if st.session_state.model is None:
        st.warning(" Entraînez d'abord un modèle")
        st.stop()

    model = st.session_state.model
    threshold = st.session_state.threshold
    X_test = st.session_state.X_test

    tab1, tab2 = st.tabs(["💳 Transaction bancaire", "🇹🇬 Mobile Money Togo"])

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

            submitted = st.form_submit_button("🔍 Analyser", type="primary", use_container_width=True)

        if submitted:
            with st.spinner("Analyse en cours..."):
                tx = {"TransactionAmt": float(amt), "card1": float(card1),
                      "hour": hour, "dayofweek": dayofweek,
                      "ProductCD": product_cd if product_cd else None,
                      "card4": card4 if card4 else None}

                df_tx = pd.DataFrame([tx])
                # Align features with model
                expected = model.get_booster().feature_names
                for col in expected:
                    if col not in df_tx.columns:
                        df_tx[col] = 0.0
                df_tx = df_tx[expected]

                proba = float(model.predict_proba(df_tx)[0, 1])
                pred = "FRAUDE" if proba >= threshold else "NORMALE"
                risk = "Critique" if proba >= 0.7 else "Élevé" if proba >= 0.55 else "Moyen" if proba >= 0.3 else "Faible"

                # Gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=proba * 100,
                    number={"suffix": "%", "font": {"size": 40, "color": "#e8eaf6"}},
                    gauge={"axis": {"range": [0, 100]},
                           "bar": {"color": "#ef5350" if pred == "FRAUDE" else "#4caf50"},
                           "steps": [{"range": [0, 30], "color": "rgba(76,175,80,0.2)"},
                                     {"range": [30, 55], "color": "rgba(255,193,7,0.2)"},
                                     {"range": [55, 70], "color": "rgba(239,108,0,0.2)"},
                                     {"range": [70, 100], "color": "rgba(198,40,40,0.2)"}],
                           "threshold": {"line": {"color": "white", "width": 2}, "thickness": 0.75, "value": threshold * 100}}))
                fig.update_layout(template="plotly_dark", height=300,
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)

                pred_color = "red" if pred == "FRAUDE" else "green"
                st.markdown(f"<h2 style='text-align:center;color:{pred_color};background:#111d2e;padding:15px;border-radius:8px;border:2px solid {pred_color};text-transform:uppercase'>{'🚨 ' if pred == 'FRAUDE' else '✅ '}{pred}</h2>", unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Score", f"{proba:.4f}")
                c2.metric("Risque", risk)
                c3.metric("Seuil", f"{threshold:.4f}")
                c4.metric("Montant", f"{amt:,} FCFA")

    with tab2:
        st.markdown("🇹🇬 Transaction Mobile Money adaptée au contexte Togo")
        with st.form("togo_form"):
            col1, col2 = st.columns(2)
            with col1:
                mt = st.number_input("Montant (FCFA)", 0, 10_000_000, 50000, 1000, key="tg_mt")
                canal = st.selectbox("Canal", ["AGENT", "USSD", "APP", "WEB"], key="tg_cnl")
                operateur = st.selectbox("Opérateur", ["TogoCom Cash", "Moov Money", "Flooz"], key="tg_op")
            with col2:
                ville = st.selectbox("Ville", ["Lomé", "Sokodé", "Kara", "Kpalimé", "Atakpamé", "Tsévié", "Dapaong"], key="tg_vil")
                type_op = st.selectbox("Type", ["TRANSFERT", "PAIEMENT", "RECHARGE", "RETRAIT"], key="tg_opr")
                device_change = st.number_input("Jours dernier changement SIM", 0, 365, 0, key="tg_dev")
            submitted_tg = st.form_submit_button("🔍 Analyser", type="primary", use_container_width=True)

        if submitted_tg:
            with st.spinner("Analyse en cours..."):
                tx = {
                    "TransactionAmt": float(mt), "card1": float(abs(hash(operateur + ville)) % 10000),
                    "card4": operateur, "ProductCD": canal,
                    "hour": 12, "dayofweek": 3,
                }
                df_tx = pd.DataFrame([tx])
                expected = model.get_booster().feature_names
                for col in expected:
                    if col not in df_tx.columns:
                        df_tx[col] = 0.0
                df_tx = df_tx[expected]

                proba = float(model.predict_proba(df_tx)[0, 1])
                pred = "FRAUDE" if proba >= threshold else "NORMALE"
                risk = "Critique" if proba >= 0.7 else "Élevé" if proba >= 0.55 else "Moyen" if proba >= 0.3 else "Faible"

                pred_color = "red" if pred == "FRAUDE" else "green"
                st.markdown(f"<h2 style='text-align:center;color:{pred_color};background:#111d2e;padding:15px;border-radius:8px;border:2px solid {pred_color};'>{'🚨 ' if pred == 'FRAUDE' else '✅ '}{pred}</h2>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.metric("Score", f"{proba:.4f}")
                c2.metric("Risque", risk)
                c3.metric("Montant", f"{mt:,} FCFA")
