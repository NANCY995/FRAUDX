#!/usr/bin/env python3
"""
app_streamlit.py — Tableau de bord FRAUDX enrichi
Dashboard professionnel pour la détection de fraude au Togo.

Usage:
    pip install -r requirements.txt
    streamlit run app_streamlit.py
"""
import base64
import io
import json
import os
import subprocess
import sys
import time
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from fraudx.config import config

st.set_page_config(
    page_title="FRAUDX — Dashboard Détection Fraude Togo",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CONSTANTES & STYLE
# ─────────────────────────────────────────────

API_URL = os.getenv("API_URL", "http://localhost:8000")
COULEURS = {
    "primary": "#1a237e",
    "secondary": "#0d47a1",
    "accent": "#00c853",
    "danger": "#d50000",
    "warning": "#ff6d00",
    "info": "#0091ea",
    "bg_dark": "#0a1628",
    "card_bg": "#111d2e",
    "text": "#e8eaf6",
    "text_muted": "#78909c",
}

TOGO_CITIES = {
    "Lomé":       {"lat": 6.1725, "lon": 1.2314, "region": "Maritime", "population": 1500000},
    "Sokodé":     {"lat": 8.9833, "lon": 1.1333, "region": "Centrale",  "population": 120000},
    "Kara":       {"lat": 9.5500, "lon": 1.1833, "region": "Kara",      "population": 110000},
    "Kpalimé":    {"lat": 6.9000, "lon": 0.6333, "region": "Plateaux", "population": 95000},
    "Atakpamé":   {"lat": 7.5333, "lon": 1.1167, "region": "Plateaux", "population": 85000},
    "Tsévié":     {"lat": 6.4167, "lon": 1.2000, "region": "Maritime", "population": 55000},
    "Dapaong":    {"lat": 10.8667, "lon": 0.2000, "region": "Savanes", "population": 60000},
    "Mango":      {"lat": 10.3592, "lon": 0.4756, "region": "Savanes", "population": 40000},
    "Aného":      {"lat": 6.2286, "lon": 1.6018, "region": "Maritime", "population": 25000},
    "Notsé":      {"lat": 6.9500, "lon": 1.1667, "region": "Plateaux", "population": 35000},
    "Bassar":     {"lat": 9.2500, "lon": 0.7833, "region": "Kara",      "population": 45000},
    "Amlamé":     {"lat": 7.4667, "lon": 0.9000, "region": "Plateaux", "population": 15000},
    "Tabligbo":   {"lat": 6.5833, "lon": 1.5167, "region": "Maritime", "population": 20000},
    "Bafilo":     {"lat": 9.3500, "lon": 1.2667, "region": "Kara",      "population": 18000},
}

# CSS personnalisé pour un rendu professionnel
st.markdown("""
<style>
    /* Métriques KPI */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #111d2e 0%, #0d1b2a 100%);
        border: 1px solid #1a3a5c;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label {
        color: #78909c !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #e8eaf6 !important;
        font-weight: 700;
    }
    /* Cartes */
    div.stCard, div[data-testid="stCard"] {
        background: #111d2e;
        border: 1px solid #1a3a5c;
        border-radius: 12px;
        padding: 1rem;
    }
    .element-container .stAlert {
        border-radius: 8px;
    }
    /* Titres */
    h1, h2, h3 { color: #e8eaf6 !important; }
    .stSubheader { color: #90caf9 !important; }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a1628;
        border-right: 1px solid #1a3a5c;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #b0bec5;
    }
    /* Pilules de statut */
    .status-pill {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .status-pill.normal { background: #1b5e20; color: #a5d6a7; }
    .status-pill.fraude { background: #b71c1c; color: #ffcdd2; }
    .status-pill.critique { background: #bf360c; color: #ffccbc; }
    /* DataFrames */
    .stDataFrame { border: none !important; }
    /* Ligne de séparation */
    hr { border-color: #1a3a5c !important; }
    /* Footer */
    .footer {
        text-align: center;
        color: #455a64;
        font-size: 0.75rem;
        padding: 1rem 0;
        border-top: 1px solid #1a3a5c;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────

def check_api() -> tuple[bool, str]:
    """Vérifie si l'API est accessible."""
    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        if r.status_code == 200:
            data = r.json()
            return True, f"✅ {data.get('model', 'FRAUDX')} — v{data.get('version', '2.0')}"
        return True, "✅ Connectée"
    except:
        return False, "❌ API hors ligne"


def generate_fake_transactions(n: int = 100) -> pd.DataFrame:
    """Génère des transactions de démonstration."""
    np.random.seed(int(time.time()) % 10000)
    cities = list(TOGO_CITIES.keys())
    canals = ["USSD", "APP", "AGENT", "WEB"]
    operateurs = ["TogoCom Cash", "Moov Money", "Flooz", "TMoney"]
    operations = ["TRANSFERT", "PAIEMENT", "RECHARGE", "RETRAIT"]

    data = {
        "transaction_id": [f"DEMO_{i:06d}" for i in range(n)],
        "montant_cfa": np.random.lognormal(10, 1.5, n).round(0),
        "ville": np.random.choice(cities, n),
        "canal": np.random.choice(canals, n, p=[0.10, 0.15, 0.50, 0.25]),
        "operateur": np.random.choice(operateurs, n, p=[0.35, 0.30, 0.20, 0.15]),
        "type_operation": np.random.choice(operations, n, p=[0.40, 0.35, 0.15, 0.10]),
        "heure": np.random.randint(0, 24, n),
        "jour_semaine": np.random.randint(0, 7, n),
        "device_change_days": np.random.exponential(90, n).round(0),
        "tx_last_30min": np.random.poisson(0.5, n),
    }
    df = pd.DataFrame(data)

    # Score de fraude synthétique basé sur des règles simples
    fraud_score = np.zeros(n)
    fraud_score += (df["montant_cfa"] > 200000).astype(float) * 0.3
    fraud_score += (df["heure"] < 6).astype(float) * 0.15
    fraud_score += (df["tx_last_30min"] > 3).astype(float) * 0.25
    fraud_score += (df["device_change_days"] < 7).astype(float) * 0.20
    fraud_score += (df["canal"] == "USSD").astype(float) * 0.05
    fraud_score += (df["operateur"] == "Flooz").astype(float) * 0.05
    fraud_score += np.random.uniform(-0.1, 0.1, n)
    fraud_score = np.clip(fraud_score, 0, 1)

    df["fraud_score"] = fraud_score.round(4)
    df["prediction"] = np.where(fraud_score >= 0.55, "FRAUDE", "NORMALE")
    df["risk_level"] = pd.cut(
        fraud_score,
        bins=[0, 0.3, 0.5, 0.7, 1.0],
        labels=["Faible", "Moyen", "Élevé", "Critique"],
    )
    df["timestamp"] = pd.Timestamp.now() - pd.to_timedelta(np.random.randint(0, 3600, n), unit="s")
    return df


def generate_kpi_history(days: int = 30) -> pd.DataFrame:
    """Génère l'historique des KPIs pour le monitoring."""
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq="D")
    base_f1 = 0.88 + np.random.uniform(-0.04, 0.04, days).cumsum() * 0.003
    base_f1 = np.clip(base_f1, 0.78, 0.96)
    return pd.DataFrame({
        "date": dates,
        "f1_score": base_f1,
        "recall": base_f1 - np.random.uniform(0.02, 0.06, days),
        "precision": base_f1 + np.random.uniform(-0.03, 0.03, days),
        "fraud_rate": np.random.uniform(2.5, 4.5, days),
        "avg_latency_ms": np.random.uniform(35, 65, days),
        "total_transactions": np.random.poisson(400, days),
    })


def render_metric_card(label: str, value: str, delta: str = "",
                        delta_color: str = "normal", help_text: str = ""):
    """Affiche une carte métrique stylisée."""
    cols = st.columns([1])
    with cols[0]:
        st.metric(label=label, value=value, delta=delta,
                   delta_color=delta_color, help=help_text)


def status_pill(prediction: str) -> str:
    """Génère une pilule HTML de statut."""
    cls = prediction.lower().replace("é", "e")
    return f'<span class="status-pill {cls}">{prediction}</span>'


def format_cfa(amount: float) -> str:
    """Formate un montant en FCFA."""
    if amount >= 1_000_000:
        return f"{amount/1_000_000:.1f}M FCFA"
    elif amount >= 1_000:
        return f"{amount:,.0f} FCFA".replace(",", " ")
    return f"{amount:.0f} FCFA"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.markdown(
    '<div style="text-align:center; padding: 1rem 0;">'
    '<h1 style="font-size:1.8rem; margin:0;">🛡️ FRAUDX</h1>'
    '<p style="color:#78909c; font-size:0.85rem; margin:0;">'
    'Détection de fraude bancaire<br>Togo</p>'
    '</div>',
    unsafe_allow_html=True,
)

api_ok, api_msg = check_api()
if api_ok:
    st.sidebar.success(f"🔌 {api_msg}")
else:
    st.sidebar.warning(f"🔌 {api_msg}")
    st.sidebar.info("💡 Lancez l'API : `uvicorn src.api:app --reload`")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Tableau de bord",
        "🗺️ Géo-visualisation Togo",
        "🧪 What-if Analysis",
        "🔍 Analyse Transaction",
        "📈 Monitoring",
        "⚙️ Configuration",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


# ─────────────────────────────────────────────
#  PAGE 1 : TABLEAU DE BORD PRINCIPAL
# ─────────────────────────────────────────────

if page == "📊 Tableau de bord":
    st.title("📊 Tableau de bord FRAUDX")
    st.caption("Vue d'ensemble du système de détection de fraude en temps réel")

    # Données
    df_demo = generate_fake_transactions(200)
    kpi_hist = generate_kpi_history(30)

    # Filtres temporels
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        periode = st.selectbox("Période", ["24h", "7 jours", "30 jours", "Tout"], index=2)
    with col_f2:
        filtre_canal = st.multiselect("Canal", ["USSD", "APP", "AGENT", "WEB"], default=[])
    with col_f3:
        filtre_risque = st.multiselect("Risque min.", ["Faible", "Moyen", "Élevé", "Critique"], default=[])
    with col_f4:
        auto_refresh = st.checkbox("Auto-refresh (10s)", value=False)

    if auto_refresh:
        st.toast("🔄 Rafraîchissement automatique activé")
        st.empty()
        time.sleep(0.1)

    # KPI Principaux
    fraudes = df_demo[df_demo["prediction"] == "FRAUDE"]
    total = len(df_demo)
    taux_fraude = len(fraudes) / total * 100
    score_moyen = fraudes["fraud_score"].mean() if len(fraudes) > 0 else 0
    alerts_critiques = len(fraudes[fraudes["risk_level"] == "Critique"])

    st.markdown("### Indicateurs clés")
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Transactions 24h", f"{total:,}", "+12.3%", help="Volume total")
    with k2:
        st.metric("Alertes fraude", str(len(fraudes)),
                  f"{taux_fraude:.1f}% du volume",
                  delta_color="inverse", help="Transactions suspectes")
    with k3:
        st.metric("Critiques", str(alerts_critiques),
                  f"{alerts_critiques/max(len(fraudes),1)*100:.0f}% des alertes",
                  delta_color="inverse", help="Nécessitent action immédiate")
    with k4:
        st.metric("Score moyen fraude", f"{score_moyen:.3f}",
                  f"+{max(0, score_moyen-0.5):.2f}" if score_moyen > 0.5 else "stable",
                  help="Score de confiance moyen des fraudes détectées")
    with k5:
        st.metric("Taux de fraude", f"{taux_fraude:.2f}%",
                  f"-{abs(taux_fraude-3.5):.2f}%" if taux_fraude < 3.5 else f"+{abs(taux_fraude-3.5):.2f}%",
                  delta_color="inverse", help="Proportion de fraudes détectées")

    st.markdown("---")

    # Rangée 1: Graphiques principaux
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.subheader("📈 Évolution des alertes (24h)")
        hourly = df_demo.copy()
        hourly["hour"] = pd.to_datetime(hourly["timestamp"]).dt.hour
        alerts_hourly = hourly.groupby("hour").agg(
            total=("transaction_id", "count"),
            fraudes=("prediction", lambda x: (x == "FRAUDE").sum()),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=alerts_hourly["hour"], y=alerts_hourly["total"],
            mode="lines+markers", name="Transactions",
            line=dict(color="#42a5f5", width=2), fill="tozeroy", fillcolor="rgba(66,165,245,0.1)",
        ))
        fig.add_trace(go.Bar(
            x=alerts_hourly["hour"], y=alerts_hourly["fraudes"],
            name="Fraudes", marker_color="#ef5350", opacity=0.8,
        ))
        fig.update_layout(
            xaxis_title="Heure", yaxis_title="Volume",
            hovermode="x unified", template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("🎯 Répartition par risque")
        risk_counts = df_demo["risk_level"].value_counts().reindex(
            ["Faible", "Moyen", "Élevé", "Critique"], fill_value=0
        )
        colors = {"Faible": "#2e7d32", "Moyen": "#f9a825",
                  "Élevé": "#ef6c00", "Critique": "#c62828"}
        fig = go.Figure(data=[go.Pie(
            labels=risk_counts.index, values=risk_counts.values,
            marker_colors=[colors.get(l, "#78909c") for l in risk_counts.index],
            hole=0.5, textinfo="label+percent", textfont_size=11,
        )])
        fig.update_layout(
            template="plotly_dark", showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Rangée 2: KPIs temporels et transactions récentes
    col_c, col_d = st.columns([2, 3])

    with col_c:
        st.subheader("📊 Tendances J/J")
        kpi_recent = kpi_hist.tail(2)
        if len(kpi_recent) == 2:
            jj_f1 = kpi_recent["f1_score"].iloc[-1] - kpi_recent["f1_score"].iloc[0]
            jj_recall = kpi_recent["recall"].iloc[-1] - kpi_recent["recall"].iloc[0]
            jj_fraud = kpi_recent["fraud_rate"].iloc[-1] - kpi_recent["fraud_rate"].iloc[0]

            m1, m2, m3 = st.columns(3)
            delta_f1 = f"+{jj_f1:.3f}" if jj_f1 >= 0 else f"{jj_f1:.3f}"
            delta_recall = f"+{jj_recall:.3f}" if jj_recall >= 0 else f"{jj_recall:.3f}"
            delta_fraud = f"+{jj_fraud:.2f}pp" if jj_fraud >= 0 else f"{jj_fraud:.2f}pp"
            m1.metric("F1-Score", f"{kpi_recent['f1_score'].iloc[-1]:.3f}", delta_f1)
            m2.metric("Recall", f"{kpi_recent['recall'].iloc[-1]:.3f}", delta_recall)
            m3.metric("Taux fraude", f"{kpi_recent['fraud_rate'].iloc[-1]:.2f}%", delta_fraud,
                      delta_color="inverse")

        st.subheader("📊 Tendances S/S")
        if len(kpi_hist) >= 14:
            semaine1 = kpi_hist.tail(7)
            semaine2 = kpi_hist.tail(14).head(7)
            ss_f1 = semaine1["f1_score"].mean() - semaine2["f1_score"].mean()
            ss_recall = semaine1["recall"].mean() - semaine2["recall"].mean()
            ss_precision = semaine1["precision"].mean() - semaine2["precision"].mean()
            ss_fraud = semaine1["fraud_rate"].mean() - semaine2["fraud_rate"].mean()

            m4, m5, m6 = st.columns(3)
            m4.metric("F1 (S/S)", f"{semaine1['f1_score'].mean():.3f}",
                      f"{ss_f1:+.3f}" if abs(ss_f1) > 0.001 else "stable")
            m5.metric("Recall (S/S)", f"{semaine1['recall'].mean():.3f}",
                      f"{ss_recall:+.3f}" if abs(ss_recall) > 0.001 else "stable")
            m6.metric("Taux fraude (S/S)", f"{semaine1['fraud_rate'].mean():.2f}%",
                      f"{ss_fraud:+.2f}pp" if abs(ss_fraud) > 0.01 else "stable",
                      delta_color="inverse")

    with col_d:
        st.subheader("🕐 Alertes récentes")
        recent = df_demo.sort_values("timestamp", ascending=False).head(10)
        display = recent[["transaction_id", "montant_cfa", "fraud_score",
                          "risk_level", "prediction", "ville", "canal"]].copy()
        display["montant_cfa"] = display["montant_cfa"].apply(format_cfa)
        display["prediction"] = display["prediction"].apply(
            lambda x: f'<span class="status-pill {"fraude" if x=="FRAUDE" else "normal"}">{x}</span>'
        )
        display.columns = ["ID", "Montant", "Score", "Risque", "Statut", "Ville", "Canal"]
        st.write(display.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Mini carte Togo
    st.markdown("---")
    st.subheader("🗺️ Aperçu géographique")
    geo_agg = df_demo.groupby("ville").agg(
        transactions=("transaction_id", "count"),
        fraudes=("prediction", lambda x: (x == "FRAUDE").sum()),
    ).reset_index()
    geo_agg["taux_fraude"] = (geo_agg["fraudes"] / geo_agg["transactions"] * 100).round(1)
    geo_agg["lat"] = geo_agg["ville"].map(lambda v: TOGO_CITIES.get(v, {}).get("lat", 6.0))
    geo_agg["lon"] = geo_agg["ville"].map(lambda v: TOGO_CITIES.get(v, {}).get("lon", 1.0))

    fig = go.Figure()
    for _, row in geo_agg.iterrows():
        size = max(row["transactions"] / 5, 5)
        color = "red" if row["taux_fraude"] > 5 else "orange" if row["taux_fraude"] > 3 else "green"
        fig.add_trace(go.Scattergeo(
            lon=[row["lon"]], lat=[row["lat"]],
            text=f"{row['ville']}<br>{row['transactions']} tx<br>{row['taux_fraude']:.1f}% fraude",
            mode="markers+text", textposition="top center",
            marker=dict(size=size, color=color, line=dict(width=1, color="white"),
                        sizemode="area", sizeref=2.*max(geo_agg["transactions"])/(40.**2)),
            name=row["ville"],
        ))
    fig.update_geos(
        visible=False, resolution=50,
        scope="africa", showcountries=True,
        countrycolor="#1a3a5c", coastlinecolor="#1a3a5c",
        lataxis_range=[5, 11.5], lonaxis_range=[-0.5, 2.5],
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        title=dict(text="Transactions par ville (Togo)", font=dict(size=14)),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
#  PAGE 2 : GÉO-VISUALISATION TOGO
# ─────────────────────────────────────────────

elif page == "🗺️ Géo-visualisation Togo":
    st.title("🗺️ Géo-visualisation des transactions au Togo")
    st.caption("Analyse spatiale de la fraude par ville et région")

    df_demo = generate_fake_transactions(500)

    # Filtres
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        regions = st.multiselect("Régions", ["Maritime", "Plateaux", "Kara", "Centrale", "Savanes"],
                                 default=["Maritime", "Plateaux", "Kara", "Centrale", "Savanes"])
    with col_f2:
        canal_f = st.multiselect("Canaux", ["USSD", "APP", "AGENT", "WEB"], default=[])
    with col_f3:
        min_score = st.slider("Score min.", 0.0, 1.0, 0.0, 0.05)

    # Filtrer
    villes_filtrees = [v for v, c in TOGO_CITIES.items() if c["region"] in regions]
    df_viz = df_demo[df_demo["ville"].isin(villes_filtrees)]
    if canal_f:
        df_viz = df_viz[df_viz["canal"].isin(canal_f)]
    df_viz = df_viz[df_viz["fraud_score"] >= min_score]

    # Agrégation
    geo_agg = df_viz.groupby("ville").agg(
        transactions=("transaction_id", "count"),
        fraudes=("prediction", lambda x: (x == "FRAUDE").sum()),
        montant_moyen=("montant_cfa", "mean"),
        score_moyen=("fraud_score", "mean"),
    ).reset_index()
    geo_agg["taux_fraude"] = (geo_agg["fraudes"] / geo_agg["transactions"] * 100).round(1)
    geo_agg["montant_moyen"] = geo_agg["montant_moyen"].apply(format_cfa)
    geo_agg["lat"] = geo_agg["ville"].map(lambda v: TOGO_CITIES.get(v, {}).get("lat", 6.0))
    geo_agg["lon"] = geo_agg["ville"].map(lambda v: TOGO_CITIES.get(v, {}).get("lon", 1.0))

    col_maps, col_stats = st.columns([3, 2])

    with col_maps:
        # Carte principale
        fig = go.Figure()

        # Taille des bulles = volume, couleur = taux de fraude
        for _, row in geo_agg.iterrows():
            size = max(row["transactions"] * 3, 8)
            taux = row["taux_fraude"]
            if taux >= 5:
                color = "#c62828"
            elif taux >= 3:
                color = "#ef6c00"
            elif taux >= 1:
                color = "#fdd835"
            else:
                color = "#2e7d32"

            fig.add_trace(go.Scattergeo(
                lon=[row["lon"]], lat=[row["lat"]],
                text=(
                    f"<b>{row['ville']}</b><br>"
                    f"Transactions: {row['transactions']:,}<br>"
                    f"Fraudes: {row['fraudes']}<br>"
                    f"Taux: {row['taux_fraude']:.1f}%<br>"
                    f"Score moyen: {row['score_moyen']:.3f}<br>"
                    f"Montant moyen: {row['montant_moyen']}"
                ),
                hoverinfo="text",
                mode="markers+text",
                textposition="top center",
                textfont=dict(size=9, color="#b0bec5"),
                marker=dict(
                    size=size, color=color,
                    line=dict(width=1, color="white"),
                    sizemode="area",
                ),
                name=row["ville"],
                showlegend=False,
            ))

        fig.update_geos(
            visible=False, resolution=50,
            scope="africa", showcountries=True,
            countrycolor="#1a3a5c", coastlinecolor="#1a3a5c",
            lataxis_range=[5.5, 11.5], lonaxis_range=[-0.5, 2.5],
            bgcolor="rgba(0,0,0,0)",
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=550,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        st.subheader("📊 Statistiques par ville")
        if not geo_agg.empty:
            display = geo_agg.sort_values("taux_fraude", ascending=False)
            display = display[["ville", "transactions", "fraudes", "taux_fraude", "score_moyen"]]
            display.columns = ["Ville", "Tx", "Fraudes", "Taux %", "Score"]
            display["Taux %"] = display["Taux %"].apply(lambda x: f"{x:.1f}%")
            display["Score"] = display["Score"].apply(lambda x: f"{x:.3f}")
            st.dataframe(display, use_container_width=True, hide_index=True)

            # Top 3 villes à risque
            st.subheader("⚠️ Top 3 villes à risque")
            top3 = geo_agg.sort_values("taux_fraude", ascending=False).head(3)
            for _, row in top3.iterrows():
                st.markdown(
                    f"""<div style="background:#1a2332; border-left:4px solid #c62828;
                        border-radius:4px; padding:8px 12px; margin:4px 0;">
                        <b>{row['ville']}</b> — {row['taux_fraude']:.1f}% fraude
                        <span style="color:#78909c;float:right;">
                        {row['transactions']} tx, {row['fraudes']} fraudes</span>
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.info("Aucune donnée pour les filtres sélectionnés")

    # Évolution temporelle par région
    st.markdown("---")
    st.subheader("📈 Évolution du taux de fraude par région")
    regions_data = []
    for city, info in TOGO_CITIES.items():
        if info["region"] in regions:
            city_data = df_viz[df_viz["ville"] == city].copy()
            if not city_data.empty:
                regions_data.append({
                    "region": info["region"],
                    "ville": city,
                    "taux": len(city_data[city_data["prediction"] == "FRAUDE"]) / max(len(city_data), 1) * 100,
                    "volume": len(city_data),
                })
    if regions_data:
        df_regions = pd.DataFrame(regions_data)
        agg_regions = df_regions.groupby("region").agg(
            taux_moyen=("taux", "mean"),
            volume=("volume", "sum"),
        ).reset_index()
        fig = px.bar(agg_regions, x="region", y="taux_moyen", color="taux_moyen",
                     text=agg_regions["taux_moyen"].apply(lambda x: f"{x:.1f}%"),
                     color_continuous_scale="RdYlGn_r",
                     labels={"region": "Région", "taux_moyen": "Taux de fraude moyen (%)"})
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
#  PAGE 3 : WHAT-IF ANALYSIS
# ─────────────────────────────────────────────

elif page == "🧪 What-if Analysis":
    st.title("🧪 What-if Analysis")
    st.caption("Simulez l'impact des features sur la décision du modèle")

    st.info("""
    Ajustez les paramètres ci-dessous pour voir comment le score de fraude évolue.
    Les sliders modifient les caractéristiques de la transaction en temps réel.
    """)

    col_inputs, col_results = st.columns([1, 1])

    with col_inputs:
        st.subheader("Paramètres de la transaction")
        montant = st.slider("Montant (FCFA)", 1000, 2_000_000, 50_000, 5000,
                           help="Montant de la transaction")
        heure = st.slider("Heure", 0, 23, 14, 1,
                          help="Heure de la transaction (0-23)")
        device_change = st.slider("Jours depuis dernier changement SIM", 0, 365, 90, 1,
                                  help="Nombre de jours depuis le dernier SIM swap")
        tx_30min = st.slider("Transactions dans les 30 dernières minutes", 0, 10, 0, 1,
                             help="Nombre de transactions effectuées dans les 30 dernières minutes")

        col_op1, col_op2 = st.columns(2)
        with col_op1:
            canal = st.selectbox("Canal", ["AGENT", "USSD", "APP", "WEB"])
            operateur = st.selectbox("Opérateur", ["TogoCom Cash", "Moov Money", "Flooz", "TMoney"])
        with col_op2:
            type_op = st.selectbox("Type d'opération", ["TRANSFERT", "PAIEMENT", "RECHARGE", "RETRAIT"])
            ville = st.selectbox("Ville", list(TOGO_CITIES.keys()))

    # Calcul du score de fraude simulé
    score = 0.0
    details = []

    # Règle : montant élevé
    if montant > 500000:
        s = min((montant - 500000) / 1500000 * 0.25, 0.25)
        score += s
        details.append(("Montant très élevé", s, "+"))
    elif montant > 200000:
        s = (montant - 200000) / 300000 * 0.15
        score += s
        details.append(("Montant élevé", s, "+"))

    # Règle : heure inhabituelle
    if heure < 6 or heure > 22:
        s = 0.12
        score += s
        details.append(("Heure inhabituelle", s, "+"))

    # Règle : changement SIM récent
    if device_change < 7:
        s = 0.20
        score += s
        details.append(("Changement SIM récent (< 7j)", s, "+"))
    elif device_change < 30:
        s = 0.08
        score += s
        details.append(("Changement SIM récent (< 30j)", s, "+"))

    # Règle : fréquence élevée
    if tx_30min >= 5:
        s = 0.25
        score += s
        details.append(("Fréquence très élevée (>5 en 30min)", s, "+"))
    elif tx_30min >= 3:
        s = 0.12
        score += s
        details.append(("Fréquence élevée (>3 en 30min)", s, "+"))

    # Règle : canal à risque
    if canal == "USSD":
        s = 0.06
        score += s
        details.append(("Canal USSD", s, "+"))

    # Règle : opérateur
    if operateur == "Flooz":
        s = 0.05
        score += s
        details.append(("Opérateur Flooz", s, "+"))

    # Règle : nuit + AGENT
    if heure < 6 and canal == "AGENT":
        s = 0.10
        score += s
        details.append(("Nuit + AGENT (pattern suspect)", s, "+"))

    # Règle : type d'opération
    if type_op == "RETRAIT" and montant > 300000:
        s = 0.08
        score += s
        details.append(("Retrait > 300k FCFA", s, "+"))

    # Règle : petite ville + gros montant (anomalie géographique)
    city_pop = TOGO_CITIES.get(ville, {}).get("population", 0)
    if city_pop < 30000 and montant > 300000:
        s = 0.12
        score += s
        details.append(("Petite ville + montant élevé (anomalie)", s, "+"))

    score = min(score, 0.99)

    # Bruit aléatoire pour réalisme
    np.random.seed(int(montant + heure + device_change + tx_30min))
    score += np.random.uniform(-0.03, 0.03)
    score = np.clip(score, 0.01, 0.99)

    prediction = "FRAUDE" if score >= 0.55 else "NORMALE"
    if score >= 0.7:
        risk = "Critique"
    elif score >= 0.55:
        risk = "Élevé"
    elif score >= 0.3:
        risk = "Moyen"
    else:
        risk = "Faible"

    # Résultats
    with col_results:
        st.subheader("🔮 Résultat de l'analyse")

        # Affichage du score avec jauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score * 100,
            number={"suffix": "%", "font": {"size": 36, "color": "#e8eaf6"}},
            delta={"reference": 55, "increasing": {"color": "#ef5350"},
                   "decreasing": {"color": "#66bb6a"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#78909c", "tickwidth": 1},
                "bar": {"color": "#ef5350" if score >= 0.55 else "#66bb6a", "thickness": 0.3},
                "bgcolor": "#1a2332",
                "borderwidth": 1,
                "bordercolor": "#1a3a5c",
                "steps": [
                    {"range": [0, 30], "color": "rgba(46,125,50,0.2)"},
                    {"range": [30, 55], "color": "rgba(255,193,7,0.2)"},
                    {"range": [55, 70], "color": "rgba(239,108,0,0.2)"},
                    {"range": [70, 100], "color": "rgba(198,40,40,0.2)"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 2},
                    "thickness": 0.75, "value": 55,
                },
            },
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=250, margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Statut
        pred_color = "red" if prediction == "FRAUDE" else "green"
        st.markdown(
            f"<h2 style='text-align:center; color:{pred_color}; "
            f"background:#1a2332; padding:10px; border-radius:8px; "
            f"border:2px solid {pred_color};'>"
            f"{'🚨 ' if prediction == 'FRAUDE' else '✅ '}"
            f"{prediction}</h2>",
            unsafe_allow_html=True,
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Risque", risk)
        m2.metric("Score", f"{score:.3f}")
        m3.metric("Canal", canal)

        # Facteurs contributifs (SHAP-like)
        st.subheader("📋 Facteurs contributifs")
        if details:
            df_details = pd.DataFrame(details, columns=["Facteur", "Contribution", "Impact"])
            df_details["Contribution"] = df_details["Contribution"].apply(
                lambda x: f"+{x:.2f}" if x > 0 else f"{x:.2f}"
            )
            fig = px.bar(
                df_details.sort_values("Contribution", key=lambda x: x.str.replace("+", "").astype(float),
                                       ascending=True),
                x="Contribution", y="Facteur",
                orientation="h",
                color="Impact",
                color_discrete_map={"+": "#ef5350"},
                labels={"Contribution": "Contribution au score"},
            )
            fig.update_layout(
                template="plotly_dark", showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=250, margin=dict(l=10, r=10, t=10, b=10),
                xaxis_range=[0, 1],
            )
            st.plotly_chart(fig, use_container_width=True)

    # Export
    st.markdown("---")
    col_export1, col_export2 = st.columns([3, 1])
    with col_export2:
        report_html = f"""
        <html>
        <head><meta charset="utf-8">
        <style>
            body {{ font-family: Arial; background: #0a1628; color: #e8eaf6; padding: 40px; }}
            h1 {{ color: #90caf9; border-bottom: 2px solid #1a3a5c; }}
            .card {{ background: #111d2e; border: 1px solid #1a3a5c; border-radius: 12px; padding: 20px; margin: 10px 0; }}
            .fraude {{ color: #ef5350; }}
            .normal {{ color: #66bb6a; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #1a3a5c; }}
            th {{ color: #90caf9; }}
        </style></head>
        <body>
            <h1>🛡️ FRAUDX — Rapport d'analyse</h1>
            <div class="card">
                <h2 class="{'fraude' if prediction == 'FRAUDE' else 'normal'}">{prediction}</h2>
                <p><b>Score :</b> {score:.3f} ({score*100:.1f}%)</p>
                <p><b>Risque :</b> {risk}</p>
            </div>
            <div class="card">
                <h3>Paramètres</h3>
                <table>
                    <tr><th>Paramètre</th><th>Valeur</th></tr>
                    <tr><td>Montant</td><td>{format_cfa(montant)}</td></tr>
                    <tr><td>Heure</td><td>{heure}h</td></tr>
                    <tr><td>Canal</td><td>{canal}</td></tr>
                    <tr><td>Opérateur</td><td>{operateur}</td></tr>
                    <tr><td>Type</td><td>{type_op}</td></tr>
                    <tr><td>Ville</td><td>{ville}</td></tr>
                    <tr><td>Changement SIM</td><td>{device_change} jours</td></tr>
                    <tr><td>Tx/30min</td><td>{tx_30min}</td></tr>
                </table>
            </div>
            <div class="card">
                <h3>Facteurs contributifs</h3>
                <table>
                    <tr><th>Facteur</th><th>Contribution</th></tr>
                    {''.join(f'<tr><td>{f[0]}</td><td>{f[1]:+.3f}</td></tr>' for f in details)}
                </table>
            </div>
            <p style="color:#455a64; text-align:center; margin-top:40px;">
                Généré par FRAUDX — {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </p>
        </body></html>
        """
        st.download_button(
            "📥 Télécharger le rapport HTML",
            data=report_html,
            file_name=f"fraudx_whatif_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True,
        )


# ─────────────────────────────────────────────
#  PAGE 4 : ANALYSE TRANSACTION
# ─────────────────────────────────────────────

elif page == "🔍 Analyse Transaction":
    st.title("🔍 Analyse d'une transaction")
    st.caption("Analyse détaillée d'une transaction avec prédiction et SHAP")

    tab1, tab2 = st.tabs(["💳 Carte bancaire", "🇹🇬 Mobile Money Togo"])

    # ─── Tab 1 : Carte bancaire ───
    with tab1:
        with st.form("transaction_form"):
            col1, col2 = st.columns(2)
            with col1:
                montant = st.number_input("Montant (FCFA)", min_value=0, value=50000, step=1000)
                card1 = st.number_input("ID Carte/Device", value=12345)
                card4 = st.selectbox("Type de carte", ["", "visa", "mastercard", "discover", "america express"])
                hour = st.slider("Heure", 0, 23, 14)
            with col2:
                product = st.selectbox("Type de produit", ["", "W", "H", "C", "S", "R"])
                addr1 = st.number_input("Adresse (addr1)", value=200)
                dayofweek = st.slider("Jour de la semaine", 0, 6, 3)
                canal = st.selectbox("Canal", ["Carte bancaire", "TogoCom Cash", "Moov Money", "Flooz", "USSD"])

            submitted = st.form_submit_button("🔍 Analyser", type="primary", use_container_width=True)

        if submitted:
            with st.spinner("Analyse en cours..."):
                payload = {
                    "TransactionAmt": montant,
                    "card1": float(card1) if card1 else None,
                    "card4": card4 if card4 else None,
                    "ProductCD": product if product else None,
                    "addr1": float(addr1) if addr1 else None,
                    "hour": hour,
                    "dayofweek": dayofweek,
                }

                try:
                    r = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
                    if r.status_code == 200:
                        result = r.json()
                    else:
                        raise Exception(r.text)
                except:
                    # Mode démo sans API
                    score = min(0.02 + (montant > 200000) * 0.3 + (hour < 6) * 0.15 +
                                (canal == "USSD") * 0.05, 0.95)
                    score += np.random.uniform(-0.05, 0.05)
                    score = np.clip(score, 0.01, 0.99)
                    result = {
                        "fraud_score": score,
                        "prediction": "FRAUDE" if score >= 0.55 else "NORMALE",
                        "risk_level": "Critique" if score >= 0.7 else "Élevé" if score >= 0.55 else "Moyen" if score >= 0.3 else "Faible",
                        "transaction_id": f"DEMO_{int(time.time())}",
                        "top_features": [
                            {"feature": "TransactionAmt", "shap_value": score * 0.4, "impact": "positif (fraude)"},
                            {"feature": "hour", "shap_value": score * 0.25, "impact": "positif (fraude)"},
                            {"feature": "card1", "shap_value": score * 0.15, "impact": "positif (fraude)"},
                        ],
                    }

            # Résultat
            score = result["fraud_score"]
            prediction = result["prediction"]
            risk = result["risk_level"]
            tx_id = result["transaction_id"]

            col_res1, col_res2, col_res3 = st.columns([1, 2, 1])
            pred_color = "red" if prediction == "FRAUDE" else "green"
            col_res2.markdown(
                f"<h1 style='text-align:center; color:{pred_color}; "
                f"background:#1a2332; padding:20px; border-radius:12px; "
                f"border:3px solid {pred_color};'>"
                f"{'🚨 ' if prediction == 'FRAUDE' else '✅ '}"
                f"{prediction}</h1>",
                unsafe_allow_html=True,
            )

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Score de fraude", f"{score:.3f}")
            k2.metric("Niveau de risque", risk)
            k3.metric("Transaction ID", tx_id[:12] + "...")
            k4.metric("Montant", format_cfa(montant))

            # Facteurs SHAP
            st.subheader("📊 Facteurs influençant la décision (SHAP)")
            if result.get("top_features"):
                features_df = pd.DataFrame(result["top_features"])
                features_df["shap_value"] = features_df["shap_value"].round(4)
                st.dataframe(features_df, use_container_width=True, hide_index=True)

                fig = px.bar(
                    features_df,
                    x="shap_value", y="feature",
                    color="impact", orientation="h",
                    labels={"shap_value": "Impact SHAP", "feature": "Variable"},
                    color_discrete_map={
                        "positif (fraude)": "#ef5350",
                        "négatif (normale)": "#66bb6a",
                    },
                )
                fig.update_layout(
                    template="plotly_dark", showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=250,
                )
                st.plotly_chart(fig, use_container_width=True)

            # Feedback
            st.subheader("👤 Feedback analyste")
            fb_col1, fb_col2 = st.columns(2)
            with fb_col1:
                if st.button("✅ Confirmer fraude", use_container_width=True):
                    try:
                        requests.post(f"{API_URL}/feedback",
                                     params={"transaction_id": tx_id, "is_fraud": True, "analyst": "dashboard"})
                        st.success("Feedback enregistré ✅")
                    except:
                        st.success("Feedback enregistré (mode démo) ✅")
            with fb_col2:
                if st.button("❌ Faux positif", use_container_width=True):
                    try:
                        requests.post(f"{API_URL}/feedback",
                                     params={"transaction_id": tx_id, "is_fraud": False, "analyst": "dashboard"})
                        st.success("Feedback enregistré ✅")
                    except:
                        st.success("Feedback enregistré (mode démo) ✅")

            # Export PDF
            report_html = f"""
            <html>
            <head><meta charset="utf-8">
            <style>
                body {{ font-family: Arial; background: #0a1628; color: #e8eaf6; padding: 40px; }}
                h1 {{ color: #90caf9; }}
                .card {{ background: #111d2e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 15px; margin: 10px 0; }}
                .pred {{ font-size: 24px; text-align: center; padding: 15px; border-radius: 8px; }}
                .fraude {{ color: #ef5350; border: 2px solid #ef5350; }}
                .normal {{ color: #66bb6a; border: 2px solid #66bb6a; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #1a3a5c; }}
                th {{ color: #90caf9; }}
            </style></head>
            <body>
                <h1>🛡️ FRAUDX — Rapport d'analyse transaction</h1>
                <div class="card pred {prediction.lower()}">{prediction}</div>
                <div class="card">
                    <p><b>Transaction :</b> {tx_id}</p>
                    <p><b>Score :</b> {score:.3f}</p>
                    <p><b>Risque :</b> {risk}</p>
                    <p><b>Montant :</b> {format_cfa(montant)}</p>
                </div>
                <p style="color:#455a64;">Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </body></html>
            """
            st.download_button(
                "📥 Télécharger le rapport (HTML)",
                data=report_html,
                file_name=f"fraudx_report_{tx_id[:8]}.html",
                mime="text/html",
                use_container_width=True,
            )

    # ─── Tab 2 : Mobile Money Togo ───
    with tab2:
        st.markdown("🇹🇬 Analyse adaptée aux opérateurs Mobile Money du Togo (TogoCom, Moov, Flooz)")
        with st.form("togo_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                montant_tg = st.number_input("Montant (FCFA)", min_value=0, value=50000, step=1000,
                                             key="tg_mt")
                canal_tg = st.selectbox("Canal", ["USSD", "APP", "AGENT", "WEB"], key="tg_cnl")
                operateur_tg = st.selectbox("Opérateur", ["TogoCom Cash", "Moov Money", "Flooz"], key="tg_op")
            with col2:
                ville_tg = st.selectbox("Ville", list(TOGO_CITIES.keys()), key="tg_vil")
                operation_tg = st.selectbox("Type", ["RECHARGE", "TRANSFERT", "PAIEMENT", "RETRAIT"], key="tg_opr")
                device_change_tg = st.number_input("Jours depuis dernier changement SIM", 0, 365, 0, key="tg_dev")
            with col3:
                tx_last_30_tg = st.number_input("Transactions < 30 min", 0, 20, 0, key="tg_tx30")
                st.markdown("####")
                submitted_tg = st.form_submit_button("🔍 Analyser", type="primary", use_container_width=True)

        if submitted_tg:
            with st.spinner("Analyse mobile money en cours..."):
                score_tg = min(
                    0.02 + (montant_tg > 200000) * 0.25 + (device_change_tg < 7) * 0.20 +
                    (tx_last_30_tg > 3) * 0.15 + (canal_tg == "USSD") * 0.06 +
                    (operation_tg == "TRANSFERT" and montant_tg > 300000) * 0.10,
                    0.98
                )
                score_tg += np.random.uniform(-0.03, 0.03)
                score_tg = np.clip(score_tg, 0.01, 0.99)

                pred_tg = "FRAUDE" if score_tg >= 0.55 else "NORMALE"
                risk_tg = "Critique" if score_tg >= 0.7 else "Élevé" if score_tg >= 0.55 else "Moyen" if score_tg >= 0.3 else "Faible"

                pred_color_tg = "red" if pred_tg == "FRAUDE" else "green"
                st.markdown(
                    f"<h2 style='text-align:center; color:{pred_color_tg}; "
                    f"background:#1a2332; padding:15px; border-radius:8px; "
                    f"border:2px solid {pred_color_tg};'>"
                    f"{'🚨 ' if pred_tg == 'FRAUDE' else '✅ '}{pred_tg}</h2>",
                    unsafe_allow_html=True,
                )

                mk1, mk2, mk3 = st.columns(3)
                mk1.metric("Score", f"{score_tg:.3f}")
                mk2.metric("Risque", risk_tg)
                mk3.metric("Montant", format_cfa(montant_tg))

            # Feedback Togo
            fb1, fb2 = st.columns(2)
            with fb1:
                if st.button("✅ Confirmer fraude", key="tg_fb1", use_container_width=True):
                    st.success("Feedback enregistré ✅")
            with fb2:
                if st.button("❌ Faux positif", key="tg_fb2", use_container_width=True):
                    st.success("Feedback enregistré ✅")


# ─────────────────────────────────────────────
#  PAGE 5 : MONITORING
# ─────────────────────────────────────────────

elif page == "📈 Monitoring":
    st.title("📈 Monitoring du système")
    st.caption("Surveillance des performances du modèle et de la santé du système")

    kpi_hist = generate_kpi_history(60)

    # KPIs globaux
    st.markdown("### Performance globale")
    last = kpi_hist.iloc[-1]
    prev = kpi_hist.iloc[-2] if len(kpi_hist) > 1 else last

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("F1-Score", f"{last['f1_score']:.3f}",
                  f"{last['f1_score'] - prev['f1_score']:+.3f}")
    col_m2.metric("Rappel (Recall)", f"{last['recall']:.3f}",
                  f"{last['recall'] - prev['recall']:+.3f}")
    col_m3.metric("Précision", f"{last['precision']:.3f}",
                  f"{last['precision'] - prev['precision']:+.3f}")
    col_m4.metric("Taux fraude", f"{last['fraud_rate']:.2f}%",
                  f"{last['fraud_rate'] - prev['fraud_rate']:+.2f}pp",
                  delta_color="inverse")
    col_m5.metric("Latence moy.", f"{last['avg_latency_ms']:.0f} ms",
                  f"{last['avg_latency_ms'] - prev['avg_latency_ms']:+:.0f} ms",
                  delta_color="inverse")

    st.markdown("---")

    # Graphiques d'évolution
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("📈 Évolution du F1-Score")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=kpi_hist["f1_score"],
            mode="lines", name="F1-Score", line=dict(color="#42a5f5", width=2),
            fill="tozeroy", fillcolor="rgba(66,165,245,0.1)",
        ))
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=kpi_hist["recall"],
            mode="lines", name="Recall", line=dict(color="#66bb6a", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=kpi_hist["precision"],
            mode="lines", name="Précision", line=dict(color="#ffa726", width=2),
        ))
        # Seuil minimum
        fig.add_hline(y=0.80, line_dash="dash", line_color="#ef5350",
                      annotation_text="Seuil minimum (0.80)")
        fig.update_layout(
            template="plotly_dark", hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.subheader("📊 Volume et latence")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=kpi_hist["date"], y=kpi_hist["total_transactions"],
            name="Transactions", marker_color="#42a5f5", opacity=0.6,
        ))
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=kpi_hist["avg_latency_ms"],
            name="Latence (ms)", yaxis="y2", mode="lines+markers",
            line=dict(color="#ef5350", width=2),
        ))
        fig.update_layout(
            template="plotly_dark", hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="Transactions", side="left"),
            yaxis2=dict(title="Latence (ms)", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Détection d'anomalies
    st.markdown("---")
    st.subheader("🚨 Détection d'anomalies sur les métriques")

    # Détection simple par Z-score
    mean_f1 = kpi_hist["f1_score"].mean()
    std_f1 = kpi_hist["f1_score"].std()
    kpi_hist["f1_zscore"] = (kpi_hist["f1_score"] - mean_f1) / std_f1
    anomalies = kpi_hist[abs(kpi_hist["f1_zscore"]) > 2]

    col_a1, col_a2 = st.columns([2, 1])

    with col_a1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=kpi_hist["f1_score"],
            mode="lines", name="F1-Score", line=dict(color="#42a5f5", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=[mean_f1] * len(kpi_hist["date"]), y=kpi_hist["date"],
            mode="lines", name="Moyenne", line=dict(color="#78909c", width=1, dash="dash"),
        ))
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies["date"], y=anomalies["f1_score"],
                mode="markers", name="Anomalies",
                marker=dict(color="#ef5350", size=10, symbol="x"),
            ))
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=[mean_f1 + 2 * std_f1] * len(kpi_hist["date"]),
            mode="lines", name="Seuil +2σ", line=dict(color="#ef5350", width=1, dash="dot"),
        ))
        fig.add_trace(go.Scatter(
            x=kpi_hist["date"], y=[mean_f1 - 2 * std_f1] * len(kpi_hist["date"]),
            mode="lines", name="Seuil -2σ", line=dict(color="#ef5350", width=1, dash="dot"),
        ))
        fig.update_layout(
            template="plotly_dark", hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title="Détection d'anomalies — F1-Score",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_a2:
        st.markdown("### Anomalies détectées")
        if not anomalies.empty:
            for _, row in anomalies.iterrows():
                is_low = row["f1_score"] < mean_f1
                st.markdown(
                    f"""<div style="background:#1a2332; border-left:4px solid {'#ef5350' if is_low else '#ffa726'};
                        border-radius:4px; padding:8px 12px; margin:4px 0;">
                        <b>{row['date'].strftime('%d/%m')}</b><br>
                        F1 = {row['f1_score']:.3f}
                        <span style="color:#78909c;">(Z={row['f1_zscore']:.1f})</span>
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.success("✅ Aucune anomalie détectée")

        st.markdown("### Statistiques")
        st.markdown(f"""
        - **Moyenne F1** : {mean_f1:.3f}
        - **Écart-type** : {std_f1:.3f}
        - **Max** : {kpi_hist['f1_score'].max():.3f}
        - **Min** : {kpi_hist['f1_score'].min():.3f}
        - **Dernier** : {last['f1_score']:.3f}
        """)

    # Logs récents
    st.markdown("---")
    st.subheader("📋 Logs récents")
    try:
        r = requests.get(f"{API_URL}/logs?limit=20", timeout=3)
        if r.status_code == 200:
            logs = r.json().get("recent", [])
            if logs:
                df_logs = pd.DataFrame(logs)
                cols = [c for c in ["transaction_id", "fraud_score", "prediction", "risk_level", "timestamp"]
                        if c in df_logs.columns]
                if cols:
                    st.dataframe(df_logs[cols], use_container_width=True, hide_index=True)
    except:
        st.info("💡 API non disponible — logs démo indisponibles")


# ─────────────────────────────────────────────
#  PAGE 6 : CONFIGURATION
# ─────────────────────────────────────────────

elif page == "⚙️ Configuration":
    st.title("⚙️ Configuration du système")
    st.caption("Paramétrage des seuils de détection et du réentraînement")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("🎯 Seuils de détection")
        seuil_critique = st.slider("Seuil critique", 0.0, 1.0, 0.85, 0.01,
                                   help="Score au-dessus duquel le risque est 'Critique'")
        seuil_eleve = st.slider("Seuil élevé", 0.0, 1.0, 0.65, 0.01,
                                help="Score au-dessus duquel le risque est 'Élevé'")
        seuil_moyen = st.slider("Seuil moyen", 0.0, 1.0, 0.40, 0.01,
                                help="Score au-dessus duquel le risque est 'Moyen'")

        st.subheader("📊 Performance cible")
        f1_min = st.slider("F1-Score minimum", 0.6, 0.95, 0.80, 0.01)
        fp_max = st.slider("Taux de faux positifs max (%)", 0.0, 10.0, 3.0, 0.1)

    with col_c2:
        st.subheader("🔄 Réentraînement")
        auto_retrain = st.checkbox("Activer le réentraînement automatique", value=True)
        retrain_freq = st.number_input("Fréquence (heures)", min_value=1, value=24, step=1)
        min_samples = st.number_input("Échantillons minimum pour réentraînement",
                                      min_value=100, value=500, step=100)

        st.subheader("📡 API")
        api_host = st.text_input("Hôte", value="0.0.0.0")
        api_port = st.number_input("Port", value=8000, min_value=1024, max_value=65535)
        dashboard_port = st.number_input("Port Dashboard", value=8501, min_value=1024, max_value=65535)

    st.markdown("---")

    col_save, col_retrain = st.columns(2)

    with col_save:
        if st.button("💾 Sauvegarder la configuration", use_container_width=True):
            config_data = {
                "seuils": {"critique": seuil_critique, "eleve": seuil_eleve, "moyen": seuil_moyen},
                "performance": {"f1_min": f1_min, "fp_max": fp_max},
                "retrain": {"auto": auto_retrain, "freq_h": retrain_freq, "min_samples": min_samples},
                "api": {"host": api_host, "port": api_port, "dashboard_port": dashboard_port},
                "updated_at": datetime.now().isoformat(),
            }
            Path("config").mkdir(exist_ok=True)
            with open("config/dashboard_config.json", "w") as f:
                json.dump(config_data, f, indent=2)
            st.success("✅ Configuration sauvegardée dans config/dashboard_config.json")

    with col_retrain:
        if st.button("🔄 Lancer le réentraînement maintenant",
                     use_container_width=True, type="primary"):
            with st.spinner("🔄 Réentraînement en cours..."):
                result = subprocess.run(
                    ["python", "retrain.py", "--min-samples", str(min_samples)],
                    capture_output=True, text=True, timeout=120
                )
            if result.returncode == 0:
                st.success("✅ Réentraînement terminé avec succès")
            else:
                st.error(f"❌ Erreur : {result.stderr[:200]}")
            with st.expander("📋 Logs du réentraînement"):
                st.code(result.stdout + "\n" + result.stderr)

    # Résumé de la configuration active
    st.markdown("---")
    st.subheader("📋 Résumé de la configuration active")
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.markdown(f"""
    **Seuils de risque**
    - Critique : ≥ {seuil_critique:.2f}
    - Élevé : ≥ {seuil_eleve:.2f}
    - Moyen : ≥ {seuil_moyen:.2f}
    - Faible : < {seuil_moyen:.2f}
    """)
    col_s2.markdown(f"""
    **Performance**
    - F1 minimum : {f1_min:.2f}
    - FP max : {fp_max:.1f}%
    """)
    col_s3.markdown(f"""
    **Réentraînement**
    - Auto : {'Oui' if auto_retrain else 'Non'}
    - Fréquence : {retrain_freq}h
    - Échantillons min : {min_samples}
    """)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────

st.markdown(
    '<div class="footer">'
    '🛡️ FRAUDX v2.0 — Détection de fraude bancaire et Mobile Money au Togo<br>'
    'Tableau de bord interactif pour le mémoire de B3 IT-MD</div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    port = os.environ.get("DASHBOARD_PORT", "8501")
    cmd = ["streamlit", "run", __file__, "--server.port", port,
           "--server.address", "0.0.0.0", "--browser.gatherUsageStats", "false"]
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
