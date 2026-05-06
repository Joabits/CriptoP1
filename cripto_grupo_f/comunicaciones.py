"""Comparacion entre sistemas aislados e interconectados."""

from __future__ import annotations


SISTEMAS: dict[str, dict] = {

    "aislado": {
        "nombre": "Sistema Aislado (StandAlone)",
        "descripcion": (
            "Sistema que opera sin conexion a redes externas."
            "El acceso fisico es el unico vector de entrada."
        ),
        "acceso": "Exclusivamente fisico y local",
        "amenaza_principal": "Acceso fisico no autorizado o robo del dispositivo",
        "ejemplos": [
            "Computador sin red en sala de servidores con llave",
            "USB con datos criticos nunca conectado a Internet",
            "Consola de control industrial aislada",
        ],
        "pilares_en_riesgo": ["Disponibilidad (acceso fisico)"],
    },

    "interconectado": {
        "nombre": "Sistema Interconectado (Networked)",
        "descripcion": (
            "Sistema que se comunica con otros a traves de un canal. "
            "El canal mismo se convierte en superficie de ataque."
        ),
        "acceso": "Remoto a traves de red (local, internet, etc)",
        "amenaza_principal": "Intercepcion, modificacion o suplantacion en el canal",
        "ejemplos": [
            "Aplicacion bancaria movil",
            "Sistema academico de notas en linea",
            "Correo electronico",
        ],
        "pilares_en_riesgo": [
            "Confidencialidad (cifrado del canal)",
            "Integridad (verificacion de datos en transito)",
            "Autenticidad (verificar identidad del emisor/receptor)",
        ],
    },
}


COMPARATIVA: list[dict[str, str]] = [
    {
        "criterio": "Superficie de ataque",
        "sistema_aislado": "Minima: solo el acceso fisico",
        "sistema_interconectado": "Alta: red, usuarios remotos, servidores, APIs y canales",
        "por_que_importa": "A mayor superficie, mas formas de atacar",
    },
    {
        "criterio": "Confidencialidad",
        "sistema_aislado": "Depende del control fisico del lugar",
        "sistema_interconectado": "Depende del cifrado, autenticacion y gestion de claves",
        "por_que_importa": "Sin cifrado, cualquiera en el canal puede leer",
    },
    {
        "criterio": "Integridad",
        "sistema_aislado": "Solo usuarios locales pueden alterar",
        "sistema_interconectado": "Riesgo de alteracion durante la transmision",
        "por_que_importa": "El mensaje puede llegar modificado sin que nadie lo note",
    },
    {
        "criterio": "Autenticidad",
        "sistema_aislado": "Se verifica por presencia fisica",
        "sistema_interconectado": "Requiere mecanismos de autenticacion digitales",
        "por_que_importa": "Un atacante puede hacerse pasar por el emisor",
    },
    {
        "criterio": "Disponibilidad",
        "sistema_aislado": "Menos dependencia de la red",
        "sistema_interconectado": "Expuesto a fallas de red, DoS y servicios externos",
        "por_que_importa": "Un atacante puede bloquear el servicio completamente",
    },
    {
        "criterio": "Deteccion de ataques",
        "sistema_aislado": "Facil: hay huellas fisicas visibles",
        "sistema_interconectado": "Dificil: un atacante puede actuar sin dejar rastros",
        "por_que_importa": "La invisibilidad del atacante remoto lo hace mas peligroso",
    },
]


def describir_sistema(tipo: str) -> dict:
    """Retorna el diccionario con la descripcion completa de un tipo de sistema.

    Parametros:
        tipo: "aislado" o "interconectado"

    Retorna:
        dict con las propiedades del sistema.

    Lanza:
        ValueError si el tipo no existe en SISTEMAS.
    """
    tipo = tipo.strip().lower()

    if tipo not in SISTEMAS:
        tipos_validos = list(SISTEMAS.keys())
        raise ValueError(
            f"Tipo '{tipo}' no reconocido. Tipos validos: {tipos_validos}"
        )
    
    return SISTEMAS[tipo].copy()


def obtener_comparativa() -> list[dict[str, str]]:
    return COMPARATIVA.copy()


