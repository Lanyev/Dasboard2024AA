import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuración del tema y estilo
st.set_page_config(
    page_title="Alan Awards 2024",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Configuración de caché para mejorar el rendimiento
@st.cache_data
def load_data(selected_file):
    data = pd.read_csv(selected_file)
    data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    return data


# Estilos CSS mejorados con variables
st.markdown(
    """
    <style>
    :root {
        --primary-color: #FF4B4B;
        --bg-color: #1a1a1a;
        --secondary-bg: #2d2d2d;
        --text-color: #ffffff;
        --border-radius: 8px;
    }
    
    .main {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    .stButton button {
        background-color: var(--primary-color);
        color: var(--text-color);
        border-radius: var(--border-radius);
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    
    .custom-card {
        background-color: var(--secondary-bg);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .data-info {
        text-align: center;
        color: var(--text-color);
        font-style: italic;
        margin-bottom: 2rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def create_header(selected_year):
    st.markdown(
        """
        <h1 style='text-align: center; color: var(--primary-color); margin-bottom: 1rem;'>
            Alan Awards 2024
        </h1>
        <div class="data-info">
            Datos tomados del año {}
        </div>
    """.format(selected_year),
        unsafe_allow_html=True,
    )


def create_filters(data):
    filters = {}
    with st.sidebar:
        st.markdown("### 🎯 Filtros")

        # Selector de archivo CSV
        csv_file = st.selectbox(
            "Seleccionar conjunto de datos",
            options=["hots2024.csv", "hots2025.csv"],
            key="csv_selector"
        )
        filters["csv_file"] = csv_file

        # Filtro de fecha si existe
        if "Date" in data.columns:
            date_range = st.date_input(
                "Rango de Fechas",
                value=(data["Date"].min(), data["Date"].max()),
                key="date_filter",
            )
            filters["Date"] = date_range

        # Agrupación de filtros por categoría
        with st.expander("Filtros de Jugador", expanded=False):
            if "Player" in data.columns:
                filters["Player"] = st.multiselect(
                    "Jugadores", options=sorted(data["Player"].unique())
                )

            if "Role" in data.columns:
                filters["Role"] = st.multiselect(
                    "Roles", options=sorted(data["Role"].unique())
                )

        with st.expander("Filtros de Partida", expanded=False):
            if "Map" in data.columns:
                filters["Map"] = st.multiselect(
                    "Mapas", options=sorted(data["Map"].unique())
                )

            if "Hero" in data.columns:
                filters["Hero"] = st.multiselect(
                    "Héroes", options=sorted(data["Hero"].unique())
                )

    return filters


[Rest of the code remains exactly the same until the main() function]


def main():
    # Selector de archivo CSV en la barra lateral
    with st.sidebar:
        selected_file = st.selectbox(
            "Seleccionar conjunto de datos",
            options=["hots2024.csv", "hots2025.csv"],
            key="csv_selector"
        )
    
    # Determinar el año seleccionado para el encabezado
    selected_year = "2024" if selected_file == "hots2024.csv" else "2025"
    
    create_header(selected_year)

    # Carga de datos
    with st.spinner("Cargando datos..."):
        original_data = load_data(selected_file)

    # Creación y aplicación de filtros
    filters = create_filters(original_data)
    filtered_data = apply_filters(original_data, filters)

    # Visualizaciones
    create_metrics(filtered_data, original_data)

    # Crear tabs para las diferentes secciones de análisis
    tab1, tab2, tab3 = st.tabs(["📊 Análisis General", "🏆 Rankings", "📈 Tendencias"])

    with tab1:
        create_hero_analysis(filtered_data)

    with tab2:
        create_rankings(filtered_data)

    with tab3:
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