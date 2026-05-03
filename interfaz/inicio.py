from __future__ import annotations

import streamlit as st

from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("Proyecto Grupo F")
    st.write(
        "Aplicacion educativa en Python para demostrar conceptos de seguridad, criptoanalisis y cifrado clasico mediante una libreria propia."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Modulos", "6")
    col2.metric("Pruebas", "Automatizadas")
    col3.metric("Arquitectura", "Libreria + interfaz")

    st.subheader("Integrantes y modulos")
    mostrar_tabla(
        [
            {"integrante": "DURAN MARCELO KELLY ALISSON", "modulo": "Mapeo de Debilidades"},
            {"integrante": "GONZALES ALBA JOSE BRAYAN", "modulo": "Seguridad en Comunicaciones"},
            {"integrante": "MAMANI PENA DANIEL JOAQUIN", "modulo": "Criptoanalisis Elegante"},
            {"integrante": "NAVARRO ACOSTA SARA EUNICE", "modulo": "Auditoria Academica"},
            {"integrante": "Grupo F", "modulo": "Analizador ESTIRANDO"},
            {"integrante": "Grupo F", "modulo": "Disco de Alberti"},
        ]
    )

    st.subheader("Ruta sugerida de demostracion")
    st.write(
        "Comenzar con activos y comunicaciones, continuar con criptoanalisis, validar expedientes academicos y cerrar con ESTIRANDO y Alberti."
    )
