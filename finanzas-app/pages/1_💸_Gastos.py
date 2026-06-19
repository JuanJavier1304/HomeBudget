import streamlit as st
from repository.categoria_repository import CategoriaRepository

st.title("💸 Registro de Gastos")

descripcion = st.text_input("Descripción")

monto = st.number_input(
    "Monto",
    min_value=0.0,
    step=1000.0
)

categorias = CategoriaRepository.get_all()

categoria_dict = {
    nombre: id
    for id, nombre in categorias
}

categoria = st.selectbox(
    "Categoría",
    list(categoria_dict.keys())
)

if st.button("Guardar gasto"):
    st.success("Gasto registrado")