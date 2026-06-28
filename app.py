import streamlit as st
from services.auth_service import authenticate
from services.session_service import get_current_user_firstname
st.title("HomeBudget")

######### Autenticación del usuario #########
if st.session_state.get("logged_in", False):
    #st.success(f"Bienvenido {st.session_state['username']}")
    st.success(f"Bienvenido {get_current_user_firstname()}")
    st.stop()

username = st.text_input("Usuario", key="ti_username")
password = st.text_input("Contraseña", type="password", key="ti_password")

if st.button("Ingresar", key="btn_ingresar", type="primary"):
    user_id, firstname = authenticate(username, password)
    if user_id:
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        st.session_state.firstname = firstname
        st.session_state.username = username
        st.switch_page("pages/1_💸_Gastos.py")
    else:
        st.error("Usuario o contraseña incorrectos")

######### Fin de Autenticación del usuario #########