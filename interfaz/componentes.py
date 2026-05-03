from __future__ import annotations

import pandas as pd
import streamlit as st


def mostrar_tabla(datos: list[dict] | dict) -> None:
    st.dataframe(pd.DataFrame(datos), width="stretch", hide_index=True)
