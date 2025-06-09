"""
Componente de análisis de composiciones de equipo para Heroes of the Storm
Analiza estadísticas de composiciones basadas en roles
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils.hero_roles import (
    get_hero_roles, get_all_roles, get_heroes_by_role, 
    classify_composition, get_composition_type, get_hero_role
)

def create_team_composition_analysis(data):
    """Crea la sección de análisis de composiciones de equipo"""
    
    st.header("🛡️ Análisis de Composiciones de Equipo")
    
    # Tabs para diferentes análisis
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Explorar Composiciones", 
        "📊 Estadísticas por Roles", 
        "🎯 Composición Personalizada",
        "📈 Tendencias de Meta"
    ])
    
    with tab1:
        explore_compositions(data)
    
    with tab2:
        role_statistics(data)
    
    with tab3:
        custom_composition_analysis(data)
    
    with tab4:
        meta_trends(data)

def explore_compositions(data):
    """Explora composiciones existentes en el dataset"""
    
    st.subheader("🔍 Explorar Composiciones Existentes")
    
    # Preparar datos con roles
    hero_roles = get_hero_roles()
    data_with_roles = data.copy()
    data_with_roles['Role'] = data_with_roles['Hero'].map(hero_roles)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_games = st.slider("Mínimo de partidas", 1, 100, 10)
    
    with col2:
        min_winrate = st.slider("Winrate mínimo (%)", 0, 100, 0)
    
    with col3:
        role_filter = st.multiselect(
            "Filtrar por roles",
            options=get_all_roles(),
            default=[]
        )
    
    # Analizar composiciones por partida
    if 'MatchID' in data.columns:
        match_compositions = analyze_match_compositions(data_with_roles)
        
        # Filtrar por criterios
        filtered_comps = match_compositions[
            (match_compositions['Games'] >= min_games) &
            (match_compositions['Winrate'] >= min_winrate/100)
        ]
        
        if role_filter:
            filtered_comps = filtered_comps[
                filtered_comps['Composition'].apply(
                    lambda x: any(role in x for role in role_filter)
                )
            ]
        
        # Mostrar resultados
        if not filtered_comps.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(
                    filtered_comps.head(20),
                    use_container_width=True
                )
            
            with col2:
                # Gráfico de winrates
                fig = px.histogram(
                    filtered_comps,
                    x='Winrate',
                    nbins=20,
                    title="Distribución de Winrates"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No se encontraron composiciones que cumplan los criterios.")
    else:
        st.info("Para análisis de composiciones completas se necesita información de MatchID.")
        show_role_distribution(data_with_roles)

def role_statistics(data):
    """Muestra estadísticas detalladas por roles"""
    
    st.subheader("📊 Estadísticas por Roles")
    
    # Preparar datos
    hero_roles = get_hero_roles()
    data_with_roles = data.copy()
    data_with_roles['Role'] = data_with_roles['Hero'].map(hero_roles)
    
    # Calcular estadísticas por rol
    role_stats = data_with_roles.groupby('Role').agg({
        'Kills': ['mean', 'std'],
        'Deaths': ['mean', 'std'],
        'Assists': ['mean', 'std'],
        'HeroDamage': ['mean', 'std'],
        'SiegeDamage': ['mean', 'std'],
        'Healing': ['mean', 'std'],
        'DamageTaken': ['mean', 'std'],
        'Experience': ['mean', 'std'],
        'PlayerName': 'count'
    }).round(2)
    
    # Aplanar columnas
    role_stats.columns = [f"{col[0]}_{col[1]}" for col in role_stats.columns]
    role_stats = role_stats.reset_index()
    role_stats['Games'] = role_stats['PlayerName_count']
    
    # Selector de métrica
    col1, col2 = st.columns([1, 3])
    
    with col1:
        metric = st.selectbox(
            "Seleccionar métrica",
            options=['Kills', 'Deaths', 'Assists', 'HeroDamage', 'SiegeDamage', 
                    'Healing', 'DamageTaken', 'Experience'],
            index=3
        )
    
    with col2:
        # Gráfico de barras por rol
        fig = px.bar(
            role_stats,
            x='Role',
            y=f'{metric}_mean',
            error_y=f'{metric}_std',
            title=f"Promedio de {metric} por Rol",
            color='Role'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.subheader("📋 Estadísticas Detalladas")
    
    display_stats = role_stats[[
        'Role', 'Games', 'Kills_mean', 'Deaths_mean', 'Assists_mean',
        'HeroDamage_mean', 'Healing_mean', 'DamageTaken_mean'
    ]].copy()
    
    display_stats.columns = [
        'Rol', 'Partidas', 'Kills (Prom)', 'Deaths (Prom)', 'Assists (Prom)',
        'Daño a Héroes (Prom)', 'Curación (Prom)', 'Daño Recibido (Prom)'
    ]
    
    st.dataframe(display_stats, use_container_width=True)
    
    # Análisis de KDA por rol
    st.subheader("⚔️ Análisis KDA por Rol")
    
    data_with_roles['KDA'] = (data_with_roles['Kills'] + data_with_roles['Assists']) / np.maximum(data_with_roles['Deaths'], 1)
    
    fig = px.box(
        data_with_roles,
        x='Role',
        y='KDA',
        title="Distribución de KDA por Rol"
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

def custom_composition_analysis(data):
    """Permite al usuario crear y analizar composiciones personalizadas"""
    
    st.subheader("🎯 Análisis de Composición Personalizada")
    
    st.write("Selecciona 5 héroes para analizar su composición:")
    
    # Preparar datos
    hero_roles = get_hero_roles()
    available_heroes = sorted([hero for hero in data['Hero'].unique() if hero in hero_roles])
    
    # Selector de héroes organizado por roles
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Seleccionar por Rol:**")
        selected_role = st.selectbox(
            "Filtrar héroes por rol",
            options=['Todos'] + get_all_roles()
        )
        
        if selected_role != 'Todos':
            filtered_heroes = get_heroes_by_role(selected_role)
            available_heroes = [h for h in available_heroes if h in filtered_heroes]
    
    with col2:
        st.write("**Composición de Equipo:**")
        selected_heroes = []
        
        for i in range(5):
            hero = st.selectbox(
                f"Héroe {i+1}",
                options=[''] + available_heroes,
                key=f"hero_{i}"
            )
            if hero:
                selected_heroes.append(hero)
        
        # Mostrar roles seleccionados
        if selected_heroes:
            st.write("**Roles en la composición:**")
            for hero in selected_heroes:
                role = get_hero_role(hero)
                st.write(f"• {hero} - {role}")
    
    # Analizar composición si está completa
    if len(selected_heroes) == 5:
        analyze_custom_composition(data, selected_heroes)
    elif len(selected_heroes) > 0:
        st.info(f"Selecciona {5 - len(selected_heroes)} héroes más para completar la composición.")

def analyze_custom_composition(data, heroes):
    """Analiza una composición personalizada"""
    
    st.write("---")
    st.subheader("📈 Análisis de la Composición Seleccionada")
    
    # Clasificar composición
    composition = classify_composition(heroes)
    comp_type = get_composition_type(composition)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tipo de Composición", comp_type)
    
    with col2:
        # Calcular estadísticas promedio
        hero_data = data[data['Hero'].isin(heroes)]
        avg_kda = (hero_data['Kills'] + hero_data['Assists']) / np.maximum(hero_data['Deaths'], 1)
        st.metric("KDA Promedio", f"{avg_kda.mean():.2f}")
    
    with col3:
        total_games = len(hero_data)
        st.metric("Datos Disponibles", f"{total_games} partidas")
    
    # Gráfico de composición
    if composition:
        fig = px.pie(
            values=list(composition.values()),
            names=list(composition.keys()),
            title="Distribución de Roles en la Composición"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Estadísticas detalladas por héroe
    st.subheader("📊 Estadísticas por Héroe")
    
    hero_stats = []
    for hero in heroes:
        hero_data = data[data['Hero'] == hero]
        if not hero_data.empty:
            stats = {
                'Héroe': hero,
                'Rol': get_hero_role(hero),
                'Partidas': len(hero_data),
                'Kills (Prom)': hero_data['Kills'].mean(),
                'Deaths (Prom)': hero_data['Deaths'].mean(),
                'Assists (Prom)': hero_data['Assists'].mean(),
                'KDA (Prom)': ((hero_data['Kills'] + hero_data['Assists']) / np.maximum(hero_data['Deaths'], 1)).mean(),
                'Daño a Héroes': hero_data['HeroDamage'].mean(),
                'Curación': hero_data['Healing'].mean()
            }
            hero_stats.append(stats)
    
    if hero_stats:
        hero_stats_df = pd.DataFrame(hero_stats)
        st.dataframe(hero_stats_df.round(2), use_container_width=True)
    
    # Recomendaciones
    provide_composition_recommendations(composition, comp_type)

def meta_trends(data):
    """Muestra tendencias del meta basadas en el tiempo"""
    
    st.subheader("📈 Tendencias del Meta")
    
    # Preparar datos con roles
    hero_roles = get_hero_roles()
    data_with_roles = data.copy()
    data_with_roles['Role'] = data_with_roles['Hero'].map(hero_roles)
    
    # Análisis temporal si hay datos de fecha
    if 'MatchDateTime' in data.columns:
        try:
            data_with_roles['Date'] = pd.to_datetime(data_with_roles['MatchDateTime'])
            data_with_roles['Month'] = data_with_roles['Date'].dt.to_period('M')
            
            # Popularidad de roles por mes
            role_popularity = data_with_roles.groupby(['Month', 'Role']).size().reset_index(name='Count')
            role_popularity['Month_str'] = role_popularity['Month'].astype(str)
            
            fig = px.line(
                role_popularity,
                x='Month_str',
                y='Count',
                color='Role',
                title="Popularidad de Roles por Mes"
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
        except:
            st.info("Los datos de fecha no están en el formato esperado.")
    
    # Top héroes por rol
    st.subheader("🏆 Héroes Más Populares por Rol")
    
    role_selected = st.selectbox(
        "Seleccionar rol para análisis",
        options=get_all_roles()
    )
    
    role_data = data_with_roles[data_with_roles['Role'] == role_selected]
    
    if not role_data.empty:
        hero_popularity = role_data['Hero'].value_counts().head(10)
        
        fig = px.bar(
            x=hero_popularity.values,
            y=hero_popularity.index,
            orientation='h',
            title=f"Top 10 Héroes Más Populares - {role_selected}"
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

def analyze_match_compositions(data):
    """Analiza composiciones por partida (si hay datos de MatchID)"""
    # Esta función requeriría datos de MatchID para agrupar por equipos
    # Por ahora retorna un DataFrame vacío como placeholder
    return pd.DataFrame()

def show_role_distribution(data):
    """Muestra distribución básica de roles"""
    
    role_counts = data['Role'].value_counts()
    
    fig = px.pie(
        values=role_counts.values,
        names=role_counts.index,
        title="Distribución de Roles en el Dataset"
    )
    st.plotly_chart(fig, use_container_width=True)

def provide_composition_recommendations(composition, comp_type):
    """Proporciona recomendaciones para la composición"""
    
    st.subheader("💡 Recomendaciones")
    
    recommendations = []
    
    if comp_type == "Standard (1 Tank)":
        recommendations.append("✅ Composición estándar equilibrada")
        recommendations.append("🎯 Enfócate en teamfights coordinados")
    
    elif comp_type == "Double Tank":
        recommendations.append("🛡️ Excelente para control de zona")
        recommendations.append("⚠️ Puede faltar daño sostenido")
    
    elif comp_type == "Double Bruiser":
        recommendations.append("💪 Gran presión en múltiples carriles")
        recommendations.append("⚠️ Vulnerable a poke damage")
    
    elif comp_type == "No Support":
        recommendations.append("⚠️ Composición muy agresiva")
        recommendations.append("🏃‍♂️ Necesitas terminar rápido")
    
    elif comp_type == "No Tank (Bruiser Solo)":
        recommendations.append("🏃‍♂️ Composición de movilidad")
        recommendations.append("⚠️ Evita teamfights frontales")
    
    else:
        recommendations.append("🤔 Composición no convencional")
        recommendations.append("📚 Requiere estrategia específica")
    
    for rec in recommendations:
        st.write(rec)