VECTORES_POR_SISTEMA: dict[str, list[dict]] = {
    "aislado": [
        {
            "vector": "Acceso fisico directo",
            "descripcion": "Alguien esta frente al equipo o lo roba",
            "riesgo": "Alto",
            "puntos": 3,
        },
        {
            "vector": "Dispositivo USB o extraible",
            "descripcion": "Conectar un USB infectado o copiar datos en uno",
            "riesgo": "Medio",
            "puntos": 2,
        },
        {
            "vector": "Insider con acceso legitimo",
            "descripcion": "Un empleado autorizado que abusa de su acceso",
            "riesgo": "Medio",
            "puntos": 2,
        },
    ],

    "interconectado": [
        {
            "vector": "Acceso fisico directo",
            "descripcion": "Alguien esta frente al equipo o lo roba",
            "riesgo": "Alto",
            "puntos": 3,
        },
        {
            "vector": "Canal de comunicacion (red)",
            "descripcion": "El camino que recorre el mensaje entre emisor y receptor",
            "riesgo": "Alto",
            "puntos": 3,
        },
        {
            "vector": "Puerto de red expuesto",
            "descripcion": "Conexion TCP/IP abierta accesible desde fuera",
            "riesgo": "Alto",
            "puntos": 3,
        },
        {
            "vector": "Credenciales de acceso",
            "descripcion": "Usuario y contrasena como unica barrera de entrada",
            "riesgo": "Alto",
            "puntos": 3,
        },
        {
            "vector": "API o servicio expuesto",
            "descripcion": "Endpoint accesible desde Internet sin restriccion",
            "riesgo": "Medio",
            "puntos": 2,
        },
        {
            "vector": "Dispositivo USB o extraible",
            "descripcion": "Conectar un USB infectado o copiar datos en uno",
            "riesgo": "Medio",
            "puntos": 2,
        },
        {
            "vector": "Insider con acceso legitimo",
            "descripcion": "Un empleado autorizado que abusa de su acceso",
            "riesgo": "Medio",
            "puntos": 2,
        },
    ]
}


def calcular_superficie_ataque(tipo: str) -> dict:
    """Calcula el puntaje de superficie de ataque de un tipo de sistema.

    Parametros:
        tipo: "aislado" o "interconectado"

    Retorna:
        dict con:
            - tipo: el tipo de sistema evaluado
            - vectores: lista de vectores de amenaza
            - puntaje_total: suma de puntos de todos los vectores
            - nivel: clasificacion cualitativa ("Bajo", "Moderado", "Alto", "Critico")
    """
    tipo = tipo.strip().lower()

    if tipo not in VECTORES_POR_SISTEMA:
        raise ValueError(
            f"Tipo '{tipo}' no reconocido. Tipos validos: {list(VECTORES_POR_SISTEMA.keys())}"
        )
    
    vectores = VECTORES_POR_SISTEMA[tipo]
    puntaje_total = sum(v["puntos"] for v in vectores)

    if puntaje_total <= 5:
        nivel = "Bajo"
        resumen = "Superficie reducida. Las amenazas son principalmente fisicas y locales."
    elif puntaje_total <= 10:
        nivel = "Moderado"
        resumen = "Superficie considerable. Se requieren controles tanto fisicos como logicos."
    elif puntaje_total <= 15:
        nivel = "Alto"
        resumen = "Superficie amplia. El canal de comunicacion expone multiples vectores remotos."
    else:
        nivel = "Critico"
        resumen = "Superficie maxima. Cada componente conectado es un vector potencial de ataque."

    return {
        "tipo": tipo,
        "vectores": vectores,
        "puntaje_total": puntaje_total,
        "nivel": nivel,
    }


