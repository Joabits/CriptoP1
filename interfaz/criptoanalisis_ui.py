from __future__ import annotations

import streamlit as st

from cripto_grupo_f import criptoanalisis
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("3. Taller de Criptoanalisis Elegante")
    mostrar_tabla(criptoanalisis.comparar_metodos())

    texto = st.text_area("Texto plano para ejemplo Cesar", "LA CRIPTOGRAFIA PROTEGE LA INFORMACION")
    clave = st.slider("Desplazamiento Cesar", 1, 25, 7)
    cifrado = criptoanalisis.cifrar_cesar(texto, clave)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Criptograma")
        st.code(cifrado)
    with col2:
        st.subheader("Mejores candidatos por fuerza bruta")
        candidatos = criptoanalisis.fuerza_bruta_cesar(cifrado)[:8]
        mostrar_tabla(candidatos)

    st.info(
        "La fuerza bruta prueba todas las claves; el criptoanalisis intenta reducir el trabajo usando patrones del idioma."
    )
