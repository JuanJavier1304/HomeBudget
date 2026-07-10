import datetime
import calendar
import pandas as pd

def get_dates_current_month():
    """
    Obtener el primer y último día del mes
    :return:
    """
    today = datetime.date.today()
    first_day = today.replace(day=1)
    _, last_day_of_month = calendar.monthrange(today.year, today.month)
    last_day = today.replace(day=last_day_of_month)

    return first_day, last_day

def get_current_date_YYYYMM():
    hoy = datetime.date.today()
    ano_inicio = 2026

    # Generar lista de años válidos (desde 2026 hasta el año actual)
    anos_disponibles = list(range(ano_inicio, hoy.year + 1))

    # Lista de números de meses (1 al 12)
    numeros_meses = list(range(1, 13))

    # Diccionario de mapeo numérico a texto visual
    mapeo_nombres_meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    # Buscar índices por defecto para la inicialización
    try:
        idx_ano_defecto = anos_disponibles.index(hoy.year)
    except ValueError:
        idx_ano_defecto = 0

    idx_mes_defecto = hoy.month - 1  # El mes actual (ej: 7) corresponde al índice 6

    return {
        "anos": anos_disponibles,
        "meses": numeros_meses,
        "mapeo_meses": mapeo_nombres_meses,
        "idx_ano": idx_ano_defecto,
        "idx_mes": idx_mes_defecto
    }

def remove_timezone(df):
    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    return df


