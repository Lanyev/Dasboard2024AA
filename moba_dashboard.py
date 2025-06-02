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
    create_composition_analysis as create_comp_analysis_alt
)
from utils.styles import apply_styles
from datetime import datetime


def main():
    # Configuración inicial
    st.set_page_config(
        page_title="Heroes of the Storm Analytics",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Selector de dataset en la barra lateral
    st.sidebar.title("⚙️ Configuración")
    
    # Obtener datasets disponibles
    available_datasets = get_available_datasets()
    
    if not available_datasets:
        st.error("No se encontraron datasets disponibles")
        return
    
    # Selector de dataset
    selected_dataset_name = st.sidebar.selectbox(
        "📊 Selecciona el Dataset:",
        list(available_datasets.keys()),
        help="Cada dataset tiene un tema visual diferente"
    )
    
    selected_file = available_datasets[selected_dataset_name]
    
    # Determinar tema basado en el dataset seleccionado
    if "2025" in selected_file:
        theme = "temporada_2025"
        dashboard_title = "🆕 Heroes Analytics - Temporada 2025"
    else:
        theme = "alan_awards_2024"
        dashboard_title = "🏆 Alan Awards 2024 - Heroes Analytics"
    
    # Aplicar estilos según el tema
    apply_styles(theme)
    
    # Mostrar información del dataset seleccionado
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Dataset Activo:** {selected_dataset_name}")
    if theme == "temporada_2025":
        st.sidebar.markdown("🎨 **Tema:** Futurista 2025")
        st.sidebar.markdown("🔥 **Características:** Nuevos visuales y métricas avanzadas")
    else:
        st.sidebar.markdown("🎨 **Tema:** Clásico Alan Awards")
        st.sidebar.markdown("🏆 **Características:** Análisis completo de la temporada 2024")
    
    # Crear header dinámico
    create_header(dashboard_title)

    # Carga de datos
    with st.spinner("Cargando datos..."):
        original_data = load_data(selected_file)
    
    # Mostrar información básica del dataset
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total de Partidas", len(original_data))
    with col2:
        st.metric("👥 Jugadores Únicos", original_data['Player'].nunique())
    with col3:
        st.metric("🦸‍♂️ Héroes Únicos", original_data['Hero'].nunique())

    # Creación y aplicación de filtros
    filters = create_filters(original_data)
    filtered_data = apply_filters(original_data, filters)

    # Visualizaciones
    create_metrics(filtered_data, original_data)

    # Manejo de pestañas usando un selectbox en la barra lateral
    tab_options = [
        "📊 Análisis General",
        "🏆 Rankings de Players", 
        "🦸‍♂️ Rankings de Héroes",
        "📈 Tendencias",
        "🚀 Analytics Profesional",
        "🔍 Exploración de Datos",
        "📋 Análisis de Composiciones",
        "🎯 Métricas Avanzadas"
    ]
    selected_tab = st.sidebar.radio("Selecciona una sección:", tab_options)

    # Mostrar el contenido según la pestaña activa
    if selected_tab == "📊 Análisis General":
        create_hero_analysis(filtered_data)
    elif selected_tab == "🏆 Rankings de Players":
        create_rankings(filtered_data)
    elif selected_tab == "🦸‍♂️ Rankings de Héroes":
        create_hero_rankings(filtered_data)
    elif selected_tab == "📈 Tendencias":
        create_time_analysis(filtered_data)
    elif selected_tab == "🚀 Analytics Profesional":
        create_professional_analytics_dashboard(filtered_data)
    elif selected_tab == "🔍 Exploración de Datos":
        create_data_exploration(filtered_data)
    elif selected_tab == "📋 Análisis de Composiciones":
        create_composition_analysis(filtered_data)
    elif selected_tab == "🎯 Métricas Avanzadas":
        create_advanced_metrics_dashboard(filtered_data)

    # Footer dinámico
    footer_version = "v2.0.0" if theme == "temporada_2025" else "v1.1.0"
    footer_subtitle = "Temporada 2025 Edition" if theme == "temporada_2025" else "Alan Awards Edition"
    
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 3rem; padding: 2rem; background: var(--secondary-bg); border-radius: var(--border-radius); border-top: 3px solid var(--primary-color);'>
            <h4 style='color: var(--primary-color); margin: 0;'>Heroes of the Storm Analytics</h4>
            <p style='color: var(--text-color); margin: 0.5rem 0;'>{footer_subtitle}</p>
            <p style='color: var(--text-color); opacity: 0.7; margin: 0;'>
                Dashboard actualizado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {footer_version}
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Indicador visual del tema activo
    if theme == "temporada_2025":
        st.markdown(
            """
            <div style='
                background: var(--gradient-primary);
                padding: 1rem;
                border-radius: var(--border-radius);
                text-align: center;
                margin-bottom: 2rem;
                color: #0F1419;
                font-weight: 600;
            '>
                🚀 MODO FUTURISTA 2025 ACTIVADO 🚀
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style='
                background-color: var(--primary-color);
                padding: 1rem;
                border-radius: var(--border-radius);
                text-align: center;
                margin-bottom: 2rem;
                color: white;
                font-weight: 600;
            '>
                🏆 MODO ALAN AWARDS 2024 🏆
            </div>
            """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
