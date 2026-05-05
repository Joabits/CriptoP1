import random

# ─────────────────────────────────────────────
# BANCO DE PREGUNTAS
# ─────────────────────────────────────────────

PREGUNTAS = {
    "P1": {
        "opciones": [
            {
                "texto": "¿El expediente del estudiante es accesible únicamente por personal docente y administrativo autorizado?",
                "principio": "Confidencialidad",
                "articulo": "la"
            },
            {
                "texto": "¿Las notas y datos personales del estudiante se envían por canales seguros?",
                "principio": "Confidencialidad",
                "articulo": "la"
            },
        ],
    },
    "P2": {
        "opciones": [
            {
                "texto": "¿El sistema detecta si una calificación fue modificada después de ser registrada por el docente?",
                "principio": "Integridad",
                "articulo": "la"
            },
            {
                "texto": "¿Si un administrativo comete un error al cargar una nota, el sistema exige un proceso formal de corrección con aprobación, en lugar de permitir edición directa?",
                "principio": "Integridad",
                "articulo": "la"
            },
        ],
    },
    "P3": {
        "opciones": [
            {
                "texto": "¿Durante períodos críticos (inscripciones, cierre de semestre), el sistema garantiza que los expedientes estarán disponibles sin interrupciones?",
                "principio": "Disponibilidad",
                "articulo": "la"
            },
            {
                "texto": "¿Si el sistema principal falla, existe un procedimiento alternativo (sistema secundario o acceso offline) para consultar los expedientes urgentes?",
                "principio": "Disponibilidad",
                "articulo": "la"
            },
        ],
    },
    "P4": {
        "opciones": [
            {
                "texto": "¿El sistema verifica la identidad del usuario antes de mostrar un expediente, mediante credenciales únicas (usuario + contraseña, o factor doble)?",
                "principio": "Autenticación",
                "articulo": "la"
            },
            {
                "texto": "¿Cuando un docente registra o modifica una calificación, el sistema guarda un registro vinculado a su identidad que impide que luego niegue haber realizado esa acción?",
                "principio": "No Repudio",
                "articulo": "el"
            },
            {
                "texto": "¿El sistema mantiene un historial completo de quién accedió, consultó o modificó cada expediente, con fecha y hora, auditable en cualquier momento?",
                "principio": "Trazabilidad",
                "articulo": "la"
            },
        ],
    },
}


# ─────────────────────────────────────────────
# GENERADOR DE EXPEDIENTE FICTICIO
# ─────────────────────────────────────────────

NOMBRES = ["Juan Pérez", "María López", "Carlos Ríos", "Ana Torrez", "Luis Mamani", "Sofía Gutiérrez"]
CARRERAS = ["Ingeniería en Sistemas", "Ingeniería Informática", "Ingeniería en Redes"]
SEMESTRES = ["1er", "2do", "3er", "4to", "5to", "6to", "7mo", "8vo", "9no"]
MATERIAS = ["Lenguajes Formales", "Redes II", "Criptografía y Seguridad", "Programación Ensamblador", "Base de Datos II", "Física I", "Programación Gráfica", "Programación II", "Estructura de datos I", "Inteligencia Artificial"]
DOCENTES = ["Ing. Vargas", "Ing. Peinado", "Ing. Vallet", "Lic. Miranda", "Ing. Zuñiga", "Ing. Shirley", "Ing. Cabello", "Ing. Mollo"]


def generar_expediente():
    """
    Genera un expediente académico ficticio con datos aleatorios.
    Retorna un diccionario con los datos del estudiante.
    """
    materias_seleccionadas = random.sample(MATERIAS, 4)
    notas = {materia: random.randint(51, 100) for materia in materias_seleccionadas}

    expediente = {
        "nombre": random.choice(NOMBRES),
        "carrera": random.choice(CARRERAS),
        "semestre": random.choice(SEMESTRES) + " semestre",
        "docente": random.choice(DOCENTES),
        "notas": notas,
    }
    return expediente


# ─────────────────────────────────────────────
# BANCO DE PREGUNTAS — SELECCIÓN ALEATORIA
# ─────────────────────────────────────────────

