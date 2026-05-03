# Libreria Criptografica y de Seguridad - Grupo F

Proyecto educativo para la materia de Criptografia y Seguridad. Incluye una libreria propia en Python y una interfaz web con Streamlit para demostrar seis modulos:

1. Mapeo de Debilidades.
2. Analisis de Seguridad en Comunicaciones.
3. Taller de Criptoanalisis Elegante.
4. Simulador de Auditoria Academica.
5. Analizador de Frecuencias ESTIRANDO.
6. Simulador Interactivo del Disco de Alberti.

## Requisitos

- Python 3.10 o superior.
- Dependencias de `requirements.txt`.

## Instalacion

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

En PowerShell de Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar la interfaz

```bash
streamlit run app.py
```

## Ejecutar pruebas

```bash
pytest
```

## Despliegue

La app esta hecha con Streamlit. Para publicarla desde GitHub, la opcion recomendada es Streamlit Community Cloud usando `app.py` como archivo principal. Tambien puede desplegarse en Render con el comando de inicio:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Vercel no es la plataforma ideal para esta app porque Streamlit necesita un servidor Python persistente. Los detalles estan en `DEPLOYMENT.md`.

## Estructura

```text
cripto_grupo_f/      Libreria reusable
app.py               Interfaz Streamlit
tests/               Pruebas automaticas
docs/                Documentacion tecnica
```

La interfaz no contiene los algoritmos directamente: llama a funciones del paquete `cripto_grupo_f`, cumpliendo el requisito de libreria propia.

## Funciones destacadas

- Mapeo de activos con vulnerabilidad, tipo de amenaza, impacto y control.
- Comparacion visual entre sistemas aislados e interconectados.
- Taller de fuerza bruta contra criptoanalisis usando Cesar.
- Auditoria academica con controles P1-P4.
- Analisis ESTIRANDO con monogramas, digramas, trigramas y sustituciones manuales.
- Disco de Alberti con posicion inicial, intervalo de rotacion, direccion y avance.
