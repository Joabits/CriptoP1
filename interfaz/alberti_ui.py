from __future__ import annotations

import math

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import Circle, FancyArrowPatch

from cripto_grupo_f import alberti
from cripto_grupo_f.alberti import ALFABETO_ES
from cripto_grupo_f.texto import ALFABETO as ALFABETO_EN

from .componentes import mostrar_tabla


_RADIO_EXTERIOR = 1.0
_RADIO_INTERIOR = 0.72
_RADIO_TEXTO_EXT = 1.12
_RADIO_TEXTO_INT = 0.6


def _dibujar_disco(
    posicion: int,
    alfabeto: str,
    tipo_disco: str,
    letra_externa: str | None = None,
    letra_interna: str | None = None,
    titulo: str | None = None,
):
    n = len(alfabeto)
    alfabeto_interior = alberti.rotar_disco(posicion, alfabeto, tipo_disco)
    paso = 2 * math.pi / n

    fig, ax = plt.subplots(figsize=(5.4, 5.4), dpi=120)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)

    ax.add_patch(Circle((0, 0), 1.32, fill=False, lw=1.2, color="#888"))
    ax.add_patch(Circle((0, 0), _RADIO_EXTERIOR, fill=True, color="#f5efe0", ec="#444", lw=1.5))
    ax.add_patch(Circle((0, 0), _RADIO_INTERIOR, fill=True, color="#1f3b6e", ec="#0d203f", lw=1.5))
    ax.add_patch(Circle((0, 0), 0.06, fill=True, color="#c8a85a", ec="#444"))

    indice_externo = alfabeto.index(letra_externa) if letra_externa and letra_externa in alfabeto else None
    letra_clave = alfabeto[posicion % n]

    for i, letra in enumerate(alfabeto):
        ang = math.pi / 2 - i * paso
        x_ext = _RADIO_TEXTO_EXT * math.cos(ang)
        y_ext = _RADIO_TEXTO_EXT * math.sin(ang)
        x_int = _RADIO_TEXTO_INT * math.cos(ang)
        y_int = _RADIO_TEXTO_INT * math.sin(ang)

        x1 = (_RADIO_EXTERIOR - 0.04) * math.cos(ang)
        y1 = (_RADIO_EXTERIOR - 0.04) * math.sin(ang)
        x2 = _RADIO_EXTERIOR * math.cos(ang)
        y2 = _RADIO_EXTERIOR * math.sin(ang)
        ax.plot([x1, x2], [y1, y2], color="#888", lw=0.8)

        resaltar_ext = indice_externo is not None and i == indice_externo
        resaltar_clave_ext = i == 0
        ax.text(
            x_ext, y_ext, letra,
            ha="center", va="center",
            fontsize=12 if n <= 26 else 11,
            fontweight="bold" if resaltar_ext or resaltar_clave_ext else "normal",
            color="#b8002b" if resaltar_ext else "#0f6b46" if resaltar_clave_ext else "#222",
            rotation=math.degrees(ang) - 90,
        )

        letra_int = alfabeto_interior[i]
        resaltar_int = indice_externo is not None and i == indice_externo and letra_interna is not None
        resaltar_clave_int = i == 0
        ax.text(
            x_int, y_int, letra_int.lower(),
            ha="center", va="center",
            fontsize=11 if n <= 26 else 10,
            fontweight="bold" if resaltar_int or resaltar_clave_int else "normal",
            color="#ffd86b" if resaltar_int else "#7dffb2" if resaltar_clave_int else "#f0f0f0",
            rotation=math.degrees(ang) - 90,
        )

    flecha = FancyArrowPatch(
        (0, 1.38), (0, _RADIO_EXTERIOR + 0.02),
        arrowstyle="-|>", mutation_scale=14, color="#b8002b", lw=1.6,
    )
    ax.add_patch(flecha)
    ax.text(0, 1.42, f"A / {letra_clave.lower()}", ha="center", va="bottom", fontsize=9, color="#b8002b")

    if indice_externo is not None:
        ang = math.pi / 2 - indice_externo * paso
        ax.plot(
            [0, 1.25 * math.cos(ang)],
            [0, 1.25 * math.sin(ang)],
            color="#b8002b", lw=1.2, ls="--", alpha=0.6,
        )

    sub = f"Posicion {posicion} - clave: {alfabeto[posicion % n]}"
    ax.set_title(titulo or sub, fontsize=11, color="#222", pad=6)
    fig.tight_layout()
    return fig


def _render_pasos(resultado: dict, alfabeto: str, tipo_disco: str, key_prefix: str) -> None:
    pasos = [p for p in resultado["pasos"] if p.get("alfabeto_exterior")]
    if not pasos:
        st.info("Introduce texto con letras para visualizar el disco.")
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
            alfabeto,
            tipo_disco,
            letra_externa=paso["entrada"],
            letra_interna=paso["salida"],
            titulo=f"Paso {indice}/{len(pasos)} - clave {paso['letra_clave']}",
        )
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    with col_info:
        st.metric("Letra de entrada (exterior)", paso["entrada"])
        st.metric("Letra de salida (interior)", paso["salida"])
        st.write(f"**Clave actual:** {paso['letra_clave']} (posicion {paso['posicion_disco']})")
        st.write(f"**Alfabeto exterior:** `{paso['alfabeto_exterior']}`")
        st.write(f"**Alfabeto interior:** `{paso['alfabeto_interior']}`")
        st.caption(paso["accion"])


