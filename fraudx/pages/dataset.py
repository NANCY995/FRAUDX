import os
import streamlit as st
import pandas as pd
from pathlib import Path
from fraudx.ui import hero_section, info_card


def render():
    hero_section()
    col1, col2, col3 = st.columns(3)
    with col1:
        info_card("Machine Learning", "XGBoost optimise par Optuna avec recall >= 85%")
    with col2:
        info_card("Analyse SHAP", "Interpretabilite des predictions avec explications visuelles")
    with col3:
        info_card("Contexte Togo", "Adapte au Mobile Money (TogoCom, Moov, Flooz)")

    st.markdown("---")
    st.subheader("Chargement du dataset")
    st.caption("Importez vos transactions ou utilisez un dataset de reference")

    col1, col2 = st.columns(2)
    with col1:
        source = st.radio("Source", ["IEEE-CIS Fraud Detection (Kaggle)", "Credit Card Fraud (ULB)", "Upload CSV"], index=0)
    with col2:
        if source == "Upload CSV":
            uploaded = st.file_uploader("Choisir un fichier CSV", type="csv")
        n_rows = st.number_input("Nombre de lignes", 1000, 200000, 50000, step=10000)

    if st.button(" Charger le dataset", use_container_width=True, type="primary"):
        with st.spinner("Chargement en cours..."):
            try:
                if source.startswith("IEEE"):
                    path = Path("data/train_transaction.csv")
                    id_path = Path("data/train_identity.csv")
                    if not path.exists():
                        with st.status("Telechargement depuis Kaggle..."):
                            import kagglehub, shutil
                            kaggle_path = Path(kagglehub.competition_download("ieee-fraud-detection"))
                            os.makedirs("data", exist_ok=True)
                            for f in ["train_transaction.csv", "train_identity.csv"]:
                                src = kaggle_path / f
                                if src.exists():
                                    shutil.copy(src, f"data/{f}")
                            path = Path("data/train_transaction.csv")
                            id_path = Path("data/train_identity.csv")
                    df = pd.read_csv(path, nrows=n_rows)
                    if id_path.exists():
                        identity = pd.read_csv(id_path, nrows=n_rows)
                        df = df.merge(identity, on="TransactionID", how="left")
                    st.session_state.df_name = f"IEEE-CIS ({len(df):,} lignes)"
                elif source.startswith("Credit"):
                    path = Path("data/creditcard.csv")
                    if not path.exists():
                        with st.status("Telechargement depuis Internet..."):
                            import requests
                            url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
                            os.makedirs("data", exist_ok=True)
                            r = requests.get(url, stream=True, timeout=120)
                            with open("data/creditcard.csv", "wb") as f:
                                f.write(r.content)
                            path = Path("data/creditcard.csv")
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
        c3.metric("Taille memoire", f"{df.memory_usage(deep=True).sum()/1024**2:.1f} Mo")
        fraud_rate = df["isFraud"].mean() * 100 if "isFraud" in df.columns else 0
        c4.metric("Taux fraude", f"{fraud_rate:.2f}%" if fraud_rate > 0 else "N/A")
        with st.expander(" Apercu des donnees", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)
        with st.expander(" Statistiques descriptives"):
            st.dataframe(df.describe(), use_container_width=True)
