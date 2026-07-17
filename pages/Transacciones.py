# Importamos streamlit y librerías necesarias
import streamlit as st
import datetime
from decimal import Decimal

# Importamos los services
from services.date_services import get_dates_current_month
from services.catalog_service import CatalogService
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.transaction_participant_service import TransactionParticipantService

# Importamos models
from models import Category, Subcategory, PaymentMethod, TransactionType, TransactionVariability, Transaction, TransactionParticipant, DateInterval
# Importamos conexión
from database.connection import get_session

# Importamos script para autenticación
from services.session_service import require_login, get_current_user_id


# Útiles para el script
require_login() ###### Autenticación ######
USER_ID = get_current_user_id()


# --- CAPA DE SERVICIOS PARA TRANSACCIONES ---

@st.cache_data
def get_transactions_by_date_range(user_id, start_date, end_date):
    with get_session() as session:
        service = TransactionService(session)
        return service.get_by_date_range(user_id, start_date, end_date)

@st.cache_data
def get_transaction_by_id(user_id, transaction_id):
    with get_session() as session:
        service = TransactionService(session)
        return service.get_by_id(user_id, transaction_id)

def insert_or_update_transaction(transaction):
    with get_session() as session:
        service = TransactionService(session)
        return service.update(transaction)

def delete_transaction(transaction_id):
    with get_session() as session:
        service = TransactionService(session)
        return service.delete(Transaction, transaction_id)

def insert_or_update_participant(participant):
    with get_session() as session:
        service = TransactionParticipantService(session)
        return service.updateFromTransaction(participant)

@st.cache_data
def get_all_without_current_user():
    with get_session() as session:
        service = UserService(session)
        return service.get_all_without_current_user(USER_ID)

@st.cache_data
def get_transaction_participants(transaction_id):
    with get_session() as session:
        service = TransactionParticipantService(session)
        return service.get_transaction_participants(USER_ID, transaction_id)

# --- CAPA DE SERVICIOS PARA CATÁLOGOS OPTIMIZADA ---

@st.cache_data
def load_catalog(model_name: str):
    """
    Función única y optimizada con caché para resolver cualquier catálogo.
    Streamlit identificará el caché basado en la cadena 'model_name'.
    """
    # Mapeo de configuración para mantener el dinamismo limpio
    catalog_map = {
        "category": (Category, "cat_repo"),
        "subcategory": (Subcategory, "sub_repo"),
        "payment_method": (PaymentMethod, "pay_repo"),
        "transaction_type": (TransactionType, "type_repo"),
        "transaction_variability": (TransactionVariability, "var_repo"),
        "date_interval": (DateInterval, "dt_interval_repo")
    }

    if model_name not in catalog_map:
        raise ValueError(f"Catálogo {model_name} no configurado.")

    model_class, repo_attr = catalog_map[model_name]

    with get_session() as session:
        catalog_service = CatalogService(session)
        return catalog_service.get_catalog(model_class, repo_attr)


# Obtenemos los catálogos para los selectbox
df_transaction_types = load_catalog("transaction_type")
df_categories = load_catalog("category")
df_subcategories = load_catalog("subcategory")
df_payment_method = load_catalog("payment_method")
df_transaction_variability = load_catalog("transaction_variability")
df_date_interval = load_catalog("date_interval")

