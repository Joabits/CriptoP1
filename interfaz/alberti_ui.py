from __future__ import annotations

import streamlit as st

from cripto_grupo_f import alberti
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("6. Simulador Interactivo del Disco de Alberti")
    texto = st.text_area("Mensaje", "LA SEGURIDAD DEL CANAL ES IMPORTANTE")
    col1, col2, col3, col4 = st.columns(4)
    posicion = col1.slider("Posicion inicial del disco interior", 0, 25, 3)
    rotar_cada = col2.number_input("Rotar cada N letras", min_value=1, max_value=50, value=5)
    direccion = col3.selectbox("Direccion", ["derecha", "izquierda"])
    avance = col4.number_input("Avance por rotacion", min_value=1, max_value=25, value=1)

    st.caption(
        f"Letra indice inicial: {alberti.ALFABETO[posicion]}. La misma configuracion debe usarse para cifrar y descifrar."
    )

    tab_cifrar, tab_descifrar = st.tabs(["Cifrar", "Descifrar"])
    with tab_cifrar:
        resultado = alberti.cifrar(texto, posicion, int(rotar_cada), direccion, int(avance))
        st.subheader("Texto cifrado")
        st.code(resultado["texto_salida"])
        st.subheader("Proceso paso a paso")
        mostrar_tabla(resultado["pasos"])

    with tab_descifrar:
        criptograma = st.text_area(
            "Criptograma Alberti",
            alberti.cifrar(texto, posicion, int(rotar_cada), direccion, int(avance))["texto_salida"],
        )
        resultado = alberti.descifrar(criptograma, posicion, int(rotar_cada), direccion, int(avance))
        st.subheader("Texto descifrado")
        st.code(resultado["texto_salida"])
        st.subheader("Proceso paso a paso")
        mostrar_tabla(resultado["pasos"])
