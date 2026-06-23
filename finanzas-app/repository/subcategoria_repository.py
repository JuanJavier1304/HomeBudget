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
	def get_subcategory_by_id(subcategory_id):
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT id, name
			FROM subcategoria
			WHERE id = %s
			""",
			(subcategory_id,)
		)

		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return result

	@staticmethod
	def get_subcategory_by_name(subcategory_name):
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT 1
			FROM subcategoria
			WHERE UPPER(name) = UPPER(%s)
			""",
			(subcategory_name,)
		)

		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return result is not None

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
	def insert(category_id, subcategory_name):

		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute(
			"""
			INSERT INTO subcategoria(category_id,name)
			VALUES(%s,%s)
			""",
			(category_id, subcategory_name)
		)

		conn.commit()

		cursor.close()
		conn.close()

	@staticmethod
	def update(subcategory_id, subcategory_name):

		conn = get_connection()
		cursor = conn.cursor()
		subcategoria = SubcategoriaRepository.get_subcategory_by_id(subcategory_id)

		cursor.execute(
			"""
			UPDATE subcategoria
			SET name = %s
			WHERE id = %s
			""",
			(subcategory_name, subcategory_id)
		)

		conn.commit()

		cursor.close()
		conn.close()

		return subcategoria

	@staticmethod
	def delete(subcategory_id):
		"""
		Elimina una subcategoría de la base de datos.
		Args:
			subcategory_id (int): Identificador de la subcategoría
		Return:
			True si se eliminó con éxito
			False si la subcategoría no se encontró
		"""

		# Obtenemos la subcategoría
		subcategory = SubcategoriaRepository.get_subcategory_by_id(subcategory_id)

		# Si la subcategoría existe...
		if subcategory:
			conn = get_connection()
			cursor = conn.cursor()

			cursor.execute(
				"""
				DELETE FROM subcategoria
				WHERE id = %s
				""",
				(subcategory_id,)
			)

			conn.commit()
			cursor.close()
			conn.close()
			return True
		
		# Si la subcategoría no se encontró, devolvemos false
		return False