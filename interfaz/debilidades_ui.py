"""
Interfaz de usuario para el Módulo de Mapeo de Debilidades Criptográficas
Streamlit UI con diseño moderno e interactivo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from cripto_grupo_f.debilidades import (
    MapeoDebilidadesCripto, 
    TipoActivo, 
    TipoAmenaza, 
    NivelRiesgo,
    Activo,
    Vulnerabilidad,
    MapeoDebilidad
)
import numpy as np

# Configuración de página - DEBE SER EL PRIMER COMANDO STREAMLIT
st.set_page_config(
    page_title="🔐 Mapeo de Debilidades Criptográficas",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    h1, h2, h3 {
        background: linear-gradient(120deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,210,255,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5);
        border-radius: 15px;
        padding: 15px;
        color: white;
        text-align: center;
    }
    
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0f23, #1a1a2e);
    }
</style>
""", unsafe_allow_html=True)

def inicializar_sesion():
    """Inicializa variables de sesión"""
    if 'motor_debilidades' not in st.session_state:
        st.session_state.motor_debilidades = MapeoDebilidadesCripto()
    if 'resultados_actuales' not in st.session_state:
        st.session_state.resultados_actuales = None
    if 'paso_actual' not in st.session_state:
        st.session_state.paso_actual = 1

def mostrar_cabecera():
    """Muestra cabecera animada"""
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🔐 Mapeo de Debilidades Criptográficas</h1>
            <p style='color: #cccccc; font-size: 1.2em;'>
                Análisis sistemático de vulnerabilidades en Hardware, Software y Datos
            </p>
            <hr style='background: linear-gradient(90deg, #00d2ff, #3a7bd5); height: 2px; border: none;'>
        </div>
        """, unsafe_allow_html=True)

def paso_seleccion_activo():
    """Paso 1: Selección de activo a analizar"""
    st.markdown("### 📋 Paso 1: Selecciona un Activo")
    
    motor = st.session_state.motor_debilidades
    
    # Mostrar activos disponibles
    activos_lista = list(motor.activos_db.values())
    
    # Crear 2 filas de 3 columnas
    for i in range(0, len(activos_lista), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(activos_lista):
                activo = activos_lista[idx]
                with cols[j]:
                    # Icono según tipo
                    if activo.tipo == TipoActivo.HARDWARE:
                        icono = "🖥️"
                        color = "#ff6b6b"
                    elif activo.tipo == TipoActivo.SOFTWARE:
                        icono = "📱"
                        color = "#4ecdc4"
                    else:
                        icono = "💾"
                        color = "#45b7d1"
                    
                    st.markdown(f"""
                    <div class='card' style='border-left: 5px solid {color};'>
                        <h3 style='margin:0; color:{color};'>{icono} {activo.nombre}</h3>
                        <p><small>{activo.tipo.value}</small></p>
                        <p>{activo.descripcion}</p>
                        <p><strong>Criticidad:</strong> {'⭐' * activo.criticidad}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🔍 Analizar {activo.nombre}", key=f"btn_{activo.id}"):
                        with st.spinner(f"Analizando {activo.nombre}..."):
                            resultados = motor.mapear_activo_con_vulnerabilidades(activo.id)
                            st.session_state.resultados_actuales = resultados
                            st.session_state.paso_actual = 2
                            st.rerun()

