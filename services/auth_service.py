import bcrypt
from database.connection import get_connection

def authenticate(username, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, firstname, password_hash
        FROM usuario
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return None

    user_id, firstname, password_hash = user

    if bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    ):
        return user_id, firstname

    return None