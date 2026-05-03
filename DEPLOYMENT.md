# Despliegue del proyecto

Esta aplicacion esta construida con Streamlit. La forma recomendada de publicarla desde GitHub es usar Streamlit Community Cloud, Render, Railway o una maquina virtual sencilla.

## Opcion recomendada: Streamlit Community Cloud

1. Subir el proyecto al repositorio GitHub `Joabits/CriptoP1`.
2. Entrar a https://share.streamlit.io/.
3. Iniciar sesion con GitHub.
4. Seleccionar el repositorio `Joabits/CriptoP1`.
5. Configurar:

```text
Branch: main
Main file path: app.py
Python version: 3.11
```

6. Deploy.

La plataforma instalara automaticamente las dependencias desde `requirements.txt`.

## Opcion Render

Crear un Web Service con estos comandos:

```text
Build command: pip install -r requirements.txt
Start command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Opcion Railway

Railway puede desplegar esta app usando el archivo `railway.json` incluido en el proyecto.

Configuracion usada:

```text
Builder: Nixpacks
Start command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Pasos desde GitHub:

1. Entrar a https://railway.app/.
2. Crear un proyecto nuevo.
3. Elegir `Deploy from GitHub repo`.
4. Seleccionar `Joabits/CriptoP1`.
5. Railway detectara Python y usara `requirements.txt`.
6. El comando de inicio saldra de `railway.json`.

## Sobre Vercel

Vercel es excelente para aplicaciones frontend y funciones serverless, pero no es la opcion adecuada para una app Streamlit completa. Streamlit ejecuta un servidor Python persistente y usa comunicacion interactiva con el navegador. En Vercel, las funciones Python son serverless y no estan pensadas para mantener un proceso Streamlit corriendo como servidor web tradicional.

Para usar Vercel de forma correcta habria que reescribir la interfaz en una tecnologia compatible con Vercel, por ejemplo Next.js, y mover la logica criptografica a una API compatible. Eso ya seria otro proyecto.

## Ejecucion local

```bash
python -m streamlit run app.py
```

## Validacion antes de publicar

```bash
python -m pytest -q
```
