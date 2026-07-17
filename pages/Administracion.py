import streamlit as st
from datetime import date, datetime, timedelta

# Importamos repositorios
from repository.category_repository import CategoryRepository
from repository.subcategory_repository import SubcategoryRepository
from repository.payment_method_repository import PaymentMethodRepository
# Importamos models
from models import Category, Subcategory, PaymentMethod, DateInterval
# Importamos conexión
from database.connection import get_session
# Importamos script para autenticación
from services.session_service import require_login
from services.date_interval_service import DateIntervalService
import services.date_services as dt_services

######### Autenticación #########
require_login()

st.set_page_config(page_title="Admin", layout="centered")
st.title(":material/settings: Administración")

# Útiles para el script
session = get_session()

def get_last_end_date_from_interval():
    with get_session() as session:
        service = DateIntervalService(session)
        return service.get_last_end_date_from_interval()

def insert_date_interval(obj):
    with get_session() as session:
        service = DateIntervalService(session)
        return service.update(obj)
		
def get_all_date_interval():
    with get_session() as session:
        service = DateIntervalService(session)
        return service.get_all()

def formatear_input(input_name):
	return input_name.strip().title()

@st.dialog("Editar categoría")
def edit_category(category_repo:Category, category_id:int, category_new_name:str):
	"""
		Dialogo para editar el nombre de una categoría existente.
		Args:
			category_repo (Category): objeto Categoría
			category_id (int): ID de la categoría a editar.
			category_new_name (str): Nuevo nombre de la categoría. 
	"""
	category_name_raw = st.text_input("Nuevo nombre de categoría:", value=category_new_name)
	category_name = formatear_input(category_name_raw)

	if st.button("💾 Guardar cambios", width="stretch"):
		
		if category_repo.get_category_by_name(category_name):
			st.error("La categoría ya existe.")
		else:
			category_to_update = Category(id=category_id, name=category_name)
			updated_category = category_repo.update(category_to_update)

			if updated_category:
				st.toast(f"Categoría {updated_category.name} actualizada correctamente.")
				st.rerun()
			else:
				st.error("Error al actualizar la categoría.")
				st.rerun()

@st.dialog("Eliminar categoría")
def delete_category(category_repo:Category, category_id:int, category_name:str):
	"""
		Dialogo para eliminar una categoría existente.
		Args:
			category_repo (Category): objeto Categoría.
			category_id (int): ID de la categoría a eliminar.
			category_name (str): Nombre de la categoría. 
	"""
	st.write(f"¿Estás seguro de que quieres eliminar la categoría {category_name}?")
	st.write("Si eliminas esta categoría, también se eliminarán todas las subcategorías asociadas")

	with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):

		if st.button(":material/check:", key=f"confirm_delete_cat_{category_id}", type="primary"):
			success = category_repo.delete(Category, id=category_id)

			if success:
				st.toast("Categoría eliminada correctamente")
				st.rerun()
			else:
				st.error("Error al eliminar categoría")
		
		if st.button("Cancelar"):
			st.rerun()

@st.dialog("Editar subcategoría")
def edit_subcategory(subcategory_repo:SubcategoryRepository, category_id:int, subcategory_id:int, subcategory_new_name:str):
	"""
		Dialogo para editar el nombre de una subcategoría existente.
		Args:
			subcategory_id (int): ID de la subcategoría a editar.
			subcategory_new_name (str): Nuevo nombre de la subcategoría. 
	"""
	subcategory_name_raw = st.text_input("Nuevo nombre de subcategoría:", value=subcategory_new_name)
	subcategory_name = formatear_input(subcategory_name_raw)

	if st.button("💾 Guardar cambios", width="stretch"):
		
		if subcategory_repo.exists_subcategory_by_name(category_id, subcategory_name):
			st.error("La subcategoría ya existe.")
		else:
			subcategory_to_update = Subcategory(id=subcategory_id, name=subcategory_name)
			updated_subcategory = subcategory_repo.update(subcategory_to_update)

			if updated_subcategory:
				st.toast(f"Subcategoría {updated_subcategory.name} actualizada correctamente.")
				st.rerun()
			else:
				st.error("Error al actualizar la subcategoría.")
				st.rerun()

@st.dialog("Eliminar subcategoría")
def delete_subcategory(subcategory_repo:SubcategoryRepository, subcategory_id:int, subcategory_name:str):
	"""
		Dialogo para eliminar una subcategoría existente.
		Args:
			subcategory_id (int): ID de la subcategoría a eliminar.
			subcategory_name (str): Nombre de la subcategoría. 
	"""
	st.write(f"¿Estás seguro de que quieres eliminar la subcategoría {subcategory_name}?")

	with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):

		if st.button(":material/check:", key=f"confirm_delete_subcat_{subcategory_id}", type="primary"):
			success = subcategory_repo.delete(Subcategory, id=subcategory_id)

			if success:
				st.toast("Subcategoría eliminada correctamente")
				st.rerun()
			else:
				st.error("Error al eliminar subcategoría")
		
		if st.button("Cancelar"):
			st.rerun()

