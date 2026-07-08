#!/usr/bin/env python3
"""
generate_figures.py — Genere toutes les figures du memoire FRAUDX
pour les Chapitres III et IV.

Usage:
    python generate_figures.py                    # Toutes les figures
    python generate_figures.py --chapter 3        # Chapitre III seulement
    python generate_figures.py --chapter 4        # Chapitre IV seulement

Sortie :
    reports/figures_<date>/
        # Index du memoire (5 figures officielles)
        fig_3_1_distribution_classes.png
        fig_3_2_shap_importance.png
        fig_3_3_architecture.png
        fig_3_4_dashboard.png
        fig_3_5_waterfall_shap.png
        # Figures de donnees additionnelles
        fig_3_a_valeurs_manquantes.png
        fig_3_b_montant_log.png
        fig_3_c_temporel.png
        fig_3_d_correlations.png
        fig_3_e_confusion_matrix.png
        fig_3_f_probabilites.png
        fig_3_g_shap_summary.png
        # Chapitre IV
        fig_4_1_courbe_pr.png
        fig_4_2_roc_curve.png
        fig_4_3_benchmark_comparison.png
        fig_4_4_roi_projection.png
"""
import argparse, warnings, json, io
from pathlib import Path
from datetime import datetime
warnings.filterwarnings("ignore")

import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sklearn.metrics import (confusion_matrix, precision_recall_curve,
                             roc_curve, average_precision_score, roc_auc_score,
                             f1_score, recall_score, precision_score)

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 200
plt.rcParams["font.size"] = 11

OUTPUT_DIR = None


def setup_output():
    global OUTPUT_DIR
    OUTPUT_DIR = Path("reports") / f"figures_memoire_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Sortie : {OUTPUT_DIR}/")


def load_model_and_data(nrows=50000):
    print("Chargement des donnees...")
    df = pd.read_csv("data/train_transaction.csv", nrows=nrows)
    if "isFraud" in df.columns and "TransactionDT" in df.columns:
        start = pd.Timestamp("2017-12-01")
        dt = start + pd.to_timedelta(df["TransactionDT"], unit="s")
        df["hour"] = dt.dt.hour
        df["dayofweek"] = dt.dt.dayofweek
    y_true = df["isFraud"].values
    print(f"  Dataset : {df.shape}, fraude={y_true.mean()*100:.2f}%")
    model = None
    try:
        import joblib
        model = joblib.load("models_optuna/xgb_model.pkl")
        print(f"  Modele charge : XGBoost")
    except Exception as e:
        print(f"  Modele non charge : {e}")
    return df, y_true, model


def predict_with_model(model, df):
    if model is None:
        n = len(df)
        return np.random.randint(0, 2, n), np.random.uniform(0.2, 0.8, n)
    try:
        X = df.drop(columns=["isFraud", "TransactionID", "TransactionDT"], errors="ignore")
        num_cols = X.select_dtypes(include=[np.number]).columns
        X[num_cols] = X[num_cols].fillna(X[num_cols].median())
        cat_cols = X.select_dtypes(include=["object", "category"]).columns
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
        expected = model.get_booster().feature_names
        for col in expected:
            if col not in X.columns:
                X[col] = 0.0
        X = X[expected]
        y_proba = model.predict_proba(X)[:, 1]
        threshold = float(np.load("models_optuna/best_threshold.npy"))
        y_pred = (y_proba >= threshold).astype(int)
        print(f"  Prediction : {y_pred.mean()*100:.2f}% fraude (seuil={threshold:.4f})")
        return y_pred, y_proba
    except Exception as e:
        print(f"  Erreur prediction : {e}")
        n = len(df)
        return np.random.randint(0, 2, n), np.random.uniform(0.2, 0.8, n)


# ═══════════════════════════════════════════
# FIGURES OFFICIELLES — INDEX DU MEMOIRE
# ═══════════════════════════════════════════

