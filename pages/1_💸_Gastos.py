import streamlit as st
from repository.categoria_repository import CategoriaRepository
from repository.subcategoria_repository import SubcategoriaRepository
from repository.metodo_pago_repository import MetodoPagoRepository
from repository.movement_repository import MovimientoRepository
from services.session_service import require_login, get_current_user_id

###### Autenticación ######
_="""require_login()
with st.sidebar:
    st.write(f"👤 {st.session_state['username']}")
    if st.button("Cerrar sesión"):
        st.session_state.clear()
        st.switch_page("app.py")"""
###### Fin Autenticación ######


st.title("💸 Movimientos")

# Creamos 3 columnas para organizar el contenido
fila_1_col_1, fila_1_col_2 = st.columns(2)

with fila_1_col_1:
    # Fila 1: Selector de fecha
    input_fecha = st.date_input("Fecha", key="input_fecha")
with fila_1_col_2:
    # Fila 1: Selector tipo movimiento
    tipos_list = ["Gasto", "Ingreso"]
    input_tipo_movimiento = st.selectbox("Tipo", tipos_list, key="selecbox_tipo_movimiento")

# Fila 2: Input Descripción
input_descripcion = st.text_input("Descripcion", key="input_descripcion")
#if not input_descripcion:
#    st.error("Ingrese una descripción")

# Fila 3: Input monto
input_monto = st.number_input("Monto (S/.)", min_value=0.0, value = 0.0, format="%.2f", key="input_monto")
st.caption(f"Monto ingresado: S/. {input_monto:.2f}")
#if input_monto <= 0:
#    st.error("El monto debe ser mayor a 0")

fila_4_col_1, fila_4_col_2 = st.columns(2)

with fila_4_col_1:
    # Fila 4: Selector categorías
    df_list_categorias = CategoriaRepository.get_all()
    if df_list_categorias:
        categorias_ids = list(df_list_categorias.keys())
        input_categoria_id = st.selectbox(
            "Categoría",
            options=categorias_ids,
            format_func=lambda x: df_list_categorias[x],
            key="selecbox_categoria"
        )

with fila_4_col_2:
    # Fila 4: Selector subcategorías (obtenemos las subcategorías de la categoría seleccionada)
    df_list_subcategorias = SubcategoriaRepository.list_by_category(input_categoria_id)
    input_subcategoria_id = None
    if df_list_subcategorias:
        subcategorias_ids = list(df_list_subcategorias.keys())
        input_subcategoria_id = st.selectbox(
            "SubCategoría",
            options=subcategorias_ids,
            format_func=lambda x: df_list_subcategorias[x],
            key="selecbox_subcategoria"
        )
    else:
        st.warning("No hay subcategorias para la categoría seleccionada")

fila_5_col_1, fila_5_col_2 = st.columns(2)

with fila_5_col_1:
    # Fila 5: Selector metodo de pago
    df_list_metodo_pago = MetodoPagoRepository.get_all()
    metodo_pago_ids = list(df_list_metodo_pago.keys())
    input_metodo_pago_id = st.selectbox(
        "Método de pago",
        options=metodo_pago_ids,
        format_func=lambda x: df_list_metodo_pago[x],
        key="selecbox_metodo_pago"
    )

with fila_5_col_2:
    # Fila 5: Selector tipo
    tipo_variable_list = ["Variable", "Fijo"]
    input_tipo_variable = st.selectbox("Tipo", tipo_variable_list, key="selecbox_tipo_variable_list")

fila_6_col_1, fila_6_col_2 = st.columns(2)
with fila_6_col_1:
    # Fila 6: Checkbox es gasto compartido
    chk_es_gasto_compartido = int(st.checkbox(label="¿Es gasto compartido?", key="chkbx_gasto_compartido"))
with fila_6_col_2:
    # Fila 6: Checkbox es gasto de hogar
    chk_es_gasto_hogar = 0
    if chk_es_gasto_compartido == 1:
        chk_es_gasto_hogar = int(st.checkbox(label="¿Es gasto del hogar?",key="user_subscription"))

# Fila 7: Input comentario
input_comentario = st.text_area("Comentario", key="input_comentario")

registrar_movimiento = st.button(
    label = "💾 Guardar movimiento",
    key="bttn_add_movement",
    width="stretch",
    type="primary",
    use_container_width=True
)

# Botón para registrar gasto
if registrar_movimiento:
    errores = []
    if not input_fecha:
        errores.append("Debe seleccionar una fecha")
    if not input_tipo_movimiento:
        errores.append("Debe seleccionar un tipo de movimiento (gasto/ingreso)")
    if not input_descripcion.strip():
        errores.append("Debe ingresar una descripción")
    if input_monto <= 0:
        errores.append("El monto debe ser mayor a 0")
    if input_categoria_id is None:
        errores.append("Debe seleccionar una categoría")
    if input_subcategoria_id is None:
        errores.append("Debe seleccionar una subcategoría")
    if input_metodo_pago_id is None:
        errores.append("Debe seleccionar un método de pago")
    if input_tipo_variable is None:
        errores.append("Debe seleccionar un tipo de gasto (variable/fijo)")
    if errores:
        for error in errores:
            st.error(error)
    else:
        MovimientoRepository.insert(
            #user_id=get_current_user_id(),
            user_id = 1,
            fecha=input_fecha,
            tipo_movimiento = input_tipo_movimiento,
            descripcion = input_descripcion,
            monto = input_monto,
            categoria_id = input_categoria_id,
            subcategoria_id = input_subcategoria_id,
            metodo_pago_id = input_metodo_pago_id,
            tipo_variable = input_tipo_variable,
            comentario = input_comentario,
            es_gasto_compartido = chk_es_gasto_compartido,
            es_gasto_hogar = chk_es_gasto_hogar
        )
        st.success("Movimiento guardado correctamente")