def obtener_pregunta(clave):
    """
    Recibe la clave de la pregunta (P1, P2, P3 o P4).
    Retorna un diccionario con el principio y la pregunta seleccionada aleatoriamente.
    """
    opcion = random.choice(PREGUNTAS[clave]["opciones"])
    return {
        "clave": clave,
        "texto": opcion["texto"],
        "principio": opcion["principio"],   # para retroalimentación
        "articulo": opcion["articulo"],     # para retroalimentación
    }

def obtener_sesion_preguntas():
    """
    Genera una sesión completa de 4 preguntas (una por cada P).
    Retorna una lista de 4 diccionarios de preguntas.
    """
    return [obtener_pregunta(clave) for clave in ["P1", "P2", "P3", "P4"]]


# ─────────────────────────────────────────────
# RETROALIMENTACIÓN POR PREGUNTA
# ─────────────────────────────────────────────

def obtener_retroalimentacion(principio, articulo, respuesta):
    """
    Recibe el principio de seguridad y la respuesta del usuario (True=Sí, False=No).
    Retorna el mensaje de retroalimentación correspondiente.
    """
    verbo = "comprometida" if articulo == "la" else "comprometido"
    if respuesta:
        return f"✅ Correcto. Este control protege {articulo} {principio} del expediente."
    else:
        return f"⚠️ Riesgo detectado. Sin este control, {articulo} {principio} del expediente está {verbo}."


# ─────────────────────────────────────────────
# MOTOR DE EVALUACIÓN
# ─────────────────────────────────────────────

PUNTOS_POR_RESPUESTA = 3  # Sí = 3 puntos, No = 0 puntos


def calcular_puntaje(respuestas):
    """
    Recibe una lista de 4 booleanos (True=Sí, False=No).
    Retorna un diccionario con el puntaje total y el nivel de riesgo.
    """
    puntaje = sum(PUNTOS_POR_RESPUESTA for r in respuestas if r)
    nivel = determinar_nivel(puntaje)
    return {
        "puntaje": puntaje,
        "maximo": 12,
        "correctas": sum(1 for r in respuestas if r),
        "nivel": nivel["nombre"],
        "estado": nivel["estado"],
        "descripcion": nivel["descripcion"],
    }




def determinar_nivel(puntaje):
    """
    Recibe el puntaje total y retorna el nivel de riesgo correspondiente.
    """
    if puntaje >= 10:
        return {
            "nombre": "Riesgo Bajo",
            "estado": "Información Segura",
            "descripcion": "El expediente presenta controles de seguridad sólidos.",
        }
    elif puntaje >= 5:
        return {
            "nombre": "Riesgo Medio",
            "estado": "Información con seguridad media",
            "descripcion": "El expediente tiene vulnerabilidades que deben corregirse.",
        }
    else:
        return {
            "nombre": "Riesgo Alto",
            "estado": "Información Insegura",
            "descripcion": "El expediente está comprometido. Se requieren medidas urgentes.",
        }


# ─────────────────────────────────────────────
# PRUEBAS RÁPIDAS (solo para desarrollo)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=== EXPEDIENTE GENERADO ===")
    expediente = generar_expediente()
    for clave, valor in expediente.items():
        print(f"  {clave}: {valor}")

    print("\n=== PREGUNTAS DE LA SESIÓN ===")
    sesion = obtener_sesion_preguntas()
    for i, pregunta in enumerate(sesion, 1):
        print(f"  {pregunta['clave']} ({pregunta['principio']}): {pregunta['texto']}")

    print("\n=== RETROALIMENTACIÓN ===")
    print(" ", obtener_retroalimentacion("Confidencialidad", "la", True))
    print(" ", obtener_retroalimentacion("Integridad", "la", False))

    print("\n=== PUNTAJES POSIBLES ===")
    casos = [
        [True, True, True, True],
        [True, True, True, False],
        [True, True, False, False],
        [True, False, False, False],
        [False, False, False, False],
    ]
    for caso in casos:
        resultado = calcular_puntaje(caso)
        print(f"  {resultado['correctas']}/4 correctas → Puntaje {resultado['puntaje']} → {resultado['nivel']} → {resultado['estado']}")
