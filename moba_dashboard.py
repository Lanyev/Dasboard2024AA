import streamlit as st
from utils.data_loader import load_data, get_available_datasets
from components.header import create_header
from components.filters import create_filters, apply_filters
from components.metrics import create_metrics
from components.hero_analysis import create_hero_analysis
from components.rankings import create_rankings
from components.rankings_hero import create_hero_rankings
from components.time_analysis import create_time_analysis
from components.professional_analytics import create_professional_analytics_dashboard
from components.data_exploration import create_data_exploration
from components.composition_analysis import create_composition_analysis
from components.advanced_analytics import (
    create_advanced_metrics_dashboard,
    create_exploration_dashboard,
    create_advanced_composition_analysis as create_comp_analysis_alt
)
from components.team_composition_analysis import create_team_composition_analysis
from components.explanations import create_general_explanation
from datetime import datetime


def main():
    # Configuración inicial
    st.set_page_config(
        page_title="Heroes of the Storm Analytics",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Limpiar mensajes de footer previos
    if 'footer_messages' in st.session_state:
        st.session_state.footer_messages = []

    # Selector de dataset en la barra lateral
    st.sidebar.title("⚙️ Configuración")
    
    # Obtener datasets disponibles
    available_datasets = get_available_datasets()
    
    if not available_datasets:
        st.error("No se encontraron datasets disponibles")
        return
    
    # Selector de dataset con selectbox (diseño original)
    st.sidebar.markdown("### 📊 Selecciona Dataset")
    selected_dataset_name = st.sidebar.selectbox(
        "Dataset:",
        options=list(available_datasets.keys()),
        format_func=lambda x: x
    )
    
    # Obtener el archivo seleccionado
    selected_file = available_datasets[selected_dataset_name]
    
    # Determinar el título basado en el dataset seleccionado
    if "2025" in selected_file:
        dashboard_title = "🌟 Alan Awards 2025 Summer Edition"
    else:
        dashboard_title = "🏆 Alan Awards 2024 Complete"
    
    # Crear header dinámico
    create_header(dashboard_title)

    # Carga de datos
    with st.spinner("Cargando datos..."):
        original_data = load_data(selected_file)
    
    # Mostrar información básica del dataset
    col1, col2, col3 = st.columns(3)
    with col1:
        # Calcular partidas únicas basado en la columna File/FileName
        file_col = 'File' if 'File' in original_data.columns else 'FileName'
        if file_col in original_data.columns:
            unique_games = original_data[file_col].nunique()
        else:
            unique_games = len(original_data)
        st.metric("📊 Total de Partidas", unique_games)
    with col2:
        st.metric("👥 Jugadores Únicos", original_data['Player'].nunique())
    with col3:
        st.metric("🦸‍♂️ Héroes Únicos", original_data['Hero'].nunique())    # Creación y aplicación de filtros
    filters = create_filters(original_data)
    filtered_data = apply_filters(original_data, filters)

    # Agregar explicación general del dashboard
    st.sidebar.markdown("---")
    create_general_explanation()

    # Visualizaciones
    create_metrics(filtered_data, original_data)    # Manejo de pestañas usando un selectbox en la barra lateral
    tab_options = [
        "📊 Análisis General",
        "🏆 Rankings de Players", 
        "🦸‍♂️ Rankings de Héroes",
        "📈 Tendencias",
        "🚀 Analytics Profesional",
        "🔍 Exploración de Datos",
        "📋 Análisis de Composiciones",
        "🛡️ Composiciones de Equipo",
        "🎯 Métricas Avanzadas"    ]
    selected_tab = st.sidebar.radio("Selecciona una sección:", tab_options)

    # Mostrar el contenido según la pestaña activa
    if selected_tab == "📊 Análisis General":
        create_hero_analysis(filtered_data)
        # Explicación ya incluida en hero_analysis.py
    elif selected_tab == "🏆 Rankings de Players":
        create_rankings(filtered_data)
        # Explicación ya incluida en rankings.py
    elif selected_tab == "🦸‍♂️ Rankings de Héroes":
        create_hero_rankings(filtered_data)
        # Explicación ya incluida en rankings_hero.py
    elif selected_tab == "📈 Tendencias":
        create_time_analysis(filtered_data)
        # Explicación ya incluida en time_analysis.py
    elif selected_tab == "🚀 Analytics Profesional":
        create_professional_analytics_dashboard(filtered_data)
        from components.professional_analytics import add_professional_analytics_explanation
        add_professional_analytics_explanation()
    elif selected_tab == "🔍 Exploración de Datos":
        create_data_exploration(filtered_data)
        from components.data_exploration import add_data_exploration_explanation
        add_data_exploration_explanation()
    elif selected_tab == "📋 Análisis de Composiciones":
        create_composition_analysis(filtered_data)
        from components.composition_analysis import add_composition_analysis_explanation
        add_composition_analysis_explanation()
    elif selected_tab == "🛡️ Composiciones de Equipo":
        create_team_composition_analysis(filtered_data)
    elif selected_tab == "🎯 Métricas Avanzadas":
        create_advanced_metrics_dashboard(filtered_data)
        from components.advanced_analytics import add_advanced_analytics_explanation
        add_advanced_analytics_explanation()    # Footer simple
    st.markdown("---")
    st.markdown(
        f"**Heroes of the Storm Analytics** | "
        f"Dashboard actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    # Mostrar mensajes de optimización y advertencias al final
    if 'footer_messages' in st.session_state and st.session_state.footer_messages:
        st.markdown("### 📊 Información del Sistema")
        for message in st.session_state.footer_messages:
            if "⚠️" in message:
                st.warning(message)
            elif "🔧" in message:
                st.info(message)
            else:
                st.info(message)


if __name__ == "__main__":
    main()
