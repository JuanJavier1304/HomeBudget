# database/connection.py
import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv(override=True)

HOST = os.getenv('PGHOST')
USER = os.getenv('PGUSER')
PASSWORD = os.getenv('PGPASSWORD')
DATABASE = os.getenv('PGDATABASE')

DATABASE_URL = (
    f"postgresql://{USER}:"
    f"{PASSWORD}@"
    f"{HOST}/"
    f"{DATABASE}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,    # Prueba la conexión antes de usarla; si Neon dormía, la reconecta automáticamente
    pool_recycle=60,       # Recicla las conexiones cada 60 segundos para evitar que queden obsoletas
    pool_size=5,           # Mantiene un grupo pequeño y eficiente de conexiones para Streamlit
    max_overflow=10        # Permite conexiones extra temporales si hay picos de tráfico
)

def get_session():
    return Session(engine)