#### Pop ups transaccion ########################
@st.dialog("Transacción", width="medium")
def updateTransaction(transaction_id):

    # Inicializamos variables con valores vacíos
    val_date=datetime.date.today()
    val_transaction_type=int(df_transaction_types['id'].iloc[0])
    val_description=None
    val_amount=0.0
    val_category_id=int(df_categories['id'].iloc[0])
    val_subcategory_id=None # Este se configura luego de seleccionar categoría
    val_payment_method_id=int(df_payment_method['id'].iloc[0])
    val_variability=int(df_transaction_variability['id'].iloc[0])
    val_is_shared=False
    val_is_household_expense=False
    val_comment=None
    val_amount_participant = 0.0
    val_participant_id = None

    if transaction_id:
        current_transaction = get_transaction_by_id(USER_ID, transaction_id)[0]

        val_date = current_transaction.transaction_date
        val_transaction_type = current_transaction.transaction_type_id
        val_description = current_transaction.description
        val_amount = Decimal(str(current_transaction.amount))
        val_category_id = current_transaction.category_id
        val_subcategory_id = current_transaction.subcategory_id
        val_payment_method_id = current_transaction.payment_method_id
        val_variability = current_transaction.transaction_variability_id
        val_is_shared = current_transaction.is_shared
        val_is_household_expense = current_transaction.is_household_expense
        val_comment = current_transaction.comment

        _="""
        val_date = current_transaction.iloc[0]["transaction_date"]
        val_transaction_type = current_transaction.iloc[0]["transaction_type_id"]
        val_description = current_transaction.iloc[0]["description"]
        val_amount = float(current_transaction.iloc[0]["amount"])
        val_category_id = current_transaction.iloc[0]["category_id"]
        val_subcategory_id = current_transaction.iloc[0]["subcategory_id"]
        val_payment_method_id = current_transaction.iloc[0]["payment_method_id"]
        val_variability = current_transaction.iloc[0]["transaction_variability_id"]
        val_is_shared = current_transaction.iloc[0]["is_shared"]
        val_is_household_expense = current_transaction.iloc[0]["is_household_expense"]
        val_comment = current_transaction.iloc[0]["comment"]
        """
    else:
        transaction_id = None

    # Creamos 2 columnas para organizar el contenido
    fila_1_col_1, fila_1_col_2 = st.columns(2)

    with fila_1_col_1:
        # Fila 1: Selector de fecha
        input_fecha = st.date_input(
            "Fecha",
            key="input_fecha",
            value=val_date
        )

    with fila_1_col_2:
        # Fila 1: Selector tipo movimiento
        #df_transaction_types = get_transaction_type()
        list_ids_types = df_transaction_types["id"].tolist()
        default_index_types = list_ids_types.index(val_transaction_type)
        input_transaction_type = st.selectbox(
            "Tipo de Transacción",
            options=list_ids_types,
            index=default_index_types,
            placeholder="Selecciona una opción",
            format_func=lambda x: df_transaction_types.loc[
                df_transaction_types["id"] == x, "name"
            ].iloc[0],
        )

    # Fila 2: Input Descripción
    input_description = st.text_input(
        "Descripcion",
        key="input_description",
        value=val_description
    )

    # Fila 3: Input monto
    input_amount = st.number_input(
        "Monto (S/.)",
        min_value=0.0,
        value=float(val_amount),
        format="%.2f",
        key="input_monto"
    )
    st.caption(f"Monto ingresado: S/. {input_amount:.2f}")

    fila_4_col_1, fila_4_col_2 = st.columns(2)

    with fila_4_col_1:
        # Fila 4: Selector categorías
        list_ids_categories = df_categories["id"].tolist()
        default_index_category = list_ids_categories.index(val_category_id)
        input_category_id = st.selectbox(
            "Categoría",
            options=list_ids_categories,
            index=default_index_category,
            placeholder="Selecciona una categoría",
            format_func=lambda x: df_categories.loc[
                df_categories["id"] == x, "name"
            ].iloc[0],
        )
    with (fila_4_col_2):
        # Fila 4: Selector subcategorías (obtenemos las subcategorías de la categoría seleccionada)
        df_subcategories_filtered = None
        list_ids_subcategories = []
        default_index_subcategory = None
        if input_category_id:
            if input_category_id != val_category_id: # Validamos si cambió el selectbox
                val_subcategory_id = None
            df_subcategories_filtered = df_subcategories[df_subcategories["category_id"] == input_category_id]
            if df_subcategories_filtered.empty:
                placeholder_text = "Sin subcategorías disponibles"
            else:
                val_subcategory_id = int(df_subcategories_filtered['id'].iloc[0]) if val_subcategory_id is None else val_subcategory_id
                list_ids_subcategories = df_subcategories_filtered["id"].tolist()
                default_index_subcategory = list_ids_subcategories.index(val_subcategory_id)
                placeholder_text = "Selecciona una subcategoría"
        else:
            placeholder_text = "Selecciona una categoría primero..."

        input_subcategory_id = st.selectbox(
            "Subcategoría",
            options=list_ids_subcategories,
            index=default_index_subcategory,
            placeholder=placeholder_text,
            format_func=lambda x: df_subcategories_filtered.loc[
                df_subcategories_filtered["id"] == x, "name"
            ].iloc[0] if df_subcategories_filtered is not None and not df_subcategories_filtered.empty else str(x),
        )

    fila_5_col_1, fila_5_col_2 = st.columns(2)

    with fila_5_col_1:
        # Fila 5: Selector metodo de pago
        list_ids_payment_methods = df_payment_method["id"].tolist()
        default_index_payment_method = list_ids_payment_methods.index(val_payment_method_id)
        input_payment_method_id = st.selectbox(
            "Método de pago",
            options=list_ids_payment_methods,
            index=default_index_payment_method,
            format_func=lambda x: df_payment_method.loc[
                df_payment_method["id"] == x, "name"
            ].iloc[0],
            key="selecbox_metodo_pago"
        )
    with fila_5_col_2:
        # Fila 5: Selector variabilidad
        list_ids_variability = df_transaction_variability["id"].tolist()
        default_index_variability = list_ids_variability.index(val_variability)
        input_transaction_variability = st.selectbox(
            "Variabilidad",
            options=list_ids_variability,
            index=default_index_variability,
            placeholder="Seleccione variabilidad",
            format_func=lambda x: df_transaction_variability.loc[
                df_transaction_variability["id"] == x, "name"
            ].iloc[0],
        )

    fila_6_col_1, fila_6_col_2 = st.columns(2)
    with fila_6_col_1:
        # Fila 6: Checkbox es gasto compartido
        input_chk_is_shared = st.checkbox(
            label="¿Es gasto compartido?",
            key="chkbx_gasto_compartido",
            value=val_is_shared
        )
    with fila_6_col_2:
        # Fila 6: Checkbox es gasto de hogar
        input_chk_is_household_expense = False
        if input_chk_is_shared:
            input_chk_is_household_expense = st.checkbox(
                label="¿Es gasto del hogar?",
                key="user_subscription",
                value=val_is_household_expense
            )

    fila_7_col_1, fila_7_col_2 = st.columns(2)
    if input_chk_is_household_expense:
        # Obtengo todos los usuarios (por ahora 1)
        df_users = get_all_without_current_user()
        df_participants = get_transaction_participants(transaction_id)
        val_participant_id = int(df_participants.iloc[0]["user_id"]) if not df_participants.empty else val_participant_id
        val_amount_participant = float(df_participants.iloc[0]["assigned_amount"]) if not df_participants.empty else val_amount_participant
        with fila_7_col_1:
            # Fila 7: Participantes (si es gasto de hogar)
            # Selector participante
            list_ids_users = df_users["id"].tolist()
            default_index_participant_id = list_ids_users.index(val_participant_id) if val_participant_id is not None else None
            input_participant_id = st.selectbox(
                "Participante",
                options=list_ids_users,
                index=default_index_participant_id,
                format_func=lambda x: df_users.loc[
                    df_users["id"] == x, "fullname"
                ].iloc[0],
                key="selecbox_participant"
            )

        with fila_7_col_2:
            # Fila 7: Monto del participante
            input_amount_participant = st.number_input(
                "Monto (S/.)",
                min_value=0.0,
                value=val_amount_participant,
                format="%.2f",
                key="input_monto_participant"
            )
            st.caption(f"Monto ingresado: S/. {input_amount_participant:.2f}")
            input_amount_current_user = input_amount - input_amount_participant



    # Fila 8: Input comentario
    input_comment = st.text_area(
        "Comentario",
        key="input_comentario",
        value=val_comment
    )

    # Botón para guardar/actualizar transacción
    save_transaction = st.button(
        label=":material/save: Guardar transacción",
        key="bttn_add_movement",
        width="stretch",
        type="primary",
        use_container_width=True
    )

    # Botón para registrar gasto
    if save_transaction:
        errores = []
        if not input_fecha:
            errores.append("Debe seleccionar una fecha")
        if not input_transaction_type:
            errores.append("Debe seleccionar un tipo de movimiento (gasto/ingreso)")
        if not input_description.strip():
            errores.append("Debe ingresar una descripción")
        if input_amount <= 0:
            errores.append("El monto debe ser mayor a 0")
        if input_category_id is None:
            errores.append("Debe seleccionar una categoría")
        if errores:
            for error in errores:
                st.error(error)
        else:
            transaction_to_insert = Transaction(
                id = transaction_id,
                # user_id=get_current_user_id(),
                user_id=USER_ID, # cambiar por la línea de arriba
                transaction_date=input_fecha,
                transaction_type_id=input_transaction_type,
                description=input_description,
                amount=Decimal(str(input_amount)),
                category_id=input_category_id,
                subcategory_id=input_subcategory_id,
                payment_method_id=input_payment_method_id,
                transaction_variability_id=input_transaction_variability,
                comment=input_comment,
                is_shared=input_chk_is_shared,
                is_household_expense=input_chk_is_household_expense
            )
            try:
                transaction_inserted = insert_or_update_transaction(transaction_to_insert)

                if input_chk_is_household_expense:
                    transaction_participant1 = TransactionParticipant(
                        transaction_id=transaction_inserted.id,
                        user_id=USER_ID,
                        assigned_amount=Decimal(str(input_amount_current_user))
                    )
                    insert_or_update_participant(transaction_participant1)
                    transaction_participant2 = TransactionParticipant(
                        transaction_id=transaction_inserted.id,
                        user_id=input_participant_id,
                        assigned_amount=Decimal(str(input_amount_participant))
                    )
                    insert_or_update_participant(transaction_participant2)
                st.toast("Transacción guardada correctamente.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))

@st.dialog("Transacción")
def deleteTransaction(transaction_id):
    """"
    Dialogo para eliminar una transaccion
    Args:
        transaction_id (int): ID de transaccion
	"""
    st.write(f"¿Estás seguro de que quieres eliminar esta transacción?")

    with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):
        if st.button(":material/delete:", key=f"confirm_delete_transaction", type="primary"):
            success = delete_transaction(transaction_id)

            if success:
                st.toast("Transacción eliminado correctamente")
                st.rerun()
            else:
                st.error("Error al eliminar transacción")

        if st.button("Cancelar"):
            st.rerun()