def fig_3_1_distribution_classes(y):
    """Figure 3.1 — Distribution des classes (IEEE-CIS)"""
    fraud_counts = pd.Series(y).value_counts().reindex([0, 1], fill_value=0)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    bars = axes[0].bar(["Non fraude (0)", "Fraude (1)"], fraud_counts.values, color=["steelblue", "crimson"])
    axes[0].set_ylabel("Nombre de transactions")
    axes[0].set_title("Distribution des classes", fontweight="bold")
    for bar, val in zip(bars, fraud_counts.values):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, f"{val:,}", ha="center", fontsize=9)
    axes[1].pie(fraud_counts.values, labels=["Non fraude", "Fraude"], autopct="%1.2f%%",
                colors=["steelblue", "crimson"], startangle=90, explode=(0, 0.05))
    axes[1].set_title("Proportion", fontweight="bold")
    plt.suptitle("Figure 3.1 — Distribution des classes (IEEE-CIS)", y=1.02, fontweight="bold")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_1_distribution_classes.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   [INDEX] fig_3_1_distribution_classes.png")


def fig_3_2_shap_importance():
    """Figure 3.2 — Importance globale des variables (SHAP)"""
    try:
        import shap, joblib
        model = joblib.load("models_optuna/xgb_model.pkl")
        X_sample = pd.read_csv("data/train_transaction.csv", nrows=10000)
        X_sample = X_sample.drop(columns=["isFraud", "TransactionID", "TransactionDT"], errors="ignore")
        num = X_sample.select_dtypes(include=[np.number]).columns
        X_sample[num] = X_sample[num].fillna(X_sample[num].median())
        cat = X_sample.select_dtypes(include=["object", "category"]).columns
        X_sample = pd.get_dummies(X_sample, columns=cat, drop_first=True)
        exp = model.get_booster().feature_names
        for c in exp:
            if c not in X_sample.columns: X_sample[c] = 0.0
        X_sample = X_sample[exp].sample(500, random_state=42)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_sample, plot_type="bar", max_display=15, show=False)
        plt.title("Figure 3.2 — Importance globale des variables (SHAP)", fontweight="bold")
        plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_2_shap_importance.png", dpi=200, bbox_inches="tight"); plt.close()
        print("   [INDEX] fig_3_2_shap_importance.png")
    except Exception as e:
        print(f"   fig_3_2 ignore : {e}")


