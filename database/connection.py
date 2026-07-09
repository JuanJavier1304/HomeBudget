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
    echo=False
)

def get_session():
    return Session(engine)