#################################################

st.set_page_config(page_title="Transacciones")
st.title(":material/payments: Transacciones")

####### Inicializamos rango de fechas del mes actual #######
first_day, last_day = get_dates_current_month()
date_range = st.date_input(
    "Selecciona un rango de fechas",
    value=(first_day, last_day),
    key="date_selector_transactions",
)
############################################################

# Creamos el contenedor para los botones Nuevo, editar y eliminar
contenedor_botones = st.container()

# Muestra los gastos según el rango de fechas
df_transacciones = None
selected = None
columns_dataframe_config = {
    "id": st.column_config.Column("ID", help="Identificador único"),
    "transaction_date": st.column_config.DateColumn("Fecha de Transacción"),
    "transaction_type_name": st.column_config.Column("Tipo Transacción"),
    "description": st.column_config.Column("Descripción"),
    "category_name": st.column_config.Column("Categoría"),
    "subcategory_name": st.column_config.Column("Subcategoría"),
    "amount": st.column_config.NumberColumn("Monto", format="S/%.2f"),  # Formatea como dinero si aplica
    "payment_method_name": st.column_config.Column("Método Pago"),
    "transaction_variability_name": st.column_config.Column("Fijo/Variable"),
    "comment": st.column_config.Column("Comentario"),
    "is_shared": st.column_config.Column("Es compartido"),
    "is_household_expense": st.column_config.Column("Es gasto de hogar"),
}

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    df_transacciones=get_transactions_by_date_range(
        user_id = USER_ID,
        start_date = start_date,
        end_date = end_date
    )
    selected = st.dataframe(
        df_transacciones,
        on_select="rerun",
        selection_mode="single-row",
        use_container_width=True,
        column_config=columns_dataframe_config,
        hide_index=True,
        height = 500
    )

    # Creamos los botones en el contenedor creado previamente
    with contenedor_botones:
        col1, col2, col3, _ = st.columns([1.5, 1.5, 1.5, 5.5])

        with col1:
            st.button(
                label="Agregar",
                icon=":material/add:",
                on_click=updateTransaction,
                args=(None,),
                type="primary",
                use_container_width=True
            )

        if len(selected.selection.rows) > 0:
            index_row = selected.selection.rows[0]
            select_id = int(df_transacciones.iloc[index_row]["id"])
            with col2:
                st.button(
                    label="Editar",
                    icon=":material/edit:",
                    on_click=updateTransaction,
                    args=(select_id,),
                    type="secondary",
                    use_container_width=True
                )
            with col3:
                st.button(
                    label="Eliminar",
                    icon=":material/delete:",
                    on_click=deleteTransaction,
                    args=(select_id,),
                    type="secondary",
                    use_container_width=True
                )

else:
    st.info("Por favor, selecciona la fecha de finalización en el calendario.")