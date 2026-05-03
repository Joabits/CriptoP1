from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from cripto_grupo_f import alberti, auditoria, comunicaciones, criptoanalisis, debilidades, frecuencias


st.set_page_config(
    page_title="Criptografia y Seguridad - Grupo F",
    page_icon=":material/lock:",
    layout="wide",
)


def mostrar_tabla(datos: list[dict] | dict) -> None:
    st.dataframe(pd.DataFrame(datos), width="stretch", hide_index=True)


def seccion_inicio() -> None:
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


def seccion_debilidades() -> None:
    st.header("1. Mapeo de Debilidades")
    tipo = st.selectbox("Tipo de activo", ["Todos", *debilidades.tipos_de_activo()])
    datos = debilidades.obtener_debilidades(tipo)
    mostrar_tabla(datos)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Resumen")
        mostrar_tabla(debilidades.resumen_por_tipo())
    with col2:
        if tipo != "Todos":
            st.subheader("Controles recomendados")
            for control in debilidades.controles_recomendados(tipo):
                st.write(f"- {control}")
        else:
            st.info("Seleccione un tipo de activo para ver controles especificos.")


def seccion_comunicaciones() -> None:
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


def seccion_criptoanalisis() -> None:
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


def seccion_auditoria() -> None:
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


def seccion_frecuencias() -> None:
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


def seccion_alberti() -> None:
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


SECCIONES = {
    "Inicio": seccion_inicio,
    "1. Mapeo de Debilidades": seccion_debilidades,
    "2. Seguridad en Comunicaciones": seccion_comunicaciones,
    "3. Fuerza Bruta vs Criptoanalisis": seccion_criptoanalisis,
    "4. Auditoria Academica": seccion_auditoria,
    "5. Frecuencias ESTIRANDO": seccion_frecuencias,
    "6. Disco de Alberti": seccion_alberti,
}


def main() -> None:
    st.title("Libreria Criptografica y de Seguridad - Grupo F")
    st.caption("Proyecto de Criptografia y Seguridad | Presentacion: 07 de mayo de 2026")
    seleccion = st.sidebar.radio("Modulo", list(SECCIONES.keys()))
    SECCIONES[seleccion]()


if __name__ == "__main__":
    main()
