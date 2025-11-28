import streamlit as st

def auth_gate():
    """
    Lightweight auth UI for Streamlit.
    If you want real auth later, swap this out for OAuth or API-key validation.
    """
    st.sidebar.title("🔐 DevRAG Authentication")
    st.sidebar.info("Local LLaMA3 running — no external API key required.")
    # keep an input for future expansion (optional)
    _ = st.sidebar.text_input("Optional API Key (unused)", type="password")
    return True
