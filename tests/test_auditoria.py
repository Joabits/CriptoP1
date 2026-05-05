import pytest
from cripto_grupo_f.auditoria import (
    generar_expediente,
    obtener_pregunta,
    obtener_sesion_preguntas,
    obtener_retroalimentacion,
    calcular_puntaje,
    determinar_nivel,
)

# ─────────────────────────────────────────────
# PRUEBAS: GENERADOR DE EXPEDIENTE
# ─────────────────────────────────────────────

def test_expediente_tiene_campos_correctos():
    """El expediente debe tener todos los campos requeridos."""
    expediente = generar_expediente()
    assert "nombre" in expediente
    assert "carrera" in expediente
    assert "semestre" in expediente
    assert "docente" in expediente
    assert "notas" in expediente

def test_expediente_tiene_4_materias():
    """El expediente debe tener exactamente 4 materias."""
    expediente = generar_expediente()
    assert len(expediente["notas"]) == 4

def test_expediente_notas_en_rango():
    """Las notas deben estar entre 51 y 100."""
    expediente = generar_expediente()
    for nota in expediente["notas"].values():
        assert 51 <= nota <= 100

def test_expediente_es_aleatorio():
    """Dos expedientes generados no deben ser idénticos siempre."""
    resultados = set()
    for _ in range(10):
        expediente = generar_expediente()
        resultados.add(expediente["nombre"])
    # Con 10 intentos y 6 nombres posibles, debe haber más de 1 nombre distinto
    assert len(resultados) > 1


# ─────────────────────────────────────────────
# PRUEBAS: BANCO DE PREGUNTAS
# ─────────────────────────────────────────────

def test_pregunta_tiene_campos_correctos():
    """Cada pregunta debe tener clave, texto, principio y articulo."""
    for clave in ["P1", "P2", "P3", "P4"]:
        pregunta = obtener_pregunta(clave)
        assert "clave" in pregunta
        assert "texto" in pregunta
        assert "principio" in pregunta
        assert "articulo" in pregunta

def test_pregunta_clave_correcta():
    """La clave devuelta debe coincidir con la solicitada."""
    for clave in ["P1", "P2", "P3", "P4"]:
        pregunta = obtener_pregunta(clave)
        assert pregunta["clave"] == clave

def test_sesion_tiene_4_preguntas():
    """Una sesión completa debe tener exactamente 4 preguntas."""
    sesion = obtener_sesion_preguntas()
    assert len(sesion) == 4

def test_sesion_tiene_todas_las_claves():
    """La sesión debe incluir P1, P2, P3 y P4."""
    sesion = obtener_sesion_preguntas()
    claves = [p["clave"] for p in sesion]
    assert "P1" in claves
    assert "P2" in claves
    assert "P3" in claves
    assert "P4" in claves

def test_preguntas_son_aleatorias():
    """P4 tiene 4 opciones, en 20 intentos debe aparecer más de 1 distinta."""
    textos = set()
    for _ in range(20):
        pregunta = obtener_pregunta("P4")
        textos.add(pregunta["texto"])
    assert len(textos) > 1


# ─────────────────────────────────────────────
# PRUEBAS: RETROALIMENTACIÓN
# ─────────────────────────────────────────────

def test_retroalimentacion_respuesta_si():
    """Respuesta Sí debe devolver mensaje positivo."""
    mensaje = obtener_retroalimentacion("Confidencialidad", "la", True)
    assert "✅" in mensaje
    assert "Confidencialidad" in mensaje

def test_retroalimentacion_respuesta_no():
    """Respuesta No debe devolver mensaje de riesgo."""
    mensaje = obtener_retroalimentacion("Integridad", "la", False)
    assert "⚠️" in mensaje
    assert "Integridad" in mensaje

def test_retroalimentacion_articulo_la():
    """Con artículo 'la' el verbo debe ser 'comprometida'."""
    mensaje = obtener_retroalimentacion("Confidencialidad", "la", False)
    assert "comprometida" in mensaje

def test_retroalimentacion_articulo_el():
    """Con artículo 'el' el verbo debe ser 'comprometido'."""
    mensaje = obtener_retroalimentacion("No Repudio", "el", False)
    assert "comprometido" in mensaje


# ─────────────────────────────────────────────
# PRUEBAS: MOTOR DE EVALUACIÓN — PUNTAJES
# ─────────────────────────────────────────────

def test_puntaje_4_correctas():
    """4 Sí → Puntaje 12 → Riesgo Bajo."""
    resultado = calcular_puntaje([True, True, True, True])
    assert resultado["puntaje"] == 12
    assert resultado["nivel"] == "Riesgo Bajo"
    assert resultado["estado"] == "Información Segura"

def test_puntaje_3_correctas():
    """3 Sí → Puntaje 9 → Riesgo Medio."""
    resultado = calcular_puntaje([True, True, True, False])
    assert resultado["puntaje"] == 9
    assert resultado["nivel"] == "Riesgo Medio"
    assert resultado["estado"] == "Información con seguridad media"

def test_puntaje_2_correctas():
    """2 Sí → Puntaje 6 → Riesgo Medio."""
    resultado = calcular_puntaje([True, True, False, False])
    assert resultado["puntaje"] == 6
    assert resultado["nivel"] == "Riesgo Medio"
    assert resultado["estado"] == "Información con seguridad media"

def test_puntaje_1_correcta():
    """1 Sí → Puntaje 3 → Riesgo Alto."""
    resultado = calcular_puntaje([True, False, False, False])
    assert resultado["puntaje"] == 3
    assert resultado["nivel"] == "Riesgo Alto"
    assert resultado["estado"] == "Información Insegura"

def test_puntaje_0_correctas():
    """0 Sí → Puntaje 0 → Riesgo Alto."""
    resultado = calcular_puntaje([False, False, False, False])
    assert resultado["puntaje"] == 0
    assert resultado["nivel"] == "Riesgo Alto"
    assert resultado["estado"] == "Información Insegura"

def test_puntaje_maximo_es_12():
    """El puntaje máximo siempre debe ser 12."""
    resultado = calcular_puntaje([True, True, True, True])
    assert resultado["maximo"] == 12

def test_contador_correctas():
    """El contador de correctas debe ser preciso."""
    resultado = calcular_puntaje([True, False, True, False])
    assert resultado["correctas"] == 2