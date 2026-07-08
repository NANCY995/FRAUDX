import streamlit as st
from pathlib import Path


FRAUDX_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="metric-container"] { background: linear-gradient(135deg, #111d2e, #1a2a4a); border:1px solid #1a3a5c; border-radius:12px; padding:12px 16px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0a1628, #0f1f3a); border-right:1px solid #1a3a5c; }
.step-active { border-left:4px solid #42a5f5; background: linear-gradient(90deg, #111d2e, #1a2a4a); padding:10px; border-radius:4px; margin:4px 0; }
.step-done { border-left:4px solid #4caf50; background: linear-gradient(90deg, #111d2e, #1a2a4a); padding:10px; border-radius:4px; margin:4px 0; }
.step-pending { border-left:4px solid #455a64; background: linear-gradient(90deg, #111d2e, #1a2a4a); padding:10px; border-radius:4px; margin:4px 0; }
.stApp { background: #0a1628; }
.hero-title { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #42a5f5, #7c4dff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
.hero-sub { font-size: 1.1rem; color: #90a4ae; margin-bottom: 2rem; }
.card { background: linear-gradient(135deg, #111d2e, #1a2a4a); border: 1px solid #1a3a5c; border-radius: 12px; padding: 20px; margin: 8px 0; }
.card-title { font-size: 1.1rem; font-weight: 600; color: #42a5f5; margin-bottom: 8px; }
.card-text { color: #b0bec5; font-size: 0.9rem; }
.badge { display: inline-block; background: #1a3a5c; color: #90caf9; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; }
div[data-testid="stExpander"] { background: linear-gradient(135deg, #111d2e, #1a2a4a) !important; border: 1px solid #1a3a5c !important; border-radius: 12px !important; }
"""


def init_session_state():
    defaults = {
        "df": None, "df_name": "", "X_train": None, "X_test": None,
        "y_train": None, "y_test": None, "model": None, "metrics": None,
        "preprocessor": None, "threshold": 0.5, "steps_done": set(),
        "optuna_progress": [], "shap_values": None, "shap_data": None,
        "model_loaded": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def sidebar_pipeline(steps, page_names, page_map, page):
    st.sidebar.markdown("<h1 style='text-align:center;'>FRAUDX</h1>", unsafe_allow_html=True)
    st.sidebar.caption("Detection de fraude bancaire par IA")
    st.sidebar.markdown("---\n### Pipeline")
    for icon, name, key in steps:
        if key in st.session_state.steps_done:
            st.sidebar.markdown(f'<div class="step-done">&#10003; {icon} {name}</div>', unsafe_allow_html=True)
        elif key == st.session_state.get("current_step"):
            st.sidebar.markdown(f'<div class="step-active">&#9654; {icon} {name}</div>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f'<div class="step-pending">{icon} {name}</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    if st.session_state.df is not None:
        st.sidebar.metric("Dataset", st.session_state.df_name, f"{len(st.session_state.df):,} lignes")
    if st.session_state.model is not None:
        status = "Pre-entraine" if st.session_state.model_loaded else "Entraine"
        st.sidebar.metric("Modele", "XGBoost", status)
        if st.session_state.metrics:
            rec = st.session_state.metrics.get("recall", 0)
            st.sidebar.metric("Recall", f"{rec:.1%}" if rec else "N/A")
    else:
        st.sidebar.warning("Aucun modele charge")
        if not st.session_state.model_loaded:
            st.sidebar.caption("Entrainez via l'onglet Entrainement")


def hero_section():
    st.markdown(
        '<div class="hero-title">FRAUDX</div>'
        '<div class="hero-sub">Systeme Intelligent de Detection de Fraude Bancaire & Mobile Money</div>',
        unsafe_allow_html=True,
    )


def info_card(title, text):
    st.markdown(
        f'<div class="card"><div class="card-title">{title}</div>'
        f'<div class="card-text">{text}</div></div>',
        unsafe_allow_html=True,
    )


def prediction_gauge(proba, threshold, height=300):
    import plotly.graph_objects as go
    pred = "FRAUDE" if proba >= threshold else "NORMALE"
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=proba * 100,
        number={"suffix": "%", "font": {"size": 40, "color": "#e8eaf6"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#ef5350" if pred == "FRAUDE" else "#4caf50"},
            "steps": [
                {"range": [0, 30], "color": "rgba(76,175,80,0.2)"},
                {"range": [30, 55], "color": "rgba(255,193,7,0.2)"},
                {"range": [55, 70], "color": "rgba(239,108,0,0.2)"},
                {"range": [70, 100], "color": "rgba(198,40,40,0.2)"},
            ],
            "threshold": {"line": {"color": "white", "width": 2}, "thickness": 0.75, "value": threshold * 100},
        },
    ))
    fig.update_layout(template="plotly_dark", height=height,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    return pred


def prediction_result(pred, proba, threshold, risk, amt):
    pred_color = "red" if pred == "FRAUDE" else "green"
    st.markdown(
        f"<h2 style='text-align:center;color:{pred_color};background:#111d2e;padding:15px;"
        f"border-radius:8px;border:2px solid {pred_color};text-transform:uppercase'>"
        f"{'🚨 ' if pred == 'FRAUDE' else '✅ '}{pred}</h2>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{proba:.4f}")
    c2.metric("Risque", risk)
    c3.metric("Seuil", f"{threshold:.4f}")
    c4.metric("Montant", f"{amt:,} FCFA")
