import streamlit as st
from services.auth_service import authenticate

st.title("HomeBudget")

username = st.text_input("Usuario", key="ti_username")
password = st.text_input(
    "Contraseña",
    type="password",
    key = "ti_password"
)

if st.button("Ingresar", key="btn_login"):
    user_id, firstname = authenticate(username,password)

    if user_id:
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        st.session_state.firstname = firstname
        st.session_state.username = username
        st.rerun()
    else:
        st.error("Usuario o contraseña incorrectos")