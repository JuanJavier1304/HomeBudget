import streamlit as st

from repository.categoria_repository import CategoriaRepository
from repository.subcategoria_repository import SubcategoriaRepository
from repository.metodo_pago_repository import MetodoPagoRepository
import pandas as pd
import time
from services.session_service import require_login

######### Autenticación #########
_="""require_login()
with st.sidebar:
    st.write(f"👤 {st.session_state['username']}")
    if st.button("Cerrar sesión"):
        st.session_state.clear()
        st.switch_page("app.py")
        """
######### Fin de Autenticación #########

#st.set_page_config(page_title="Admin", layout="wide")
st.title("⚙️ Administración")

def formatear_input(input_name):
	return input_name.strip().title()

@st.dialog("Editar categoría")
def edit_category(category_id:int, category_new_name:str):
	"""
		Dialogo para editar el nombre de una categoría existente.
		Args:
			category_id (int): ID de la categoría a editar.
			category_new_name (str): Nuevo nombre de la categoría. 
	"""
	category_name_raw = st.text_input("Nuevo nombre de categoría:", value=category_new_name)
	category_name = formatear_input(category_name_raw)

	if st.button("💾 Guardar cambios", width="stretch"):
		
		if CategoriaRepository.get_category_by_name(category_name):
			st.error("La categoría ya existe.")
		else:
			updated_category = CategoriaRepository.update(category_id, category_name)

			if updated_category:
				up_id, up_name = updated_category #desempaquetamos la tupla
				st.toast(f"Categoría {up_name} actualizada correctamente.")
				st.rerun()
			else:
				st.error("Error al actualizar la categoría.")
				st.rerun()

@st.dialog("Eliminar categoría")
def delete_category(category_id:int, category_name:str):
	"""
		Dialogo para eliminar una categoría existente.
		Args:
			category_id (int): ID de la categoría a eliminar.
			category_name (str): Nombre de la categoría. 
	"""
	st.write(f"¿Estás seguro de que quieres eliminar la categoría {category_name}?")
	st.write("Si eliminas esta categoría, también se eliminarán todas las subcategorías asociadas")

	with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):

		if st.button(":material/check:", key=f"confirm_delete_cat_{category_id}", type="primary"):
			success = CategoriaRepository.delete(category_id)

			if success:
				st.toast("Categoría eliminada correctamente")
				st.rerun()
			else:
				st.error("Error al eliminar categoría")
		
		if st.button("Cancelar"):
			st.rerun()

@st.dialog("Editar subcategoría")
def edit_subcategory(category_id:int, subcategory_id:int, subcategory_new_name:str):
	"""
		Dialogo para editar el nombre de una subcategoría existente.
		Args:
			subcategory_id (int): ID de la subcategoría a editar.
			subcategory_new_name (str): Nuevo nombre de la subcategoría. 
	"""
	subcategory_name_raw = st.text_input("Nuevo nombre de subcategoría:", value=subcategory_new_name)
	subcategory_name = formatear_input(subcategory_name_raw)

	if st.button("💾 Guardar cambios", width="stretch"):
		
		if SubcategoriaRepository.get_subcategory_by_name(category_id, subcategory_name):
			st.error("La subcategoría ya existe.")
		else:
			updated_subcategory = SubcategoriaRepository.update(subcategory_id, subcategory_name)

			if updated_subcategory:
				up_id, up_name = updated_subcategory #desempaquetamos la tupla
				st.toast(f"Subcategoría {up_name} actualizada correctamente.")
				st.rerun()
			else:
				st.error("Error al actualizar la subcategoría.")
				st.rerun()

@st.dialog("Eliminar subcategoría")
def delete_subcategory(subcategory_id:int, subcategory_name:str):
	"""
		Dialogo para eliminar una subcategoría existente.
		Args:
			subcategory_id (int): ID de la subcategoría a eliminar.
			subcategory_name (str): Nombre de la subcategoría. 
	"""
	st.write(f"¿Estás seguro de que quieres eliminar la subcategoría {subcategory_name}?")

	with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):

		if st.button(":material/check:", key=f"confirm_delete_subcat_{subcategory_id}", type="primary"):
			success = SubcategoriaRepository.delete(subcategory_id)

			if success:
				st.toast("Subcategoría eliminada correctamente")
				st.rerun()
			else:
				st.error("Error al eliminar subcategoría")
		
		if st.button("Cancelar"):
			st.rerun()

@st.dialog("Editar método de pago")
def edit_payment_method(payment_method_id:int, payment_method_new_name:str):
	"""
		Dialogo para editar el nombre de un método de pago existente.
		Args:
			payment_method_id (int): ID del método de pago a editar.
			payment_method_new_name (str): Nuevo nombre del método de pago. 
	"""
	payment_method_name_raw = st.text_input("Nuevo nombre del método de pago:", value=payment_method_new_name)
	payment_method_name = formatear_input(payment_method_name_raw)

	if st.button("💾 Guardar cambios", width="stretch"):
		
		if MetodoPagoRepository.get_payment_method_by_name(payment_method_name):
			st.error("El método de pago ya existe.")
		else:
			updated_payment_method = MetodoPagoRepository.update(payment_method_id, payment_method_name)

			if updated_payment_method:
				up_id, up_name = updated_payment_method #desempaquetamos la tupla
				st.toast(f"Método de pago {up_name} actualizada correctamente.")
				st.rerun()
			else:
				st.error("Error al actualizar el método de pago.")
				st.rerun()
				
