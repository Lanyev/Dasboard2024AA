import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_advanced_metrics_dashboard(filtered_data):
    """Dashboard de métricas avanzadas y KPIs profesionales"""
    st.header("🔬 Métricas Avanzadas")
    
    if filtered_data.empty:
        st.warning("No hay datos disponibles con los filtros aplicados.")
        return
    
    # Métricas de eficiencia
    st.subheader("📊 Métricas de Eficiencia")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_damage_per_min = filtered_data['HeroDmg'].mean() / (filtered_data['GameTime'].dt.total_seconds().mean() / 60)
        st.metric("Daño por Minuto", f"{avg_damage_per_min:.0f}")
    
    with col2:
        avg_healing_per_min = filtered_data['HealShield'].mean() / (filtered_data['GameTime'].dt.total_seconds().mean() / 60)
        st.metric("Curación por Minuto", f"{avg_healing_per_min:.0f}")
    
    with col3:
        kill_participation = (filtered_data['Takedowns'].sum() / filtered_data['Deaths'].sum()) if filtered_data['Deaths'].sum() > 0 else 0
        st.metric("Ratio K/D Global", f"{kill_participation:.2f}")
    
    with col4:
        avg_xp_per_min = filtered_data['XP'].mean() / (filtered_data['GameTime'].dt.total_seconds().mean() / 60)
        st.metric("XP por Minuto", f"{avg_xp_per_min:.0f}")
    
    # Análisis de correlaciones
    st.subheader("🔗 Análisis de Correlaciones")
    
    numeric_cols = ['HeroDmg', 'DmgTaken', 'HealShield', 'XP', 'Takedowns', 'Deaths']
    available_cols = [col for col in numeric_cols if col in filtered_data.columns]
    
    if len(available_cols) >= 2:
        correlation_matrix = filtered_data[available_cols].corr()
        
        fig = px.imshow(correlation_matrix, 
                       text_auto=True, 
                       aspect="auto",
                       color_continuous_scale='RdBu',
                       title="Matriz de Correlación de Métricas")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top performers por categoría
    st.subheader("🏅 Top Performers por Categoría")
    
    categories = {
        'Daño a Héroes': 'HeroDmg',
        'Curación': 'HealShield', 
        'Experiencia': 'XP',
        'Takedowns': 'Takedowns'
    }
    
    cols = st.columns(len(categories))
    
    for idx, (category, column) in enumerate(categories.items()):
        if column in filtered_data.columns:
            with cols[idx]:
                top_player = filtered_data.loc[filtered_data[column].idxmax()]
                st.metric(
                    label=f"👑 {category}",
                    value=f"{top_player[column]:,.0f}",
                    delta=f"{top_player['Player']} ({top_player['Hero']})"
                )


def create_exploration_dashboard(filtered_data):
    """Dashboard de exploración de datos"""
    st.header("🔍 Exploración de Datos")
    
    if filtered_data.empty:
        st.warning("No hay datos disponibles con los filtros aplicados.")
        return
    
    # Distribuciones
    st.subheader("📈 Distribuciones de Métricas")
    
    numeric_columns = ['HeroDmg', 'DmgTaken', 'HealShield', 'XP', 'Takedowns', 'Deaths']
    available_columns = [col for col in numeric_columns if col in filtered_data.columns]
    
    if available_columns:
        selected_metric = st.selectbox("Selecciona una métrica:", available_columns)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma
            fig_hist = px.histogram(filtered_data, x=selected_metric, 
                                  title=f"Distribución de {selected_metric}",
                                  nbins=30)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = px.box(filtered_data, y=selected_metric,
                           title=f"Box Plot de {selected_metric}")
            st.plotly_chart(fig_box, use_container_width=True)
    
    # Análisis por roles
    if 'Role' in filtered_data.columns:
        st.subheader("🎭 Análisis por Roles")
        
        role_stats = filtered_data.groupby('Role').agg({
            'HeroDmg': 'mean',
            'DmgTaken': 'mean', 
            'HealShield': 'mean',
            'XP': 'mean'
        }).round(0)
        
        st.dataframe(role_stats, use_container_width=True)


def create_composition_analysis(filtered_data):
    """Análisis de composiciones de equipo"""
    st.header("📋 Análisis de Composiciones")
    
    if filtered_data.empty:
        st.warning("No hay datos disponibles con los filtros aplicados.")
        return
    
    # Análisis de roles más comunes
    if 'Role' in filtered_data.columns:
        st.subheader("🎭 Distribución de Roles")
        
        role_counts = filtered_data['Role'].value_counts()
        
        fig = px.pie(values=role_counts.values, names=role_counts.index,
                    title="Distribución de Roles en las Partidas")
        st.plotly_chart(fig, use_container_width=True)
    
    # Héroes más populares
    st.subheader("🦸‍♂️ Héroes Más Utilizados")
    
    hero_popularity = filtered_data['Hero'].value_counts().head(10)
    
    fig = px.bar(x=hero_popularity.index, y=hero_popularity.values,
                title="Top 10 Héroes Más Utilizados",
                labels={'x': 'Héroe', 'y': 'Cantidad de Partidas'})
    fig.update_xaxis(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de win rates por héroe
    if 'Winner' in filtered_data.columns:
        st.subheader("🏆 Win Rates por Héroe")
        
        hero_winrates = filtered_data.groupby('Hero').agg({
            'Winner': lambda x: (x == 'Winner').mean() * 100
        }).round(1)
        hero_winrates.columns = ['Win Rate %']
        hero_winrates = hero_winrates.sort_values('Win Rate %', ascending=False)
        
        # Mostrar solo héroes con al menos 3 partidas
        hero_counts = filtered_data['Hero'].value_counts()
        hero_winrates_filtered = hero_winrates[hero_winrates.index.isin(hero_counts[hero_counts >= 3].index)]
        
        st.dataframe(hero_winrates_filtered.head(15), use_container_width=True)
