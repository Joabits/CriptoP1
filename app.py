from __future__ import annotations

import streamlit as st

from interfaz import (
    alberti_ui,
    auditoria_ui,
    comunicaciones_ui,
    criptoanalisis_ui,
    debilidades_ui,
    frecuencias_ui,
    inicio,
)


st.set_page_config(
    page_title="Criptografia y Seguridad - Grupo F",
    page_icon=":material/lock:",
    layout="wide",
)


SECCIONES = {
    "Inicio": inicio.mostrar,
    "1. Mapeo de Debilidades": debilidades_ui.mostrar,
    "2. Seguridad en Comunicaciones": comunicaciones_ui.mostrar,
    "3. Fuerza Bruta vs Criptoanalisis": criptoanalisis_ui.mostrar,
    "4. Auditoria Academica": auditoria_ui.mostrar,
    "5. Frecuencias ESTIRANDO": frecuencias_ui.mostrar,
    "6. Disco de Alberti": alberti_ui.mostrar,
}


def main() -> None:
    st.title("Libreria Criptografica y de Seguridad - Grupo F")
    st.caption("Proyecto de Criptografia y Seguridad | Presentacion: 07 de mayo de 2026")
    seleccion = st.sidebar.radio("Modulo", list(SECCIONES.keys()))
    SECCIONES[seleccion]()


if __name__ == "__main__":
    main()
