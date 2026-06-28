from database.connection import get_connection
import pandas as pd
import streamlit as st

class CategoriaRepository:

	@staticmethod
	@st.cache_data
	def get_all():
		"""
		Lista todas las categorías en la base de datos.
		Return:
			Diccionario de datos result
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT id, name
						FROM categoria
						ORDER BY id
					""")

					categorias = {
						row[0]: row[1]
						for row in cursor.fetchall()
					}
					return categorias
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()

	@staticmethod
	def insert(name):
		"""
		Insertar nueva categoría a la base de datos.
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						"""
						INSERT INTO categoria (name)
						VALUES (%s)
						""",
						(name, )
					)
					conn.commit()
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			CategoriaRepository.get_all.clear()

	@staticmethod
	def get_category_by_id(category_id):
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT id, name
						FROM categoria
						WHERE id = %s
						""",
						(category_id,)
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
	def get_category_by_name(category_name):
		"""
		Verificar si categoría existe buscándolo por nombre
		:param category_name: Nombre de la categoria
		:return: True si existe, None si no
		"""

		conn = None
		cursor = None
		try:
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
			return result is not None
		except Exception as e:
			print(f"Error al buscar la categoría: {e}")
			return False
		finally:
			if cursor:
				cursor.close()
			if conn:
				conn.close()

	@staticmethod
	def update(category_id, category_name):
		"""
		Actualizar categoria
		:param category_id: id de categoria
		:param category_name: nombre de categoria
		:return:
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					categoria = CategoriaRepository.get_category_by_id(category_id)
					cursor.execute(
						"""
						UPDATE categoria
						SET name = %s
						WHERE id = %s
						""",
						(category_name, category_id)
					)

					conn.commit()
					return categoria
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			CategoriaRepository.get_all.clear()

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

		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						"""
						DELETE FROM categoria
						WHERE id = %s
						""",
						(category_id,)
					)

					conn.commit()
					return True
		except Exception as e:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			CategoriaRepository.get_all.clear()
