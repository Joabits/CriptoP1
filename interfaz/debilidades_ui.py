from __future__ import annotations

import streamlit as st

from cripto_grupo_f import debilidades
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("1. Mapeo de Debilidades")
    tipo = st.selectbox("Tipo de activo", ["Todos", *debilidades.tipos_de_activo()])
    datos = debilidades.obtener_debilidades(tipo)
    mostrar_tabla(datos)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Resumen")
        mostrar_tabla(debilidades.resumen_por_tipo())
    with col2:
        if tipo != "Todos":
            st.subheader("Controles recomendados")
            for control in debilidades.controles_recomendados(tipo):
                st.write(f"- {control}")
        else:
            st.info("Seleccione un tipo de activo para ver controles especificos.")