@st.dialog("Editar método de pago")
def edit_payment_method(payment_method_repo:PaymentMethod, payment_method_id:int, payment_method_name:str):
	"""
		Dialogo para editar el nombre de un metodo de pago existente.
		Args:
			payment_method_id (int): ID del metodo de pago a editar.
			payment_method_name (str): Antiguo nombre del metodo de pago.
	"""
	payment_method_name_raw = st.text_input("Nuevo nombre del método de pago:", value=payment_method_name)
	payment_method_name = formatear_input(payment_method_name_raw)

	if st.button("💾 Guardar cambios", width="stretch"):
		
		if payment_method_repo.get_payment_method_by_name(payment_method_name):
			st.error("El método de pago ya existe.")
		else:
			payment_method_to_update = PaymentMethod(id=payment_method_id, name=payment_method_name)
			updated_payment_method = payment_method_repo.update(payment_method_to_update)

			if updated_payment_method:
				st.toast(f"Método de pago {updated_payment_method.name} actualizada correctamente.")
				st.rerun()
			else:
				st.error("Error al actualizar el método de pago.")
				st.rerun()
				
@st.dialog("Eliminar método de pago")
def delete_payment_method(payment_method_repo:PaymentMethod, payment_method_id:int, payment_method_name:str):
	"""
		Dialogo para eliminar un método de pago existente.
		Args:
			payment_method_id (int): ID del método de pago a eliminar.
			payment_method_name (str): Nombre del método de pago. 
	"""
	st.write(f"¿Estás seguro de que quieres eliminar el método de pago {payment_method_name}?")

	with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):

		if st.button(":material/check:", key=f"confirm_delete_pm_{payment_method_id}", type="primary"):
			success = payment_method_repo.delete(PaymentMethod, id=payment_method_id)

			if success:
				st.toast("Método de pago eliminado correctamente")
				st.rerun()
			else:
				st.error("Error al eliminar método de pago")
		
		if st.button("Cancelar"):
			st.rerun()


tab_category, tab_subcategory, tab_payment_method, tab_dates_interval = st.tabs(
	[
		"Categorías",
		"Subcategorías",
		"Métodos de pago",
		"Periodos"
	]
)

with tab_category:
	category_repo = CategoryRepository(session)

	# Agregar categoría
	ti_nueva_categoria_raw = st.text_input("Nueva categoría", key="new_category")
	ti_nueva_categoria = formatear_input(ti_nueva_categoria_raw)

	if st.button(
		label="💾 Guardar categoría",
		key="bttn_add_category",
		width="stretch",
		type="primary"
	):
		if ti_nueva_categoria:
			if category_repo.get_category_by_name(ti_nueva_categoria):
				st.error("La categoría ya existe.")
			else:
				new_category = Category(name=ti_nueva_categoria)
				category_repo.insert(new_category)
				st.success("Categoría creada correctamente.")
				st.rerun()
		else:
			st.error("Categoría no puede estar vacía")

	# Listar categorías existentes
	df_list_categorias = category_repo.get_all(Category)
	for row in df_list_categorias.itertuples():
		with st.container(horizontal=True, border=True, vertical_alignment="center", width="stretch"):
			col_id, col_name, col_edit, col_delete = st.columns([1, 5, 1, 1])

			col_id.write(f"{row.id}")
			col_name.write(f"{row.name}")
			col_edit.button(label=":material/edit:",
			key=f"edit_{row.id}",
			on_click=edit_category,
			args=(category_repo, row.id,row.name),
			type="secondary"
			)
			col_delete.button(label=":material/delete:",
			key=f"delete_{row.id}",
			on_click=delete_category,
			args=(category_repo, row.id,row.name),
			type="primary"
			)

with tab_subcategory:
	subcategory_repo = SubcategoryRepository(session)
	categorias_ids = df_list_categorias['id'].tolist()
	dicc_categorias = dict(zip(df_list_categorias['id'], df_list_categorias['name']))
	categoria_id = st.selectbox(
		"Categoría",
		options=categorias_ids,
		format_func=lambda x:dicc_categorias[x],
		key="selecbox_subcategoria"
	)
	df_list_subcategorias = subcategory_repo.list_by_category(category_id=categoria_id)

	# Agregar subcategoría
	ti_nueva_subcategoria_raw = st.text_input("Nueva subcategoría", key="new_subcategory")
	ti_nueva_subcategoria = formatear_input(ti_nueva_subcategoria_raw)

	if st.button(
		label="💾 Guardar subcategoría",
		key="bttn_add_subcategory",
		width="stretch",
		type="primary"
	):
		if ti_nueva_subcategoria:
			if subcategory_repo.exists_subcategory_by_name(categoria_id,ti_nueva_subcategoria):
				st.error("La subcategoría ya existe.")
			else:
				new_subcategory = Subcategory(category_id=categoria_id, name=ti_nueva_subcategoria)
				subcategory_repo.insert(new_subcategory)
				st.success("Subcategoría creada correctamente.")
				st.rerun()
		else:
			st.error("Subcategoría no puede estar vacía")

	# Listar subcategorías existentes
	for row in df_list_subcategorias.itertuples():
		with st.container(horizontal=True, border=True, vertical_alignment="center", width="stretch"):
			col_id, col_name, col_edit, col_delete = st.columns([1, 5, 1, 1])

			col_id.write(f"{row.id}")
			col_name.write(f"{row.name}")
			col_edit.button(label=":material/edit:",
			key=f"edit_subcat_{row.id}",
			on_click=edit_subcategory,
			args=(subcategory_repo, categoria_id, row.id, row.name),
			type="secondary"
			)
			col_delete.button(label=":material/delete:",
			key=f"delete_subcat_{row.id}",
			on_click=delete_subcategory,
			args=(subcategory_repo, row.id,row.name),
			type="primary"
			)

