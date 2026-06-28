from database.connection import get_connection
import pandas as pd


class UsuarioRepository:

	@staticmethod
	def get_all():
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT id, firstname, lastname, username, password
			FROM usuario
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
	def get_category_by_id(category_id):
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT id, name
			FROM categoria
			WHERE id = %s
			""",
			(category_id,)
		)

		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return result

	@staticmethod
	def get_category_by_name(category_name):
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT 1
			FROM categoria
			WHERE UPPER(name) = UPPER(%s)
			""",
			(category_name,)
		)

		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return result is not None

	@staticmethod
	def update(id, name):

		conn = get_connection()
		cursor = conn.cursor()
		categoria = CategoriaRepository.get_category_by_id(id)

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

		return categoria

	@staticmethod
	def delete(category_id):
		"""
		Elimina una categoría de la base de datos.
		Args:
			category_id (int): Identificador de la categoría
		Return:
			True si se eliminó con éxito
			False si la categoría no se encontró
		"""

		# Obtenemos la categoría
		category = CategoriaRepository.get_category_by_id(category_id)

		# Si la categoría existe...
		if category:
			conn = get_connection()
			cursor = conn.cursor()

			cursor.execute(
				"""
				DELETE FROM categoria
				WHERE id = %s
				""",
				(category_id,)
			)

			conn.commit()
			cursor.close()
			conn.close()
			return True
		
		# Si la categoría no se encontró, devolvemos false
		return False