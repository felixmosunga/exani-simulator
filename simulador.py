import streamlit as st
import time
import json
from datetime import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="EXANI-II Professional Simulator",
    page_icon="🎓",
    layout="wide"
)

# Inicializar estado de la sesión
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0
if 'respuestas_usuario' not in st.session_state:
    st.session_state.respuestas_usuario = {}
if 'puntuacion' not in st.session_state:
    st.session_state.puntuacion = 0
if 'tiempo_inicio' not in st.session_state:
    st.session_state.tiempo_inicio = datetime.now()
if 'examen_terminado' not in st.session_state:
    st.session_state.examen_terminado = False

# BASE DE DATOS DE PREGUNTAS
preguntas = [
    {
        "area": "Pensamiento Matemático",
        "texto": "¿Cuál es el resultado de la ecuación: 2x + 5 = 13?",
        "opciones": ["A) x = 3", "B) x = 4", "C) x = 5"],
        "correcta": 1
    },
    {
        "area": "Pensamiento Matemático", 
        "texto": "¿Cuál es la raíz cuadrada de 64?",
        "opciones": ["A) 6", "B) 8", "C) 10"],
        "correcta": 1
    },
    {
        "area": "Pensamiento Matemático",
        "texto": "Si 3x - 7 = 14, ¿cuál es el valor de x?",
        "opciones": ["A) x = 5", "B) x = 7", "C) x = 9"],
        "correcta": 1
    },
    {
        "area": "Comprensión Lectora",
        "texto": "¿Cuál es el sinónimo de 'efímero'?",
        "opciones": ["A) Permanente", "B) Temporal", "C) Eterno"],
        "correcta": 1
    },
    {
        "area": "Comprensión Lectora",
        "texto": "¿Qué significa 'perspicaz'?",
        "opciones": ["A) Confuso", "B) Ingenuo", "C) Agudo"],
        "correcta": 2
    },
    {
        "area": "Redacción Indirecta",
        "texto": "¿Cuál oración está correctamente escrita?",
        "opciones": [
            "A) Hubieron muchas personas", 
            "B) Hubo muchas personas", 
            "C) Habían muchas personas"
        ],
        "correcta": 1
    },
    {
        "area": "Biología",
        "texto": "¿Cuál es la unidad básica de la vida?",
        "opciones": ["A) El átomo", "B) La célula", "C) El tejido"],
        "correcta": 1
    },
    {
        "area": "Historia",
        "texto": "¿En qué año se independizó México?",
        "opciones": ["A) 1810", "B) 1821", "C) 1910"],
        "correcta": 1
    },
    {
        "area": "Física",
        "texto": "La velocidad se calcula como:",
        "opciones": ["A) distancia × tiempo", "B) distancia ÷ tiempo", "C) tiempo ÷ distancia"],
        "correcta": 1
    },
    {
        "area": "Química",
        "texto": "¿Cuál es el símbolo del oro?",
        "opciones": ["A) Go", "B) Au", "C) Ag"],
        "correcta": 1
    }
]

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-card {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# HEADER PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>🎓 EXANI-II Professional Simulator</h1>
    <p>Simulador Oficial CENEVAL 2026</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("📊 Panel de Control")
    st.metric("Pregunta", f"{st.session_state.pregunta_actual + 1}", f"de {len(preguntas)}")
    st.metric("Respondidas", len(st.session_state.respuestas_usuario))
    st.metric("Puntuación", st.session_state.puntuacion)
    
    progreso = (st.session_state.pregunta_actual + 1) / len(preguntas)
    st.progress(progreso)
    
    tiempo_transcurrido = datetime.now() - st.session_state.tiempo_inicio
    minutos = int(tiempo_transcurrido.total_seconds() // 60)
    segundos = int(tiempo_transcurrido.total_seconds() % 60)
    st.write(f"⏰ Tiempo: {minutos}:{segundos:02d}")
    
    if st.button("🔄 Reiniciar", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# CONTENIDO PRINCIPAL
if not st.session_state.examen_terminado:
    pregunta_actual = preguntas[st.session_state.pregunta_actual]
    
    st.markdown(f"""
    <div class="question-card">
        <h3>📚 {pregunta_actual['area']}</h3>
        <h2>Pregunta {st.session_state.pregunta_actual + 1}</h2>
        <p style="font-size: 1.2em;">{pregunta_actual['texto']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    respuesta_seleccionada = st.radio(
        "Selecciona tu respuesta:",
        pregunta_actual['opciones'],
        key=f"pregunta_{st.session_state.pregunta_actual}"
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⬅️ Anterior", disabled=(st.session_state.pregunta_actual == 0)):
            st.session_state.pregunta_actual -= 1
            st.rerun()
    
    with col2:
        if st.button("✅ Responder"):
            indice_respuesta = pregunta_actual['opciones'].index(respuesta_seleccionada)
            
            if st.session_state.pregunta_actual not in st.session_state.respuestas_usuario:
                st.session_state.respuestas_usuario[st.session_state.pregunta_actual] = indice_respuesta
                
                if indice_respuesta == pregunta_actual['correcta']:
                    st.success("🎉 ¡Correcto!")
                    st.balloons()
                    st.session_state.puntuacion += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['opciones'][pregunta_actual['correcta']]}")
            else:
                st.info("Ya respondiste esta pregunta")
    
    with col3:
        if st.button("➡️ Siguiente", disabled=(st.session_state.pregunta_actual >= len(preguntas) - 1)):
            st.session_state.pregunta_actual += 1
            st.rerun()
    
    with col4:
        if st.button("🏁 Terminar"):
            st.session_state.examen_terminado = True
            st.rerun()
    
    # Navegación rápida
    st.write("### 🗂️ Navegación Rápida")
    cols = st.columns(min(len(preguntas), 5))
    for i, pregunta in enumerate(preguntas[:5]):
        with cols[i]:
            if i == st.session_state.pregunta_actual:
                estado = f"🔵 {i+1}"
            elif i in st.session_state.respuestas_usuario:
                estado = f"✅ {i+1}"
            else:
                estado = f"⚪ {i+1}"
            
            if st.button(estado, key=f"nav_{i}"):
                st.session_state.pregunta_actual = i
                st.rerun()

else:
    # RESULTADOS
    st.title("🏆 ¡Examen Completado!")
    
    porcentaje = (st.session_state.puntuacion / len(preguntas)) * 100
    tiempo_total = datetime.now() - st.session_state.tiempo_inicio
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Puntuación", f"{porcentaje:.1f}%")
    with col2:
        st.metric("✅ Correctas", st.session_state.puntuacion)
    with col3:
        minutos_total = int(tiempo_total.total_seconds() // 60)
        st.metric("⏰ Tiempo", f"{minutos_total}:{int(tiempo_total.total_seconds() % 60):02d}")
    
    if porcentaje >= 70:
        st.success("🎉 ¡APROBADO!")
    elif porcentaje >= 60:
        st.warning("⚠️ Regular")
    else:
        st.error("📚 Reprobado")
    
    if st.button("🔄 Nuevo Examen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Footer
st.markdown("---")
st.markdown("**Desarrollado por Von Carloo MC**")
