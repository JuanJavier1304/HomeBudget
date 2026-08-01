# Importamos streamlit y librerías necesarias
import streamlit as st
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from openpyxl import Workbook
# Importamos los services y script para autenticación
from services.transaction_service import TransactionService
from services.transfer_service import TransferService
from services.date_services import remove_timezone, get_today
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
def get_household_balance(df):
    with get_session() as session:
        service = TransactionService(session)
        return service.get_household_balance(df)

def get_transfer_by_id(transfer_id):
    with get_session() as session:
        service = TransferService(session)
        return service.get_transfer_by_id(transfer_id)
    
def insert_or_update_transfer(transfer):
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
def add_transfer_dialog(id_transfer=None, df_transactions=None, id_from=None, name_from=None, id_to=None, name_to=None, diff=None):
    init_date_transfer = get_today()
    init_comment = None
    init_name_from = name_from
    init_name_to = name_to
    init_amount_transfer = Decimal(diff) if diff is not None else None
    init_mensaje = "Se saldará el monto de S/:"
    init_id_from = int(id_from) if id_from is not None else None
    init_id_to = int(id_to) if id_to is not None else None

    st.write(df_transactions)
    if id_transfer:
        #Traigo todos los valores de la transferencia
        transfer_obj = get_transfer_by_id(id_transfer)
        init_date_transfer = transfer_obj.date_transfer
        init_comment = transfer_obj.comment
        init_name_from = transfer_obj.user_name_from
        init_name_to = transfer_obj.user_name_to
        init_amount_transfer = transfer_obj.amount_transfer
        init_id_from = transfer_obj.user_id_from
        init_id_to = transfer_obj.user_id_to
        init_mensaje = "Monto de transferencia S/:"

    st.info(f"## :material/money_bag: {init_mensaje} {init_amount_transfer:.2f}")
    st.write(
        f"### :material/person: De: **{init_name_from}**\n"
        f"### :material/person: Hacia: **{init_name_to}**\n"
        f"")

    input_date = st.date_input(
            "Fecha de transferencia",
            key="input_date_transfer",
            value=init_date_transfer
        )
    input_comment = st.text_area(
        "Comentario",
        key="input_comentario",
        value=init_comment,
        max_chars=150
    )

    save_transfer = st.button(
        label=":material/save: Guardar transferencia",
        key="bttn_add_transfer",
        width="stretch",
        type="primary"
    )

    if save_transfer:
        transfer_to_insert = Transfer(
            id=int(id_transfer) if id_transfer is not None else None,
            id_user_from=init_id_from,
            id_user_to=init_id_to,
            amount_transfer=init_amount_transfer,
            date_transfer=input_date,
            comment=input_comment
        )

        try:
            transfer_inserted = insert_or_update_transfer(transfer_to_insert)
            if id_transfer is None:
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
    # 1: DF, 2: Nombre de columnas, 3: Orden de columnas
    df_shared_transactions, columns_dataframe_config, columns_order = get_shared_transactions()

    if not df_shared_transactions.empty:
        # Dataframe gastos compartidos
        df_shared_transactions = df_shared_transactions[columns_order]
        df_style = df_shared_transactions.style.apply(highlight_columns, axis=0)

        container_metricas = st.container(border=True)
        # Creamos el contenedor para los boton Saldar Pendientes
        contenedor_botones = st.container()

        event = st.dataframe(
                df_style,
                on_select="rerun",
                #on_select="ignore",
                #selection_mode="single-row",
                selection_mode="multi-row",
                use_container_width=True,
                column_config=columns_dataframe_config,
                hide_index=True
        )
        st.write(f"{len(df_shared_transactions)} filas.")

        with container_metricas:
            selected_rows = event.selection.rows
            if selected_rows:
                # Hacemos el balance inicial
                df_filtrado = df_shared_transactions.iloc[selected_rows]
            else:
                df_filtrado = df_shared_transactions
            
            balance_df = get_household_balance(df_filtrado)
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

        # Creamos los botones en el contenedor creado anteriormente
        with contenedor_botones:
            col1, col2, _ = st.columns([3, 3, 5.5])

            with col1:
                #disabled_check = len(event.selection.rows) == 0
                st.button(
                    label="Saldar pendientes",
                    icon=":material/check_circle:",
                    on_click=add_transfer_dialog,
                    #args=(
                    #    df_transactions=df_filtrado,
                    #    id_from=metric3_id_from,
                    #    name_from=metric3_name_from,
                    #    id_to=metric3_id_to,
                    #    name_to=metric3_name_to,
                    #    diff=metric3_diff
                    #)
                    kwargs={
                        "df_transactions": df_filtrado,
                        "id_from": metric3_id_from,
                        "name_from": metric3_name_from,
                        "id_to": metric3_id_to,
                        "name_to": metric3_name_to,
                        "diff": metric3_diff
                    },
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
        st.subheader("Historial")
        col_edit, col_download = st.columns([4,1])
        with col_edit:
            edit_container = st.container()
        with col_download:
            #Se reserva espacio para el botón de descarga en Excel
            btn_dwnl_xls_transfer = st.container()

        event_show_transfers = st.dataframe(
            df_transfer_styled,
            column_config=columns_df_config_show_transfer,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True
            #height = 500
        )
        st.write(f"{len(df_show_transfer)} filas.")

        with edit_container:
            selected_rows_show_transfer = event_show_transfers.selection.rows
            
            id_transfer=None
            status_btn_edit = True
            if selected_rows_show_transfer:
                # Hacemos el balance inicial
                id_transfer = df_show_transfer.iloc[selected_rows_show_transfer]['id'].iloc[0]
                status_btn_edit = False
            else:
                status_btn_edit = True
            
            btn_edit = st.button(
                ":material/edit: Editar transferencia",
                type="primary",
                disabled=status_btn_edit,
                on_click=add_transfer_dialog,
                # args=(id_transfer=id_transfer)
                kwargs={
                    "id_transfer": id_transfer
                }
            )
            
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
        

