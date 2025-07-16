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
        "area": "Pensamiento Matemático",
        "texto": "¿Cuál es el 15% de 200?",
        "opciones": ["A) 25", "B) 30", "C) 35"],
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
        "area": "Comprensión Lectora",
        "texto": "La palabra 'altruista' se refiere a alguien que:",
        "opciones": ["A) Es egoísta", "B) Ayuda a otros", "C) Es tímido"],
        "correcta": 1
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
        "area": "Redacción Indirecta",
        "texto": "¿Cuál es la forma correcta?",
        "opciones": [
            "A) A través de", 
            "B) Atravez de", 
            "C) A travéz de"
        ],
        "correcta": 0
    },
    {
        "area": "Redacción Indirecta",
        "texto": "Completa: 'Se ___ las llaves'",
        "opciones": ["A) perdieron", "B) perdió", "C) perdiran"],
        "correcta": 0
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
    },
    {
        "area": "Literatura",
        "texto": "¿Quién escribió 'Cien años de soledad'?",
        "opciones": ["A) Vargas Llosa", "B) García Márquez", "C) Octavio Paz"],
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
    .stats-container {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# HEADER PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>🎓 EXANI-II Professional Simulator</h1>
    <p>Simulador Oficial CENEVAL 2026 | Versión Web Completa</p>
    <p>📱 Accesible desde cualquier dispositivo</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR - Panel de Control
with st.sidebar:
    st.title("📊 Panel de Control")
    
    # Estadísticas principales
    st.markdown("### 📈 Estadísticas")
    st.metric("Pregunta", f"{st.session_state.pregunta_actual + 1}", f"de {len(preguntas)}")
    st.metric("Respondidas", len(st.session_state.respuestas_usuario))
    st.metric("Puntuación", st.session_state.puntuacion)
    
    # Progreso visual
    progreso = (st.session_state.pregunta_actual + 1) / len(preguntas)
    st.progress(progreso)
    st.write(f"Progreso: {progreso*100:.1f}%")
    
    # Tiempo transcurrido
    tiempo_transcurrido = datetime.now() - st.session_state.tiempo_inicio
    minutos = int(tiempo_transcurrido.total_seconds() // 60)
    segundos = int(tiempo_transcurrido.total_seconds() % 60)
    st.write(f"⏰ Tiempo: {minutos}:{segundos:02d}")
    
    # Distribución por áreas
    st.markdown("### 📚 Por Áreas")
    areas_respondidas = {}
    for idx, resp in st.session_state.respuestas_usuario.items():
        area = preguntas[idx]['area']
        if area not in areas_respondidas:
            areas_respondidas[area] = 0
        areas_respondidas[area] += 1
    
    for area in set(p['area'] for p in preguntas):
        respondidas = areas_respondidas.get(area, 0)
        total_area = len([p for p in preguntas if p['area'] == area])
        st.write(f"{area}: {respondidas}/{total_area}")
    
    # Botones de control
    st.markdown("---")
    if st.button("🔄 Reiniciar Examen", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    if st.button("📊 Ver Resultados", use_container_width=True):
        st.session_state.examen_terminado = True
        st.rerun()

# CONTENIDO PRINCIPAL
if not st.session_state.examen_terminado:
    # Mostrar pregunta actual
    pregunta_actual = preguntas[st.session_state.pregunta_actual]
    
    st.markdown(f"""
    <div class="question-card">
        <h3>📚 {pregunta_actual['area']}</h3>
        <h2>Pregunta {st.session_state.pregunta_actual + 1}</h2>
        <p style="font-size: 1.2em; margin-top: 1rem;">{pregunta_actual['texto']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Opciones de respuesta
    respuesta_seleccionada = st.radio(
        "Selecciona tu respuesta:",
        pregunta_actual['opciones'],
        key=f"pregunta_{st.session_state.pregunta_actual}"
    )
    
    # Botones de navegación
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⬅️ Anterior", disabled=(st.session_state.pregunta_actual == 0), use_container_width=True):
            st.session_state.pregunta_actual -= 1
            st.rerun()
    
    with col2:
        if st.button("✅ Responder", use_container_width=True):
            # Guardar respuesta
            indice_respuesta = pregunta_actual['opciones'].index(respuesta_seleccionada)
            
            # Si es primera vez que responde esta pregunta
            if st.session_state.pregunta_actual not in st.session_state.respuestas_usuario:
                st.session_state.respuestas_usuario[st.session_state.pregunta_actual] = indice_respuesta
                
                # Verificar si es correcta
                if indice_respuesta == pregunta_actual['correcta']:
                    st.success("🎉 ¡Correcto!")
                    st.balloons()
                    st.session_state.puntuacion += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['opciones'][pregunta_actual['correcta']]}")
            else:
                st.info("Ya respondiste esta pregunta anteriormente")
    
    with col3:
        if st.button("➡️ Siguiente", disabled=(st.session_state.pregunta_actual >= len(preguntas) - 1), use_container_width=True):
            st.session_state.pregunta_actual += 1
            st.rerun()
    
    with col4:
        if st.button("🏁 Terminar", use_container_width=True):
            st.session_state.examen_terminado = True
            st.rerun()
    
    # Navegación rápida
    st.markdown("---")
    st.write("### 🗂️ Navegación Rápida")
    
    # Mostrar preguntas en filas de 5
    for fila in range(0, len(preguntas), 5):
        cols = st.columns(5)
        for i in range(5):
            idx = fila + i
            if idx < len(preguntas):
                with cols[i]:
                    # Determinar estado
                    if idx == st.session_state.pregunta_actual:
                        estado = f"🔵 {idx+1}"
                    elif idx in st.session_state.respuestas_usuario:
                        estado = f"✅ {idx+1}"
                    else:
                        estado = f"⚪ {idx+1}"
                    
                    if st.button(estado, key=f"nav_{idx}", use_container_width=True):
                        st.session_state.pregunta_actual = idx
                        st.rerun()

else:
    # PANTALLA DE RESULTADOS
    st.markdown("# 🏆 ¡Examen Completado!")
    
    # Calcular estadísticas finales
    total_respondidas = len(st.session_state.respuestas_usuario)
    porcentaje = (st.session_state.puntuacion / len(preguntas)) * 100 if len(preguntas) > 0 else 0
    tiempo_total = datetime.now() - st.session_state.tiempo_inicio
    
    # Mostrar puntuación principal
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Puntuación Final", f"{porcentaje:.1f}%", f"{st.session_state.puntuacion}/{len(preguntas)}")
    
    with col2:
        st.metric("⏰ Tiempo Total", f"{int(tiempo_total.total_seconds()//60)}:{int(tiempo_total.total_seconds()%60):02d}")
    
    with col3:
        if porcentaje >= 70:
            st.success("🎉 ¡APROBADO!")
        elif porcentaje >= 60:
            st.warning("⚠️ Regular")
        else:
            st.error("📚 Reprobado")
    
    # Análisis por áreas
    st.markdown("## 📈 Análisis por Áreas")
    
    areas_stats = {}
    for idx, resp in st.session_state.respuestas_usuario.items():
        area = preguntas[idx]['area']
        if area not in areas_stats:
            areas_stats[area] = {'correctas': 0, 'total': 0}
        
        areas_stats[area]['total'] += 1
        if resp == preguntas[idx]['correcta']:
            areas_stats[area]['correctas'] += 1
    
    # Crear DataFrame para mostrar resultados
    data_areas = []
    for area, stats in areas_stats.items():
        porcentaje_area = (stats['correctas'] / stats['total']) * 100 if stats['total'] > 0 else 0
        data_areas.append({
            'Área': area,
            'Correctas': stats['correctas'],
            'Total': stats['total'],
            'Porcentaje': f"{porcentaje_area:.1f}%"
        })
    
    if data_areas:
        df = pd.DataFrame(data_areas)
        st.dataframe(df, use_container_width=True)
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Nuevo Examen", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    with col2:
        # Preparar datos para exportar
        resultados_export = {
            'puntuacion_final': f"{porcentaje:.1f}%",
            'correctas': st.session_state.puntuacion,
            'total_preguntas': len(preguntas),
            'tiempo_total': str(tiempo_total).split('.')[0],
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'areas': areas_stats
        }
        
        if st.download_button(
            "📁 Descargar Resultados",
            data=json.dumps(resultados_export, indent=2, ensure_ascii=False),
            file_name=f"EXANI_Resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        ):
            st.success("Resultados descargados!")
    
    with col3:
        if st.button("📊 Compartir Resultados", use_container_width=True):
            texto_compartir = f"""
🎓 EXANI-II Simulator - Mis Resultados

📊 Puntuación: {porcentaje:.1f}%
✅ Correctas: {st.session_state.puntuacion}/{len(preguntas)}
⏰ Tiempo: {int(tiempo_total.total_seconds()//60)}:{int(tiempo_total.total_seconds()%60):02d}
📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}

¡Prueba el simulador tú también!
            """
            st.text_area("Copia este texto para compartir:", texto_compartir, height=150)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
    <h4>🎓 EXANI-II Professional Simulator</h4>
    <p>Desarrollado por <strong>Von Carloo MC</strong></p>
    <p>📧 Contacto | 🌐 Web Version | 💻 Desktop Version</p>
    <p><small>Simulador educativo para preparación CENEVAL</small></p>
</div>
""", unsafe_allow_html=True)
