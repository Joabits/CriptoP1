# Despliegue del proyecto

Esta aplicacion esta construida con Streamlit y fue preparada para desplegarse en Railway desde GitHub.

## Plataforma usada: Railway

Railway despliega la app usando el archivo `railway.json` incluido en el proyecto.

Configuracion usada:

```text
Builder: Nixpacks
Start command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Railway detecta Python, instala las dependencias desde `requirements.txt` y ejecuta el comando de inicio definido en `railway.json`.

## Archivos usados para el despliegue

```text
railway.json              Configuracion de Railway
requirements.txt          Dependencias Python
runtime.txt               Version de Python sugerida
.streamlit/config.toml    Configuracion de Streamlit
app.py                    Entrada principal de la app
```

## Variables y puerto

Railway define automaticamente la variable `$PORT`. Por eso el comando de inicio usa:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Ejecucion local

```bash
python -m streamlit run app.py
```

## Validacion

```bash
python -m pytest -q
```
