import streamlit as st
from utils.data_loader import load_data
from components.header import create_header
from components.filters import create_filters, apply_filters
from components.metrics import create_metrics
from components.hero_analysis import create_hero_analysis
from components.rankings import create_rankings
from components.time_analysis import create_time_analysis
from utils.styles import apply_styles
from datetime import datetime


def main():
    # Configuración inicial
    st.set_page_config(
        page_title="Alan Awards 2024",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_styles()
    create_header()

    # Carga de datos
    with st.spinner("Cargando datos..."):
        original_data = load_data()

    # Creación y aplicación de filtros
    filters = create_filters(original_data)
    filtered_data = apply_filters(original_data, filters)

    # Visualizaciones
    create_metrics(filtered_data, original_data)

    # Manejo de pestañas usando un selectbox en la barra lateral
    tab_options = ["📊 Análisis General", "🏆 Rankings", "📈 Tendencias"]
    selected_tab = st.sidebar.radio("Selecciona una sección:", tab_options)

    # Mostrar el contenido según la pestaña activa
    if selected_tab == "📊 Análisis General":
        create_hero_analysis(filtered_data)
    elif selected_tab == "🏆 Rankings":
        create_rankings(filtered_data)
    elif selected_tab == "📈 Tendencias":
        create_time_analysis(filtered_data)

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: var(--secondary-bg); border-radius: var(--border-radius);'>
            <p>Dashboard actualizado: {}</p>
        </div>
    """.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
