from database.connection import get_connection
import pandas as pd
import streamlit as st

class MetodoPagoRepository:

	@staticmethod
	@st.cache_data
	def get_all():
		"""
		Obtener todos los registros de los métodos de pago de la base de datos.
		:return: diccionario de datos result
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT id, name
						FROM metodo_pago
						ORDER BY id
					""")

					metodos_pago = {
						row[0]: row[1]
						for row in cursor.fetchall()
					}
					return metodos_pago
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()

	@staticmethod
	def get_payment_method_by_id(payment_method_id):

		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT id, name
						FROM metodo_pago
						WHERE id = %s
						""",
						   (payment_method_id,)
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
	def get_payment_method_by_name(payment_method_name):
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute("""
						SELECT 1
						FROM metodo_pago
						WHERE UPPER(name) = UPPER(%s)
						""",
						   (payment_method_name,)
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
	def insert(payment_method_name):
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						"""
                        INSERT INTO metodo_pago (name)
                        VALUES (%s)
                        """,
						(payment_method_name,)
					)
					conn.commit()

		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			MetodoPagoRepository.get_all.clear()

	@staticmethod
	def update(payment_method_id, payment_method_name):
		"""
		Modificar el método de pago de la base de datos.
		Args:
			payment_method_id (int): Identificador del método de pago
			payment_method_name (str): Nombre del método de pago
		Return:
			Trpayment_method: el nombre anterior del método de pago
		"""
		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					payment_method = MetodoPagoRepository.get_payment_method_by_id(payment_method_id)

					cursor.execute(
						"""
                        UPDATE metodo_pago
                        SET name = %s
                        WHERE id = %s
                        """,
						(payment_method_name, payment_method_id)
					)
					conn.commit()

					return payment_method
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			MetodoPagoRepository.get_all.clear()

	@staticmethod
	def delete(payment_method_id):
		"""
		Elimina método de pago de la base de datos.
		Args:
			payment_method_id (int): Identificador del método de pago
		Return:
			True si se eliminó con éxito
			False si el método de pago no se encontró
		"""

		conn = None
		cursor = None
		try:
			with get_connection() as conn:
				with conn.cursor() as cursor:
					cursor.execute(
						"""
                        DELETE FROM metodo_pago
                        WHERE id = %s
                        """,
						(payment_method_id,)
					)

					conn.commit()
					return True
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()
			MetodoPagoRepository.get_all.clear()
