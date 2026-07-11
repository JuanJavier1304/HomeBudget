# Importamos streamlit y librerías necesarias
import streamlit as st
import datetime

# Importamos los services
from services.transaction_service import TransactionService
from services.transfer_service import TransferService
# Importamos models
from models import Transfer, Transaction
# Importamos conexión
from database.connection import get_session

# Importamos script para autenticación
from services.session_service import require_login, get_current_user_id


# Útiles para el script
require_login() ###### Autenticación (si no estás en sesión, no muestra página) ######
USER_ID = get_current_user_id() ###### Obtener el usuario en sesión


# --- CAPA DE SERVICIOS PARA TRANSFERENCIAS ---

@st.cache_data
def get_shared_transactions():
    with get_session() as session:
        service = TransactionService(session)
        return service.get_shared_transactions()

@st.cache_data
def get_household_balance():
    with get_session() as session:
        service = TransactionService(session)
        return service.get_household_balance()

def insert_transfer(transfer):
    with get_session() as session:
        service = TransferService(session)
        return service.update(transfer)

def update_transaction(transaction):
    with get_session() as session:
        service = TransactionService(session)
        return service.update_transaction_by_transfer(transaction)

def highlight_columns(col):
    # Si es la columna objetivo, aplica color; si no, déjala vacía
    if col.name in ("fullname_sec", "assigned_amount"):
        return ['background-color: #fff3cd; color: #856404; font-weight: bold'] * len(col)
    return [''] * len(col)

@st.dialog("Transferencia", width="medium")
def add_transfer_dialog(df_transactions, id_from, name_from, id_to, name_to, diff):
    today = datetime.date.today()
    st.write()
    st.info(f"## :material/money_bag: Se saldará el monto de S/: `{diff:.2f}`\n"
        f"### :material/person: De: **{name_from}**\n"
        f"### :material/person: Hacia: **{name_to}**\n"
        f"### :material/today: Fecha de hoy: **{today}**"
        f"")

    input_comment = st.text_area(
        "Comentario",
        key="input_comentario"
    )

    save_transfer = st.button(
        label=":material/save: Guardar transferencia",
        key="bttn_add_transfer",
        width="stretch",
        type="primary"
    )
    if save_transfer:
        today = datetime.date.today()
        transfer_to_insert = Transfer(
            id_user_from=id_from,
            id_user_to=id_to,
            amount_transfer=diff,
            date_transfer=today,
            comment=input_comment
        )

        try:
            transfer_inserted = insert_transfer(transfer_to_insert)
            for index, row in df_transactions.iterrows():
                transaction_to_update = Transaction(
                    id=row['id'],
                    transfer_id=transfer_inserted.id,
                    real_amount=(row['amount']-row['assigned_amount'])
                )
                transaction_updated = update_transaction(transaction_to_update)
            st.toast("Transacción guardada correctamente.")
            st.rerun()
        except ValueError as e:
            st.error(str(e))


st.set_page_config(page_title="Transferencias")
st.title(":material/currency_exchange: Transferencias")

####### Inicializamos rango de fechas del mes actual #######
# Creamos el contenedor para los botones Nuevo, editar y eliminar
contenedor_botones = st.container()

# Muestra los gastos compartidos
columns_dataframe_config = {
    "id": None,
    "transaction_date": st.column_config.DateColumn("Fecha de Transacción", format="YYYY-MM-DD"),
    "fullname_princ": st.column_config.Column("¿Quién pagó?"),
    "description": st.column_config.Column("Descripción"),
    "category_name": st.column_config.Column("Categoría"),
    "subcategory_name": st.column_config.Column("Subcategoría"),
    "amount": st.column_config.NumberColumn("Monto", format="S/%.2f"),
    "fullname_sec": st.column_config.Column("Devuelve"),
    "assigned_amount": st.column_config.NumberColumn("Monto a devolver", format="S/%.2f"),
    "comment": st.column_config.Column("Comentario"),
    "is_household_expense": None,
    "id_user_princ": None,
    "id_user_sec": None
}
columns_order = [
    "id",
    "transaction_date",
    "description",
    "category_name",
    "subcategory_name",
    "amount",
    "fullname_princ",
    "fullname_sec",
    "assigned_amount",
    "comment"
]

df_shared_transactions = get_shared_transactions()

if not df_shared_transactions.empty:

    balance_df = get_household_balance()
    _="""
    st.write(balance_df)
    receiver = balance_df.loc[
        balance_df["balance"].idxmax()
    ]
    st.write(receiver)

    payer = balance_df.loc[
        balance_df["balance"].idxmin()
    ]
    st.write(payer)
    """

    columns_metric = st.columns(3)


    for idx, fila in balance_df.iterrows():
        user_name = fila["username"]
        user_ammount = fila["debt"]
        with columns_metric[idx]:
            st.metric(label=f"Total a devolver por {user_name}:", value=f"S/.{user_ammount}")

    # Obtenemos quién debe más y cuánto
    metric3_id_to = balance_df.loc[balance_df['debt'].idxmin(), 'user_id']
    metric3_id_from = balance_df.loc[balance_df['debt'].idxmax(), 'user_id']
    metric3_name_to = balance_df.loc[balance_df['debt'].idxmin(), 'username']
    metric3_name_from = balance_df.loc[balance_df['debt'].idxmax(), 'username']
    metric3_diff = abs(balance_df['debt'].iloc[0] - balance_df['debt'].iloc[1])
    with columns_metric[(2)]:
        st.metric(label=f"Devolver a {metric3_name_to}:", value=f"S/.{metric3_diff}", delta="Saldo a devolver")

    # Creamos el contenedor para los botones Nuevo, editar y eliminar
    contenedor_botones = st.container()

    # Dataframe gastos compartidos
    df_shared_transactions = df_shared_transactions[columns_order]
    df_style = df_shared_transactions.style.apply(highlight_columns, axis=0)

    event = st.dataframe(
            df_style,
            #on_select="rerun",
            on_select="ignore",
            #selection_mode="single-row",
            #selection_mode="multi-row",
            use_container_width=True,
            column_config=columns_dataframe_config,
            hide_index=True
    )

    # Creamos los botones en el contenedor creado anteriormente
    with contenedor_botones:
        col1, col2, _ = st.columns([3, 3, 5.5])

        with col1:
            #disabled_check = len(event.selection.rows) == 0
            st.button(
                label="Saldar pendientes",
                icon=":material/check_circle:",
                on_click=add_transfer_dialog,
                args=(df_shared_transactions,metric3_id_from,metric3_name_from,metric3_id_to,metric3_name_to,metric3_diff),
                type="primary",
                use_container_width=True,
                #disabled=disabled_check
            )
else:
    st.info("No hay gastos compartidos por saldar")
