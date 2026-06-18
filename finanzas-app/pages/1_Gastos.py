import streamlit as st

st.title("💸 Registro de Gastos")

descripcion = st.text_input("Descripción")

monto = st.number_input(
    "Monto",
    min_value=0.0,
    step=1000.0
)

categoria = st.selectbox(
    "Categoría",
    [
        "Comida",
        "Transporte",
        "Hogar",
        "Salud",
        "Entretenimiento"
    ]
)

if st.button("Guardar gasto"):
    st.success("Gasto registrado")