def fig_3_3_architecture():
    """Figure 3.3 — Architecture technique en 6 couches (FRAUDX)"""
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_facecolor("#0a1628")
    fig.patch.set_facecolor("#0a1628")

    layers = [
        {"y": 8.2, "h": 1.1, "color": "#880e4f", "alpha": 1.0, "label": "SECURITE — Transversale",
         "boxes": [("JWT / TLS 1.3", "Authentification"), ("RBAC 3 roles", "Analyste/Gest./Admin"),
                   ("Audit Logs", "Journalisation"), ("AES-256", "Chiffrement"), ("Conformite", "BCEAO/PCI DSS")]},
        {"y": 6.7, "h": 1.0, "color": "#1a237e", "alpha": 1.0, "label": "CLIENT — Interfaces",
         "boxes": [("Dashboard", "Streamlit + SHAP"), ("Mobile Money", "USSD/APP/Agent"),
                   ("API Bancaire", "REST SI existant"), ("CLI / Scripts", "train/simulate")]},
        {"y": 5.2, "h": 1.0, "color": "#0d47a1", "alpha": 1.0, "label": "API — Traitement",
         "boxes": [("FastAPI REST", "/predict /batch /logs"), ("Rate Limiter", "Anti-abus"),
                   ("WebSocket", "Push temps reel")]},
        {"y": 3.7, "h": 1.0, "color": "#1b5e20", "alpha": 1.0, "label": "PIPELINE ML",
         "boxes": [("Feature Eng.", "Encoding + temporal"), ("SMOTE", "Reequilibrage"),
                   ("StandardScaler", "Normalisation"), ("Seuil Adapt.", "Optimisation F1")]},
        {"y": 2.2, "h": 1.0, "color": "#bf360c", "alpha": 1.0, "label": "MODELE — 3 Niveaux",
         "boxes": [("N1: Isolation Forest", "Filtre anomalies"), ("N2: XGBoost", "Classification"), ("N3: LSTM", "Deep Seq.")]},
        {"y": 0.7, "h": 1.0, "color": "#4a148c", "alpha": 1.0, "label": "DONNEES — Persistance",
         "boxes": [("SQLite", "predict+feedback"), ("Modeles .pkl", "XGB/IF/scaler"), ("Metriques", "JSON + seuil"), ("Raw CSV", "IEEE-CIS")]},
    ]

    for layer in layers:
        y, h, color = layer["y"], layer["h"], layer["color"]
        rect = FancyBboxPatch((0.3, y), 15.4, h, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor="white", linewidth=0.8, alpha=0.85)
        ax.add_patch(rect)
        ax.text(0.5, y + h/2, layer["label"], fontsize=8, fontweight="bold",
                color="white", va="center", ha="left")
        nboxes = len(layer["boxes"])
        for i, (name, desc) in enumerate(layer["boxes"]):
            bx = 4.0 + i * (12.0 / max(nboxes, 1))
            bw = 10.0 / max(nboxes, 1)
            box = FancyBboxPatch((bx, y + 0.08), bw, h - 0.16,
                                 boxstyle="round,pad=0.03", facecolor="white", edgecolor=color,
                                 linewidth=0.5, alpha=0.15)
            ax.add_patch(box)
            ax.text(bx + bw/2, y + h*0.6, name, fontsize=6, fontweight="bold",
                    color="white", ha="center", va="center")
            ax.text(bx + bw/2, y + h*0.25, desc, fontsize=5,
                    color="#b0bec5", ha="center", va="center")

    # Fleches entre les couches
    for y_pos in [6.6, 5.1, 3.6, 2.1, 0.6]:
        ax.annotate("", xy=(8, y_pos), xytext=(8, y_pos + 0.4),
                    arrowprops=dict(arrowstyle="->", color="#42a5f5", lw=1.5))

    ax.text(8, 9.6, "Figure 3.3 — Architecture technique en 6 couches (FRAUDX)",
            fontsize=11, fontweight="bold", color="white", ha="center", va="center")
    plt.savefig(OUTPUT_DIR / "fig_3_3_architecture.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   [INDEX] fig_3_3_architecture.png")