@st.dialog("Eliminar método de pago")
def delete_payment_method(payment_method_id:int, payment_method_name:str):
	"""
		Dialogo para eliminar un método de pago existente.
		Args:
			payment_method_id (int): ID del método de pago a eliminar.
			payment_method_name (str): Nombre del método de pago. 
	"""
	st.write(f"¿Estás seguro de que quieres eliminar el método de pago {payment_method_name}?")

	with st.container(horizontal=True, border=True, vertical_alignment="center", horizontal_alignment="center", width="stretch"):

		if st.button(":material/check:", key=f"confirm_delete_pm_{payment_method_id}", type="primary"):
			success = MetodoPagoRepository.delete(payment_method_id)

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

# Listamos todos los métodos de pago
df_list_metodo_pago = MetodoPagoRepository.get_all()

with tab_category:

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
			if CategoriaRepository.get_category_by_name(ti_nueva_categoria):
				st.error("La categoría ya existe.")
			else:
				CategoriaRepository.insert(ti_nueva_categoria)
				st.success("Categoría creada correctamente.")
				st.rerun()
		else:
			st.error("Categoría no puede estar vacía")

	# Listar categorías existentes
	df_list_categorias = CategoriaRepository.get_all()
	categorias_ids = list(df_list_categorias)
	for id_category, name_category in df_list_categorias.items():
		with st.container(horizontal=True, border=True, vertical_alignment="center", width="stretch"):
			col_id, col_name, col_edit, col_delete = st.columns([1, 5, 1, 1])

			col_id.write(f"{id_category}")
			col_name.write(f"{name_category}")
			col_edit.button(label=":material/edit:",
			key=f"edit_{id_category}",
			on_click=edit_category,
			args=(id_category,name_category),
			type="secondary"
			)
			col_delete.button(label=":material/delete:",
			key=f"delete_{id_category}",
			on_click=delete_category,
			args=(id_category,name_category),
			type="primary"
			)

with tab_subcategory:

	categoria_id = st.selectbox(
		"Categoría",
		options=categorias_ids,
		format_func=lambda x:df_list_categorias[x],
		key="selecbox_subcategoria"
	)
	df_list_subcategorias = SubcategoriaRepository.list_by_category(categoria_id)

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
			if SubcategoriaRepository.get_subcategory_by_name(categoria_id,ti_nueva_subcategoria):
				st.error("La subcategoría ya existe.")
			else:
				SubcategoriaRepository.insert(categoria_id, ti_nueva_subcategoria)
				st.success("Subcategoría creada correctamente.")
				st.rerun()
		else:
			st.error("Subcategoría no puede estar vacía")

	# Listar categorías existentes
	for subcategory_id, subcategory_name in df_list_subcategorias.items():
		with st.container(horizontal=True, border=True, vertical_alignment="center", width="stretch"):
			col_id, col_name, col_edit, col_delete = st.columns([1, 5, 1, 1])

			col_id.write(f"{subcategory_id}")
			col_name.write(f"{subcategory_name}")
			col_edit.button(label=":material/edit:",
			key=f"edit_subcat_{subcategory_id}",
			on_click=edit_subcategory,
			args=(categoria_id, subcategory_id, subcategory_name),
			type="secondary"
			)
			col_delete.button(label=":material/delete:",
			key=f"delete_subcat_{subcategory_id}",
			on_click=delete_subcategory,
			args=(subcategory_id,subcategory_name),
			type="primary"
			)

with tab_payment_method:

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
			if MetodoPagoRepository.get_payment_method_by_name(ti_new_payment_method):
				st.error("El método de pago ya existe.")
			else:
				MetodoPagoRepository.insert(ti_new_payment_method)
				st.success("Método de pago creado correctamente.")
				st.rerun()
		else:
			st.error("Método de pago no puede estar vacía")

	# Listar métodos de pago existentes
	for payment_method_id, payment_method_name in df_list_metodo_pago.items():
		with st.container(horizontal=True, border=True, vertical_alignment="center", width="stretch"):
			col_id, col_name, col_edit, col_delete = st.columns([1, 5, 1, 1])

			col_id.write(f"{payment_method_id}")
			col_name.write(f"{payment_method_name}")
			col_edit.button(label=":material/edit:",
			key=f"edit_pm_{payment_method_id}",
			on_click=edit_payment_method,
			args=(payment_method_id,payment_method_name),
			type="secondary"
			)
			col_delete.button(label=":material/delete:",
			key=f"delete_pm_{payment_method_id}",
			on_click=delete_payment_method,
			args=(payment_method_id,payment_method_name),
			type="primary"
			)


