import streamlit as st
import pandas as pd
import plotly.express as px
from .explanations import create_explanation_section


def create_rankings(filtered_data):
    st.markdown("### 🏆 Rankings Top 5 y Bottom 5")

    # Crear una copia y convertir columnas de tiempo
    df = filtered_data.copy()
    time_columns = ["SpentDead", "GameTime"]
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col])

    # Métricas curadas y relevantes para rankings
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
        st.warning("No hay métricas disponibles para crear rankings")
        return

    # Selector de métrica
    col1, col2 = st.columns(2)
    with col1:
        selected_metric = st.selectbox(
            "Selecciona una métrica:", 
            list(available_metrics.keys()),
            format_func=lambda x: available_metrics[x]
        )
    with col2:
        aggregation = st.selectbox("Agregación:", ["Promedio", "Total", "Máximo"])

    if len(df) == 0:
        st.warning("No hay datos para mostrar")
        return    # Verificar columnas disponibles
    player_col = "PlayerName" if "PlayerName" in df.columns else "Player"
    hero_col = "HeroName" if "HeroName" in df.columns else "Hero"
    
    # Agrupar por jugador y calcular estadísticas con información del héroe
    if aggregation == "Promedio":
        stats = df.groupby(player_col)[selected_metric].mean().sort_values(ascending=False)
        # Para obtener el héroe más usado por cada jugador en esta métrica
        hero_info = df.groupby([player_col, hero_col])[selected_metric].mean().reset_index()
        hero_info = hero_info.loc[hero_info.groupby(player_col)[selected_metric].idxmax()]
    elif aggregation == "Total":
        stats = df.groupby(player_col)[selected_metric].sum().sort_values(ascending=False)
        # Para obtener el héroe con mayor contribución total por jugador
        hero_info = df.groupby([player_col, hero_col])[selected_metric].sum().reset_index()
        hero_info = hero_info.loc[hero_info.groupby(player_col)[selected_metric].idxmax()]
    else:  # Máximo
        stats = df.groupby(player_col)[selected_metric].max().sort_values(ascending=False)
        # Para obtener el héroe con el valor máximo por jugador
        hero_info = df.loc[df.groupby(player_col)[selected_metric].idxmax()][[player_col, hero_col, selected_metric]]    # Crear dos columnas para Top 5 y Bottom 5
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### 🥇 Top 5 - {selected_metric}")
        top_5 = stats.head(5).reset_index()
        
        if len(top_5) > 0:
            # Agregar información del héroe
            top_5_with_hero = top_5.copy()
            hero_dict = dict(zip(hero_info[player_col], hero_info[hero_col]))
            top_5_with_hero['Héroe'] = top_5_with_hero[player_col].map(hero_dict)
            
            # Crear gráfico de barras para Top 5
            fig_top = px.bar(
                top_5_with_hero,
                x=player_col,
                y=selected_metric,
                title=f"Top 5 Jugadores - {selected_metric} ({aggregation})",
                color=selected_metric,
                color_continuous_scale="Blues",
                template="plotly_white",
                hover_data={'Héroe': True}        )
        fig_top.update_layout(height=400)
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Mostrar tabla con héroe
        display_cols = [player_col, 'Héroe', selected_metric]
        st.dataframe(
            top_5_with_hero[display_cols].style.highlight_max(axis=0), 
            use_container_width=True
        )

    with col2:
        st.markdown(f"#### 📉 Bottom 5 - {selected_metric}")
        bottom_5 = stats.tail(5).reset_index()
        
        if len(bottom_5) > 0:
            # Agregar información del héroe
            bottom_5_with_hero = bottom_5.copy()
            hero_dict = dict(zip(hero_info[player_col], hero_info[hero_col]))
            bottom_5_with_hero['Héroe'] = bottom_5_with_hero[player_col].map(hero_dict)
            
            # Crear gráfico de barras para Bottom 5
            fig_bottom = px.bar(
                bottom_5_with_hero,
                x=player_col,
                y=selected_metric,
                title=f"Bottom 5 Jugadores - {selected_metric} ({aggregation})",
                color=selected_metric,
                color_continuous_scale="Reds",
                template="plotly_white",
                hover_data={'Héroe': True}
            )
            fig_bottom.update_layout(height=400)
            st.plotly_chart(fig_bottom, use_container_width=True)
            
            # Mostrar tabla con héroe
            display_cols = [player_col, 'Héroe', selected_metric]
            st.dataframe(
                bottom_5_with_hero[display_cols].style.highlight_min(axis=0), 
                use_container_width=True
            )

    # Estadísticas generales
    st.markdown("#### 📊 Estadísticas Generales")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Jugadores", len(stats))
    
    with col2:
        if len(stats) > 0:
            st.metric(f"Promedio {selected_metric}", f"{stats.mean():.2f}")
    
    with col3:
        if len(stats) > 0:
            st.metric(f"Máximo {selected_metric}", f"{stats.max():.2f}")
    
    with col4:
        if len(stats) > 0:
            st.metric(f"Mínimo {selected_metric}", f"{stats.min():.2f}")

    # Añadir explicación detallada al final
    st.markdown("---")
    create_explanation_section('rankings_players')