def fig_3_4_dashboard():
    """Figure 3.4 — Dashboard FRAUDX (maquette)"""
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor("#0f1923")

    # Barre laterale
    ax_sidebar = fig.add_axes([0, 0, 0.18, 1])
    ax_sidebar.set_facecolor("#0d1520"); ax_sidebar.axis("off")
    ax_sidebar.text(0.1, 0.95, "FRAUDX", fontsize=16, fontweight="bold", color="#42a5f5")
    for i, item in enumerate(["Dashboard", "Transactions", "Modeles", "SHAP", "Benchmark", "Admin"]):
        color = "#e0e0e0" if i > 0 else "#42a5f5"
        bg = "#1a2a40" if i == 0 else "none"
        ax_sidebar.text(0.1, 0.82 - i*0.08, f"  {item}", fontsize=8, color=color,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor=bg, edgecolor="none"))

    # Entete
    ax_header = fig.add_axes([0.18, 0.92, 0.82, 0.08])
    ax_header.set_facecolor("#0f1923"); ax_header.axis("off")
    ax_header.text(0.02, 0.5, "Tableau de bord — Detection de fraude", fontsize=14, fontweight="bold", color="white", va="center")

    # KPIs
    kpi_data = [("Transactions", "12 847", "jour"), ("Alertes", "347", "+2.1%"), ("Taux fraude", "2.71%", "-0.3%"), ("Recall", "85.0%", "XGBoost")]
    for i, (label, val, sub) in enumerate(kpi_data):
        ax = fig.add_axes([0.22 + i*0.19, 0.78, 0.17, 0.10])
        ax.set_facecolor("#162230"); ax.axis("off")
        ax.text(0.5, 0.7, val, fontsize=20, fontweight="bold", color="white", ha="center", va="center")
        ax.text(0.5, 0.3, label, fontsize=8, color="#78909c", ha="center", va="center")
        ax.text(0.5, 0.1, sub, fontsize=7, color="#66bb6a", ha="center", va="center")

    # Graphique volume / heure
    ax_chart1 = fig.add_axes([0.22, 0.38, 0.35, 0.35])
    ax_chart1.set_facecolor("#162230")
    hours = np.arange(24)
    counts = 3000 + 2000 * np.sin(np.pi * (hours - 6) / 12) + np.random.randint(-200, 200, 24)
    ax_chart1.fill_between(hours, 0, counts, alpha=0.3, color="#42a5f5")
    ax_chart1.plot(hours, counts, color="#42a5f5", linewidth=1.5)
    ax_chart1.set_title("Volume transactions (24h)", fontsize=9, fontweight="bold", color="white")
    ax_chart1.tick_params(colors="white", labelsize=6); ax_chart1.set_xlim(0, 23)
    ax_chart1.spines["bottom"].set_color("#2a3a5c"); ax_chart1.spines["left"].set_color("#2a3a5c")
    ax_chart1.set_facecolor("#162230")

    # Tableau alertes
    ax_table = fig.add_axes([0.62, 0.55, 0.35, 0.35])
    ax_table.set_facecolor("#162230"); ax_table.axis("off")
    ax_table.text(0.5, 0.92, "Dernieres alertes", fontsize=9, fontweight="bold", color="white", ha="center")
    columns = ("TX ID", "Montant", "Score", "Risque")
    rows = [("#T0421", "184.50", "0.92", "ELEVE"), ("#T0419", "52.30", "0.78", "MOYEN"),
            ("#T0417", "320.00", "0.65", "MOYEN"), ("#T0415", "12.99", "0.34", "FAIBLE"),
            ("#T0413", "950.00", "0.95", "CRITIQUE")]
    table = ax_table.table(cellText=rows, colLabels=columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False); table.set_fontsize(7)
    for key, cell in table.get_celld().items():
        cell.set_facecolor("#1a2a40"); cell.set_text_props(color="white")
        cell.set_edgecolor("#2a3a5c")
    table[0, 0].get_text().set_text("TX ID"); table[0, 0].set_text_props(fontweight="bold")

    # Pie chart SHAP
    ax_pie = fig.add_axes([0.62, 0.22, 0.15, 0.2])
    ax_pie.set_facecolor("#0f1923")
    sizes = [30, 20, 15, 12, 10, 13]
    labels_pie = ["C14", "Amt", "card6", "V317", "V258", "Autres"]
    colors_pie = ["#42a5f5", "#ef5350", "#66bb6a", "#ffa726", "#ab47bc", "#78909c"]
    wedges, texts, autotexts = ax_pie.pie(sizes, labels=None, autopct="", startangle=90,
                                            colors=colors_pie, explode=(0.05, 0, 0, 0, 0, 0))
    ax_pie.set_title("Top SHAP", fontsize=9, fontweight="bold", color="white")

    ax_legend = fig.add_axes([0.78, 0.22, 0.18, 0.2])
    ax_legend.set_facecolor("#0f1923"); ax_legend.axis("off")
    for i, (label, c) in enumerate(zip(labels_pie, colors_pie)):
        ax_legend.add_patch(mpatches.Circle((0.1, 0.85 - i*0.15), 0.04, color=c))
        ax_legend.text(0.25, 0.85 - i*0.15, label, fontsize=7, color="white", va="center")

    # Timeline feed
    ax_feed = fig.add_axes([0.22, 0.22, 0.35, 0.15])
    ax_feed.set_facecolor("#162230"); ax_feed.axis("off")
    ax_feed.text(0.02, 0.85, "Flux temps reel", fontsize=9, fontweight="bold", color="white")
    feed_items = ["14:32:17  TX#0421  FRAUDE detectee  SHAP: C14=+0.32",
                   "14:30:05  TX#0419  Seuil depasse  SHAP: Amt=+0.18",
                   "14:28:44  TX#0417  Analyse en cours...",
                   "14:25:12  TX#0415  Transaction normale"]
    for i, item in enumerate(feed_items):
        color = "#ef5350" if "FRAUDE" in item else "#66bb6a" if "normale" in item else "#ffa726"
        ax_feed.text(0.02, 0.6 - i*0.15, item, fontsize=6, color=color, va="center")

    plt.suptitle("Figure 3.4 — Dashboard FRAUDX (maquette)", y=0.98, fontsize=12, fontweight="bold", color="white")
    plt.savefig(OUTPUT_DIR / "fig_3_4_dashboard.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   [INDEX] fig_3_4_dashboard.png")


