from __future__ import annotations

import streamlit as st

from cripto_grupo_f import comunicaciones
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("2. Seguridad en Comunicaciones")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sistema aislado")
        st.graphviz_chart(
            """
            digraph {
                rankdir=LR;
                node [shape=box, style=rounded];
                Usuario -> SistemaLocal -> DatosLocales;
            }
            """
        )
    with col2:
        st.subheader("Sistema interconectado")
        st.graphviz_chart(
            """
            digraph {
                rankdir=LR;
                node [shape=box, style=rounded];
                Usuario -> Red -> Servidor -> BaseDatos;
                Atacante -> Red [style=dashed];
            }
            """
        )

    mostrar_tabla(comunicaciones.obtener_comparativa())

    st.subheader("Evaluador de canal")
    c1, c2, c3 = st.columns(3)
    cifrado = c1.checkbox("Cifrado activo", value=True)
    autenticado = c2.checkbox("Autenticacion activa", value=True)
    integridad = c3.checkbox("Integridad verificada", value=False)
    resultado = comunicaciones.evaluar_canal(cifrado, autenticado, integridad)
    st.metric("Estado", resultado["estado"], resultado["riesgo"])
    if resultado["faltantes"]:
        st.warning("Falta: " + ", ".join(resultado["faltantes"]))

    mensaje = st.text_input("Mensaje de prueba", "Notas finales del curso")
    atacante = st.checkbox("El atacante intercepta el canal", value=True)
    simulacion = comunicaciones.simular_transmision(mensaje, atacante, cifrado)
    st.code(simulacion["observacion_del_atacante"])
