import streamlit as st

st.set_page_config(
    page_title="Finanzas Hogar",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Finanzas Hogar")

st.markdown("""
Bienvenido al sistema de finanzas personales.

Utiliza el menú lateral para navegar entre módulos.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Ingresos", "$0")

with col2:
    st.metric("Gastos", "$0")

with col3:
    st.metric("Balance", "$0")

st.info("Proyecto en construcción 🚀")