def mostrar() -> None:
    st.header("6. Simulador Interactivo del Disco de Alberti")
    st.caption(
        "Dos anillos concentricos: el exterior es el alfabeto claro (mayusculas) y el interior es el "
        "alfabeto cifrado (minusculas) que rota cada N letras."
    )

    idioma = st.radio(
        "Alfabeto",
        ["Espanol (27 letras, con \u00d1)", "Ingles (26 letras)"],
        horizontal=True,
        key="alberti_idioma",
    )
    alfabeto = ALFABETO_ES if idioma.startswith("Espanol") else ALFABETO_EN
    n = len(alfabeto)
    st.caption(f"Alfabeto activo ({n} letras): `{alfabeto}`")

    tipo_disco_label = st.radio(
        "Tipo de disco interior",
        ["Alberti clasico mezclado", "Escolar desplazado"],
        horizontal=True,
        key="alberti_tipo_disco",
        help="El clasico usa un alfabeto interior mezclado. El escolar usa el alfabeto en orden y solo lo desplaza.",
    )
    tipo_disco = alberti.TIPO_DISCO_ESCOLAR if tipo_disco_label.startswith("Escolar") else alberti.TIPO_DISCO_CLASICO

    texto_default = "LA SE\u00d1ORA CRUZ\u00d3 EL CANAL" if n == 27 else "LA SEGURIDAD DEL CANAL ES IMPORTANTE"
    texto = st.text_area("Mensaje", texto_default)

    col1, col2, col3, col4 = st.columns(4)
    posicion = col1.slider(
        "Posicion inicial del disco interior", 0, n - 1, min(3, n - 1),
        help="Letra del disco interior que queda alineada debajo de la A exterior. Si eliges F, veras f bajo A.",
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

    st.caption(
        f"Clave inicial: {alfabeto[posicion]}. En el disco se alinea {alfabeto[posicion].lower()} debajo de la A exterior."
    )
    st.caption(f"Disco interior activo: `{alberti.rotar_disco(posicion, alfabeto, tipo_disco)}`")

    with st.expander("Que significan estos controles"):
        st.markdown(
            "- **Posicion inicial**: define la clave visible del disco interior. Si eliges F, la f del disco interior "
            "queda debajo de la A exterior.\n"
            "- **Tipo de disco interior**: el clasico usa un alfabeto mezclado; el escolar usa el alfabeto normal "
            "desplazado, como muchos discos hechos en papel.\n"
            "- **Rotar cada N letras**: despues de cifrar/descifrar esa cantidad de letras, el disco interior gira. "
            "Por ejemplo, con 5 rota al procesar la letra 6, 11, 16, etc.\n"
            "- **Direccion**: indica si ese giro suma posiciones hacia la derecha o resta posiciones hacia la izquierda.\n"
            "- **Avance por rotacion**: indica cuantas posiciones se mueve el disco en cada giro. Con avance 1 se mueve "
            "una letra; con avance 3 se mueve tres letras."
        )

    with st.expander("Vista previa del disco con la posicion inicial", expanded=True):
        fig = _dibujar_disco(posicion, alfabeto, tipo_disco, titulo=f"Disco inicial - clave {alfabeto[posicion]}")
        st.pyplot(fig, width="content")
        plt.close(fig)

    tab_cifrar, tab_descifrar = st.tabs(["Cifrar", "Descifrar"])
    with tab_cifrar:
        resultado = alberti.cifrar(
            texto, posicion, int(rotar_cada), direccion, int(avance), alfabeto=alfabeto, tipo_disco=tipo_disco
        )
        st.subheader("Texto cifrado")
        st.code(resultado["texto_salida"])
        _render_pasos(resultado, alfabeto, tipo_disco, key_prefix="cif")
        st.subheader("Proceso paso a paso")
        mostrar_tabla(resultado["pasos"])

    with tab_descifrar:
        criptograma = st.text_area(
            "Criptograma Alberti",
            alberti.cifrar(
                texto, posicion, int(rotar_cada), direccion, int(avance), alfabeto=alfabeto, tipo_disco=tipo_disco
            )["texto_salida"],
        )
        resultado = alberti.descifrar(
            criptograma, posicion, int(rotar_cada), direccion, int(avance), alfabeto=alfabeto, tipo_disco=tipo_disco
        )
        st.subheader("Texto descifrado")
        st.code(resultado["texto_salida"])
        _render_pasos(resultado, alfabeto, tipo_disco, key_prefix="dec")
        st.subheader("Proceso paso a paso")
        mostrar_tabla(resultado["pasos"])
