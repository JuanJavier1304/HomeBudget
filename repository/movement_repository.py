from database.connection import get_connection
import pandas as pd


class MovimientoRepository:

	@staticmethod
	def get_all():
		# En construcción
		return None

	@staticmethod
	def insert(user_id, fecha, tipo_movimiento, descripcion, monto, categoria_id, subcategoria_id, metodo_pago_id, tipo_variable, comentario, es_gasto_compartido,es_gasto_hogar):
		"""
		Registra nuevo movimiento a la base de datos.
		Args:
			user_id (int): ID del usuario que registra
			fecha (date): Fecha del movimiento
			tipo_movimiento (str): Tipo de movimiento (gasto/ingreso)
			descripcion (str): Descripción del movimiento
			monto (double): Monto del movimiento
			categoria_id (int): ID de la categoría del movimiento
			subcategoria_id (int): ID de la subcategoría del movimiento
			metodo_pago_id (int): ID del método de pago del movimiento
			tipo_variable (str): Variabilidad del movimiento (fijo o variable)
			comentario (str): Comentario del movimiento
		"""

		conn = None
		cursor = None
		try:
			conn = get_connection()
			cursor = conn.cursor()

			cursor.execute(
				"""
				INSERT INTO movimiento (
					user_id,
					movement_date,
					movement_type,
					description,
					category_id,
					subcategory_id, 
					amount,
					payment_method_id,
					variability,
					comment,
					is_shared,
					is_household_expense
				) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
				""",
				(
					user_id,
				 	fecha,
				 	tipo_movimiento,
				 	descripcion,
				 	categoria_id,
					subcategoria_id,
				 	monto,
					metodo_pago_id,
					tipo_variable,
					comentario,
					es_gasto_compartido,
					es_gasto_hogar
				)
			)
			conn.commit()
		except Exception:
			conn.rollback()
			raise
		finally:
			cursor.close()
			conn.close()


	@staticmethod
	def get_movement_by_date(user_id, movement_date):
		"""
		Lista los movimientos por fecha
		Args:
			user_id (int): ID del usuario
			fecha (date): Fecha del movimiento
		"""
		conn = get_connection()
		cursor = conn.cursor()

		cursor.execute("""
			SELECT id,
				m.movement_date,
				m.movement_type,
				m.description,
				C.name as category_name,
				sc.name as subcategory_name,
				m.amount,
				pm.name as payment_method_name,
				m.variability,
				m.comment
			FROM movimiento m
				INNER JOIN categoria c ON c.id = m.category_id
				INNER JOIN subcategoria sc ON sc.id = m.subcategory_id
				INNER JOIN metodo_pago mp ON mp.id = m.payment_method_id
			WHERE m.user_id = %s and m.movement_date = %s
			""",
			(user_id, movement_date)
		)

		result = cursor.fetchall()

		cursor.close()
		conn.close()

		return result

	@staticmethod
	def update(id, name):
		# En construcción
		return None

	@staticmethod
	def delete(category_id):
		# En construcción
		return None