from database.connection import get_connection
import pandas as pd


class MetodoPagoRepository:

	@staticmethod
	def get_all():
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT id, name
			FROM metodo_pago
			ORDER BY id
		""")

		result = cursor.fetchall()

		cursor.close()
		conn.close()

		columnas_dinamicas = [desc[0] for desc in cursor.description]

		return pd.DataFrame(result, columns=columnas_dinamicas)

	@staticmethod
	def get_payment_method_by_id(payment_method_id):
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT id, name
			FROM metodo_pago
			WHERE id = %s
			""",
			(payment_method_id,)
		)

		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return result

	@staticmethod
	def get_payment_method_by_name(payment_method_name):
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT 1
			FROM metodo_pago
			WHERE UPPER(name) = UPPER(%s)
			""",
			(payment_method_name,)
		)

		result = cursor.fetchone()

		cursor.close()
		conn.close()

		return result is not None


	@staticmethod
	def insert(payment_method_name):

		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute(
			"""
			INSERT INTO metodo_pago (name)
			VALUES (%s)
			""",
			(payment_method_name, )
		)

		conn.commit()

		cursor.close()
		conn.close()

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
		conn = get_connection()
		cursor = conn.cursor()
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

		cursor.close()
		conn.close()

		return payment_method

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

		# Obtenemos la categoría
		payment_method = MetodoPagoRepository.get_payment_method_by_id(payment_method_id)

		# Si la categoría existe...
		if payment_method:
			conn = get_connection()
			cursor = conn.cursor()

			cursor.execute(
				"""
				DELETE FROM metodo_pago
				WHERE id = %s
				""",
				(payment_method_id,)
			)

			conn.commit()
			cursor.close()
			conn.close()
			return True
		
		# Si la categoría no se encontró, devolvemos false
		return False
