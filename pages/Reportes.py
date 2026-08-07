import pandas as pd

import streamlit as st
from io import BytesIO
from openpyxl import Workbook

# Importamos conexión
from database.connection import get_session
# Importamos script para autenticación
from services.session_service import require_login, get_current_user_id
from services.transaction_service import TransactionService
from services.catalog_service import CatalogService
from services.date_services import remove_timezone, get_dates_current_month, get_today
from services.utils_services import rename_columns_df_excel


# Útiles para el script
st.set_page_config(page_title="Reportes", layout="wide")
require_login() ###### Autenticación (si no estás en sesión, no muestra página) ######
USER_ID = get_current_user_id() ###### Obtener el usuario en sesión

# --- CAPA DE SERVICIOS PARA TRANSACCIONES ---
@st.cache_data
def get_transactions_by_date_range(user_id, start_date, end_date):
    with get_session() as session:
        service = TransactionService(session)
        return service.get_by_date_range(user_id, start_date, end_date)

@st.cache_data
def load_catalog(model_name: str):
    with get_session() as session:
        catalog_service = CatalogService(session)
        return catalog_service.get_catalog(model_name)


st.title(":material/assignment: Reportes")


with st.container(border=True):
    col_intervals, col_date_range = st.columns(2)
    with col_intervals:
        ####### Inicializamos rango de fechas del mes actual #######
        df_date_interval = load_catalog("date_interval")
        interval_options = {
            row["name"]: {
                "inicio": row["start_date"],
                "fin": row["end_date"],
            }
            for _, row in df_date_interval.iterrows()
        }

        selected_date_interval = st.selectbox(
            "Selecciona un intervalo:",
            options=list(interval_options.keys()),
            index=None
        )
        fecha_inicio=None
        fecha_fin=None
        if selected_date_interval is not None:
            fecha_inicio = interval_options[selected_date_interval]["inicio"]
            fecha_fin = interval_options[selected_date_interval]["fin"]

    with col_date_range:
        ####### Inicializamos rango de fechas del mes actual #######
        if fecha_inicio is None or fecha_fin is None:
            first_day, last_day = get_dates_current_month()
        else:
            first_day = fecha_inicio
            last_day = fecha_fin

        # Generamos un key dinámico basado en el intervalo seleccionado
        # Si cambia el intervalo, cambia el key, forzando la actualización visual
        input_key = f"date_selector_{selected_date_interval}"

        date_range = st.date_input(
            "Selecciona un rango de fechas",
            value=(first_day, last_day),
            key=input_key
        )

with st.container(border=True):
    col_cat, col_subcat, col_tx_type = st.columns(3)
    with col_cat:
        ## FILTRO MÚLTIPLE DE CATEGORÍAS
        df_categories = load_catalog("category")
        list_categories = df_categories.name.tolist()
        selected_categories = st.multiselect(
            label="Filtra por categorías:",
            options=list_categories,
            default=list_categories
        )
    with col_subcat:
        ## FILTRO MÚLTIPLE DE SUBCATEGORÍAS
        df_subcategories = load_catalog("subcategory") # Traemos todas las subcategorías
        df_subcat_merge = pd.merge(
            df_categories, 
            df_subcategories, 
            left_on='id', 
            right_on='category_id',
            suffixes=('_category', '_subcategory')
        ) # Join con categories
        df_subcategories = df_subcat_merge[df_subcat_merge["name_category"].isin(selected_categories)]  # Filtramos subcategorías según las categorías seleccionadas
        list_subcategories = df_subcategories.name_subcategory.tolist()
        selected_subcategories = st.multiselect(
            label="Filtra por subcategorías:",
            options=list_subcategories,
            default=list_subcategories
        )
    with col_tx_type:
        ## FILTRO MÚLTIPLE DE GASTOS O INGRESO
        df_transaction_types = load_catalog("transaction_type")
        list_transaction_types = df_transaction_types.name.tolist()
        selected_transaction_types = st.multiselect(
            label="Filtra por tipo de transacción:",
            options=list_transaction_types,
            default=list_transaction_types
        )


if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    df_transacciones, columns_dataframe_config = get_transactions_by_date_range(
            user_id = USER_ID,
            start_date = start_date,
            end_date = end_date
        )
    st.page_link("pages/Transacciones.py", label="Agregar/Editar transacciones") 

    df_transacciones["amount"] = df_transacciones["real_amount"].combine_first(df_transacciones["amount"]) # Reemplaza amount con real_amount, a menos que real_amount sea nulo
    columns_dataframe_config["id"] = None # No necesitamos el ID en el DataFrame mostrado
    columns_dataframe_config["real_amount"] = None # Borramos el campo de monto real del DataFrame mostrado


    df_show = df_transacciones[df_transacciones['category_name'].isin(selected_categories)]
    df_filtrado = df_transacciones[
        (df_transacciones['category_name'].isin(selected_categories)) &
        (df_transacciones['subcategory_name'].isin(selected_subcategories)) &
        (df_transacciones['transaction_type_name'].isin(selected_transaction_types))
    ]
    selected = st.dataframe(
        df_filtrado,
        #on_select="rerun",
        #selection_mode="single-row",
        use_container_width=True,
        column_config=columns_dataframe_config,
        hide_index=True
    )
    st.write(f"{len(df_transacciones)} filas.")

else:
    st.info("Por favor, selecciona la fecha de finalización en el calendario.")
