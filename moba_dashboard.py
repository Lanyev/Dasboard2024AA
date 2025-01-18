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
def load_data():
    data = pd.read_csv("hots_cleaned_data_modified.csv")
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
    """.format(
            selected_year
        ),
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
            key="csv_selector",
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


def apply_filters(data, filters):
    filtered_data = data.copy()

    for column, filter_vals in filters.items():
        if filter_vals:
            if column == "Date":
                filtered_data = filtered_data[
                    (filtered_data["Date"].dt.date >= filter_vals[0])
                    & (filtered_data["Date"].dt.date <= filter_vals[1])
                ]
            elif isinstance(filter_vals, (list, tuple)) and filter_vals:
                filtered_data = filtered_data[filtered_data[column].isin(filter_vals)]

    return filtered_data


def create_metrics(filtered_data, original_data):
    st.markdown("### 📊 Métricas Clave")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_games = len(filtered_data)
        st.metric(
            "Total Partidas",
            f"{total_games:,}",
            delta=f"{total_games - len(original_data):+,} filtradas",
        )

    with col2:
        avg_damage = filtered_data["HeroDmg"].mean()
        st.metric(
            "Daño Promedio",
            f"{avg_damage:,.0f}",
            delta=f"{(avg_damage - original_data['HeroDmg'].mean()):+,.0f}",
        )

    with col3:
        win_rate = (filtered_data["Winner"] == "Winner").mean() * 100
        st.metric(
            "Tasa de Victoria",
            f"{win_rate:.1f}%",
            delta=f"{win_rate - ((original_data['Winner'] == 'Winner').mean() * 100):+.1f}%",
        )

    with col4:
        avg_time = filtered_data["GameTime"].mean()
        st.metric("Tiempo Promedio", str(avg_time).split(".")[0], delta_color="off")


def create_hero_analysis(filtered_data):
    st.markdown("### 🦸‍♂️ Análisis de Héroes")

    col1, col2 = st.columns(2)

    with col1:
        # Winrate por héroe
        hero_stats = (
            filtered_data.groupby("Hero")
            .agg(
                {
                    "Winner": lambda x: (x == "Winner").mean() * 100,
                    "HeroDmg": "mean",
                    "Assists": "mean",
                }
            )
            .round(2)
        )

        fig = px.scatter(
            hero_stats.reset_index(),
            x="HeroDmg",
            y="Winner",
            size="Assists",
            color="Winner",
            hover_name="Hero",
            title="Relación Daño vs. Winrate por Héroe",
            template="plotly_dark",
            color_continuous_scale="RdYlBu",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top héroes por rol
        if "Role" in filtered_data.columns:
            role_hero_stats = (
                filtered_data.groupby(["Role", "Hero"])
                .agg(
                    {
                        "Winner": lambda x: (x == "Winner").mean() * 100,
                        "HeroDmg": "mean",
                    }
                )
                .round(2)
            )

            fig = px.treemap(
                role_hero_stats.reset_index(),
                path=[px.Constant("Todos"), "Role", "Hero"],
                values="HeroDmg",
                color="Winner",
                title="Distribución de Héroes por Rol",
                template="plotly_dark",
                color_continuous_scale="RdYlBu",
            )
            st.plotly_chart(fig, use_container_width=True)


def create_time_analysis(filtered_data):
    if "Date" in filtered_data.columns:
        st.markdown("### 📅 Análisis Temporal")

        col1, col2 = st.columns(2)

        with col1:
            # Tendencia de métricas en el tiempo
            daily_stats = (
                filtered_data.groupby("Date")
                .agg(
                    {
                        "HeroDmg": "mean",
                        "Assists": "mean",
                        "Winner": lambda x: (x == "Winner").mean() * 100,
                    }
                )
                .round(2)
            )

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=daily_stats.index,
                    y=daily_stats["HeroDmg"],
                    name="Daño",
                    line=dict(color="#FF4B4B"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=daily_stats.index,
                    y=daily_stats["Winner"],
                    name="Winrate",
                    yaxis="y2",
                    line=dict(color="#4B4BFF"),
                )
            )

            fig.update_layout(
                title="Tendencias Diarias",
                template="plotly_dark",
                yaxis2=dict(title="Winrate (%)", overlaying="y", side="right"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Distribución de partidas por hora del día
            if "Hour" in filtered_data.columns:
                hourly_games = filtered_data.groupby("Hour").size()

                fig = px.bar(
                    hourly_games,
                    title="Distribución de Partidas por Hora",
                    template="plotly_dark",
                    color=hourly_games.values,
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(fig, use_container_width=True)


def create_rankings(filtered_data):
    st.markdown("### 🏆 Rankings Top 5 y Bottom 5")

    # Crear una copia y convertir columnas de tiempo
    df = filtered_data.copy()
    time_columns = ["SpentDead", "GameTime"]
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col])

    # Obtener columnas numéricas
    exclude_columns = ["Hour", "Date"]
    numeric_columns = df.select_dtypes(
        include=["int64", "float64", "timedelta64"]
    ).columns
    numeric_columns = [col for col in numeric_columns if col not in exclude_columns]

    # Categorías de métricas
    metric_categories = {
        "Combate": ["HeroDmg", "SiegeDmg", "HeroKills", "Deaths", "Assists"],
        "Economía": ["XP", "MercCaptures"],
        "Objetivos": ["SpentDead", "GameTime"],
    }

    selected_category = st.selectbox(
        "Selecciona categoría de métricas", options=list(metric_categories.keys())
    )

    category_columns = [
        col for col in metric_categories[selected_category] if col in df.columns
    ]

    if category_columns:
        tabs = st.tabs(["Top 5", "Bottom 5"])

        with tabs[0]:  # Top 5
            for column in category_columns:
                st.markdown(f"#### 📈 Top 5 en {column}")

                # Obtener top 5
                top_5 = df.nlargest(5, column)[["Player", "Hero", "Role", column]]

                col1, col2 = st.columns([3, 1])
                with col1:
                    # Crear copia para visualización
                    plot_data = top_5.copy()
                    if pd.api.types.is_timedelta64_dtype(plot_data[column]):
                        plot_data[column] = plot_data[column].apply(
                            lambda x: str(x).split(".")[0]
                        )

                    fig = px.bar(
                        plot_data,
                        x="Player",
                        y=column,
                        color="Hero",
                        text=column,
                        title=f"Top 5 {column}",
                        template="plotly_dark",
                    )
                    fig.update_traces(texttemplate="%{text}", textposition="outside")
                    fig.update_layout(height=300, margin=dict(t=30, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Crear copia para tabla
                    table_data = top_5.copy()
                    if pd.api.types.is_timedelta64_dtype(table_data[column]):
                        table_data[column] = table_data[column].apply(
                            lambda x: str(x).split(".")[0]
                        )
                        st.dataframe(table_data, height=300)
                    else:
                        st.dataframe(
                            table_data.style.background_gradient(
                                cmap="Reds", subset=[column]
                            ).format({column: "{:.2f}"}),
                            height=300,
                        )

        with tabs[1]:  # Bottom 5
            for column in category_columns:
                st.markdown(f"#### 📉 Bottom 5 en {column}")

                # Obtener bottom 5
                bottom_5 = df.nsmallest(5, column)[["Player", "Hero", "Role", column]]

                col1, col2 = st.columns([3, 1])
                with col1:
                    # Crear copia para visualización
                    plot_data = bottom_5.copy()
                    if pd.api.types.is_timedelta64_dtype(plot_data[column]):
                        plot_data[column] = plot_data[column].apply(
                            lambda x: str(x).split(".")[0]
                        )

                    fig = px.bar(
                        plot_data,
                        x="Player",
                        y=column,
                        color="Hero",
                        text=column,
                        title=f"Bottom 5 {column}",
                        template="plotly_dark",
                    )
                    fig.update_traces(texttemplate="%{text}", textposition="outside")
                    fig.update_layout(height=300, margin=dict(t=30, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Crear copia para tabla
                    table_data = bottom_5.copy()
                    if pd.api.types.is_timedelta64_dtype(table_data[column]):
                        table_data[column] = table_data[column].apply(
                            lambda x: str(x).split(".")[0]
                        )
                        st.dataframe(table_data, height=300)
                    else:
                        st.dataframe(
                            table_data.style.background_gradient(
                                cmap="Blues", subset=[column]
                            ).format({column: "{:.2f}"}),
                            height=300,
                        )


def main():
    # Selector de archivo CSV en la barra lateral
    with st.sidebar:
        selected_file = st.selectbox(
            "Seleccionar conjunto de datos",
            options=["hots2024.csv", "hots2025.csv"],
            key="csv_selector",
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
