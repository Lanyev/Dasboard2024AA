import streamlit as st
import plotly.express as px
import pandas as pd


def create_hero_analysis(filtered_data):
    """Genera un análisis visual de los héroes basado en las métricas seleccionadas."""

    st.markdown("### 🦸‍♂️ Análisis de Héroes")    # Obtener nombres de columnas relevantes
    numeric_columns = [
        "HeroDmg",
        "DmgTaken", 
        "XP",
        "Assists",
        "Deaths",
        "HeroKills",
        "Takedowns",
        "MinionDmg",
        "StructDmg",
        "SiegeDmg",
        "CC",
        "HealShield"
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
        # Usar índice seguro para las columnas por defecto
        default_x_index = 0
        if "HeroDmg" in valid_numeric_columns:
            default_x_index = valid_numeric_columns.index("HeroDmg")
        
        x_column = st.selectbox(
            "Eje X",
            options=valid_numeric_columns,
            index=default_x_index,
        )
        
        default_y_index = 0
        if "Assists" in valid_numeric_columns:
            default_y_index = valid_numeric_columns.index("Assists")
        
        y_column = st.selectbox(
            "Eje Y",
            options=valid_numeric_columns,
            index=default_y_index,
        )        # Validar que tenemos datos y columnas necesarias
        if len(filtered_data) == 0:
            st.warning("No hay datos disponibles con los filtros aplicados.")
            return
            
        required_columns = ["Winner", "Hero", x_column, y_column]
        missing_columns = [col for col in required_columns if col not in filtered_data.columns]
        
        if missing_columns:
            st.error(f"Columnas faltantes en los datos: {missing_columns}")
            st.info("Columnas disponibles: " + ", ".join(filtered_data.columns.tolist()))
            return
        
        # Asegurar que 'Winner' sea numérico (1 para victorias, 0 para derrotas)
        filtered_data["Winner"] = (filtered_data["Winner"] == "Winner").astype(int)

        # Construir diccionario de agregación dinámicamente
        agg_dict = {
            "Winner": lambda x: x.mean() * 100,  # Tasa de victoria en porcentaje
        }
        
        # Solo agregar columnas que existen
        numeric_cols_for_agg = [x_column, y_column, "HeroKills", "Assists", "Deaths"]
        for col in numeric_cols_for_agg:
            if col in filtered_data.columns:
                agg_dict[col] = "mean"        # Calcular estadísticas agregadas
        try:
            hero_aggregated_stats = (
                filtered_data.groupby("Hero")
                .agg(agg_dict)
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
            
        except Exception as e:
            st.error(f"Error en el análisis de héroes: {e}")
            st.info("Verificando datos disponibles...")
            if len(filtered_data) == 0:
                st.warning("No hay datos disponibles con los filtros aplicados.")
            else:
                st.info(f"Datos disponibles: {len(filtered_data)} filas")
                st.info(f"Columnas disponibles: {', '.join(filtered_data.columns)}")
            return

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
