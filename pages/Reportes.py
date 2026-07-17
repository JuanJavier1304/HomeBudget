import streamlit as st
from io import BytesIO
from openpyxl import Workbook

# Importamos conexión
from database.connection import get_session
# Importamos script para autenticación
from services.session_service import require_login, get_current_user_id
from services.transaction_service import TransactionService
from services.date_services import get_current_date_YYYYMM, remove_timezone
from services.utils_services import rename_columns_df_excel


# Útiles para el script
st.set_page_config(page_title="Reporte Mensual", layout="wide")
require_login() ###### Autenticación (si no estás en sesión, no muestra página) ######
USER_ID = get_current_user_id() ###### Obtener el usuario en sesión

@st.cache_data
def get_transactions_by_month(user_id, year, month):
    with get_session() as session:
        service = TransactionService(session)
        return service.get_transactions_by_month(user_id, year, month)

def calculare_balance(df):
    with get_session() as session:
        service = TransactionService(session)
        return service.calculare_balance(df)

def household_expense_style(row):
    if row['is_household_expense']:
        return ['background-color: #E6F2FF'] * len(row)
    else:
        return [''] * len(row)

def color_transaction_type(value):
    if value == "Gasto":
        return "color: #C62828"
    elif value == "Ingreso":
        return "color: #2E7D32;"
    return ""

def color_amount(row):
    if row["final_amount"] == "Ingreso":
        return "color: #2E7D32;"
    else:
        return "color: #C62828;"

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

st.title(":material/bar_chart: Reporte mensual")
#st.header(":bar_chart: Control de Gastos e Ingresos", divider="blue")

with st.container(border=True):
    init_dates = get_current_date_YYYYMM()
    col_year, col_month, col_spaces = st.columns([1,1,2])
    with col_year:
        # Selector de Año: Se posiciona automáticamente en el año actual
        selected_year = st.selectbox(
            "Año",
            options=init_dates["anos"],
            index=init_dates["idx_ano"]
        )
    with col_month:
        # Selector de Mes: Se posiciona automáticamente en el mes actual
        selected_month = st.selectbox(
            "Mes",
            options=init_dates["meses"],
            index=init_dates["idx_mes"],
            format_func=lambda x: init_dates["mapeo_meses"][x]
        )

    # 1: DF, 2: Nombre de columnas, 3: Orden de columnas
    df_transactions, columns_dataframe_config, columns_order = get_transactions_by_month(USER_ID, selected_year, selected_month)
    df_show = df_transactions[columns_order]

    total_income, total_expense, balance = calculare_balance(df_transactions)
    colsumm1, colsumm2, colsumm3 = st.columns(3)
    with colsumm1:
        st.metric(
            label="🟢 Total Ingresos",
            value=f"S/{total_income:,.2f}",
            delta=total_income if total_income > 0 else None
        )
    with colsumm2:
        st.metric(
            label="🔴 Total Gastos",
            value=f"S/{total_expense:,.2f}",
            delta=-total_expense if total_expense > 0 else None
        )
    with colsumm3:
        st.metric(
            label="⚖️ Balance Neto",
            value=f"S/{balance:,.2f}",
            delta=f"S/{balance:,.2f}",
            delta_color="off"
        )

col_link_transactions, col_download = st.columns([4,1])
with col_link_transactions:
    st.page_link("pages/Transacciones.py", label="Agregar/Editar transacciones") 
with col_download:
    dwnlbtn = st.container()

df_styled = (
    df_show.style
    .apply(household_expense_style, axis=1)
    .apply(lambda row: [color_amount(row)] if row.name >= 0 else [""],
        subset=["final_amount"],
        axis=1)
    .map(color_transaction_type, subset=["transaction_type_name"])
    .set_properties(subset=["final_amount"],**{"font-weight": "bold"})
)
# Mostrar el detalle
if df_show.empty:
    st.info("No hay información para mostrar, seleccione otro año/mes")
else:
    st.dataframe(
        df_styled,
        column_config=columns_dataframe_config,
        hide_index=True,
        use_container_width=True,
        height = 500
    )
    st.write(f"{len(df_show)} filas.")
    st.write(":blue-background[Nota: En celeste los gastos compartidos.]")
    df_excel = (
        remove_timezone(df_show)
        .rename(columns=rename_columns_df_excel())
    )
    excel_file = generate_excel(df_excel)

    with dwnlbtn:
        st.download_button(
            label=":material/download: Descargar Excel",
            data=excel_file,
            file_name=f"Reporte_{selected_year}{selected_month:02d}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
