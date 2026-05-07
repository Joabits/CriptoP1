from __future__ import annotations

import math

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import Circle, FancyArrowPatch

from cripto_grupo_f import alberti
from cripto_grupo_f.alberti import ALFABETO_EXTERIOR, ALFABETO_INTERIOR

from .componentes import mostrar_tabla


_RADIO_EXTERIOR = 1.0
_RADIO_INTERIOR = 0.72
_RADIO_TEXTO_EXT = 1.13
_RADIO_TEXTO_INT = 0.59


def _dibujar_disco(
    posicion: int,
    tipo_disco: str,
    letra_externa: str | None = None,
    letra_interna: str | None = None,
    titulo: str | None = None,
):
    n = len(ALFABETO_EXTERIOR)
    alfabeto_interior_rotado = alberti.rotar_disco(posicion, tipo_disco)
    paso = 2 * math.pi / n

    fig, ax = plt.subplots(figsize=(6.0, 6.0), dpi=130)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # Anillos
    ax.add_patch(Circle((0, 0), 1.35, fill=False, lw=1.0, color="#999"))
    ax.add_patch(Circle((0, 0), _RADIO_EXTERIOR, fill=True, color="#f5f0e8", ec="#333", lw=1.8))
    ax.add_patch(Circle((0, 0), _RADIO_INTERIOR - 0.01, fill=True, color="#f5f0e8", ec="#333", lw=1.8))
    ax.add_patch(Circle((0, 0), _RADIO_INTERIOR - 0.13, fill=True, color="#ddd8cc", ec="#555", lw=1.0))
    ax.add_patch(Circle((0, 0), 0.07, fill=True, color="#888", ec="#333"))

    # Indices para resaltado
    indice_externo = ALFABETO_EXTERIOR.index(letra_externa) if letra_externa and letra_externa in ALFABETO_EXTERIOR else None

    for i in range(n):
        ang = math.pi / 2 - i * paso

        # Lineas divisorias disco exterior
        x1 = (_RADIO_EXTERIOR - 0.06) * math.cos(ang - paso / 2)
        y1 = (_RADIO_EXTERIOR - 0.06) * math.sin(ang - paso / 2)
        x2 = 1.32 * math.cos(ang - paso / 2)
        y2 = 1.32 * math.sin(ang - paso / 2)
        ax.plot([x1, x2], [y1, y2], color="#999", lw=0.7)

        # Lineas divisorias disco interior
        xi1 = (_RADIO_INTERIOR - 0.14) * math.cos(ang - paso / 2)
        yi1 = (_RADIO_INTERIOR - 0.14) * math.sin(ang - paso / 2)
        xi2 = (_RADIO_INTERIOR - 0.01) * math.cos(ang - paso / 2)
        yi2 = (_RADIO_INTERIOR - 0.01) * math.sin(ang - paso / 2)
        ax.plot([xi1, xi2], [yi1, yi2], color="#999", lw=0.7)

        # Letra exterior
        x_ext = _RADIO_TEXTO_EXT * math.cos(ang)
        y_ext = _RADIO_TEXTO_EXT * math.sin(ang)
        letra_ext = ALFABETO_EXTERIOR[i]
        resaltar_ext = indice_externo is not None and i == indice_externo
        ax.text(
            x_ext, y_ext, letra_ext,
            ha="center", va="center",
            fontsize=10,
            fontweight="bold" if resaltar_ext else "normal",
            color="#b8002b" if resaltar_ext else "#111",
            rotation=math.degrees(ang) - 90,
        )

        # Letra interior
        x_int = _RADIO_TEXTO_INT * math.cos(ang)
        y_int = _RADIO_TEXTO_INT * math.sin(ang)
        letra_int = alfabeto_interior_rotado[i]
        resaltar_int = indice_externo is not None and i == indice_externo
        ax.text(
            x_int, y_int, letra_int,
            ha="center", va="center",
            fontsize=9,
            fontweight="bold" if resaltar_int else "normal",
            color="#b8002b" if resaltar_int else "#222",
            rotation=math.degrees(ang) - 90,
        )

    # Flecha indicadora (apunta a la primera posicion del exterior = A)
    ang_flecha = math.pi / 2  # apunta arriba (A esta en la cima)
    flecha = FancyArrowPatch(
        (1.42 * math.cos(ang_flecha), 1.42 * math.sin(ang_flecha)),
        (1.28 * math.cos(ang_flecha), 1.28 * math.sin(ang_flecha)),
        arrowstyle="-|>", mutation_scale=14, color="#b8002b", lw=1.6,
    )
    ax.add_patch(flecha)

    # Indicador de clave
    simbolo_clave = ALFABETO_INTERIOR[posicion % n]
    ax.text(0, -1.47, f"Clave: A exterior → '{simbolo_clave}' interior",
            ha="center", va="center", fontsize=9, color="#b8002b")

    if indice_externo is not None:
        ang_l = math.pi / 2 - indice_externo * paso
        ax.plot(
            [0, 1.22 * math.cos(ang_l)],
            [0, 1.22 * math.sin(ang_l)],
            color="#b8002b", lw=1.2, ls="--", alpha=0.6,
        )

    ax.set_title(titulo or f"Posicion {posicion} - clave: {simbolo_clave}", fontsize=11, color="#222", pad=8)
    fig.tight_layout()
    return fig


