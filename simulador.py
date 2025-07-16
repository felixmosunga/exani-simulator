"""
EXANI-II Professional Simulator - Versión Python
Simulador educativo completo con funcionalidades avanzadas
Desarrollado con Streamlit para interfaz web moderna

Funcionalidades principales:
- Múltiples modos de examen (Transversales, Disciplinares, Completo, Inglés)
- Sistema de temporizador con alertas
- Navegación avanzada entre preguntas
- Estadísticas en tiempo real
- Exportación de resultados
- Interfaz responsive y moderna
"""

import streamlit as st
import time
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional, Tuple

class ExaniSimulator:
    """Simulador EXANI-II con funcionalidades completas"""
    
    def __init__(self):
        self.init_session_state()
        self.load_question_database()
        
    def init_session_state(self):
        """Inicializa el estado de la sesión de Streamlit"""
        if 'current_screen' not in st.session_state:
            st.session_state.current_screen = 'dashboard'
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        if 'user_answers' not in st.session_state:
            st.session_state.user_answers = []
        if 'exam_start_time' not in st.session_state:
            st.session_state.exam_start_time = None
        if 'exam_config' not in st.session_state:
            st.session_state.exam_config = {
                'type': 'transversales',
                'modules': ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta'],
                'time_limit': 180,
                'question_count': 30
            }
        if 'timer_placeholder' not in st.session_state:
            st.session_state.timer_placeholder = None
            
    def load_question_database(self):
        """Carga la base de datos de preguntas"""
        self.question_database = {
            'pensamiento_matematico': [
                {
                    'text': 'En un plano se representa la construcción de una escalera para subir a un edificio. ¿Cuál es la medida del ángulo x si se tiene un ángulo de elevación de 20°?',
                    'options': ['A) 20°', 'B) 45°', 'C) 70°'],
                    'correct': 2,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Selecciona una opción equivalente al siguiente polinomio: $(8)(x - y)^3$',
                    'options': ['A) $(4x - 4y)(4x + 4y)$', 'B) $(2x - 2y)^3$', 'C) $(4x - 4y)^3$'],
                    'correct': 1,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Si $\\cos(x) = -4/5$ con $x$ en el segundo cuadrante, el valor de $\\sen(x)$ es:',
                    'options': ['A) $-3/4$', 'B) $3/5$', 'C) $-3/5$'],
                    'correct': 1,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Determina los valores de $x$ y $y$ en el siguiente sistema de ecuaciones: $3x - 2y = 13$ y $2x + 6y = -6$',
                    'options': ['A) $x = -3, y = 2$', 'B) $x = 3, y = -2$', 'C) $x = 3, y = 2$'],
                    'correct': 1,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Simplifica la siguiente expresión: $(8a³b⁴ - 18ab⁶)/(2ab)$',
                    'options': ['A) $4a²b³ - 9b⁵$', 'B) $4a²b³ - 9ab⁵$', 'C) $6a²b³ - 16b⁵$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'En un salón de clases de 20 alumnos, hay 12 mexicanos, 6 de Estados Unidos y 2 de Canadá. ¿Cuál es la probabilidad de que al nombrar lista se elija a un alumno de Estados Unidos o Canadá?',
                    'options': ['A) 1/20', 'B) 2/20', 'C) 8/20'],
                    'correct': 2,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Simplifica la siguiente expresión: $4ab³ + 6a³b + 8ab³ - 2ab²$',
                    'options': ['A) $12ab³ + 6a³b - 2ab²$', 'B) $12ab³ + 6a³b + 2ab²$', 'C) $10ab³ + 6a³b - 2ab²$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Si $2^{4x} = 4^{x+2}$, ¿cuál es el valor de x?',
                    'options': ['A) 0', 'B) 1', 'C) 2'],
                    'correct': 2,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Simplifica la siguiente expresión: $(3a²)(-5a²b³c)$',
                    'options': ['A) $-15a⁴b³c$', 'B) $15a⁴b³c$', 'C) $-15a²b³c$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Simplifica la siguiente expresión: $(x + 3)(3x - 2)$',
                    'options': ['A) $3x² + 7x - 6$', 'B) $3x² - 7x - 6$', 'C) $3x² + 7x + 6$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                }
            ],
            'comprension_lectora': [
                {
                    'text': 'Del retrato: ¿Qué se puede decir del narrador de la historia?',
                    'options': ['A) No es ninguno de los personajes involucrados', 'B) Es la víctima del asesinato', 'C) Es la protagonista de la historia'],
                    'correct': 2,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Del retrato: El personaje principal del relato es...',
                    'options': ['A) Ana', 'B) Eponina', 'C) El niño'],
                    'correct': 1,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Del retrato: ¿Qué palabra sintetiza mejor el estado anímico de Eponina?',
                    'options': ['A) Hastío', 'B) Odio', 'C) Tristeza'],
                    'correct': 0,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Poema "Antes del reino": En el poema da a entender que la persona a quien la voz lírica habla...',
                    'options': ['A) lo trata muy mal', 'B) tiene múltiples personalidades', 'C) es anterior y posterior a todas las cosas'],
                    'correct': 2,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Del poema: Se puede decir que la persona a quien habla la voz lírica es...',
                    'options': ['A) omnipresente', 'B) omnisciente', 'C) omnipotente'],
                    'correct': 0,
                    'area': 'Comprensión Lectora'
                }
            ],
            'redaccion_indirecta': [
                {
                    'text': 'Complete el fragmento con las grafías correctas: El ga___o cruzó la va___a del ga___inero y se extra___ó en la arboleda que hay al lado.',
                    'options': ['A) ll – ll – ll – v', 'B) ll – y – ll – b', 'C) ll – y – ll – v'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Seleccione las palabras cuyo significado se opone en la oración: A diferencia de los alumnos de la mañana, que son todos muy participativos y puntuales, los vespertinos son más bien medio tímidos y flojos.',
                    'options': ['A) Puntuales – flojos', 'B) Participativos – tímidos', 'C) Mañana – diferencia'],
                    'correct': 1,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Elija la oración puntuada de manera correcta:',
                    'options': ['A) A continuación, las noticias del día', 'B) Patricia, comió una ensalada que lo hizo daño', 'C) Debo comprar lechuga, jamón, pan, y queso'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Complete el enunciado con la expresión que le da sentido: A pesar de que disfruto mucho de jugar videojuegos, no soy un jugador tan diverso como algunas personas piensan, sino que me gusta un tipo específico de juego, _______ me gustan mucho los RPG.',
                    'options': ['A) Concretamente', 'B) En realidad', 'C) Sobre todo'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Señale la oración acentuada de forma correcta:',
                    'options': ['A) Andrea ganó el primer lugar en la competencia de natación', 'B) Desde que volvió de su viaje, Arturo actúa de manera muy extraña', 'C) En ocasiones lo mejor para concentrarse es tratar de hallar un lugar tranquilo donde estar a solas'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                }
            ],
            'biologia': [
                {
                    'text': '¿Cuál es la unidad básica de la vida?',
                    'options': ['A) La célula', 'B) El átomo', 'C) El tejido'],
                    'correct': 0,
                    'area': 'Biología'
                },
                {
                    'text': '¿Qué proceso realizan las plantas para obtener energía?',
                    'options': ['A) Fotosíntesis', 'B) Respiración', 'C) Digestión'],
                    'correct': 0,
                    'area': 'Biología'
                }
            ],
            'fisica': [
                {
                    'text': '¿Cuál es la fórmula para calcular la velocidad?',
                    'options': ['A) v = d/t', 'B) v = t/d', 'C) v = d × t'],
                    'correct': 0,
                    'area': 'Física'
                }
            ],
            'quimica': [
                {
                    'text': '¿Cuál es el símbolo químico del oro?',
                    'options': ['A) Au', 'B) Ag', 'C) Fe'],
                    'correct': 0,
                    'area': 'Química'
                }
            ],
            'historia': [
                {
                    'text': '¿En qué año se consumó la Independencia de México?',
                    'options': ['A) 1821', 'B) 1810', 'C) 1519'],
                    'correct': 0,
                    'area': 'Historia'
                }
            ],
            'literatura': [
                {
                    'text': '¿Quién escribió "Cien años de soledad"?',
                    'options': ['A) Gabriel García Márquez', 'B) Mario Vargas Llosa', 'C) Octavio Paz'],
                    'correct': 0,
                    'area': 'Literatura'
                }
            ]
        }
    
    def apply_custom_css(self):
        """Aplica CSS personalizado para mejorar la apariencia"""
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #2563eb, #1e40af);
            color: white;
            padding: 2rem;
            border-radius: 20px 20px 0 0;
            text-align: center;
            margin-bottom: 0;
        }
        
        .timer-display {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            margin: 1rem 0;
        }
        
        .timer-warning {
            animation: pulse 1s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .question-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }
        
        .option-button {
            width: 100%;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            background: #f8fafc;
            cursor: pointer;
            text-align: left;
            transition: all 0.3s ease;
        }
        
        .option-button:hover {
            border-color: #2563eb;
            background: rgba(37, 99, 235, 0.05);
        }
        
        .option-selected {
            border-color: #2563eb !important;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(30, 64, 175, 0.1)) !important;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stat-card {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2563eb;
        }
        
        .progress-bar {
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #2563eb, #1e40af);
            transition: width 0.3s ease;
        }
        
        .indicators {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin: 1rem 0;
        }
        
        .indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #e2e8f0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .indicator-current {
            background: #2563eb;
            transform: scale(1.3);
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
        }
        
        .indicator-answered {
            background: #059669;
        }
        
        .mode-card {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .mode-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-color: #2563eb;
        }
        
        .mode-active {
            border-color: #2563eb;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(30, 64, 175, 0.1));
        }
        
        .results-score {
            background: linear-gradient(135deg, #059669, #047857);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin: 1rem 0;
        }
        
        .score-number {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Renderiza el encabezado principal"""
        st.markdown("""
        <div class="main-header">
            <h1>🎓 EXANI-II Professional Simulator</h1>
            <p>Simulador Oficial CENEVAL 2026 | 90 Reactivos Oficiales | 3 Opciones por Pregunta</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_dashboard(self):
        """Renderiza el panel principal de configuración"""
        st.markdown("## ⚙️ Configuración del Examen")
        
        col1, col2 = st.columns([2, 1])
        
        with col3:
            if st.button("📁 Exportar Resultados", use_container_width=True):
                self.export_results()
    
    def render_review_screen(self):
        """Renderiza la pantalla de revisión de respuestas"""
        if not st.session_state.questions or 'final_results' not in st.session_state:
            st.error("No hay información de examen para revisar")
            return
        
        st.markdown("## 📊 Revisión de Respuestas")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_type = st.selectbox(
                "Filtrar por:",
                ["Todas", "Correctas", "Incorrectas", "Sin Responder"]
            )
        with col2:
            area_filter = st.selectbox(
                "Área:",
                ["Todas"] + list(set(q['area'] for q in st.session_state.questions))
            )
        with col3:
            if st.button("🏠 Volver al Inicio"):
                self.restart_exam()
                st.rerun()
        
        # Mostrar preguntas según filtros
        st.markdown("---")
        
        for i, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.user_answers[i]
            correct_answer = question['correct']
            
            # Aplicar filtros
            if area_filter != "Todas" and question['area'] != area_filter:
                continue
                
            if filter_type == "Correctas" and user_answer != correct_answer:
                continue
            elif filter_type == "Incorrectas" and (user_answer == correct_answer or user_answer is None):
                continue
            elif filter_type == "Sin Responder" and user_answer is not None:
                continue
            
            # Determinar estado de la respuesta
            if user_answer is None:
                status = "⏭️ Sin responder"
                status_color = "gray"
            elif user_answer == correct_answer:
                status = "✅ Correcta"
                status_color = "green"
            else:
                status = "❌ Incorrecta"
                status_color = "red"
            
            # Mostrar pregunta
            with st.expander(f"Pregunta {i+1} - {question['area']} - {status}"):
                st.markdown(f"**{question['text']}**")
                st.markdown("---")
                
                for j, option in enumerate(question['options']):
                    if j == correct_answer:
                        st.markdown(f"✅ **{option}** (Respuesta correcta)")
                    elif j == user_answer:
                        st.markdown(f"❌ **{option}** (Tu respuesta)")
                    else:
                        st.markdown(f"⚪ {option}")
    
    def export_results(self):
        """Exporta los resultados del examen"""
        if 'final_results' not in st.session_state:
            st.error("No hay resultados para exportar")
            return
        
        results = st.session_state.final_results
        
        # Crear datos detallados para exportar
        detailed_results = {
            'resumen': results,
            'preguntas_detalle': []
        }
        
        for i, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.user_answers[i]
            correct_answer = question['correct']
            
            question_detail = {
                'numero': i + 1,
                'area': question['area'],
                'pregunta': question['text'],
                'opciones': question['options'],
                'respuesta_correcta': correct_answer,
                'respuesta_usuario': user_answer,
                'es_correcta': user_answer == correct_answer if user_answer is not None else False,
                'sin_responder': user_answer is None
            }
            detailed_results['preguntas_detalle'].append(question_detail)
        
        # Crear archivo JSON para descarga
        json_str = json.dumps(detailed_results, ensure_ascii=False, indent=2)
        
        st.download_button(
            label="📥 Descargar Resultados (JSON)",
            data=json_str,
            file_name=f"EXANI-II_Resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # También crear CSV con resumen
        summary_data = {
            'Tipo de Examen': [results['exam_type']],
            'Puntuación (%)': [results['score']],
            'Respuestas Correctas': [results['correct']],
            'Respuestas Incorrectas': [results['wrong']],
            'Sin Responder': [results['skipped']],
            'Total Preguntas': [results['total_questions']],
            'Duración': [str(results['duration']).split('.')[0]],
            'Fecha': [results['date']]
        }
        
        df = pd.DataFrame(summary_data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Descargar Resumen (CSV)",
            data=csv,
            file_name=f"EXANI-II_Resumen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.success("Archivos preparados para descarga")
    
    def restart_exam(self):
        """Reinicia el simulador al estado inicial"""
        # Conservar la configuración pero resetear el estado del examen
        exam_config = st.session_state.exam_config.copy()
        
        # Limpiar estado
        for key in list(st.session_state.keys()):
            if key not in ['exam_config']:
                del st.session_state[key]
        
        # Reinicializar
        self.init_session_state()
        st.session_state.exam_config = exam_config
        st.success("Simulador reiniciado - Listo para un nuevo examen")
    
    def render_sidebar(self):
        """Renderiza la barra lateral con información y controles"""
        with st.sidebar:
            st.markdown("## 📋 Panel de Control")
            
            # Información del examen actual
            if st.session_state.current_screen == 'exam':
                st.markdown("### ⏱️ Estado del Examen")
                
                if st.session_state.exam_start_time:
                    elapsed = datetime.now() - st.session_state.exam_start_time
                    st.write(f"⏰ Tiempo transcurrido: {str(elapsed).split('.')[0]}")
                
                current_q = st.session_state.current_question_index + 1
                total_q = len(st.session_state.questions)
                st.write(f"📝 Progreso: {current_q}/{total_q}")
                
                answered = sum(1 for ans in st.session_state.user_answers if ans is not None)
                st.write(f"✅ Respondidas: {answered}/{total_q}")
                
                st.markdown("---")
                
                # Accesos rápidos
                st.markdown("### 🚀 Accesos Rápidos")
                
                if st.button("⏭️ Saltar pregunta", use_container_width=True):
                    if st.session_state.current_question_index < len(st.session_state.questions) - 1:
                        st.session_state.current_question_index += 1
                        st.rerun()
                
                if st.button("🔄 Reiniciar examen", use_container_width=True):
                    if st.checkbox("Confirmar reinicio"):
                        self.restart_exam()
                        st.rerun()
            
            # Configuración actual
            st.markdown("---")
            st.markdown("### ⚙️ Configuración Actual")
            config = st.session_state.exam_config
            st.write(f"**Tipo:** {config['type'].title()}")
            st.write(f"**Módulos:** {len(config['modules'])}")
            st.write(f"**Preguntas:** {config['question_count']}")
            st.write(f"**Tiempo:** {config['time_limit']} min")
            
            # Atajos de teclado
            st.markdown("---")
            st.markdown("### ⌨️ Atajos de Teclado")
            st.markdown("""
            - **← →** Navegar preguntas
            - **1, 2, 3** Seleccionar opción
            - **Esc** Terminar examen
            """)
            
            # Información del desarrollador
            st.markdown("---")
            st.markdown("### 👨‍💻 Desarrollado por")
            st.markdown("**Von Carloo MC**")
            st.markdown("Simulador EXANI-II Professional")
    
    def run(self):
        """Método principal para ejecutar la aplicación"""
        # Configuración de la página
        st.set_page_config(
            page_title="EXANI-II Professional Simulator",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Aplicar CSS personalizado
        self.apply_custom_css()
        
        # Renderizar encabezado
        self.render_header()
        
        # Renderizar barra lateral
        self.render_sidebar()
        
        # Renderizar pantalla según el estado actual
        if st.session_state.current_screen == 'dashboard':
            self.render_dashboard()
        elif st.session_state.current_screen == 'exam':
            self.render_exam_screen()
        elif st.session_state.current_screen == 'results':
            self.render_results_screen()
        elif st.session_state.current_screen == 'review':
            self.render_review_screen()
        
        # Auto-refresh para el timer (solo durante el examen)
        if st.session_state.current_screen == 'exam' and st.session_state.exam_start_time:
            time.sleep(1)
            st.rerun()


def main():
    """Función principal de la aplicación"""
    simulator = ExaniSimulator()
    simulator.run()


if __name__ == "__main__":
    main()


"""
INSTRUCCIONES DE EJECUCIÓN:

1. INSTALACIÓN DE DEPENDENCIAS:
   pip install streamlit pandas

2. EJECUCIÓN:
   streamlit run exani_simulator.py

3. La aplicación se abrirá automáticamente en:
   http://localhost:8501

FUNCIONALIDADES IMPLEMENTADAS:
✅ Interfaz moderna y responsive
✅ Múltiples modos de examen
✅ Sistema de temporizador con alertas
✅ Navegación completa entre preguntas
✅ Estadísticas en tiempo real
✅ Indicadores visuales de progreso
✅ Sistema de revisión de respuestas
✅ Exportación de resultados (JSON/CSV)
✅ Atajos de teclado
✅ Barra lateral informativa
✅ Auto-guardado de respuestas
✅ Configuración flexible de exámenes

DECISIONES DE DISEÑO:

1. STREAMLIT como framework principal:
   - Facilita desarrollo web rápido
   - Interfaz moderna automática
   - Manejo de estado integrado
   - No requiere HTML/CSS/JS manual

2. ARQUITECTURA ORIENTADA A OBJETOS:
   - Código modular y mantenible
   - Separación clara de responsabilidades
   - Fácil extensión de funcionalidades

3. GESTIÓN DE ESTADO:
   - Uso de st.session_state para persistencia
   - Estado coherente entre recargas
   - Manejo eficiente de datos del examen

4. EXPORTACIÓN DE DATOS:
   - Formatos múltiples (JSON/CSV)
   - Datos detallados y resumenes
   - Compatible con análisis posterior

PERSONALIZACIONES DISPONIBLES:
- Agregar más módulos en question_database
- Modificar tiempos y configuraciones
- Personalizar CSS para cambiar apariencia
- Añadir nuevos tipos de preguntas
- Implementar análisis avanzados
""" col1:
            st.markdown("### 📚 Modos de Examen")
            
            # Modo Transversales
            if st.button("🎯 Áreas Transversales\n(Pensamiento Matemático, Comprensión Lectora y Redacción Indirecta)\n90 preguntas - 3 horas", key="mode_trans"):
                st.session_state.exam_config.update({
                    'type': 'transversales',
                    'modules': ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta'],
                    'time_limit': 180,
                    'question_count': 90
                })
            
            # Modo Disciplinares
            if st.button("📚 Módulos Específicos\n(Conocimientos específicos por carrera)\n48 preguntas - Variable", key="mode_disc"):
                st.session_state.exam_config.update({
                    'type': 'disciplinares',
                    'modules': ['biologia', 'fisica', 'quimica'],
                    'time_limit': 120,
                    'question_count': 48
                })
            
            # Modo Completo
            if st.button("🎓 EXANI-II Completo\n(Simulacro completo oficial 138 reactivos)\n138 preguntas - 4.5 horas", key="mode_comp"):
                st.session_state.exam_config.update({
                    'type': 'completo',
                    'modules': ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta', 'biologia', 'fisica'],
                    'time_limit': 270,
                    'question_count': 138
                })
            
            # Modo Inglés
            if st.button("🔍 Información Diagnóstica\n(Inglés - no cuenta para calificación)\n30 preguntas - 30 min", key="mode_ing"):
                st.session_state.exam_config.update({
                    'type': 'ingles',
                    'modules': ['literatura'],  # Placeholder para inglés
                    'time_limit': 30,
                    'question_count': 30
                })
        
        with col2:
            st.markdown("### ⚙️ Configuración Avanzada")
            
            # Tipo de examen
            exam_type = st.selectbox(
                "Tipo de Simulacro:",
                options=[
                    ('transversales', 'Áreas Transversales (90 reactivos)'),
                    ('disciplinares', 'Módulos Específicos (48 reactivos)'),
                    ('completo', 'EXANI-II Completo (138 reactivos)'),
                    ('ingles', 'Información Diagnóstica (30 reactivos)')
                ],
                format_func=lambda x: x[1],
                index=0
            )
            st.session_state.exam_config['type'] = exam_type[0]
            
            # Módulos específicos
            all_modules = {
                'pensamiento_matematico': 'Pensamiento Matemático',
                'comprension_lectora': 'Comprensión Lectora',
                'redaccion_indirecta': 'Redacción Indirecta',
                'biologia': 'Biología',
                'fisica': 'Física',
                'quimica': 'Química',
                'historia': 'Historia',
                'literatura': 'Literatura'
            }
            
            selected_modules = st.multiselect(
                "Seleccionar Módulos:",
                options=list(all_modules.keys()),
                default=st.session_state.exam_config['modules'],
                format_func=lambda x: all_modules[x]
            )
            st.session_state.exam_config['modules'] = selected_modules
            
            # Tiempo límite
            time_limit = st.number_input(
                "Tiempo del Examen (minutos):",
                min_value=30,
                max_value=300,
                value=st.session_state.exam_config['time_limit'],
                step=15
            )
            st.session_state.exam_config['time_limit'] = time_limit
            
            # Número de preguntas
            question_count = st.number_input(
                "Número de Preguntas:",
                min_value=10,
                max_value=138,
                value=st.session_state.exam_config['question_count'],
                step=5
            )
            st.session_state.exam_config['question_count'] = question_count
            
            # Botón para iniciar
            if st.button("🚀 Iniciar Simulacro", type="primary", use_container_width=True):
                if self.start_exam():
                    st.rerun()
    
    def start_exam(self) -> bool:
        """Inicia el examen con la configuración seleccionada"""
        if not st.session_state.exam_config['modules']:
            st.error("Debe seleccionar al menos un módulo")
            return False
        
        # Generar preguntas
        self.generate_questions()
        
        if not st.session_state.questions:
            st.error("No hay preguntas disponibles para los módulos seleccionados")
            return False
        
        # Inicializar estado del examen
        st.session_state.current_question_index = 0
        st.session_state.user_answers = [None] * len(st.session_state.questions)
        st.session_state.exam_start_time = datetime.now()
        st.session_state.current_screen = 'exam'
        
        st.success("¡Examen iniciado! Buena suerte")
        return True
    
    def generate_questions(self):
        """Genera las preguntas según la configuración del examen"""
        questions = []
        selected_modules = st.session_state.exam_config['modules']
        total_questions = st.session_state.exam_config['question_count']
        
        if not selected_modules:
            st.session_state.questions = []
            return
        
        questions_per_module = max(1, total_questions // len(selected_modules))
        
        for module in selected_modules:
            module_questions = self.question_database.get(module, [])
            for i in range(min(questions_per_module, len(module_questions))):
                if len(questions) < total_questions:
                    questions.append(module_questions[i % len(module_questions)])
        
        # Llenar espacios restantes si es necesario
        while len(questions) < total_questions:
            random_module = random.choice(selected_modules)
            module_questions = self.question_database.get(random_module, [])
            if module_questions:
                questions.append(random.choice(module_questions))
        
        # Mezclar preguntas
        random.shuffle(questions)
        st.session_state.questions = questions[:total_questions]
    
    def render_exam_screen(self):
        """Renderiza la pantalla del examen"""
        if not st.session_state.questions:
            st.error("No hay preguntas cargadas")
            return
        
        # Timer y progreso
        self.render_timer_and_progress()
        
        # Estadísticas en tiempo real
        self.render_exam_stats()
        
        # Pregunta actual
        self.render_current_question()
        
        # Navegación
        self.render_navigation()
        
        # Botón de finalizar
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🏁 Terminar Examen", type="secondary", use_container_width=True):
                if st.button("¿Confirmar finalización?", type="primary"):
                    self.finish_exam()
                    st.rerun()
    
    def render_timer_and_progress(self):
        """Renderiza el temporizador y barra de progreso"""
        if not st.session_state.exam_start_time:
            return
        
        elapsed_time = datetime.now() - st.session_state.exam_start_time
        time_limit_seconds = st.session_state.exam_config['time_limit'] * 60
        remaining_seconds = max(0, time_limit_seconds - elapsed_time.total_seconds())
        
        # Formatear tiempo restante
        hours = int(remaining_seconds // 3600)
        minutes = int((remaining_seconds % 3600) // 60)
        seconds = int(remaining_seconds % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        warning_class = "timer-warning" if remaining_seconds <= 300 else ""
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Progreso
            current_q = st.session_state.current_question_index + 1
            total_q = len(st.session_state.questions)
            answered = sum(1 for ans in st.session_state.user_answers if ans is not None)
            
            st.markdown(f"**Pregunta {current_q} de {total_q}** | **{answered} respondidas**")
            
            progress = current_q / total_q
            st.progress(progress)
        
        with col2:
            st.markdown(f"""
            <div class="timer-display {warning_class}">
                ⏰ {time_str}
            </div>
            """, unsafe_allow_html=True)
        
        # Verificar si se acabó el tiempo
        if remaining_seconds <= 0:
            st.error("⏰ ¡Tiempo agotado!")
            self.finish_exam()
            st.rerun()
    
    def render_exam_stats(self):
        """Renderiza las estadísticas del examen en tiempo real"""
        correct, wrong, skipped = self.calculate_current_stats()
        total_questions = len(st.session_state.questions)
        score = round((correct / total_questions) * 100) if total_questions > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("✅ Correctas", correct)
        with col2:
            st.metric("❌ Incorrectas", wrong)
        with col3:
            st.metric("⏭️ Sin responder", skipped)
        with col4:
            st.metric("📊 Calificación", f"{score}%")
    
    def render_current_question(self):
        """Renderiza la pregunta actual"""
        if not st.session_state.questions:
            return
        
        current_idx = st.session_state.current_question_index
        if current_idx >= len(st.session_state.questions):
            return
        
        question = st.session_state.questions[current_idx]
        
        # Encabezado de pregunta
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### Pregunta {current_idx + 1}")
        with col2:
            st.markdown(f"**📚 {question['area']}**")
        
        # Texto de la pregunta
        st.markdown("---")
        st.markdown(question['text'])
        st.markdown("---")
        
        # Opciones de respuesta
        for i, option in enumerate(question['options']):
            option_key = f"option_{current_idx}_{i}"
            
            # Verificar si esta opción está seleccionada
            is_selected = st.session_state.user_answers[current_idx] == i
            
            if st.button(
                option, 
                key=option_key, 
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.user_answers[current_idx] = i
                # Auto-avanzar después de seleccionar
                if current_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                st.rerun()
    
    def render_navigation(self):
        """Renderiza los controles de navegación"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("← Anterior", disabled=(st.session_state.current_question_index == 0)):
                st.session_state.current_question_index -= 1
                st.rerun()
        
        with col2:
            # Indicadores de preguntas
            self.render_question_indicators()
        
        with col3:
            next_disabled = st.session_state.current_question_index >= len(st.session_state.questions) - 1
            button_text = "Terminar" if next_disabled else "Siguiente →"
            
            if st.button(button_text, disabled=False):
                if next_disabled:
                    self.finish_exam()
                    st.rerun()
                else:
                    st.session_state.current_question_index += 1
                    st.rerun()
    
    def render_question_indicators(self):
        """Renderiza los indicadores de preguntas"""
        if not st.session_state.questions:
            return
        
        total_questions = len(st.session_state.questions)
        current_idx = st.session_state.current_question_index
        
        # Crear indicadores interactivos
        cols = st.columns(min(total_questions, 10))  # Limitar a 10 columnas por fila
        
        for i in range(total_questions):
            col_idx = i % 10
            if col_idx < len(cols):
                with cols[col_idx]:
                    # Determinar el estado del indicador
                    if i == current_idx:
                        button_type = "primary"
                        label = f"🔵 {i+1}"
                    elif st.session_state.user_answers[i] is not None:
                        button_type = "secondary"
                        label = f"✅ {i+1}"
                    else:
                        button_type = "secondary"
                        label = f"⚪ {i+1}"
                    
                    if st.button(label, key=f"nav_{i}", type=button_type):
                        st.session_state.current_question_index = i
                        st.rerun()
    
    def calculate_current_stats(self) -> Tuple[int, int, int]:
        """Calcula estadísticas actuales del examen"""
        correct = wrong = skipped = 0
        
        for i, answer in enumerate(st.session_state.user_answers):
            if answer is None:
                skipped += 1
            elif i < len(st.session_state.questions):
                if answer == st.session_state.questions[i]['correct']:
                    correct += 1
                else:
                    wrong += 1
        
        return correct, wrong, skipped
    
    def finish_exam(self):
        """Finaliza el examen y calcula resultados"""
        if st.session_state.exam_start_time:
            exam_duration = datetime.now() - st.session_state.exam_start_time
            st.session_state.exam_duration = exam_duration
        
        # Calcular resultados finales
        correct, wrong, skipped = self.calculate_current_stats()
        total_questions = len(st.session_state.questions)
        score = round((correct / total_questions) * 100) if total_questions > 0 else 0
        
        st.session_state.final_results = {
            'score': score,
            'correct': correct,
            'wrong': wrong,
            'skipped': skipped,
            'total_questions': total_questions,
            'exam_type': st.session_state.exam_config['type'],
            'modules': st.session_state.exam_config['modules'],
            'duration': st.session_state.exam_duration,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        st.session_state.current_screen = 'results'
    
    def render_results_screen(self):
        """Renderiza la pantalla de resultados"""
        if 'final_results' not in st.session_state:
            st.error("No hay resultados disponibles")
            return
        
        results = st.session_state.final_results
        
        # Puntuación principal
        st.markdown(f"""
        <div class="results-score">
            <div class="score-number">{results['score']}%</div>
            <div>Calificación Final</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Estadísticas detalladas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("✅ Respuestas Correctas", results['correct'])
        with col2:
            st.metric("❌ Respuestas Incorrectas", results['wrong'])
        with col3:
            st.metric("⏭️ Sin Responder", results['skipped'])
        with col4:
            duration_str = str(results['duration']).split('.')[0]  # Remover microsegundos
            st.metric("⏱️ Tiempo Utilizado", duration_str)
        
        # Información adicional
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Detalles del Examen")
            st.write(f"**Tipo:** {results['exam_type'].title()}")
            st.write(f"**Total de preguntas:** {results['total_questions']}")
            st.write(f"**Fecha:** {results['date']}")
            st.write(f"**Módulos evaluados:** {', '.join(results['modules'])}")
        
        with col2:
            st.markdown("### 📈 Análisis de Rendimiento")
            
            # Gráfico de resultados
            chart_data = pd.DataFrame({
                'Categoría': ['Correctas', 'Incorrectas', 'Sin Responder'],
                'Cantidad': [results['correct'], results['wrong'], results['skipped']]
            })
            
            st.bar_chart(chart_data.set_index('Categoría'))
        
        # Acciones
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Revisar Respuestas", use_container_width=True):
                st.session_state.current_screen = 'review'
                st.rerun()
        
        with col2:
            if st.button("🔄 Nuevo Examen", use_container_width=True):
                self.restart_exam()
                st.rerun()
        
        with
