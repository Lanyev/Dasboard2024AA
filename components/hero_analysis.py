import streamlit as st
import plotly.express as px
import pandas as pd


def create_hero_analysis(filtered_data):
    """Genera un análisis visual de los héroes basado en las métricas seleccionadas."""

    st.markdown("### 🦸‍♂️ Análisis de Héroes")

    # Obtener nombres de columnas relevantes
    numeric_columns = [
        "HeroDmg",
        "Assists",
        "Deaths",
        "HeroKills",
        "Takedowns",
        "MinionDmg",
        "StructDmg",
    ]
    category_columns = ["Winner", "Hero", "Role"]

    # Validar si todas las columnas necesarias están en el DataFrame
    available_columns = filtered_data.columns.tolist()
    valid_numeric_columns = [col for col in numeric_columns if col in available_columns]

    if not valid_numeric_columns:
        st.warning(
            "No hay suficientes columnas numéricas disponibles para el análisis."
        )
        return

    col1, col2 = st.columns(2)

    with col1:
        x_column = st.selectbox(
            "Eje X",
            options=valid_numeric_columns,
            index=valid_numeric_columns.index("HeroDmg"),
        )
        y_column = st.selectbox(
            "Eje Y",
            options=valid_numeric_columns,
            index=valid_numeric_columns.index("Assists"),
        )

        # Asegurar que 'Winner' sea numérico (1 para victorias, 0 para derrotas)
        filtered_data["Winner"] = (filtered_data["Winner"] == "Winner").astype(int)

        # Calcular estadísticas agregadas
        hero_aggregated_stats = (
            filtered_data.groupby("Hero")
            .agg(
                {
                    "Winner": lambda x: x.mean()
                    * 100,  # Tasa de victoria en porcentaje
                    "HeroDmg": "mean",
                    "Assists": "mean",
                    "Deaths": "mean",
                    "HeroKills": "mean",
                }
            )
            .round(2)
        )

        # Generar gráfico de dispersión
        fig = px.scatter(
            hero_aggregated_stats.reset_index(),
            x=x_column,
            y=y_column,
            size="Assists",
            color="Winner",
            hover_name="Hero",
            title=f"Relación {x_column} vs. {y_column} por Héroe",
            template="plotly_dark",
            color_continuous_scale="greens",  # Escala de color más intuitiva
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "Role" in filtered_data.columns:
            role_hero_stats = (
                filtered_data.groupby(["Role", "Hero"])
                .agg(
                    {
                        "Winner": lambda x: x.mean() * 100,  # Convertir a porcentaje
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
                color_continuous_scale="greens",
            )
            st.plotly_chart(fig, use_container_width=True)