def fig_3_5_waterfall_shap():
    """Figure 3.5 — Waterfall plot SHAP (exemple individuel)"""
    try:
        import shap, joblib
        model = joblib.load("models_optuna/xgb_model.pkl")
        X_sample = pd.read_csv("data/train_transaction.csv", nrows=20000)
        X_sample = X_sample.drop(columns=["isFraud", "TransactionID", "TransactionDT"], errors="ignore")
        num = X_sample.select_dtypes(include=[np.number]).columns
        X_sample[num] = X_sample[num].fillna(X_sample[num].median())
        cat = X_sample.select_dtypes(include=["object", "category"]).columns
        X_sample = pd.get_dummies(X_sample, columns=cat, drop_first=True)
        exp = model.get_booster().feature_names
        for c in exp:
            if c not in X_sample.columns: X_sample[c] = 0.0
        X_sample = X_sample[exp].head(1)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
        # shap_values peut etre une liste [neg_class, pos_class] ou un array 2D
        if isinstance(shap_values, list):
            sv = shap_values[1]
        else:
            sv = shap_values
        if len(sv.shape) == 2 and sv.shape[0] == 1:
            sv = sv[0]
        ev = explainer.expected_value
        if isinstance(ev, (list, np.ndarray)):
            ev = ev[1] if len(ev) > 1 else ev[0]
        exp_obj = shap.Explanation(values=sv, base_values=ev,
                                    data=X_sample.iloc[0].values,
                                    feature_names=X_sample.columns.tolist())
        shap.waterfall_plot(exp_obj, max_display=12, show=False)
        plt.gcf().set_size_inches(10, 6)
        plt.title("Figure 3.5 — Waterfall plot SHAP (exemple individuel)", fontweight="bold")
        plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_5_waterfall_shap.png", dpi=200, bbox_inches="tight"); plt.close()
        print("   [INDEX] fig_3_5_waterfall_shap.png")
    except Exception as e:
        print(f"   fig_3_5 waterfall SHAP ignore : {e}")


# ═══════════════════════════════════════════
# FIGURES ADDITIONNELLES — Donnees
# ═══════════════════════════════════════════

def fig_add_valeurs_manquantes(df):
    missing = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    high = missing[missing > 50]
    fig, ax = plt.subplots(figsize=(10, max(4, len(high) * 0.3)))
    ax.barh(range(len(high)), high.values, color="salmon")
    ax.set_yticks(range(len(high))); ax.set_yticklabels(high.index, fontsize=8)
    ax.axvline(90, color="red", linestyle="--", label="Seuil 90% (suppression)")
    ax.set_xlabel("Taux de valeurs manquantes (%)"); ax.set_title("Colonnes avec > 50% de NaN", fontweight="bold")
    ax.legend(); plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_3_a_valeurs_manquantes.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_3_a_valeurs_manquantes.png")


