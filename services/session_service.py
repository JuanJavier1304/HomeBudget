import streamlit as st

def require_login():
    if not st.session_state.get("logged_in", False):
        st.warning("Debes iniciar sesión.")
        st.switch_page("app.py")
        st.stop()

def get_current_user_id():
    return st.session_state.get("user_id")

def get_current_user_firstname():
    return st.session_state.get("firstname")