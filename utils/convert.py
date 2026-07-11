from sqlmodel import SQLModel
import pandas as pd

def sqlmodel_to_df(data: SQLModel) -> pd.DataFrame:
    """
    Convierte un resultado de SQLModel (v1) en un DataFrame de Pandas.
    Soporta una única instancia (.first()) o una lista de instancias (.all()).
    """
    # Validar si el resultado es nulo o una lista vacía
    if data is None or (isinstance(data, list) and len(data) == 0):
        return pd.DataFrame()

    # Normalizar la entrada: si es un objeto único, lo metemos en una lista
    es_lista = isinstance(data, list)
    lista_instancias = data if es_lista else [data]

    # Obtener el primer elemento para inspeccionar sus columnas de forma segura
    primer_elemento = lista_instancias[0]
    columns_names = list(primer_elemento.__class__.__fields__.keys())

    # Convertir cada objeto de la lista a un diccionario nativo usando .dict()
    datos_filas = [instancia.dict() for instancia in lista_instancias]

    # 5. Retornar el DataFrame finalizado
    return pd.DataFrame(datos_filas, columns=columns_names)

def list_to_df(to_convert, columns_names) -> pd.DataFrame:
    df = pd.DataFrame.from_records(to_convert.all(), columns=columns_names)
    return df