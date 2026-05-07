import streamlit as st
from cripto_grupo_f.auditoria import (
    generar_expediente,
    obtener_sesion_preguntas,
    obtener_retroalimentacion,
    calcular_puntaje,
)

# ─────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────

def inyectar_estilos():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;500;600;700&display=swap');

    /* ── Tipografía general ── */
    section[data-testid="stMain"], p, li, span, div {
        font-family: 'Exo 2', sans-serif;
    }

    /* ── Fondo blanco (igual que el resto del proyecto) ── */
    .stApp { background-color: #ffffff !important; }
    section[data-testid="stMain"] > div { background-color: #ffffff !important; }

    /* ── Texto oscuro sobre fondo blanco ── */
    p, li, div { color: #1a1a2e; }

    /* ── Label de sección ── */
    .au-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.82rem;
        letter-spacing: 0.18em;
        color: #1a6abf;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
        display: block;
    }

    /* ── Título ── */
    .au-title {
        font-size: 2rem;
        font-weight: 700;
        color: #0d1b2a;
        line-height: 1.15;
        margin-bottom: 0.5rem;
    }

    /* ── Tarjeta ── */
    .au-card {
        background: #f4f8ff;
        border: 1px solid #d0e4ff;
        border-radius: 12px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.2rem;
    }

    /* ── Expediente: filas ── */
    .au-field-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #d0e4ff;
        font-size: 0.9rem;
    }
    .au-field-row:last-child { border-bottom: none; }
    .au-field-key {
        font-family: 'Share Tech Mono', monospace;
        color: #1a6abf;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        min-width: 120px;
    }
    .au-field-val { color: #0d1b2a; text-align: right; font-weight: 500; }

    /* ── Pills de notas ── */
    .au-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #e8f1ff;
        border: 1px solid #b0ccf0;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.82rem;
        color: #0d1b2a;
    }
    .au-pill-num {
        font-family: 'Share Tech Mono', monospace;
        color: #1a6abf;
        font-weight: 700;
    }

    /* ── Barra de progreso ── */
    .au-progress-bg {
        background: #e0ecff;
        border-radius: 20px;
        height: 6px;
        margin-bottom: 1.4rem;
        overflow: hidden;
    }
    .au-progress-fill {
        height: 6px;
        border-radius: 20px;
        background: linear-gradient(90deg, #1a6abf, #4a9eff);
    }

    /* ── Caja de pregunta ── */
    .au-pregunta {
        background: #f4f8ff;
        border-left: 3px solid #1a6abf;
        border-radius: 0 10px 10px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        font-size: 1rem;
        color: #0d1b2a;
        line-height: 1.65;
    }
    .au-badge {
        display: inline-block;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.15em;
        background: #ddeeff;
        color: #1a6abf;
        border: 1px solid #a0c4f0;
        border-radius: 4px;
        padding: 2px 8px;
        margin-bottom: 0.7rem;
        text-transform: uppercase;
    }

    /* ── Retroalimentación ── */
    .au-retro-ok {
        background: #edfff4;
        border: 1px solid #5cb87a;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #1a6b38 !important;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .au-retro-warn {
        background: #fff8e6;
        border: 1px solid #e0a020;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #7a4800 !important;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* ── Veredicto ── */
    .au-veredicto-nivel {
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .au-veredicto-estado {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        color: #1a6abf;
        margin-top: 0.3rem;
    }
    .au-color-rojo  { color: #cc2222; }
    .au-color-ambar { color: #c07800; }
    .au-color-verde { color: #1a7a38; }

    /* ── Puntaje ── */
    .au-puntaje-num {
        font-family: 'Share Tech Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: #1a6abf;
    }
    .au-puntaje-max {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.3rem;
        color: #8aaccc;
    }

    /* ── Botones ── */
    .stButton > button {
        background: #1a6abf !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 0.08em !important;
        padding: 0.55rem 1.2rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }

    /* ── Tubos wrapper ── */
    .au-tubos-wrapper {
        display: flex;
        justify-content: center;
        margin: 1.2rem 0 1.5rem 0;
    }

    .stButton > button, .stButton > button p, .stButton > button div, .stButton > button span {
        color: #ffffff !important;
    }
                
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "pantalla": "inicio",
        "expediente": None,
        "sesion": None,
        "pregunta_idx": 0,
        "respuestas": [],
        "retroalimentaciones": [],
        "mostrar_retro": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def campo_html(key, val):
    return f"""
    <div class="au-field-row">
        <span class="au-field-key">{key}</span>
        <span class="au-field-val">{val}</span>
    </div>"""


def tubos_svg(nivel):
    """SVG de los 3 tubos de riesgo."""
    if nivel == "Riesgo Alto":
        estados = [True, True, True]
    elif nivel == "Riesgo Medio":
        estados = [True, True, False]
    else:  # Riesgo Bajo
        estados = [True, False, False]

    alturas   = [45, 75, 110]
    etiquetas = ["BAJO", "MEDIO", "ALTO"]
    COLOR_LLENO = "#1a6abf"
    COLOR_BORDE = "#1a6abf"
    W      = 60
    GAP    = 28
    MAX_H  = 130
    TOTAL_W = 3 * W + 2 * GAP + 40

    partes = [f'<svg width="{TOTAL_W}" height="{MAX_H + 28}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(3):
        x     = 20 + i * (W + GAP)
        y_top = MAX_H - alturas[i]
        fill  = COLOR_LLENO if estados[i] else "white"
        partes.append(
            f'<rect x="{x}" y="{y_top}" width="{W}" height="{alturas[i]}" '
            f'rx="22" ry="22" fill="{fill}" stroke="{COLOR_BORDE}" stroke-width="2"/>'
        )
        partes.append(
            f'<text x="{x + W // 2}" y="{MAX_H + 22}" text-anchor="middle" '
            f'font-family="Share Tech Mono, monospace" font-size="13" '
            f'fill="{COLOR_BORDE}" letter-spacing="1">{etiquetas[i]}</text>'
        )
    partes.append("</svg>")

    svg = "".join(partes)
    return f'<div class="au-tubos-wrapper">{svg}</div>'


def barra_progreso_html(actual, total):
    pct = int((actual / total) * 100)
    return (
        f'<div class="au-progress-bg">'
        f'<div class="au-progress-fill" style="width:{pct}%;"></div>'
        f'</div>'
    )


# ─────────────────────────────────────────────
# PANTALLA 1: INICIO
# ─────────────────────────────────────────────

def pantalla_inicio():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown(
            '<div style="text-align:center; padding: 2rem 0 1rem;">'
            '<span class="au-label">módulo 4 · criptografía y seguridad</span>'
            '<div class="au-title">Simulador de<br>Auditoría Académica</div>'
            '<p style="color:#5a7a9a; margin-bottom:1.5rem;">'
            'Evalúa si un expediente estudiantil cumple con los<br>'
            'principios de seguridad de la información.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="au-card" style="text-align:left;">'
            '<span class="au-label" style="margin-bottom:0.8rem;">¿cómo funciona?</span>'
            '<div style="font-size:0.90rem; color:#4a6a8a; line-height:2;">'
            '◈ Se genera un expediente ficticio<br>'
            '◈ Respondes 4 preguntas de control (P1–P4)<br>'
            '◈ Recibes retroalimentación por cada respuesta<br>'
            '◈ Obtienes el nivel de riesgo del expediente'
            '</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("▶  INICIAR AUDITORÍA", width="stretch"):
            st.session_state.expediente   = generar_expediente()
            st.session_state.sesion       = obtener_sesion_preguntas()
            st.session_state.pregunta_idx = 0
            st.session_state.respuestas   = []
            st.session_state.retroalimentaciones = []
            st.session_state.mostrar_retro = False
            st.session_state.pantalla = "expediente"
            st.rerun()


# ─────────────────────────────────────────────
# PANTALLA 2: EXPEDIENTE
# ─────────────────────────────────────────────

def pantalla_expediente():
    exp = st.session_state.expediente
    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown(
            '<span class="au-label">expediente académico generado</span>'
            '<div class="au-title" style="font-size:1.6rem; margin-bottom:1rem;">'
            'Revisa el expediente antes de auditar</div>',
            unsafe_allow_html=True,
        )
        filas = (
            campo_html("NOMBRE",   exp["nombre"])  +
            campo_html("CARRERA",  exp["carrera"]) +
            campo_html("SEMESTRE", exp["semestre"]) +
            campo_html("DOCENTE",  exp["docente"])
        )
        st.markdown(f'<div class="au-card">{filas}</div>', unsafe_allow_html=True)

        pills = "".join([
            f'<span class="au-pill">{mat} <span class="au-pill-num">{nota}</span></span>'
            for mat, nota in exp["notas"].items()
        ])
        st.markdown(
            f'<div class="au-card">'
            f'<span class="au-label" style="margin-bottom:0.6rem;">calificaciones</span>'
            f'{pills}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INICIAR PREGUNTAS DE CONTROL", width="stretch"):
            st.session_state.pantalla = "preguntas"
            st.rerun()


# ─────────────────────────────────────────────
# PANTALLA 3: PREGUNTAS
# ─────────────────────────────────────────────

def pantalla_preguntas():
    idx    = st.session_state.pregunta_idx
    sesion = st.session_state.sesion
    total  = len(sesion)

    if idx >= total:
        st.session_state.pantalla = "veredicto"
        st.rerun()
        return

    pregunta = sesion[idx]
    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown(
            f'<span class="au-label">pregunta {idx + 1} de {total}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(barra_progreso_html(idx, total), unsafe_allow_html=True)
        st.markdown(
            f'<div class="au-pregunta">'
            f'<span class="au-badge">{pregunta["principio"]}</span><br>'
            f'{pregunta["texto"]}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.mostrar_retro:
            retro = st.session_state.retroalimentaciones[-1]
            clase = "au-retro-ok" if "✅" in retro else "au-retro-warn"
            st.markdown(f'<div class="{clase}">{retro}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            label = "SIGUIENTE PREGUNTA ▶" if idx + 1 < total else "VER VEREDICTO FINAL ▶"
            if st.button(label, width="stretch"):
                st.session_state.pregunta_idx += 1
                st.session_state.mostrar_retro = False
                st.rerun()
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✔  SÍ", width="stretch"):
                    _registrar_respuesta(pregunta, True)
            with c2:
                if st.button("✘  NO", width="stretch"):
                    _registrar_respuesta(pregunta, False)


def _registrar_respuesta(pregunta, respuesta: bool):
    retro = obtener_retroalimentacion(
        pregunta["principio"], pregunta["articulo"], respuesta)
    st.session_state.respuestas.append(respuesta)
    st.session_state.retroalimentaciones.append(retro)
    st.session_state.mostrar_retro = True
    st.rerun()


# ─────────────────────────────────────────────
# PANTALLA 4: VEREDICTO
# ─────────────────────────────────────────────

def pantalla_veredicto():
    resultado = calcular_puntaje(st.session_state.respuestas)
    nivel  = resultado["nivel"]
    sesion = st.session_state.sesion

    if nivel == "Riesgo Alto":
        color_clase, icono = "au-color-rojo",  "🔴"
    elif nivel == "Riesgo Medio":
        color_clase, icono = "au-color-ambar", "🟡"
    else:
        color_clase, icono = "au-color-verde", "🟢"

    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown(
            f'<div style="text-align:center; padding: 1rem 0 0.5rem;">'
            f'<span class="au-label" style="font-size:1.1rem; letter-spacing:0.2em;">resultado de auditoría</span>'
            f'<div class="au-veredicto-nivel {color_clase}">{resultado["estado"]}</div>'
            f'<div style="font-family:Share Tech Mono,monospace; font-size:0.99rem; color:#1a6abf; letter-spacing:0.1em; margin-top:0.3rem;">RIESGO</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(tubos_svg(nivel), unsafe_allow_html=True)

        st.markdown(
            f'<div class="au-card" style="text-align:center;">'
            f'<span class="au-label">puntaje obtenido</span>'
            f'<div><span class="au-puntaje-num">{resultado["puntaje"]}</span>'
            f'<span class="au-puntaje-max"> / {resultado["maximo"]}</span></div>'
            f'<div style="font-size:0.85rem; color:#5a7a9a; margin-top:0.3rem;">'
            f'{resultado["correctas"]} de 4 controles implementados</div>'
            f'<div style="font-size:0.88rem; color:#3a5a7a; margin-top:0.5rem;">'
            f'{resultado["descripcion"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<span class="au-label" style="margin-top:0.5rem; margin-bottom:0.4rem;">'
            'resumen de controles</span>',
            unsafe_allow_html=True,
        )

        for pregunta, retro in zip(sesion, st.session_state.retroalimentaciones):
            clase = "au-retro-ok" if "✅" in retro else "au-retro-warn"
            st.markdown(
                f'<div class="{clase}">'
                f'<span style="font-family:\'Share Tech Mono\',monospace; font-size:0.68rem; opacity:0.6; margin-right:6px;">'
                f'{pregunta["clave"]} · {pregunta["principio"]}</span><br>'
                f'{retro}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄  NUEVA AUDITORÍA", width="stretch"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA — llamado desde app.py
# ─────────────────────────────────────────────

def mostrar():
    init_state()
    inyectar_estilos()

    pantalla = st.session_state.pantalla

    if pantalla == "inicio":
        pantalla_inicio()
    elif pantalla == "expediente":
        pantalla_expediente()
    elif pantalla == "preguntas":
        pantalla_preguntas()
    elif pantalla == "veredicto":
        pantalla_veredicto()