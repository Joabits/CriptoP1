from __future__ import annotations

import streamlit as st

from cripto_grupo_f import criptoanalisis
from .componentes import mostrar_tabla


def mostrar() -> None:
    st.header("3. Taller de Criptoanalisis Elegante")
    st.write(
        "Laboratorio interactivo para comparar la busqueda exhaustiva con un analisis criptografico basado en patrones del idioma."
    )

    tab_taller, tab_guia = st.tabs(["Taller", "Guia comparativa"])

    with tab_taller:
        st.subheader("Ejemplo interactivo")
        texto = st.text_area("Texto plano para ejemplo Cesar", "LA CRIPTOGRAFIA PROTEGE LA INFORMACION")
        nombre_alfabeto = st.selectbox("Alfabeto", list(criptoanalisis.ALFABETOS_CESAR.keys()), index=1)
        alfabeto = criptoanalisis.ALFABETOS_CESAR[nombre_alfabeto]
        clave = st.slider("Desplazamiento Cesar", 1, len(alfabeto) - 1, 7)
        cifrado = criptoanalisis.cifrar_cesar(texto, clave, alfabeto)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Criptograma")
            st.code(cifrado)
            st.caption(
                f"Resultado de aplicar Cesar con desplazamiento {clave} usando alfabeto {nombre_alfabeto.lower()}."
            )
            st.subheader("Descifrado correcto")
            st.code(criptoanalisis.descifrar_cesar(cifrado, clave, alfabeto))
            st.caption("Se muestra con la clave seleccionada para comprobar el resultado del taller.")
        with col2:
            st.subheader("Mejores candidatos por fuerza bruta")
            candidatos = criptoanalisis.fuerza_bruta_cesar(cifrado, alfabeto)[:8]
            mostrar_tabla(candidatos)

        st.subheader("Lectura criptoanalitica")
        st.write(
            "Ahora el taller usa una pista tecnica: si una letra aparece mucho en el criptograma, podria corresponder a una letra frecuente del castellano. Como primera hipotesis se compara con E."
        )
        analisis = criptoanalisis.analisis_criptoanalitico_cesar(cifrado, alfabeto)
        mostrar_tabla(analisis[:8])

        if analisis:
            mejor = analisis[0]
            st.success(
                f"Hipotesis prioritaria: probar clave {mejor['clave_sugerida']}. Resultado: {mejor['texto_posible']}."
            )
            if mejor["puntaje_linguistico"] == 0:
                st.warning(
                    "Con textos muy cortos hay poca evidencia estadistica; por eso conviene confirmar con la clave elegida o usar un texto mas largo."
                )

        st.info(
            "La fuerza bruta prueba claves una por una; el criptoanalisis explica por que ciertas claves merecen revisarse primero."
        )

    with tab_guia:
        st.subheader("Fuerza bruta: ataque burdo")
        st.write(
            "La fuerza bruta es una busqueda exhaustiva: intenta todas las claves posibles hasta encontrar una salida legible o verificable. En Cesar funciona porque solo existen 25 desplazamientos utiles; en sistemas modernos, el espacio de claves vuelve este enfoque impracticable."
        )
        st.code(
            """para cada clave posible:
    descifrar el criptograma
    revisar si el texto parece correcto""",
            language="text",
        )

        st.subheader("Criptoanalisis: ataque tecnico y cientifico")
        st.write(
            "El criptoanalisis no se limita a probar. Observa el criptosistema, el idioma, la estructura matematica y los patrones del criptograma para reducir la busqueda. Por eso formula hipotesis: letras frecuentes, palabras probables, repeticiones y debilidades del algoritmo."
        )
        st.code(
            """observar el criptograma
medir frecuencias y patrones
formular una hipotesis
probar primero las claves con mejor respaldo""",
            language="text",
        )

        st.subheader("Comparacion directa")
        mostrar_tabla(criptoanalisis.comparar_metodos())

        st.subheader("Definiciones de respaldo")
        mostrar_tabla(criptoanalisis.definiciones_autores())

        st.warning(
            "Mensaje para la exposicion: fuerza bruta significa insistir; criptoanalisis significa investigar antes de insistir."
        )
