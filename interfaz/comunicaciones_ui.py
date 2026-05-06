from __future__ import annotations

import streamlit as st

from cripto_grupo_f import comunicaciones
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("2. Seguridad en Comunicaciones")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Sistemas",
        "Superficie de Ataque",
        "Amenazas del Canal",
        "Evaluador CIA",
        "Simulador",
    ])


    # PESTAÑA 1 — Tipos de sistema y comparativa
    with tab1:
        st.subheader("Tipos de sistema")
        tipo = st.radio(
            "Selecciona el tipo de sistema:",
            options=["aislado", "interconectado"],
            horizontal=True,
            key="radio_sistemas",
        )
        sistema = comunicaciones.describir_sistema(tipo)

        col1, col2 = st.columns(2)
        col1.metric("Sistema", sistema["nombre"])
        col2.metric("Amenaza principal", sistema["amenaza_principal"])

        st.write("**Descripcion:**", sistema["descripcion"])
        st.write("**Tipo de acceso:**", sistema["acceso"])

        st.write("**Ejemplos:**")
        for ejemplo in sistema["ejemplos"]:
            st.write(f"- {ejemplo}")
        
        st.write("**Pilares CIA en riesgo:**")
        for pilar in sistema["pilares_en_riesgo"]:
            st.write(f"- {pilar}")

        st.divider()
        st.subheader("Comparativa entre sistemas")
        mostrar_tabla(comunicaciones.obtener_comparativa())


    # PESTAÑA 2 — Superficie de ataque    
    with tab2:
        st.subheader("Calculo de superficie de ataque")
        tipo_sa = st.radio(
            "Sistema a evaluar:",
            options=["aislado", "interconectado"],
            horizontal=True,
            key="radio_superficie",
        )
        superficie = comunicaciones.calcular_superficie_ataque(tipo_sa)

        col1, col2 = st.columns(2)
        col1.metric("Puntaje total", superficie["puntaje_total"])
        col2.metric("Nivel de riesgo", superficie["nivel"])

        st.subheader("Vectores de ataque")
        mostrar_tabla(superficie["vectores"])


    # PESTAÑA 3 — Amenazas del canal
    with tab3:
        st.subheader("Amenazas en el canal de comunicacion")
        filtro = st.radio(
            "Mostrar amenazas:",
            options=["Todas", "Pasivo", "Activo"],
            horizontal=True,
            key="radio_amenazas",
        )
        if filtro == "Todas":
            amenazas = comunicaciones.obtener_amenazas_canal()
        else:
            amenazas = comunicaciones.filtrar_amenazas_por_tipo(filtro)

        mostrar_tabla(amenazas)


    # PESTAÑA 4 — Evaluador CIA
    with tab4:
        st.subheader("Evaluador de canal - Triada CIA")
        c1, c2, c3 = st.columns(3)
        cifrado = c1.checkbox("Cifrado (Confidencialidad)", value=True)
        autenticado = c2.checkbox("Autenticacion (Autenticidad)", value=True)
        integridad = c3.checkbox("Integridad verificada", value=False)

        resultado = comunicaciones.evaluar_canal(cifrado, autenticado, integridad)

        col1, col2 = st.columns(2)
        col1.metric("Puntaje", f"{resultado['puntaje']} / 100")
        col2.metric("Nivel", resultado["nivel"])

        if resultado["pilares_activos"]:
            st.success("Pilares activos: " + ", ".join(resultado["pilares_activos"]))

        if resultado["pilares_faltantes"]:
            st.warning("Pilares faltantes - huecos en el canal:")
            mostrar_tabla(resultado["pilares_faltantes"])

        st.info(resultado["diagnostico"])


    # PESTAÑA 5 — Simulador de transmision
    with tab5:
        st.subheader("Simulador de transmision paso a paso")

        mensaje = st.text_input("Mensaje a transmitir:", "Nota final: 9.5")
        col1, col2 = st.columns(2)
        canal_cifrado = col1.checkbox("Activar cifrado del canal", value=True)
        tipo_ataque = col2.selectbox(
            "Escenario de ataque:",
            options=["ninguno", "pasivo", "activo"]
        )

        sim = comunicaciones.simular_transmision(mensaje, canal_cifrado, tipo_ataque)

        st.caption(f"Escenario activo: **{sim['escenario']}**")
        st.subheader("Log de eventos")
        mostrar_tabla(sim["log"])

        st.divider()
        col1, col2 = st.columns(2)
        col1.write(f"**Mensaje original:** `{sim['mensaje_original']}`")
        col2.write(f"**Mensaje recibido:** `{sim['mensaje_recibido']}`")

        if sim["advertencia"].startswith("Sin vulnerabilidades"):
            st.success(sim["advertencia"])
        else:
            st.error(sim["advertencia"])


