import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuración de la página en Modo Oscuro Minimalista
st.set_page_config(
    page_title="StudyFlow - Gestor Minimalista",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para forzar un Modo Oscuro elegante y limpio
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #161b22;
    }
    h1, h2, h3 {
        color: #f0f6fc !important;
    }
    .metric-card {
        background-color: #21262d;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# Simulación de Base de Datos en Memoria (Sesión de Streamlit)
if 'materias' not in st.session_state:
    st.session_state.materias = ["Cálculo III", "Física II", "Historia"]

if 'temas' not in st.session_state:
    st.session_state.temas = {
        "Cálculo III": ["Integrales Dobles", "Series de Fourier"],
        "Física II": ["Termodinámica", "Electromagnetismo"],
        "Historia": ["Revolución Industrial"]
    }

if 'tareas' not in st.session_state:
    # Estructura: Materia, Tarea, Fecha (YYYY-MM-DD), Estado
    st.session_state.tareas = [
        {"materia": "Cálculo III", "tarea": "Resolver lista de ejercicios 4", "fecha": str(date.today()), "completada": False},
        {"materia": "Física II", "tarea": "Informe de laboratorio de calor", "fecha": str(date.today()), "completada": False}
    ]

# ==================== BARRA LATERAL (NAVEGACIÓN) ====================
st.sidebar.title("📚 StudyFlow")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Menú Principal", ["📖 Gestión por Materias", "📅 Calendario Mensual", "✅ Todas las Tareas"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Consejo:** Para usarlo también en tu celular, ejecuta el comando con tu IP local o despliégalo gratis en Streamlit Cloud.")

# ==================== 1. GESTIÓN POR MATERIAS ====================
if menu == "📖 Gestión por Materias":
    st.title("Gestión de Materias, Temas y Tareas")
    st.markdown("Organiza tu contenido académico por materia de forma limpia y rápida.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Tus Materias")
        nueva_materia = st.text_input("Agregar nueva materia")
        if st.button("Guardar Materia", use_container_width=True):
            if nueva_materia and nueva_materia not in st.session_state.materias:
                st.session_state.materias.append(nueva_materia)
                st.session_state.temas[nueva_materia] = []
                st.success(f"Materia '{nueva_materia}' agregada.")
                st.rerun()

        materia_seleccionada = st.selectbox("Selecciona una materia para editar:", st.session_state.materias)

    with col2:
        if materia_seleccionada:
            st.subheader(f"Detalles de: {materia_seleccionada}")
            
            # Pestañas internas para Temas y Tareas de esa materia específica
            tab_temas, tab_tareas_mat = st.tabs(["📚 Temas de Estudio", "📝 Tareas de la Materia"])

            with tab_temas:
                nuevo_tema = st.text_input(f"Nuevo tema para {materia_seleccionada}", key="input_tema")
                if st.button("Añadir Tema"):
                    if nuevo_tema:
                        st.session_state.temas[materia_seleccionada].append(nuevo_tema)
                        st.success("Tema agregado con éxito.")
                        st.rerun()
                
                st.markdown("##### Temas registrados:")
                temas_lista = st.session_state.temas.get(materia_seleccionada, [])
                if temas_lista:
                    for t in temas_lista:
                        st.markdown(f"- 📌 {t}")
                else:
                    st.info("No hay temas registrados para esta materia.")

            with tab_tareas_mat:
                desc_tarea = st.text_input("Descripción de la tarea", key="input_desc_tarea")
                fecha_tarea = st.date_input("Fecha límite", key="input_fecha_tarea")
                
                if st.button("Añadir Tarea a la Materia"):
                    if desc_tarea:
                        st.session_state.tareas.append({
                            "materia": materia_seleccionada,
                            "tarea": desc_tarea,
                            "fecha": str(fecha_tarea),
                            "completada": False
                        })
                        st.success("Tarea guardada correctamente.")
                        st.rerun()

# ==================== 2. CALENDARIO MENSUAL ====================
elif menu == "📅 Calendario Mensual":
    st.title("Calendario Mensual Interactivo")
    st.markdown("Selecciona una fecha para consultar qué tareas y pendientes tienes programados para ese día.")

    fecha_seleccionada = st.date_input("Selecciona un día en el calendario:", value=date.today())
    fecha_str = str(fecha_seleccionada)

    st.markdown(f"### 📋 Tareas para el día: **{fecha_str}**")

    # Filtrar tareas que coincidan con la fecha seleccionada
    tareas_del_dia = [t for t in st.session_state.tareas if t['fecha'] == fecha_str]

    if tareas_del_dia:
        for idx, t in enumerate(tareas_del_dia):
            estado_emoji = "✅" if t['completada'] else "⏳"
            st.markdown(f"""
            <div style="background-color: #161b22; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #58a6ff;">
                <b>{t['materia']}</b>: {t['tarea']} &nbsp;&nbsp; <i>({estado_emoji})</i>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay tareas programadas para este día específico. ¡Día libre o excelente momento para repasar!")

# ==================== 3. TODAS LAS TAREAS ====================
elif menu == "✅ Todas las Tareas":
    st.title("Vista General de Tareas")
    st.markdown("Tus tareas ordenadas automáticamente por proximidad de fecha de vencimiento.")

    if st.session_state.tareas:
        # Ordenar tareas por fecha
        tareas_ordenadas = sorted(st.session_state.tareas, key=lambda x: x['fecha'])

        for idx, t in enumerate(tareas_ordenadas):
            col_check, col_info, col_fecha = st.columns([0.1, 0.7, 0.2])
            
            with col_check:
                # Checkbox para marcar completada
                completada = st.checkbox("", value=t['completada'], key=f"chk_{idx}")
                st.session_state.tareas[idx]['completada'] = completada

            with col_info:
                estilo = "text-decoration: line-through; color: gray;" if completada else ""
                st.markdown(f"<span style='{estilo}'><b>[{t['materia']}]</b> {t['tarea']}</span>", unsafe_allow_html=True)

            with col_fecha:
                st.markdown(f"<span style='color: #8b949e; font-size: 0.9em;'>📅 {t['fecha']}</span>", unsafe_allow_html=True)
    else:
        st.info("¡Felicidades! No tienes ninguna tarea registrada por ahora.")