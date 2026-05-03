from __future__ import annotations

import streamlit as st

from cripto_grupo_f import auditoria


def mostrar() -> None:
    st.header("4. Simulador de Auditoria Academica")
    preguntas = auditoria.obtener_preguntas()
    respuestas = {}

    for codigo, datos in preguntas.items():
        respuestas[codigo] = st.checkbox(f"{codigo}. {datos['pregunta']}", value=False)

    resultado = auditoria.evaluar_auditoria(respuestas)
    col1, col2, col3 = st.columns(3)
    col1.metric("Resultado", resultado["estado"])
    col2.metric("Nivel", resultado["nivel"])
    col3.metric("Puntaje", f"{resultado['puntaje']}/{resultado['maximo']}")

    if resultado["recomendaciones"]:
        st.subheader("Recomendaciones")
        for recomendacion in resultado["recomendaciones"]:
            st.write(f"- {recomendacion}")
    else:
        st.success("Los controles principales estan cubiertos.")
