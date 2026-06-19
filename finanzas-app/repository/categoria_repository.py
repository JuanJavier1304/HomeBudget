from database.connection import get_connection
import pandas as pd


class CategoriaRepository:

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name
            FROM categoria
            ORDER BY id
        """)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        columnas_dinamicas = [desc[0] for desc in cursor.description]

        #return result
        return pd.DataFrame(result, columns=columnas_dinamicas)

    @staticmethod
    def insert(name):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO categoria (name)
            VALUES (%s)
            """,
            (name, )
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def update(id, name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE categoria
            SET name = %s
            WHERE id = %s
            """,
            (name, id)
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def delete(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM categoria
            WHERE id = %s
            """,
            (id,)
        )

        conn.commit()

        cursor.close()
        conn.close()