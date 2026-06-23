import streamlit as st
from repository.categoria_repository import CategoriaRepository
from repository.subcategoria_repository import SubcategoriaRepository
from repository.metodo_pago_repository import MetodoPagoRepository

st.title("💸 Registro de Gastos")

tab1, tab2, tab3 = st.tabs([
    "Registrar",
    "Consultar",
    "Editar / Eliminar"
])

df_list_categorias = CategoriaRepository.get_all()
df_list_metodo_pago = MetodoPagoRepository.get_all()

with st.form("form_movimiento"):

    fecha = st.date_input("Fecha")

    tipo = st.selectbox("Tipo",["Ingreso", "Gasto"])

    descripcion = st.text_input("Descripción")

    categoria = st.selectbox("Categoría",df_list_categorias["name"])

    categoria_id = df_list_categorias.loc[
        df_list_categorias["name"] == categoria,
        "id"
    ].iloc[0]

    
    df_list_subcategorias = SubcategoriaRepository.list_by_category(int(categoria_id))

    subcategoria = st.selectbox(
        "Subcategoría",
        df_list_subcategorias["name"]
    )

    monto = st.number_input(
        "Monto",
        min_value=0.0,
        step=0.01
    )

    metodo_pago = st.selectbox(
        "Método de pago",
        df_list_metodo_pago["name"]
    )

    tipo_gasto = None

    if tipo == "Gasto":
        tipo_gasto = st.radio(
            "Tipo de gasto",
            ["Fijo", "Variable"]
        )

    comentario = st.text_area("Comentario")

    errores = []

    if monto <= 0:
        errores.append(
            "El monto debe ser mayor a 0"
        )

    if not descripcion:
        errores.append(
            "Ingrese una descripción"
        )

    if errores:
        for e in errores:
            st.error(e)
    else:
        st.write("BIEN!")