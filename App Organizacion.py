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
    st.session_state.tareas = [
        {"materia": "Cálculo III", "tarea": "Resolver lista de ejercicios 4", "fecha": str(date.today()), "completada": False},
        {"materia": "Física II", "tarea": "Informe de laboratorio de calor", "fecha": str(date.today()), "completada": False}
    ]

if 'materia_activa' not in st.session_state:
    st.session_state.materia_activa = None

# ==================== BARRA LATERAL (NAVEGACIÓN) ====================
st.sidebar.title("📚 StudyFlow")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Menú Principal", ["📖 Gestión por Materias", "📅 Calendario Mensual", "✅ Todas las Tareas"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Haz clic en una materia para ver sus temas y tareas.")

# ==================== 1. GESTIÓN POR MATERIAS ====================
if menu == "📖 Gestión por Materias":
    
    # Vista Principal: Lista de Materias y opción de agregar/eliminar
    if st.session_state.materia_activa is None:
        st.title("Gestión de Materias")
        st.markdown("Selecciona una materia para entrar a sus detalles o administra tu lista.")

        col_izq, col_der = st.columns([1, 1], gap="large")

        with col_izq:
            st.subheader("Tus Materias")
            if st.session_state.materias:
                for mat in st.session_state.materias:
                    c1, c2 = st.columns([0.7, 0.3])
                    with c1:
                        if st.button(f"📖 {mat}", key=f"btn_ver_{mat}", use_container_width=True):
                            st.session_state.materia_activa = mat
                            st.rerun()
                    with c2:
                        if st.button("🗑️ Borrar", key=f"btn_del_mat_{mat}", use_container_width=True):
                            st.session_state.materias.remove(mat)
                            if mat in st.session_state.temas:
                                del st.session_state.temas[mat]
                            st.session_state.tareas = [t for t in st.session_state.tareas if t['materia'] != mat]
                            st.rerun()
            else:
                st.info("No hay materias registradas.")

        with col_der:
            st.subheader("Agregar Nueva Materia")
            nueva_materia = st.text_input("Nombre de la materia", placeholder="Ej. Química")
            if st.button("Guardar Materia", use_container_width=True):
                if nueva_materia and nueva_materia not in st.session_state.materias:
                    st.session_state.materias.append(nueva_materia)
                    st.session_state.temas[nueva_materia] = []
                    st.success(f"Materia '{nueva_materia}' agregada.")
                    st.rerun()
                elif not nueva_materia:
                    st.warning("Escribe un nombre válido.")
                else:
                    st.warning("Esa materia ya existe.")

    # Vista Detallada de la Materia Seleccionada
    else:
        mat_actual = st.session_state.materia_activa
        
        if st.button("← Volver a la lista de materias"):
            st.session_state.materia_activa = None
            st.rerun()

        st.title(f"Detalles de: {mat_actual}")
        
        tab_temas, tab_tareas_mat = st.tabs(["📚 Temas de Estudio", "📝 Tareas de la Materia"])

        with tab_temas:
            st.subheader(f"Nuevo tema para {mat_actual}")
            nuevo_tema = st.text_input("Nombre del tema", key="input_tema_val")
            if st.button("Añadir Tema"):
                if nuevo_tema:
                    st.session_state.temas[mat_actual].append(nuevo_tema)
                    st.success("Tema agregado con éxito.")
                    st.rerun()
            
            st.markdown("### Temas registrados:")
            temas_lista = st.session_state.temas.get(mat_actual, [])
            if temas_lista:
                for idx, t in enumerate(temas_lista):
                    c_t1, c_t2 = st.columns([0.85, 0.15])
                    with c_t1:
                        st.markdown(f"- 📌 {t}")
                    with c_t2:
                        if st.button("🗑️", key=f"del_tema_{mat_actual}_{idx}", use_container_width=True):
                            st.session_state.temas[mat_actual].pop(idx)
                            st.rerun()
            else:
                st.info("No hay temas registrados para esta materia.")

        with tab_tareas_mat:
            st.subheader(f"Nueva tarea para {mat_actual}")
            desc_tarea = st.text_input("Descripción de la tarea", key="input_desc_tarea_val")
            fecha_tarea = st.date_input("Fecha límite", key="input_fecha_tarea_val")
            
            if st.button("Añadir Tarea a la Materia"):
                if desc_tarea:
                    st.session_state.tareas.append({
                        "materia": mat_actual,
                        "tarea": desc_tarea,
                        "fecha": str(fecha_tarea),
                        "completada": False
                    })
                    st.success("Tarea guardada correctamente.")
                    st.rerun()
            
            st.markdown("### Tareas de esta materia:")
            tareas_mat = [t for t in st.session_state.tareas if t['materia'] == mat_actual]
            if tareas_mat:
                for idx, t in enumerate(tareas_mat):
                    c_tm1, c_tm2, c_tm3 = st.columns([0.6, 0.25, 0.15])
                    with c_tm1:
                        st.markdown(f"- {t['tarea']}")
                    with c_tm2:
                        st.markdown(f"📅 {t['fecha']}")
                    with c_tm3:
                        if st.button("🗑️", key=f"del_mat_tarea_{idx}", use_container_width=True):
                            st.session_state.tareas.remove(t)
                            st.rerun()
            else:
                st.info("No hay tareas registradas para esta materia.")

