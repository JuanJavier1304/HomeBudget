from database.connection import get_connection
import streamlit as st

class SubcategoriaRepository:

	@staticmethod
	@st.cache_data
	def get_subcategory_by_id(subcategory_id):
		"""
		Listar subcategoría por id
		:param subcategory_id: ID de la subcategoría
		:return: subcategoría
		"""

		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT id, name
						FROM subcategoria
						WHERE id = %s
						""",
						   (subcategory_id,)
					)

					result = cursor.fetchone()
					return result
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()

	@staticmethod
	def get_subcategory_by_name(category_id, subcategory_name):
		"""
		Obtener  subcategoría por nombre
		:param subcategory_name: nombre de subcategoría
		:param category_id: id de la categoría
		:return:
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT 1
						FROM subcategoria
						WHERE UPPER(name) = UPPER(%s)
							and category_id = %s
						""",
						(subcategory_name, category_id)
					)

					result = cursor.fetchone()
					return result is not None
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()

	@staticmethod
	def list_by_category(category_id):
		"""
		Lista las subcategorias por categoría en la base de datos.
		:param category_id: id de la categoría
		:return: diccionario de datos result
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT
							s.id,
							s.name
						FROM subcategoria s
						WHERE s.category_id = %s
						ORDER BY s.id, s.name
					""",
						(category_id,)
					)

					result = {
						row[0]: row[1]
						for row in cursor.fetchall()
					}

					return result
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()

	@staticmethod
	def insert(category_id, subcategory_name):
		"""
		Insertar una subcategoria en la base de datos.
		:param category_id: id de la categora
		:param subcategory_name: nombre de subcategoria
		:return:
		"""

		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						"""
						INSERT INTO subcategoria(category_id,name)
						VALUES(%s,%s)
						""",
						(category_id, subcategory_name)
					)

					conn.commit()
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			SubcategoriaRepository.get_subcategory_by_id.clear()

	@staticmethod
	def update(subcategory_id, subcategory_name):
		"""
		Actualizar una subcategoria en la base de datos.
		:param subcategory_id: id de la subcategoria
		:param subcategory_name: nombre de subcategoria
		:return:
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
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
					return subcategoria
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			SubcategoriaRepository.get_subcategory_by_id.clear()

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

		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						"""
						DELETE FROM subcategoria
						WHERE id = %s
						""",
						(subcategory_id,)
					)

					conn.commit()
					return True
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			SubcategoriaRepository.get_subcategory_by_id.clear()
