import streamlit as st

# Importamos streamlit y librerías necesarias
import datetime

# Importamos los services
from services.account_holder_service import AccountHolderService

# Importamos models
from models import AccountHolder
# Importamos conexión
from database.connection import get_session

# Importamos script para autenticación
from services.session_service import require_login, get_current_user_id

# Útiles para el script
require_login() ###### Autenticación ######
USER_ID = get_current_user_id()

st.set_page_config(page_title="Cuentas por cobrar")
st.title(":material/credit_card_clock: Cuentas por cobrar")

def formatear_input(input_name):
	return input_name.strip().title()

def get_account_holders(user_id):
    with get_session() as session:
        service = AccountHolderService(session)
        return service.get_account_holders(user_id)

def get_account_holder_by_id(account_holder_id):
    with get_session() as session:
        service = AccountHolderService(session)
        return service.get_account_holder_by_id(account_holder_id)

def insert_or_update_account_holder(obj):
    with get_session() as session:
        service = AccountHolderService(session)
        return service.update(obj)

@st.dialog("Agregar/Editar Cuenta", width="small")
def account_holder_dialog(account_holder_id):
    if account_holder_id:
        account_holder_init = get_account_holder_by_id(account_holder_id)
        st.write(account_holder_init)
        st.write(account_holder_init.firstname)

    input_firstname = st.text_input(
        "Nombre",
        key="input_firstname",
        #value=val_description
    )
    input_lastname = st.text_input(
        "Apellido",
        key="input_lastname",
        #value=val_description
    )
    input_relationship = st.text_input(
        "Relación (opcional)",
        key="input_relationship",
        placeholder="Ej: Papá, tío, primo, amigo..."
        #value=val_description
    )
    input_opening_balance = st.number_input(
        "Monto Apertura (S/.)",
        min_value=0.0,
        #value=input_opening_balance,
        format="%.2f",
        key="input_opening_balance"
    )
    st.caption(f"Monto ingresado: S/. {input_opening_balance:.2f}")

    input_chk_is_enabled = st.checkbox(
        label="Cuenta activa",
        key="account_enabled",
        #value=val_is_household_expense
    )

    btn_save = st.button(
            label=":material/save: Guardar cuenta",
            key="bttn_add_account_holder",
            width="stretch",
            type="primary",
            use_container_width=True
        )
    
    if btn_save:
        errores = []
        if not input_firstname:
            errores.append("Debe ingresar un nombre")
        if not input_lastname:
            errores.append("Debe ingresar un apellido")
        if errores:
            for error in errores:
                st.error(error)
        else:
            account_holder_to_save = AccountHolder(
                id = account_holder_id,
                user_id = USER_ID,
                firstname = formatear_input(input_firstname),
                lastname = formatear_input(input_lastname),
                relationship = formatear_input(input_relationship),
                is_enabled = input_chk_is_enabled,
                opening_balance = input_opening_balance
            )
            try:
                account_holder_result = insert_or_update_account_holder(account_holder_to_save)
                st.toast("Cuenta guardada correctamente.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
    
@st.dialog("Eliminar Cuenta", width="small")
def deleteAccountHolder(account_holder_id):
    st.info("En construcción :rocket:")

tab_transacciones, tab_administrar = st.tabs(
	[
		"Transacciones",
		"Administrar"
	]
)

with tab_transacciones:
    st.info(":rocket: En construcción")
with tab_administrar:
    st.subheader("Cuentas")

    # 1: DF, 2: Nombre de columnas, 3: Orden de columnas
    df_account_holders, columns_dataframe_config, columns_order = get_account_holders(USER_ID)

    bttns_container = st.container()
    selected_rows = 0
    if not df_account_holders.empty:
        df_account_holders = df_account_holders[columns_order]
        event_account_holders = st.dataframe(
            df_account_holders,
            on_select="rerun",
            selection_mode="single-row",
            use_container_width=True,
            column_config=columns_dataframe_config,
            hide_index=True
        )
        selected_rows = event_account_holders.selection.rows
        st.write(f"{len(df_account_holders)} fila(s).")
    else:
        st.info("No hay cuentas por mostrar")


    with bttns_container:
        col1, col2, col3, _ = st.columns([1, 1, 1, 2])

        with col1:
            st.button(
                label="Agregar cuenta",
                icon=":material/add:",
                on_click=account_holder_dialog,
                args=(None,),
                type="primary",
                use_container_width=True,
                disabled=False if len(selected_rows) <= 0 else True
            )

        if len(selected_rows) > 0:
            index_row = selected_rows[0]
            select_id = int(df_account_holders.iloc[index_row]["id"])
            with col2:
                st.button(
                    label="Editar",
                    icon=":material/edit:",
                    on_click=account_holder_dialog,
                    args=(select_id,),
                    type="secondary",
                    use_container_width=True
                )
            with col3:
                st.button(
                    label="Eliminar",
                    icon=":material/delete:",
                    on_click=deleteAccountHolder,
                    args=(select_id,),
                    type="secondary",
                    use_container_width=True
                )