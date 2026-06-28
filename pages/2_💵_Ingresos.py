import streamlit as st

st.title("💵 Registro de Ingresos")

descripcion = st.text_input("Descripción")

monto = st.number_input(
    "Monto",
    min_value=0.0,
    step=1000.0
)

if st.button("Guardar ingreso"):
    st.success("Ingreso registrado")