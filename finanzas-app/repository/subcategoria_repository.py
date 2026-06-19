from database.connection import get_connection
import pandas as pd

class SubcategoriaRepository:

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.id,
                c.name,
                s.name
            FROM subcategoria s
                INNER JOIN categoria c ON c.id = s.category_id
            ORDER BY c.name, s.name
        """)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        columnas_dinamicas = [desc[0] for desc in cursor.description]

        #return result
        return pd.DataFrame(result, columns=columnas_dinamicas)

    @staticmethod
    def list_by_category(category_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.id,
                c.name as category_name,
                s.name
            FROM subcategoria s
                INNER JOIN categoria c ON c.id = s.category_id
            WHERE c.id = %s
            ORDER BY s.id, s.name
        """,
            (category_id,)
        )

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        columnas_dinamicas = [desc[0] for desc in cursor.description]

        #return result
        return pd.DataFrame(result, columns=columnas_dinamicas)

    @staticmethod
    def insert(category_id, name):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO subcategoria(category_id,name)
            VALUES(%s,%s)
            """,
            (category_id, name)
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
            DELETE FROM subcategoria
            WHERE id = %s
            """,
            (id,)
        )

        conn.commit()

        cursor.close()
        conn.close()