def mostrar_matriz_riesgos():
    """Muestra matriz de riesgos interactiva"""
    st.markdown("### 🎯 Matriz de Riesgos (Activos vs Amenazas)")
    
    motor = st.session_state.motor_debilidades
    
    # Forzar recalculo de matriz con todos los activos
    todos_resultados = []
    for activo_id in motor.activos_db.keys():
        resultados = motor.mapear_activo_con_vulnerabilidades(activo_id)
        todos_resultados.extend(resultados)
    
    # Construir matriz manualmente
    amenazas = [a.value for a in TipoAmenaza]
    activos_nombres = [a.nombre for a in motor.activos_db.values()]
    
    matriz = np.zeros((len(activos_nombres), len(amenazas)))
    
    for mapeo in todos_resultados:
        i = activos_nombres.index(mapeo.activo.nombre)
        j = amenazas.index(mapeo.amenaza.value)
        matriz[i, j] = max(matriz[i, j], mapeo.riesgo_calculado)
    
    if matriz.size > 0:
        fig = px.imshow(
            matriz,
            x=amenazas,
            y=activos_nombres,
            color_continuous_scale='RdYlGn_r',
            aspect="auto",
            title="Mapa de Calor de Riesgos",
            text_auto=True,
            labels=dict(color="Riesgo (0-10)")
        )
        fig.update_layout(height=500, width=900)
        st.plotly_chart(fig, use_container_width=True)
        
        # Explicación matemática
        with st.expander("📐 Explicación Matemática del Algoritmo"):
            st.markdown("""
            ### Fórmula de Cálculo de Riesgo
            
            $$
            \\text{Riesgo}(a_i, v_j) = P_{ij} \\times I_{ij} \\times 2
            $$
            
            $$
            P_{ij} = 0.4 \\cdot \\mathbf{1}_{T(a_i)=T(v_j)} + 0.4 \\cdot R_{ij} + 0.2 \\cdot \\frac{C(a_i)}{5}
            $$
            
            ### Donde:
            
            | Símbolo | Significado | Rango |
          |---------|-------------|-------|
          | $P_{ij}$ | Probabilidad de explotación | [0, 1] |
          | $I_{ij}$ | Impacto potencial | [1, 5] |
          | $C(a_i)$ | Criticidad del activo | [1, 5] |
          | $R_{ij}$ | Relevancia directa | {0, 1} |
            
            ### Interpretación de Riesgo:
            - 🔴 **≥ 8.0**: Crítico - Acción inmediata
            - 🟠 **6.0 - 7.9**: Alto - Prioridad alta
            - 🟡 **4.0 - 5.9**: Medio - Planificar corrección
            - 🟢 **< 4.0**: Bajo - Monitorear
            """)

