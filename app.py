import streamlit as st
from services.user_service import UserService
from models import User
from database.connection import get_session

st.set_page_config(page_title="Home[Budget]",layout="wide")

def authenticate(obj):
    with get_session() as session:
        service = UserService(session)
        return service.authenticate(obj)

# 1. Inicializar el estado de autenticación si no existe
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. Definir las páginas del sistema
#st.subheader(f"acá va un subtítulo")
page_login = st.Page("app.py", title="Login", icon=":material/login:")
page_transacciones = st.Page("pages/Transacciones.py", title="Transacciones ", icon=":material/payments:")
page_tranferencias = st.Page("pages/Transferencias.py", title="Transferencias ", icon=":material/currency_exchange:")
page_reportes = st.Page("pages/Reportes.py", title="Reportes", icon=":material/analytics:")
page_administracion = st.Page("pages/Administracion.py", title="Administración", icon=":material/settings:")

# 3. Controlar la navegación según el estado de login
if st.session_state.logged_in:
    # Crea títulos de sección automáticos con separadores integrados
    pg = st.navigation({
        "Operaciones": [page_transacciones, page_tranferencias],
        "Analytics": [page_reportes],
        "Administración": [page_administracion]
    }, position="sidebar")

    #pg = st.navigation([page_transacciones, page_tranferencias, page_reportes, page_administracion], position="sidebar")

    # Si está logueado, mostramos el sidebar con sus páginas
    st.sidebar.write(f"### :material/person: Bienvenido **:blue-background[{st.session_state['firstname']}]**")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
        pg = st.navigation([page_login], position="hidden")
else:
    # Si NO está logueado, pasamos una lista vacía para ocultar el sidebar
    pg = st.navigation([page_login], position="hidden")

    # Renderizamos el formulario de login directamente en la página principal
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.title("Home:orange[Budget]")
        with st.form("login_form"):
            st.header("Iniciar Sesión")
            username = st.text_input("Usuario", key="ti_username")
            password = st.text_input("Contraseña", type="password", key="ti_password")
            #btn_ingresar = st.button("Ingresar", key="btn_ingresar", type="primary")
            btn_ingresar = st.form_submit_button("Ingresar",type="primary")

        if btn_ingresar:
            user_to_authenticate = User(username=username, password_hash=password)
            auth_user = authenticate(user_to_authenticate)  # devuelve (id, username, password)
            if auth_user is not None:
                st.session_state.logged_in = True
                st.session_state.user_id = auth_user[0]
                st.session_state.firstname = auth_user[1]
                # st.switch_page("pages/Transacciones.py")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# 4. Ejecutar la página activa (solo si está logueado)
if st.session_state.logged_in:
    pg.run()