"""
ATTENTION : Cette app est OBSOLÈTE.
Utilisez app.py à la place — elle contient tout (dataset, preproc, training, benchmark, prediction).

Lancement correct :
    streamlit run app.py

L'application déployée sur Streamlit Cloud doit pointer vers app.py, PAS app_streamlit.py.
"""
import streamlit as st
st.set_page_config(page_title="FRAUDX — Redirection", page_icon="🛡️")
st.warning("Cette app est obsolète. Remplacez par app.py dans les settings Streamlit Cloud.")
st.info("Lancez : `streamlit run app.py`")
st.stop()
