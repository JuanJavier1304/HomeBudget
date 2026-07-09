import streamlit as st
from services.session_service import get_current_user_firstname
from services.user_service import UserService
from models import User
from database.connection import get_session

def authenticate_user(user):
    with get_session() as session:
        service = UserService(session)
        return service.authenticate(user)

def get_login():
    if 'user_id' in st.session_state:
        #generate_menu(st.session_state['user_id'])
        generate_menu(st.session_state['firstname'])
    else:
        username = st.text_input("Usuario", key="ti_username")
        password = st.text_input("Contraseña", type="password", key="ti_password")
        if st.button("Ingresar", key="btn_ingresar", type="primary"):
            user_to_authenticate = User(username=username, password_hash=password)
            auth_user = authenticate_user(user_to_authenticate)  # devuelve (id, username, password)
            if auth_user is not None:
                st.session_state.logged_in = True
                st.session_state.user_id = auth_user[0]
                st.session_state.firstname = auth_user[1]
                #st.switch_page("pages/Transacciones.py")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
