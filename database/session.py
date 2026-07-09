# database/session.py
from sqlmodel import Session
from database.engine import engine

def get_session():
    return Session(engine)