# ==================== 2. CALENDARIO MENSUAL ====================
elif menu == "📅 Calendario Mensual":
    st.title("Calendario Mensual Interactivo")
    st.markdown("Selecciona una fecha para consultar qué tareas y pendientes tienes programados para ese día.")

    fecha_seleccionada = st.date_input("Selecciona un día en el calendario:", value=date.today())
    fecha_str = str(fecha_seleccionada)

    st.markdown(f"### 📋 Tareas para el día: **{fecha_str}**")

    tareas_del_dia = [t for t in st.session_state.tareas if t['fecha'] == fecha_str]

    if tareas_del_dia:
        for t in tareas_del_dia:
            estado_emoji = "✅" if t['completada'] else "⏳"
            st.markdown(f"""
            <div style="background-color: #161b22; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #58a6ff;">
                <b>{t['materia']}</b>: {t['tarea']} &nbsp;&nbsp; <i>({estado_emoji})</i>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay tareas programadas para este día específico.")

# ==================== 3. TODAS LAS TAREAS ====================
elif menu == "✅ Todas las Tareas":
    st.title("Vista General de Tareas")
    st.markdown("Tus tareas ordenadas automáticamente por proximidad de fecha de vencimiento.")

    if st.session_state.tareas:
        tareas_ordenadas = sorted(st.session_state.tareas, key=lambda x: x['fecha'])

        for idx, t in enumerate(tareas_ordenadas):
            col_check, col_info, col_fecha, col_del = st.columns([0.08, 0.55, 0.22, 0.15])
            
            with col_check:
                completada = st.checkbox("", value=t['completada'], key=f"chk_all_{idx}")
                original_idx = st.session_state.tareas.index(t)
                st.session_state.tareas[original_idx]['completada'] = completada

            with col_info:
                estilo = "text-decoration: line-through; color: gray;" if completada else ""
                nombre_materia = t.get('materia', 'Materia')
                st.markdown(f"<span style='{estilo}'><b>[{nombre_materia}]</b> {t['tarea']}</span>", unsafe_allow_html=True)

            with col_fecha:
                st.markdown(f"<span style='color: #8b949e; font-size: 0.9em;'>📅 {t['fecha']}</span>", unsafe_allow_html=True)

            with col_del:
                if st.button("🗑️", key=f"del_tarea_all_{idx}", use_container_width=True):
                    st.session_state.tareas.pop(original_idx)
                    st.rerun()
    else:
        st.info("¡Felicidades! No tienes ninguna tarea registrada por ahora.")