with tab_payment_method:
	payment_method_repo = PaymentMethodRepository(session)

	# Agregar metodo de pago
	ti_new_payment_method_raw = st.text_input("Nuevo método de pago", key="new_payment_method")
	ti_new_payment_method = formatear_input(ti_new_payment_method_raw)

	if st.button(
		label="💾 Guardar método de pago",
		key="bttn_add_payment_method",
		width="stretch",
		type="primary"
	):
		if ti_new_payment_method:
			if payment_method_repo.get_payment_method_by_name(ti_new_payment_method):
				st.error("El método de pago ya existe.")
			else:
				new_payment_method = PaymentMethod(name=ti_new_payment_method)
				payment_method_repo.insert(new_payment_method)
				st.success("Método de pago creado correctamente.")
				st.rerun()
		else:
			st.error("Método de pago no puede estar vacía")

	# Listar métodos de pago existentes
	df_list_metodo_pago = payment_method_repo.get_all(PaymentMethod)
	for row in df_list_metodo_pago.itertuples():
		with st.container(horizontal=True, border=True, vertical_alignment="center", width="stretch"):
			col_id, col_name, col_edit, col_delete = st.columns([1, 5, 1, 1])

			col_id.write(f"{row.id}")
			col_name.write(f"{row.name}")
			col_edit.button(label=":material/edit:",
				key=f"edit_pm_{row.id}",
				on_click=edit_payment_method,
				args=(payment_method_repo, row.id,row.name),
				type="secondary"
			)
			col_delete.button(label=":material/delete:",
				key=f"delete_pm_{row.id}",
				on_click=delete_payment_method,
				args=(payment_method_repo, row.id,row.name),
				type="primary"
			)

with tab_dates_interval:
	last_day_bd = get_last_end_date_from_interval()

	# Regla UX: La nueva fecha de inicio sugerida es el día siguiente al último cierre
	init_date = last_day_bd + timedelta(days=1)

	# 2. Selector de Rango de Fechas Integrado
	rango_fechas = st.date_input(
		"Selecciona el rango del periodo:",
		value=(init_date, init_date + timedelta(days=30)), # Fechas por defecto en el form
		min_value=date(2026, 1, 1),
		format="DD/MM/YYYY"
	)

	disabled_btn_date_interval = True
	type_btn_date_interval = "secondary"
	# 3. Validación Reactiva en Pantalla
	if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
		start_date, end_date = rango_fechas
		
		# Validar contra el último registro para evitar solapamientos en Frontend
		if start_date <= last_day_bd:
			st.error(f":material/error: Error: La fecha de inicio ({start_date.strftime('%d/%m/%Y')}) se solapa con el periodo anterior que terminó el {last_day_bd.strftime('%d/%m/%Y')}.")
			disabled_btn_date_interval = True
			type_btn_date_interval = "secondary"
		else:
			st.success(f":material/check: Rango válido: {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')} (Total: {(end_date - start_date).days + 1} días)")
			disabled_btn_date_interval = False
			type_btn_date_interval = "primary"
	else:
		st.info("💡 Por favor, selecciona ambas fechas (Inicio y Fin) en el calendario.")

	date_interval_btn = st.button("💾 Guardar Intervalo", disabled=disabled_btn_date_interval, type=type_btn_date_interval, width="stretch")
	# El botón solo se activa si pasa la regla de negocio
	if date_interval_btn:
		periodName = dt_services.getPeriodName(start_date, end_date)
		new_date_interval = DateInterval(start_date=start_date, end_date=end_date, name=periodName)
		insert_date_interval(new_date_interval)
		st.toast(":material/save: Intervalo guardado con éxito")
		st.rerun()

	st.divider()
	st.subheader("Historial de Intervalos")

	df_date_intervals, columns_dataframe_config, columns_order = get_all_date_interval()
	df_show = df_date_intervals[columns_order]
	st.dataframe(df_show, column_config=columns_dataframe_config, use_container_width=True, hide_index = True)
