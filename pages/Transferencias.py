# Importamos streamlit y librerías necesarias
import streamlit as st
import datetime
from io import BytesIO
from openpyxl import Workbook

# Importamos los services y script para autenticación
from services.transaction_service import TransactionService
from services.transfer_service import TransferService
from services.date_services import remove_timezone
from services.utils_services import rename_columns_df_transfer_excel
from services.session_service import require_login, get_current_user_id
# Importamos models
from models import Transfer, Transaction
# Importamos conexión
from database.connection import get_session

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
def get_previously_transfer():
    with get_session() as session:
        service = TransferService(session)
        return service.get_previously_transfer()

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

def generate_excel(df):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Reporte"

    # Encabezados
    ws.append(df.columns.tolist())

    # Datos
    for row in df.itertuples(index=False):
        ws.append(row)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output

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
tab_fix_pendings, tab_show_transfer = st.tabs(
	[
		"Por saldar",
		"Saldados"
	]
)

with tab_fix_pendings:
    ####### Inicializamos rango de fechas del mes actual #######
    # Creamos el contenedor para los botones Nuevo, editar y eliminar
    contenedor_botones = st.container()

    # 1: DF, 2: Nombre de columnas, 3: Orden de columnas
    df_shared_transactions, columns_dataframe_config, columns_order = get_shared_transactions()

    if not df_shared_transactions.empty:

        balance_df = get_household_balance()

        with st.container(border=True):
            columns_metric = st.columns(3)

            # Obtenemos quién debe más y cuánto
            metric3_id_to = balance_df.loc[balance_df['debt'].idxmin(), 'user_id']
            metric3_id_from = balance_df.loc[balance_df['debt'].idxmax(), 'user_id']
            metric3_name_to = balance_df.loc[balance_df['debt'].idxmin(), 'username']
            metric3_name_from = balance_df.loc[balance_df['debt'].idxmax(), 'username']
            metric3_diff = abs(balance_df['debt'].iloc[0] - balance_df['debt'].iloc[1])

            for idx, fila in balance_df.iterrows():
                user_name = fila["username"]
                user_ammount = fila["debt"]
                with columns_metric[idx]:
                    st.metric(label=f"Total a devolver por {user_name}:", value=f"S/.{user_ammount}")
            with columns_metric[(2)]:
                st.metric(label=f"Devolver a {metric3_name_to}:", value=f"S/.{metric3_diff}", delta="Saldo a devolver")

        # Creamos el contenedor para los boton Saldar Pendientes
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
        st.write(f"{len(df_shared_transactions)} filas.")

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
with tab_show_transfer:

    # 1: DF, 2: Nombre de columnas, 3: Orden de columnas
    df_show_transfer, columns_df_config_show_transfer, columns_order_show_transfer = get_previously_transfer()
    df_show_transfer = df_show_transfer[columns_order_show_transfer]
    df_transfer_styled = df_show_transfer.style.set_properties(subset=["amount_transfer"],**{"font-weight": "bold"})
    
    # Mostrar el detalle
    if df_show_transfer.empty:
        st.info("No hay información para mostrar")
    else:
        #Se reserva espacio para el botón de descarga en Excel
        col_subtitle, col_download = st.columns([4,1])
        with col_subtitle:
            st.subheader("Historial")
        with col_download:
            btn_dwnl_xls_transfer = st.container()
        st.dataframe(
            df_transfer_styled,
            column_config=columns_df_config_show_transfer,
            use_container_width=True,
            #height = 500
        )
        st.write(f"{len(df_show_transfer)} filas.")
        df_excel = (
            remove_timezone(df_show_transfer)
            .rename(columns=rename_columns_df_transfer_excel())
        )
        excel_file = generate_excel(df_excel)

        with btn_dwnl_xls_transfer:
            st.download_button(
                label=":material/download: Descargar Excel",
                data=excel_file,
                file_name=f"Reporte_Transferencias.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

