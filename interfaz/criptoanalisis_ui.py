from __future__ import annotations

import streamlit as st

from cripto_grupo_f import criptoanalisis
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("3. Taller de Criptoanalisis Elegante")
    st.write(
        "Laboratorio interactivo para comparar la busqueda exhaustiva con un analisis criptografico basado en patrones del idioma."
    )

    tab_taller, tab_fundamento, tab_manual = st.tabs(
        ["Taller", "Fundamento", "Manual de uso"]
    )

    with tab_fundamento:
        st.subheader("Objetivo")
        st.write(
            "Demostrar que romper un cifrado clasico no siempre exige probar claves al azar: tambien se puede razonar sobre el algoritmo, el idioma y la estructura del criptograma."
        )

        st.subheader("Algoritmo usado")
        st.write(
            "El taller usa el cifrado Cesar, un cifrado por sustitucion monoalfabetica donde cada letra se desplaza una cantidad fija de posiciones dentro del alfabeto."
        )
        st.code(
            """C = (P + k) mod 26
P = (C - k) mod 26""",
            language="text",
        )
        st.caption(
            "P es la posicion de la letra original, C la posicion cifrada y k el desplazamiento o clave."
        )

        st.subheader("Explicacion matematica y criptografica")
        st.write(
            "Matematicamente, Cesar trabaja con aritmetica modular: cuando el desplazamiento supera la Z, el conteo vuelve a la A. Criptograficamente, su debilidad es que solo tiene 25 claves utiles y conserva patrones del idioma, por eso puede analizarse con palabras frecuentes como DE, LA, EL o EN."
        )
        mostrar_tabla(criptoanalisis.comparar_metodos())

        st.subheader("Ejemplo")
        st.write("Con clave 7, la letra A pasa a H, B pasa a I y Z pasa a G.")
        mostrar_tabla(
            [
                {"texto_plano": "LA", "clave": 7, "criptograma": criptoanalisis.cifrar_cesar("LA", 7)},
                {
                    "texto_plano": "CRIPTO",
                    "clave": 7,
                    "criptograma": criptoanalisis.cifrar_cesar("CRIPTO", 7),
                },
            ]
        )

    with tab_taller:
        st.subheader("Ejemplo interactivo")
        texto = st.text_area("Texto plano para ejemplo Cesar", "LA CRIPTOGRAFIA PROTEGE LA INFORMACION")
        clave = st.slider("Desplazamiento Cesar", 1, 25, 7)
        cifrado = criptoanalisis.cifrar_cesar(texto, clave)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Criptograma")
            st.code(cifrado)
            st.caption(f"Resultado de aplicar Cesar con desplazamiento {clave}.")
        with col2:
            st.subheader("Mejores candidatos por fuerza bruta")
            candidatos = criptoanalisis.fuerza_bruta_cesar(cifrado)[:8]
            mostrar_tabla(candidatos)

        st.info(
            "La fuerza bruta prueba todas las claves; el criptoanalisis intenta reducir el trabajo usando patrones del idioma."
        )

    with tab_manual:
        st.subheader("Manual de uso")
        st.write(
            "1. Escriba un mensaje en el campo de texto del taller.\n"
            "2. Elija un desplazamiento Cesar entre 1 y 25.\n"
            "3. Observe el criptograma generado automaticamente.\n"
            "4. Revise la tabla de fuerza bruta: cada fila prueba una clave posible.\n"
            "5. Use el puntaje linguistico para identificar candidatos mas probables.\n"
            "6. Compruebe que la clave correcta recupera un texto legible."
        )
        st.warning(
            "Este taller es educativo: Cesar no debe usarse para proteger informacion real porque su espacio de claves es demasiado pequeno."
        )
