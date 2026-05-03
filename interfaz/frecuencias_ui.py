from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from cripto_grupo_f import frecuencias
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("5. Analizador de Frecuencias ESTIRANDO")
    criptograma = st.text_area(
        "Criptograma",
        "KZ RLPQHGZQKZ KZ JQOZ KZ OQHZ RQZKZ KZQ ZKJQKQJQ",
        height=140,
    )
    filas = frecuencias.calcular_frecuencias(criptograma)

    if not filas:
        st.warning("Ingrese al menos una letra para analizar.")
        return

    df = pd.DataFrame(filas)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Conteo de monogramas")
        mostrar_tabla(filas)
    with col2:
        st.metric("Presencia de E,A,O,S,R,N,I,D,C", f"{frecuencias.porcentaje_estirando(criptograma)}%")

    st.subheader("Histograma")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df["letra"], df["frecuencia_%"], label="Criptograma")
    ax.plot(df["letra"], df["castellano_%"], color="red", marker="o", label="Castellano")
    ax.set_ylabel("Frecuencia %")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

    sugerencias = frecuencias.sugerir_sustituciones(criptograma)
    st.subheader("Sustituciones sugeridas")
    mostrar_tabla(sugerencias)
    mapa = {item["letra_cifrada"]: item["sugerencia_texto_plano"] for item in sugerencias}

    texto_mapa = st.text_area(
        "Sustituciones manuales o ajustadas",
        ", ".join(f"{origen}={destino}" for origen, destino in mapa.items()),
        help="Use formatos como X=E, Q=A o X->E. Las letras no asignadas se muestran como guion bajo.",
    )
    try:
        mapa_manual = frecuencias.parsear_sustituciones(texto_mapa)
        st.subheader("Previsualizacion con sustituciones")
        st.code(frecuencias.aplicar_sustituciones(criptograma, mapa_manual))
    except ValueError as error:
        st.error(str(error))

    tab_digramas, tab_trigramas = st.tabs(["Digramas", "Trigramas"])
    with tab_digramas:
        mostrar_tabla(frecuencias.contar_ngramas(criptograma, longitud=2))
        st.caption("Patrones comunes esperados: " + ", ".join(frecuencias.DIGRAMAS_COMUNES))
    with tab_trigramas:
        mostrar_tabla(frecuencias.contar_ngramas(criptograma, longitud=3))
        st.caption("Patrones comunes esperados: " + ", ".join(frecuencias.TRIGRAMAS_COMUNES))
