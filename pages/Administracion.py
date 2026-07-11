import streamlit as st

# Importamos repositorios
from repository.category_repository import CategoryRepository
from repository.subcategory_repository import SubcategoryRepository
from repository.payment_method_repository import PaymentMethodRepository
# Importamos models
from models import Category, Subcategory, PaymentMethod
# Importamos conexión
from database.connection import get_session
# Importamos script para autenticación
from services.session_service import require_login

######### Autenticación #########
require_login()

st.set_page_config(page_title="Admin", layout="centered")
st.title(":material/settings: Administración")

# Útiles para el script
session = get_session()

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


tab_category, tab_subcategory, tab_payment_method = st.tabs(
	[
		"Categorías",
		"Subcategorías",
		"Métodos de pago"
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