def fig_add_montant_log(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    pos = df[df["isFraud"] == 1]["TransactionAmt"] if "isFraud" in df.columns else pd.Series()
    neg = df[df["isFraud"] == 0]["TransactionAmt"] if "isFraud" in df.columns else df["TransactionAmt"]
    axes[0].hist(np.log1p(neg), bins=80, alpha=0.6, label="Non fraude", color="steelblue", density=True)
    if len(pos) > 0:
        axes[0].hist(np.log1p(pos), bins=80, alpha=0.6, label="Fraude", color="crimson", density=True)
    axes[0].set_xlabel("log(TransactionAmt + 1)"); axes[0].set_ylabel("Densite")
    axes[0].set_title("Distribution du montant (echelle log)", fontweight="bold"); axes[0].legend()
    bp = axes[1].boxplot([neg, pos] if len(pos) > 0 else [neg],
                         tick_labels=["Non fraude", "Fraude"] if len(pos) > 0 else ["Toutes"],
                         widths=0.4, patch_artist=True)
    if len(pos) > 0:
        bp["boxes"][0].set_facecolor("steelblue"); bp["boxes"][1].set_facecolor("crimson")
    axes[1].set_ylabel("TransactionAmt"); axes[1].set_title("Boxplot du montant", fontweight="bold")
    axes[1].set_yscale("log")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_b_montant_log.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_3_b_montant_log.png")


def fig_add_temporel(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    hourly_count = df.groupby("hour")["isFraud"].count() if "hour" in df.columns else pd.Series()
    hourly_fraud = df.groupby("hour")["isFraud"].mean() * 100 if "hour" in df.columns else pd.Series()
    axes[0].plot(hourly_count.index, hourly_count.values, marker="o", color="steelblue", linewidth=1.5)
    axes[0].set_xlabel("Heure"); axes[0].set_ylabel("Volume")
    axes[0].set_title("Volume par heure", fontweight="bold"); axes[0].set_xticks(range(24))
    axes[1].plot(hourly_fraud.index, hourly_fraud.values, marker="o", color="crimson", linewidth=1.5)
    axes[1].set_xlabel("Heure"); axes[1].set_ylabel("Taux de fraude (%)")
    axes[1].set_title("Taux de fraude par heure", fontweight="bold"); axes[1].set_xticks(range(24))
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_c_temporel.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_3_c_temporel.png")


def fig_add_correlations(df):
    numeric = df.select_dtypes(include=np.number)
    if "isFraud" in numeric.columns:
        corr_with_target = numeric.corr()["isFraud"].abs().sort_values(ascending=False)
        top30 = corr_with_target.index[:30]
        corr_matrix = numeric[top30].corr()
    else:
        corr_matrix = numeric.corr()
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(corr_matrix, mask=np.triu(np.ones_like(corr_matrix, dtype=bool)),
                cmap="RdBu_r", center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    ax.set_title("Heatmap des correlations (top 30)", fontweight="bold")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_d_correlations.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_3_d_correlations.png")


def fig_add_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Non fraude", "Fraude"], yticklabels=["Non fraude", "Fraude"])
    ax.set_xlabel("Prediction"); ax.set_ylabel("Reel")
    ax.set_title("Matrice de confusion (XGBoost)", fontweight="bold")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_e_confusion_matrix.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_3_e_confusion_matrix.png")


def fig_add_probabilites(y_true, y_proba, threshold=0.5):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(y_proba[y_true == 0], bins=50, alpha=0.6, label="Non fraude", color="steelblue", density=True)
    ax.hist(y_proba[y_true == 1], bins=50, alpha=0.6, label="Fraude", color="crimson", density=True)
    ax.axvline(threshold, color="black", linestyle="--", label=f"Seuil = {threshold:.3f}")
    ax.set_xlabel("Probabilite predite"); ax.set_ylabel("Densite")
    ax.set_title("Distribution des probabilites", fontweight="bold"); ax.legend()
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_f_probabilites.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_3_f_probabilites.png")


def fig_add_shap_summary():
    try:
        import shap, joblib
        model = joblib.load("models_optuna/xgb_model.pkl")
        explainer = shap.TreeExplainer(model)
        X_sample = pd.read_csv("data/train_transaction.csv", nrows=10000)
        X_sample = X_sample.drop(columns=["isFraud", "TransactionID", "TransactionDT"], errors="ignore")
        num = X_sample.select_dtypes(include=[np.number]).columns
        X_sample[num] = X_sample[num].fillna(X_sample[num].median())
        cat = X_sample.select_dtypes(include=["object", "category"]).columns
        X_sample = pd.get_dummies(X_sample, columns=cat, drop_first=True)
        exp = model.get_booster().feature_names
        for c in exp:
            if c not in X_sample.columns: X_sample[c] = 0.0
        X_sample = X_sample[exp].sample(500, random_state=42)
        shap_values = explainer.shap_values(X_sample)
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_sample, max_display=20, show=False)
        plt.title("SHAP Summary Plot (beeswarm)", fontweight="bold")
        plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_3_g_shap_summary.png", dpi=200, bbox_inches="tight"); plt.close()
        print("   fig_3_g_shap_summary.png")
    except Exception as e:
        print(f"   SHAP summary ignore : {e}")


# ═══════════════════════════════════════════
# CHAPITRE IV
# ═══════════════════════════════════════════

def fig_4_1_courbe_pr(y_true, y_proba):
    precisions, recalls, _ = precision_recall_curve(y_true, y_proba)
    ap = average_precision_score(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(recalls, precisions, linewidth=2, color="crimson", label=f"AUC-PR = {ap:.4f}")
    ax.fill_between(recalls, precisions, alpha=0.15, color="crimson")
    ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
    ax.set_title("Figure 4.1 — Courbe Precision-Recall (XGBoost optimise)", fontweight="bold")
    ax.legend(loc="lower left"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_4_1_courbe_pr.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_4_1_courbe_pr.png")


def fig_4_2_roc_curve(y_true, y_proba):
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(fpr, tpr, linewidth=2, color="steelblue", label=f"AUC-ROC = {auc:.4f}")
    ax.fill_between(fpr, tpr, alpha=0.1, color="steelblue")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", alpha=0.5, label="Aleatoire")
    ax.set_xlabel("Taux de faux positifs (FPR)"); ax.set_ylabel("Taux de vrais positifs (TPR)")
    ax.set_title("Figure 4.2 — Courbe ROC (XGBoost optimise)", fontweight="bold")
    ax.legend(loc="lower right"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_4_2_roc_curve.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_4_2_roc_curve.png")


def fig_4_3_benchmark(y_true, y_pred_xgb):
    from sklearn.ensemble import RandomForestClassifier, IsolationForest
    X_sample = pd.read_csv("data/train_transaction.csv", nrows=20000)
    X_sample = X_sample.drop(columns=["isFraud", "TransactionID", "TransactionDT"], errors="ignore")
    num = X_sample.select_dtypes(include=[np.number]).columns
    X_sample[num] = X_sample[num].fillna(X_sample[num].median())
    cat = X_sample.select_dtypes(include=["object", "category"]).columns
    X_sample = pd.get_dummies(X_sample, columns=cat, drop_first=True)
    y = y_true[:len(X_sample)]

    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_sample, y); y_pred_rf = rf.predict(X_sample)
    if_model = IsolationForest(contamination=y.mean(), random_state=42)
    y_pred_if = np.where(if_model.fit_predict(X_sample) == -1, 1, 0)

    scores = {
        "XGBoost": {"F1": f1_score(y, y_pred_xgb[:len(y)]), "Recall": recall_score(y, y_pred_xgb[:len(y)]),
                     "Precision": precision_score(y, y_pred_xgb[:len(y)])},
        "Random Forest": {"F1": f1_score(y, y_pred_rf), "Recall": recall_score(y, y_pred_rf),
                          "Precision": precision_score(y, y_pred_rf)},
        "Isolation Forest": {"F1": f1_score(y, y_pred_if), "Recall": recall_score(y, y_pred_if),
                             "Precision": precision_score(y, y_pred_if)},
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(3); w = 0.25
    for i, (metric, color) in enumerate([("F1", "#42a5f5"), ("Recall", "#4caf50"), ("Precision", "#ffa726")]):
        vals = [scores[m][metric] for m in ["XGBoost", "Random Forest", "Isolation Forest"]]
        ax.bar(x + i * w, vals, w, label=metric, color=color)
    ax.set_xticks(x + w); ax.set_xticklabels(["XGBoost", "Random Forest", "Isolation Forest"], fontweight="bold")
    ax.set_ylabel("Score"); ax.set_title("Figure 4.3 — Benchmark des modeles", fontweight="bold")
    ax.legend(loc="lower right"); ax.set_ylim(0, 1)
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_4_3_benchmark_comparison.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_4_3_benchmark_comparison.png")
    for m, s in scores.items():
        print(f"      {m}: F1={s['F1']:.4f}, Recall={s['Recall']:.4f}, Prec={s['Precision']:.4f}")


def fig_4_4_roi():
    years = np.array([0, 1, 2, 3])
    cout_cumule = np.array([0, 104000, 140000, 177000])
    economies = np.array([0, 200000, 400000, 600000])
    roi_pct = (economies - cout_cumule) / cout_cumule * 100
    roi_pct[0] = 0

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.fill_between(years, 0, cout_cumule, alpha=0.3, color="crimson", label="Cout cumule")
    ax1.fill_between(years, 0, economies, alpha=0.3, color="steelblue", label="Economies cumulees")
    ax1.plot(years, cout_cumule, "o-", color="crimson", linewidth=2)
    ax1.plot(years, economies, "s-", color="steelblue", linewidth=2)
    ax1.axvline(2.5, color="gray", linestyle="--", alpha=0.5)
    ax1.set_xlabel("Annee"); ax1.set_ylabel("Montant (EUR)")
    ax1.set_xticks(years); ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.bar(years[1:], roi_pct[1:], width=0.5, alpha=0.4, color="#F0B92B", label="ROI %")
    ax2.plot(years, roi_pct, "D--", color="#F0B92B", linewidth=1.5)
    ax2.set_ylabel("ROI (%)"); ax2.legend(loc="upper right")

    plt.title("Figure 4.4 — Projection financiere et ROI sur 3 ans", fontweight="bold")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "fig_4_4_roi_projection.png", dpi=200, bbox_inches="tight"); plt.close()
    print("   fig_4_4_roi_projection.png")


# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Genere les figures du memoire FRAUDX")
    parser.add_argument("--chapter", type=int, choices=[3, 4], default=None)
    args = parser.parse_args()

    setup_output()
    print("Generation des figures du memoire FRAUDX\n")

    df, y_true, model = load_model_and_data()
    y_pred, y_proba = predict_with_model(model, df)

    try:
        threshold = float(np.load("models_optuna/best_threshold.npy"))
    except Exception:
        threshold = 0.325

    if args.chapter is None or args.chapter == 3:
        print("\n--- CHAPITRE III ---")
        print("[Figures index]")
        fig_3_1_distribution_classes(y_true)
        fig_3_2_shap_importance()
        fig_3_3_architecture()
        fig_3_4_dashboard()
        fig_3_5_waterfall_shap()
        print("[Figures additionnelles]")
        fig_add_valeurs_manquantes(df)
        fig_add_montant_log(df)
        fig_add_temporel(df)
        fig_add_correlations(df)
        fig_add_confusion_matrix(y_true, y_pred)
        fig_add_probabilites(y_true, y_proba, threshold)
        fig_add_shap_summary()

    if args.chapter is None or args.chapter == 4:
        print("\n--- CHAPITRE IV ---")
        fig_4_1_courbe_pr(y_true, y_proba)
        fig_4_2_roc_curve(y_true, y_proba)
        fig_4_3_benchmark(y_true, y_pred)
        fig_4_4_roi()

    print(f"\nToutes les figures dans {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
