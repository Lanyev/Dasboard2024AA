import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from .explanations import create_explanation_section


def create_hero_rankings(filtered_data):
    st.markdown("### 🏆 Rankings de Héroes (Top 5 y Bottom 5)")
    
    # Crear una copia y convertir columnas de tiempo
    df = filtered_data.copy()
    time_columns = ["SpentDead", "GameTime"]
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col])

    # Métricas curadas y relevantes para rankings de héroes
    key_metrics = {
        "HeroDamage": "Daño a Héroes",
        "HeroKills": "Asesinatos",
        "Assists": "Asistencias", 
        "Takedowns": "Takedowns",
        "Deaths": "Muertes",
        "DamageTaken": "Daño Recibido",
        "Experience": "Experiencia",
        "HealingShielding": "Curación/Escudos",
        "StructureDamage": "Daño a Estructuras",
        "SelfHealing": "Auto-curación",
        "HeroLevel": "Nivel de Héroe",
        "MercCampCaptures": "Capturas de Mercenarios",
        "TownKills": "Asesinatos en Ciudad"
    }
    
    # Filtrar métricas que realmente existen en el dataset
    available_metrics = {k: v for k, v in key_metrics.items() if k in df.columns}
    
    if not available_metrics:
        st.warning("No hay métricas disponibles para crear rankings de héroes")
        return

    # Selector de métrica
    col1, col2 = st.columns(2)
    with col1:
        selected_metric = st.selectbox(
            "Selecciona una métrica:", 
            list(available_metrics.keys()),
            format_func=lambda x: available_metrics[x],
            key="hero_metric"
        )
    with col2:
        aggregation = st.selectbox("Agregación:", ["Promedio", "Total", "Máximo"], key="hero_agg")

    if len(df) == 0:
        st.warning("No hay datos para mostrar")
        return

    # Agrupar por héroe y calcular estadísticas
    hero_col = "HeroName" if "HeroName" in df.columns else "Hero"
    if aggregation == "Promedio":
        stats = df.groupby(hero_col)[selected_metric].mean().sort_values(ascending=False)
    elif aggregation == "Total":
        stats = df.groupby(hero_col)[selected_metric].sum().sort_values(ascending=False)
    else:  # Máximo
        stats = df.groupby(hero_col)[selected_metric].max().sort_values(ascending=False)

    # Crear dos columnas para Top 5 y Bottom 5
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🥇 Top 5 Héroes - {available_metrics.get(selected_metric, selected_metric)}")
        top_5 = stats.head(5).reset_index()
        
        if len(top_5) > 0:
            # Crear gráfico de barras para Top 5
            fig_top = px.bar(
                top_5,
                x=hero_col,
                y=selected_metric,
                title=f"Top 5 Héroes - {available_metrics.get(selected_metric, selected_metric)} ({aggregation})",
                color=selected_metric,
                color_continuous_scale="Viridis",
                template="plotly_white"
            )
            fig_top.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_top, use_container_width=True)
            
            # Mostrar tabla
            st.dataframe(top_5.style.highlight_max(axis=0), use_container_width=True)

    with col2:
        st.markdown(f"#### 📉 Bottom 5 Héroes - {available_metrics.get(selected_metric, selected_metric)}")
        bottom_5 = stats.tail(5).reset_index()
        
        if len(bottom_5) > 0:
            # Crear gráfico de barras para Bottom 5
            fig_bottom = px.bar(
                bottom_5,
                x=hero_col,
                y=selected_metric,
                title=f"Bottom 5 Héroes - {available_metrics.get(selected_metric, selected_metric)} ({aggregation})",
                color=selected_metric,
                color_continuous_scale="Reds",
                template="plotly_white"
            )
            fig_bottom.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_bottom, use_container_width=True)
            
            # Mostrar tabla
            st.dataframe(bottom_5.style.highlight_min(axis=0), use_container_width=True)

    # Mostrar estadísticas generales
    st.markdown("### 📊 Estadísticas Generales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Héroes", len(stats))
    
    with col2:
        promedio = stats.mean()
        if hasattr(promedio, 'total_seconds'):
            # Si es un timedelta, convertir a minutos y segundos
            total_seconds = int(promedio.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            metric_str = f"{minutes}m {seconds}s"
        else:
            metric_str = f"{promedio:.2f}"
        st.metric(f"Promedio {available_metrics.get(selected_metric, selected_metric)}", metric_str)
    
    with col3:
        std_dev = stats.std()
        if hasattr(std_dev, 'total_seconds'):
            # Si es un timedelta, convertir a minutos y segundos
            total_seconds = int(std_dev.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            metric_str = f"{minutes}m {seconds}s"
        else:
            metric_str = f"{std_dev:.2f}"
        st.metric(f"Desviación Estándar", metric_str)

    # Añadir explicación detallada al final
    st.markdown("---")
    create_explanation_section('rankings_heroes')