AMENAZAS_CANAL: list[dict[str, str]] = [
    {
        "nombre": "Intercepcion (Eavesdropping)",
        "tipo_ataque": "Pasivo",
        "descripcion": "El atacante copia el mensaje mientras viaja por el canal sin modificarlo. El emisor y receptor no lo detectan.",
        "ejemplo": "Captura de trafico en una red WiFi publica sin cifrar",
        "pilar_violado": "Confidencialidad",
        "contramedida":  "Cifrar el canal: aunque el atacante copie, no puede leer",
    },
    {
        "nombre": "Modificacion (Tampering / MITM)",
        "tipo_ataque": "Activo",
        "descripcion": (
            "El atacante intercepta el mensaje, lo altera y lo reenvía. "
            "El receptor recibe una version falsa creyendo que es autentica."
        ),
        "ejemplo": "Cambiar 'Nota: 9.5' por 'Nota: 3.0' antes de que llegue al sistema",
        "pilar_violado": "Integridad",
        "contramedida": "Verificar que el mensaje no fue alterado (firma o hash)",
    },
    {
        "nombre": "Suplantacion (Spoofing)",
        "tipo_ataque": "Activo",
        "descripcion": (
            "El atacante se hace pasar por el emisor legitimo. "
            "El receptor cree que habla con quien debe, pero no."
        ),
        "ejemplo": "Enviar mensajes al servidor como si se fuera el docente autorizado",
        "pilar_violado": "Autenticidad",
        "contramedida": "Verificar la identidad del emisor antes de aceptar el mensaje",
    },
]


def filtrar_amenazas_por_tipo(tipo_ataque: str) -> list[dict[str, str]]:
    """Retorna solo las amenazas del tipo de ataque indicado.

    Parametros:
        tipo_ataque: "Pasivo" o "Activo" 

    Retorna:
        Lista de amenazas filtradas. Puede ser una lista vacia si no hay coincidencias.
    """
    tipo_ataque = tipo_ataque.strip().capitalize()

    tipos_validos = {"Pasivo", "Activo"}
    if tipo_ataque not in tipos_validos:
        raise ValueError(
            f"Tipo '{tipo_ataque}' no reconocido. Tipos validos: {sorted(tipos_validos)}"
        )

    return [a for a in AMENAZAS_CANAL if a["tipo_ataque"] == tipo_ataque]


def obtener_amenazas_canal() -> list[dict[str, str]]:
    return AMENAZAS_CANAL.copy()


PESOS_CIA: dict[str, int] = {
    "confidencialidad": 40,
    "autenticidad": 35,
    "integridad": 25,
}



def evaluar_canal(cifrado: bool, autenticado: bool, integridad: bool) -> dict:
    """Evalua el nivel de seguridad de un canal usando la triada CIA ponderada.

    Cada pilar tiene un peso distinto que refleja su importancia en el canal:
        - confidencialidad (cifrado):  40 puntos
        - autenticidad (autenticado):  35 puntos
        - integridad (integridad):     25 puntos
    Puntaje total posible: 100 puntos.

    Parametros:
        cifrado:     True si el canal usa cifrado (confidencialidad)
        autenticado: True si se verifica la identidad del emisor (autenticidad)
        integridad:  True si se verifica que el mensaje no fue alterado (integridad)

    Retorna:
        dict con:
            - puntaje:           puntaje total obtenido (0-100)
            - nivel:             "Critico", "Inseguro", "Parcialmente seguro" o "Seguro"
            - pilares_activos:   lista de pilares CIA que estan activos
            - pilares_faltantes: lista de dicts con diagnostico de cada pilar ausente
            - diagnostico:       texto explicativo del estado general del canal
    """

    puntaje = 0
    pilares_activos = []
    pilares_faltantes = []

    if cifrado:
        puntaje += PESOS_CIA["confidencialidad"]
        pilares_activos.append("Confidencialidad")
    else:
        pilares_faltantes.append({
            "pilar": "Confidencialidad",
            "peso_perdido": PESOS_CIA["confidencialidad"],
            "consecuencia": "El atacante puede leer el contenido del mensaje en texto plano",
            "amenaza_habilitada": "Intercepcion (Eavesdropping)",
        })

    if autenticado:
        puntaje += PESOS_CIA["autenticidad"]
        pilares_activos.append("Autenticidad")
    else:
        pilares_faltantes.append({
            "pilar": "Autenticidad",
            "peso_perdido": PESOS_CIA["autenticidad"],
            "consecuencia": "No es posible verificar quien envio el mensaje",
            "amenaza_habilitada": "Suplantacion (Spoofing) y Repeticion (Replay)",
        })

    if integridad:
        puntaje += PESOS_CIA["integridad"]
        pilares_activos.append("Integridad")
    else:
        pilares_faltantes.append({
            "pilar": "Integridad",
            "peso_perdido": PESOS_CIA["integridad"],
            "consecuencia": "El mensaje puede haber sido alterado en transito sin que nadie lo detecte",
            "amenaza_habilitada": "Modificacion (Tampering / MITM)",
        })

    if puntaje >= 85:
        nivel = "Seguro"
        diagnostico = (
            "El canal cumple los tres pilares CIA. "
            "Las amenazas de intercepcion, modificacion y suplantacion estan controladas."
        )
    elif puntaje >= 65:
        nivel = "Parcialmente Seguro"
        diagnostico = (
            "El canal tiene controles importantes pero presenta huecos. "
            "Un atacante puede explotar los pilares faltantes."
        )
    elif puntaje >= 40:
        nivel = "Inseguro"
        diagnostico = (
            "El canal carece de controles fundamentales. "
            "La mayoria de las amenazas del canal estan activas."
        )
    else:
        nivel = "Critico"
        diagnostico = (
            "El canal no tiene protecciones basicas. "
            "Cualquier atacante en la red puede interceptar, modificar o suplantar mensajes."
        )

    return {
        "puntaje": puntaje,
        "nivel": nivel,
        "pilares_activos": pilares_activos,
        "pilares_faltantes": pilares_faltantes,
        "diagnostico": diagnostico,
    }