def paso_resultados():
    """Paso 2: Visualización de resultados"""
    st.markdown("### 📊 Paso 2: Resultados del Análisis")
    
    resultados = st.session_state.resultados_actuales
    
    if not resultados:
        st.warning("⚠️ No hay resultados para mostrar. Vuelve al Paso 1.")
        if st.button("← Volver a seleccionar activo"):
            st.session_state.paso_actual = 1
            st.rerun()
        return
    
    motor = st.session_state.motor_debilidades
    activo_analizado = resultados[0].activo
    
    # Métricas resumen
    col1, col2, col3, col4 = st.columns(4)
    
    riesgos = [r.riesgo_calculado for r in resultados]
    criticos = sum(1 for r in riesgos if r >= 6)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🎯 {len(resultados)}</h3>
            <p>Vulnerabilidades</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>⚠️ {criticos}</h3>
            <p>Críticas (≥6)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{np.mean(riesgos):.1f}</h3>
            <p>Riesgo Promedio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_riesgo = max(riesgos)
        if max_riesgo >= 8:
            nivel = "🔴 CRÍTICO"
        elif max_riesgo >= 6:
            nivel = "🟠 ALTO"
        elif max_riesgo >= 4:
            nivel = "🟡 MEDIO"
        else:
            nivel = "🟢 BAJO"
        st.markdown(f"""
        <div class='metric-card'>
            <h3>{max_riesgo:.1f}</h3>
            <p>Riesgo Máximo {nivel}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabla detallada
    df = pd.DataFrame([{
        "ID": r.vulnerabilidad.id,
        "Vulnerabilidad": r.vulnerabilidad.nombre[:40],
        "Amenaza": r.amenaza.value,
        "Probabilidad": f"{r.probabilidad*100:.0f}%",
        "Impacto": "⭐" * r.impacto,
        "Riesgo": r.riesgo_calculado
    } for r in resultados])
    
    # Color coding para la tabla
    def color_riesgo(val):
        if val >= 8:
            return 'background-color: #ff4444; color: white'
        elif val >= 6:
            return 'background-color: #ff8800; color: white'
        elif val >= 4:
            return 'background-color: #ffcc00; color: black'
        else:
            return 'background-color: #00cc66; color: white'
    
    st.dataframe(df.style.applymap(color_riesgo, subset=['Riesgo']), 
                 use_container_width=True, height=400)
    
    # Gráfico de barras
    fig = go.Figure()
    colores = ['#ff4444' if r >= 8 else '#ff8800' if r >= 6 else '#ffcc00' if r >= 4 else '#00cc66' 
               for r in [r.riesgo_calculado for r in resultados]]
    
    fig.add_trace(go.Bar(
        x=[r.vulnerabilidad.id for r in resultados],
        y=[r.riesgo_calculado for r in resultados],
        marker_color=colores,
        text=[f"{r.riesgo_calculado:.1f}" for r in resultados],
        textposition='auto',
        textfont=dict(size=14, color='white')
    ))
    fig.update_layout(
        title=f"📈 Riesgos por Vulnerabilidad - {activo_analizado.nombre}",
        xaxis_title="Vulnerabilidad",
        yaxis_title="Nivel de Riesgo (0-10)",
        yaxis_range=[0, 10.5],
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recomendaciones
    st.markdown("### 💡 Recomendaciones Prioritarias")
    
    criticas = motor.generar_informe_critico(umbral_riesgo=5)
    if criticas:
        for critica in criticas[:3]:
            with st.expander(f"⚠️ {critica['vulnerabilidad']} - Riesgo: {critica['riesgo']:.1f}"):
                st.markdown(f"""
                - **Activo:** {critica['activo']}
                - **Amenaza:** {critica['amenaza']}
                - **Probabilidad:** {critica['probabilidad']}
                - **Referencia CWE:** {critica['cwe_id']}
                - **Recomendación:** {critica['recomendacion']}
                """)
    else:
        st.success("✅ No se encontraron vulnerabilidades críticas. El sistema está bien protegido.")
    
    # Botones navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Analizar otro activo", use_container_width=True):
            st.session_state.paso_actual = 1
            st.session_state.resultados_actuales = None
            st.rerun()
    with col2:
        if st.button("📥 Exportar Informe CSV", use_container_width=True):
            df.to_csv("informe_debilidades.csv", index=False)
            st.success("✅ Informe exportado como 'informe_debilidades.csv'")

def mostrar_estadisticas_globales():
    """Muestra estadísticas globales"""
    st.markdown("### 📈 Estadísticas Globales del Sistema")
    
    motor = st.session_state.motor_debilidades
    
    # Ejecutar análisis para todos los activos
    todos_mapeos = []
    for activo_id in motor.activos_db.keys():
        resultados = motor.mapear_activo_con_vulnerabilidades(activo_id)
        todos_mapeos.extend(resultados)
    
    if todos_mapeos:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Mapeos", len(todos_mapeos))
        with col2:
            riesgos = [m.riesgo_calculado for m in todos_mapeos]
            st.metric("Riesgo Promedio", f"{np.mean(riesgos):.1f}")
        with col3:
            criticos = sum(1 for m in todos_mapeos if m.riesgo_calculado >= 6)
            st.metric("Hallazgos Críticos", criticos)
        with col4:
            activos_unicos = len(set(m.activo.id for m in todos_mapeos))
            st.metric("Activos Analizados", activos_unicos)
        
        # Gráfico de distribución de riesgos
        riesgos_valores = [m.riesgo_calculado for m in todos_mapeos]
        fig = px.histogram(
            x=riesgos_valores, 
            nbins=20,
            title="Distribución de Niveles de Riesgo",
            labels={'x': 'Nivel de Riesgo', 'y': 'Frecuencia'},
            color_discrete_sequence=['#00d2ff']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def sidebar_info():
    """Barra lateral con información"""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/security-checked.png", width=80)
        st.markdown("## 🔐 Módulo de Debilidades")
        st.markdown("---")
        
        st.markdown("### 🎯 Metodología")
        st.markdown("""
        1. **Clasificación** de activos (HW/SW/Datos)
        2. **Asociación** con vulnerabilidades CWE
        3. **Cálculo** de riesgos con fórmula matemática
        4. **Recomendaciones** accionables
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Escala de Riesgo")
        st.markdown("""
        - 🔴 **8.0 - 10.0:** Crítico
        - 🟠 **6.0 - 7.9:** Alto  
        - 🟡 **4.0 - 5.9:** Medio
        - 🟢 **0.0 - 3.9:** Bajo
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Referencias")
        st.markdown("""
        - CWE (Common Weakness Enumeration)
        - CVSS v3.1
        - NIST SP 800-30
        """)
        
        st.markdown("---")
        st.markdown(f"""
        ### 📋 Resumen Rápido
        - **Vulnerabilidades:** {len(st.session_state.motor_debilidades.vulnerabilidades_db)}
        - **Activos:** {len(st.session_state.motor_debilidades.activos_db)}
        - **Tipos Amenaza:** {len(TipoAmenaza)}
        """)
        
        if st.button("🔄 Resetear Análisis", use_container_width=True):
            st.session_state.paso_actual = 1
            st.session_state.resultados_actuales = None
            st.rerun()

def mostrar():
    """Función principal"""
    inicializar_sesion()
    mostrar_cabecera()
    sidebar_info()
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🔍 Análisis de Debilidades", "📊 Matriz de Riesgos", "ℹ️ Documentación"])
    
    with tab1:
        if st.session_state.paso_actual == 1:
            paso_seleccion_activo()
        elif st.session_state.paso_actual == 2:
            paso_resultados()
    
    with tab2:
        mostrar_matriz_riesgos()
        mostrar_estadisticas_globales()
    
    with tab3:
        st.markdown("""
        ### 📖 Documentación Técnica del Módulo
        
        #### 🎯 Objetivo
        Identificar sistemáticamente cómo las debilidades en activos (Hardware, Software, Datos) 
        pueden ser explotadas por amenazas específicas, calculando su riesgo asociado.
        
        #### 🧠 Algoritmo Implementado
        
        **Matching basado en reglas ponderadas:**
                    Coincidencia de tipo (40%)
        - Relevancia directa (40%)
        - Criticidad del activo (20%)
        - Ajuste por CVSS (+20% si score >= 8.0)
        """) # <--- Asegúrate de que tenga esto para cerrar el markdown

if __name__ == "__main__":
    mostrar()
        
def formulario_nuevo_activo():
    """Formulario para agregar activos dinámicamente"""
    st.sidebar.markdown("### ➕ Registrar Nuevo Activo")
    with st.sidebar.form("form_nuevo_activo"):
        nombre = st.text_input("Nombre del Activo", placeholder="Ej: Base de Datos RRHH")
        tipo = st.selectbox("Categoría", options=[t for t in TipoActivo], format_func=lambda x: x.value)
        desc = st.text_area("Descripción breve")
        crit = st.slider("Criticidad (1-5)", 1, 5, 3)
        
        btn_crear = st.form_submit_button("Guardar Activo")
        
        if btn_crear:
            if nombre and desc:
                # Generar un ID único basado en el nombre
                nuevo_id = f"CUSTOM_{nombre.replace(' ', '_').upper()}"
                st.session_state.motor_debilidades.agregar_nuevo_activo(
                    nuevo_id, nombre, tipo, desc, crit
                )
                st.success(f"✅ '{nombre}' registrado!")
                st.rerun()
            else:
                st.error("Por favor, llena todos los campos.")

def sidebar_info():
    """Barra lateral actualizada con el formulario"""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/security-checked.png", width=80)
        st.markdown("## 🔐 Módulo de Debilidades")
        st.markdown("---")
        
        # --- AQUÍ INSERTAMOS EL NUEVO FORMULARIO ---
        formulario_nuevo_activo()
        st.markdown("---")
        
        st.markdown("### 🎯 Metodología")
        st.markdown("""
        1. **Clasificación** (HW/SW/Datos)
        2. **Asociación** (CWE)
        3. **Cálculo** de riesgos
        4. **Recomendaciones**
        """)
        
        if st.button("🔄 Resetear Todo", use_container_width=True):
            # Al resetear, reiniciamos el motor para limpiar los creados si se desea
            st.session_state.motor_debilidades = MapeoDebilidadesCripto()
            st.session_state.paso_actual = 1
            st.session_state.resultados_actuales = None
            st.rerun()