def _render_pasos(resultado: dict, tipo_disco: str, key_prefix: str) -> None:
    pasos = [p for p in resultado["pasos"] if p.get("alfabeto_exterior")]
    if not pasos:
        st.info("Introduce texto con letras del alfabeto exterior para visualizar el disco.")
        return

    st.subheader("Disco animado")
    indice = st.slider(
        "Paso",
        min_value=1,
        max_value=len(pasos),
        value=1,
        key=f"{key_prefix}_paso",
        help="Desliza para avanzar letra a letra y ver como rota el disco interior.",
    )
    paso = pasos[indice - 1]

    col_disco, col_info = st.columns([3, 2])
    with col_disco:
        fig = _dibujar_disco(
            int(paso["posicion_disco"]),
            tipo_disco,
            letra_externa=paso["entrada"],
            letra_interna=paso["salida"],
            titulo=f"Paso {indice}/{len(pasos)} - clave '{paso['simbolo_clave']}'",
        )
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    with col_info:
        st.metric("Letra entrada (exterior)", paso["entrada"])
        st.metric("Simbolo salida (interior)", paso["salida"])
        st.write(f"**Clave actual:** `{paso['simbolo_clave']}` (posicion {paso['posicion_disco']})")
        st.write(f"**Disco exterior:** `{paso['alfabeto_exterior']}`")
        st.write(f"**Disco interior:** `{paso['alfabeto_interior']}`")
        st.caption(paso["accion"])


def mostrar() -> None:
    st.header("6. Simulador Interactivo del Disco de Alberti")
    st.caption(
        "Recreacion del disco original de Leon Battista Alberti (1466). "
        "El anillo exterior contiene las letras latinas (sin H, J, K, U, W, Y) mas los numeros 1-4. "
        "El anillo interior contiene letras en minuscula mas los simbolos &, h, k, y."
    )

    n = len(ALFABETO_EXTERIOR)
    st.caption(f"Alfabeto exterior ({n} simbolos): `{ALFABETO_EXTERIOR}`")
    st.caption(f"Alfabeto interior ({n} simbolos): `{ALFABETO_INTERIOR}`")

    tipo_disco_label = st.radio(
        "Tipo de disco interior",
        ["Alberti clasico (historico)", "Escolar desplazado"],
        horizontal=True,
        key="alberti_tipo_disco",
        help="El clasico usa el alfabeto interior mezclado historico de Alberti. El escolar solo desplaza el orden.",
    )
    tipo_disco = alberti.TIPO_DISCO_ESCOLAR if tipo_disco_label.startswith("Escolar") else alberti.TIPO_DISCO_CLASICO

    texto_default = "EL SECRETO"
    texto = st.text_area("Mensaje (solo letras del alfabeto exterior)", texto_default)

    col1, col2, col3, col4 = st.columns(4)
    posicion = col1.slider(
        "Posicion inicial del disco interior", 0, n - 1, 0,
        help="Define que simbolo interior queda alineado con la A exterior.",
    )
    rotar_cada = col2.number_input(
        "Rotar cada N letras", min_value=1, max_value=50, value=5,
        help="Cantidad de letras procesadas antes de girar el disco interior.",
    )
    direccion = col3.selectbox(
        "Direccion", ["derecha", "izquierda"],
        help="Sentido en que se mueve el disco interior cuando toca rotar.",
    )
    avance = col4.number_input(
        "Avance por rotacion", min_value=1, max_value=n - 1, value=1,
        help="Numero de posiciones que avanza el disco cada vez que rota.",
    )

    simbolo_inicial = ALFABETO_INTERIOR[posicion]
    st.caption(f"Clave inicial: `{simbolo_inicial}` queda alineado debajo de la A exterior.")
    st.caption(f"Disco interior activo: `{alberti.rotar_disco(posicion, tipo_disco)}`")

    with st.expander("Que significan estos controles"):
        st.markdown(
            "- **Posicion inicial**: define que simbolo del disco interior queda alineado con la A exterior.\n"
            "- **Tipo de disco**: el clasico usa el alfabeto interior historico de Alberti; el escolar simplemente desplaza.\n"
            "- **Rotar cada N letras**: tras cifrar/descifrar esa cantidad de letras, el disco interior gira.\n"
            "- **Direccion**: sentido del giro (derecha suma posiciones, izquierda resta).\n"
            "- **Avance**: posiciones que se mueve el disco en cada rotacion.\n\n"
            "**Nota historica**: Alberti usaba los numeros 1-4 del disco exterior para indicar cuando rotar el disco "
            "y a que posicion, insertandolos en el criptograma como senales de rotacion."
        )

    with st.expander("Vista previa del disco con la posicion inicial", expanded=True):
        fig = _dibujar_disco(posicion, tipo_disco, titulo=f"Disco inicial - clave '{simbolo_inicial}'")
        st.pyplot(fig, width="content")
        plt.close(fig)

    tab_cifrar, tab_descifrar = st.tabs(["Cifrar", "Descifrar"])
    with tab_cifrar:
        resultado = alberti.cifrar(
            texto, posicion, int(rotar_cada), direccion, int(avance), tipo_disco=tipo_disco
        )
        st.subheader("Texto cifrado")
        st.code(resultado["texto_salida"])
        _render_pasos(resultado, tipo_disco, key_prefix="cif")
        st.subheader("Proceso paso a paso")
        mostrar_tabla(resultado["pasos"])

    with tab_descifrar:
        criptograma_default = alberti.cifrar(
            texto, posicion, int(rotar_cada), direccion, int(avance), tipo_disco=tipo_disco
        )["texto_salida"]
        criptograma = st.text_area("Criptograma Alberti", criptograma_default)
        resultado = alberti.descifrar(
            criptograma, posicion, int(rotar_cada), direccion, int(avance), tipo_disco=tipo_disco
        )
        st.subheader("Texto descifrado")
        st.code(resultado["texto_salida"])
        _render_pasos(resultado, tipo_disco, key_prefix="dec")
        st.subheader("Proceso paso a paso")
        mostrar_tabla(resultado["pasos"])