def _cifrar_visual(texto: str) -> str:
    """Aplica ROT-3 al texto para representar visualmente un cifrado.

    No es criptografia real — es una transformacion didactica que muestra que el contenido es ilegible sin conocer el algoritmo inverso.
    Solo desplaza letras; numeros, espacios y signos no cambian.
    """
    resultado = []
    for caracter in texto:
        if caracter.isalpha():
            base = ord("A") if caracter.isupper() else ord("a")
            desplazado = (ord(caracter) - base + 3) % 26 + base
            resultado.append(chr(desplazado))
        else:
            resultado.append(caracter)
        
    return "".join(resultado)


def _modificar_como_atacante(mensaje: str) -> str:
    """Simula la modificacion del mensaje por un atacante activo (MITM).

    Reemplaza la ultima palabra por '[ALTERADO]' para representar que
    el contenido fue cambiado antes de llegar al receptor.
    """
    palabras = mensaje.split()
    if palabras:
        palabras[-1] = "[ALTERADO]"
    return " ".join(palabras)
    

def simular_transmision(
    mensaje: str, 
    canal_cifrado: bool,
    tipo_ataque: str = "ninguno", 
) -> dict:
    """Simula el recorrido de un mensaje por el canal y genera un log de eventos.

    Parametros:
        mensaje:       texto que el emisor quiere enviar al receptor
        canal_cifrado: True si el canal aplica cifrado al mensaje en transito
        tipo_ataque:   escenario de ataque — "ninguno", "pasivo" o "activo"
                       - "ninguno": canal limpio, sin atacante
                       - "pasivo":  el atacante copia el mensaje pero no lo modifica
                       - "activo":  el atacante intercepta y altera el mensaje (MITM)

    Retorna:
        dict con:
            - escenario:        descripcion del escenario simulado
            - mensaje_original: el mensaje que envio el emisor
            - mensaje_recibido: lo que recibio el receptor (puede diferir si hubo ataque activo)
            - canal:            "Cifrado" o "Sin cifrar"
            - tipo_ataque:      el escenario de ataque normalizado
            - log:              lista de eventos ordenados, cada uno con:
                                    paso, etapa, evento, contenido_visible
            - advertencia:      texto de alerta si el canal tiene vulnerabilidades

    Lanza:
        ValueError si tipo_ataque no es "ninguno", "pasivo" ni "activo".
    """
    tipo_ataque = tipo_ataque.strip().lower()
    tipos_validos = {"ninguno", "pasivo", "activo"}
    if tipo_ataque not in tipos_validos:
        raise ValueError(
            f"tipo_ataque '{tipo_ataque}' no reconocido. "
            f"Valores validos: {sorted(tipos_validos)}"
        )
    
    log = []
    paso = 1

    # --- Paso 1: el emisor prepara el mensaje ---
    log.append({
        "paso": paso,
        "etapa": "Emisor",
        "evento": "Prepara el mensaje para enviarlo",
        "contenido_visible": mensaje,
    })
    paso += 1

    # --- Paso 2: el canal transforma el mensaje si está cifrado ---
    if canal_cifrado:
        mensaje_en_canal = _cifrar_visual(mensaje)
        log.append({
            "paso": paso,
            "etapa": "Canal",
            "evento": "Cifra el mensaje antes de transmitirlo (ROT-3 visual)",
            "contenido_visible": mensaje_en_canal,
        })
    else:
        mensaje_en_canal = mensaje
        log.append({
            "paso": paso,
            "etapa": "Canal",
            "evento": "El mensaje viaja sin cifrar — cualquiera en la red puede leerlo",
            "contenido_visible": mensaje_en_canal,
        })
    paso += 1

    # --- Paso 3: el atacante actúa (si hay ataque) ---
    mensaje_a_recibir = mensaje_en_canal

    if tipo_ataque == "pasivo":
        if canal_cifrado:
            log.append({
                "paso": paso,
                "etapa": "Atacante",
                "evento": "Copia el mensaje pero no puede leerlo (canal cifrado)",
                "contenido_visible": f"[ve: {mensaje_en_canal}]  ← ilegible",
            })
        else:
            log.append({
                "paso": paso,
                "etapa": "Atacante",
                "evento": "Copia el mensaje y lo lee completo (canal sin cifrar)",
                "contenido_visible": f"[lee: {mensaje_en_canal}]  ← INTERCEPCION exitosa",
            })
        paso += 1

    elif tipo_ataque == "activo":
        mensaje_modificado = _modificar_como_atacante(mensaje_en_canal)
        log.append({
            "paso": paso,
            "etapa": "Atacante",
            "evento": "Intercepta el mensaje, lo modifica y lo reenvía (MITM)",
            "contenido_visible": (
                f"[original: {mensaje_en_canal}]  →  "
                f"[modificado: {mensaje_modificado}]"
            ),
        })
        mensaje_a_recibir = mensaje_modificado
        paso += 1


    # --- Paso 4: el receptor recibe el mensaje ---
    if canal_cifrado:
        mensaje_recibido = _cifrar_visual(mensaje_a_recibir)
        log.append({
            "paso": paso,
            "etapa": "Receptor",
            "evento": "Descifra el mensaje recibido",
            "contenido_visible": mensaje_recibido,
        })
    else:
        mensaje_recibido = mensaje_a_recibir
        log.append({
            "paso": paso,
            "etapa": "Receptor",
            "evento": "Recibe el mensaje tal como llego por el canal",
            "contenido_visible": mensaje_recibido,
        })

    # --- Advertencia según vulnerabilidades del canal ---
    if not canal_cifrado and tipo_ataque == "ninguno":
        advertencia = (
            "Canal sin cifrar: aunque no hay ataque activo, "
            "cualquier observador en la red puede leer el mensaje."
        )
    elif tipo_ataque == "pasivo" and not canal_cifrado:
        advertencia = (
            "Intercepcion exitosa: el atacante leyo el contenido completo. "
            "Activa el cifrado del canal para evitarlo."
        )
    elif tipo_ataque == "activo":
        advertencia = (
            "Ataque MITM exitoso: el receptor recibio un mensaje alterado "
            "y no tiene forma de detectarlo sin verificacion de integridad."
        )
    else:
        advertencia = "Sin vulnerabilidades detectadas en este escenario."

    return {
        "escenario": f"Ataque {tipo_ataque} | Canal {'cifrado' if canal_cifrado else 'sin cifrar'}",
        "mensaje_original": mensaje,
        "mensaje_recibido": mensaje_recibido,
        "canal": "Cifrado" if canal_cifrado else "Sin cifrar",
        "tipo_ataque": tipo_ataque,
        "log": log,
        "advertencia": advertencia,
    }