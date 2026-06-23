import streamlit as st

from repository.categoria_repository import CategoriaRepository
from repository.subcategoria_repository import SubcategoriaRepository
from repository.metodo_pago_repository import MetodoPagoRepository
import pandas as pd
import time

st.title("⚙️ Administración")

tab1, tab2, tab3 = st.tabs(
    [
        "Categorías",
        "Subcategorías",
        "Métodos de pago"
    ]
)

# Listamos todas las categorías
df_list_categorias = CategoriaRepository.get_all()
# Listamos todos los métodos de pago
df_list_metodo_pago = MetodoPagoRepository.get_all()

with tab1:
    df_edited_category = st.data_editor(
        df_list_categorias,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "id": st.column_config.NumberColumn(
                "ID",
                disabled=True,
                width="small"
            ),
            "name": st.column_config.TextColumn(
                "Nombre",
                width="large",
                required=True
            )
        },
        key="data_editor_categoria"
    )

    if st.button(
        "💾 Guardar cambios",
        use_container_width=True,
        key="btn_guardar_categorias"
    ):
        categorias_en_grilla = (
            df_edited_category["name"]
            .fillna("")
            .str.strip()
            .str.lower()
        )
        duplicados = categorias_en_grilla[categorias_en_grilla.duplicated()]

        if not duplicados.empty:
            st.error(f"La categoría '{duplicados.iloc[0]}' está repetida.")
            st.stop()

        # ELIMINAR REGISTROS
        ids_originales = set(df_list_categorias["id"].dropna())
        ids_finales = set(df_edited_category["id"].dropna())
        ids_eliminados = ids_originales - ids_finales
        for id_categoria in ids_eliminados:
            CategoriaRepository.delete(id_categoria)

        for _, row in df_edited_category.iterrows():

            nombre = str(row["name"]).strip().title()

            if not nombre:
                st.error("Todas las categorías deben tener nombre.")
                st.stop()

            if not nombre:
                continue

            # NUEVO
            if pd.isna(row["id"]):
                CategoriaRepository.insert(nombre)

            # UPDATE
            else:
                registro_original = df_list_categorias[
                    df_list_categorias["id"] == row["id"]
                    ].iloc[0]

                if registro_original["name"] != nombre:
                    CategoriaRepository.update(
                        row["id"],
                        nombre
                    )

        st.success("Cambios guardados")

        st.rerun()

with tab2:

    categoria_id = st.selectbox(
        "Categoría",
        options=df_list_categorias["id"].tolist(),
        format_func=lambda x:
        df_list_categorias.loc[
            df_list_categorias["id"] == x,
            "name"
        ].iloc[0],
        key="selecbox_subcategoria"
    )

    df_list_subcategorias = SubcategoriaRepository.list_by_category(categoria_id)

    st.markdown("#### Subcategorías")
    df_edited_subcategory = st.data_editor(
        df_list_subcategorias,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "id": st.column_config.NumberColumn(
                "ID",
                disabled=True,
                width="small"
            ),
            "category_name": st.column_config.TextColumn(
                "Categoría",
                disabled=True,
                width="medium",
            ),
            "name": st.column_config.TextColumn(
                "Subcategoría",
                required=True,
                width="mediums",
            )
        },
        key="data_editor_subcategoria"
    )


    if st.button(
        "💾 Guardar cambios",
        use_container_width=True,
        key="btn_guardar_subcategorias"
    ):
        subcategorias_en_grilla = (
            df_edited_subcategory["name"]
            .fillna("")
            .str.strip()
            .str.lower()
        )
        duplicados = subcategorias_en_grilla[subcategorias_en_grilla.duplicated()]

        if not duplicados.empty:
            st.error(f"La categoría '{duplicados.iloc[0]}' está repetida.")
            st.stop()

        # ELIMINAR REGISTROS
        ids_originales_sc = set(df_list_subcategorias["id"].dropna())
        ids_finales_sc = set(df_edited_subcategory["id"].dropna())
        ids_eliminados_sc = ids_originales_sc - ids_finales_sc
        for id_categoria in ids_eliminados_sc:
            SubcategoriaRepository.delete(id_categoria)

        for _, row in df_edited_subcategory.iterrows():

            nombre_sc = str(row["name"]).strip().title()

            if not nombre_sc:
                continue

            # NUEVO
            if pd.isna(row["id"]):
                SubcategoriaRepository.insert(categoria_id, nombre_sc)

            # UPDATE
            else:
                registro_original = df_list_subcategorias[
                    df_list_subcategorias["id"] == row["id"]
                    ].iloc[0]

                if registro_original["name"] != nombre_sc:
                    SubcategoriaRepository.update(
                        row["id"],
                        nombre_sc
                    )

        st.success("Cambios guardados")

        st.rerun()

with tab3:

    df_edited_metodo_pago = st.data_editor(
        df_list_metodo_pago,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "id": st.column_config.NumberColumn(
                "ID",
                disabled=True,
                width="small"
            ),
            "name": st.column_config.TextColumn(
                "Nombre",
                width="large",
                required=True
            )
        },
        key="data_editor_metodo_pago"
    )

    if st.button(
        "💾 Guardar cambios",
        use_container_width=True,
        key="btn_guardar_metodo_pago"
    ):

        # ELIMINAR REGISTROS
        ids_originales = set(df_list_metodo_pago["id"].dropna())
        ids_finales = set(df_edited_metodo_pago["id"].dropna())
        ids_eliminados = ids_originales - ids_finales
        for id_metodo_pago in ids_eliminados:
            MetodoPagoRepository.delete(id_metodo_pago)

        for _, row in df_edited_metodo_pago.iterrows():

            nombre = str(row["name"]).strip().title()

            if not nombre:
                st.error("Todas las categorías deben tener nombre.")
                st.stop()

            if not nombre:
                continue

            # NUEVO
            if pd.isna(row["id"]):
                MetodoPagoRepository.insert(nombre)

            # UPDATE
            else:
                registro_original = df_list_metodo_pago[
                    df_list_metodo_pago["id"] == row["id"]
                    ].iloc[0]

                if registro_original["name"] != nombre:
                    MetodoPagoRepository.update(
                        row["id"],
                        nombre
                    )

        st.success("Cambios guardados")

        st.rerun()

