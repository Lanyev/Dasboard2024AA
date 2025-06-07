import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from collections import Counter


def create_composition_analysis(filtered_data):
    """Análisis de composiciones de equipo y sinergias."""
    st.markdown("### 📋 Análisis de Composiciones")
    
    if 'Role' not in filtered_data.columns or 'Hero' not in filtered_data.columns:
        st.warning("Se necesitan las columnas 'Role' y 'Hero' para el análisis de composiciones.")
        return
    
    # Pestañas para diferentes análisis
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎭 Composiciones por Rol",
        "🤝 Sinergias de Héroes", 
        "🎯 Meta Analysis",
        "📊 Estadísticas de Equipo"
    ])
    
    with tab1:
        create_role_composition_analysis(filtered_data)
    
    with tab2:
        create_hero_synergy_analysis(filtered_data)
    
    with tab3:
        create_meta_analysis(filtered_data)
    
    with tab4:
        create_team_statistics(filtered_data)


def create_role_composition_analysis(data):
    """Análisis de composiciones por roles."""
    st.markdown("#### 🎭 Análisis de Composiciones por Rol")
    
    try:
        # Distribución de roles
        role_distribution = data['Role'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pastel de distribución de roles
            fig_pie = px.pie(
                values=role_distribution.values,
                names=role_distribution.index,
                title="📊 Distribución de Roles",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Gráfico de barras
            fig_bar = px.bar(
                x=role_distribution.index,
                y=role_distribution.values,
                title="📈 Frecuencia de Roles",
                template="plotly_dark",
                color=role_distribution.values,
                color_continuous_scale="viridis"
            )
            fig_bar.update_layout(
                xaxis_title="Rol",
                yaxis_title="Número de Partidas"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Análisis de rendimiento por rol
        if 'Winner' in data.columns:
            st.markdown("##### 🏆 Rendimiento por Rol")
            
            role_performance = data.groupby('Role').agg({
                'Winner': lambda x: (x == 'Winner').mean() * 100,
                'HeroDmg': 'mean',
                'Deaths': 'mean',
                'Assists': 'mean'
            }).round(2)
            
            role_performance.columns = ['Win Rate (%)', 'Avg Hero Damage', 'Avg Deaths', 'Avg Assists']
            
            st.dataframe(role_performance, use_container_width=True)
            
            # Gráfico de win rate por rol
            fig_winrate = px.bar(
                x=role_performance.index,
                y=role_performance['Win Rate (%)'],
                title="🎯 Tasa de Victoria por Rol",
                template="plotly_dark",
                color=role_performance['Win Rate (%)'],
                color_continuous_scale="RdYlGn"
            )
            fig_winrate.update_layout(
                xaxis_title="Rol",
                yaxis_title="Tasa de Victoria (%)"
            )
            st.plotly_chart(fig_winrate, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error en análisis de roles: {e}")


def create_hero_synergy_analysis(data):
    """Análisis de sinergias entre héroes."""
    st.markdown("#### 🤝 Análisis de Sinergias de Héroes")
    
    try:
        # Top héroes más utilizados
        hero_usage = data['Hero'].value_counts().head(15)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Héroes más populares
            fig_usage = px.bar(
                x=hero_usage.values,
                y=hero_usage.index,
                orientation='h',
                title="🔥 Héroes Más Utilizados (Top 15)",
                template="plotly_dark",
                color=hero_usage.values,
                color_continuous_scale="plasma"
            )
            fig_usage.update_layout(
                xaxis_title="Número de Partidas",
                yaxis_title="Héroe",
                height=500
            )
            st.plotly_chart(fig_usage, use_container_width=True)
        
        with col2:
            # Win rate por héroe (solo héroes con >5 partidas)
            if 'Winner' in data.columns:
                hero_stats = data.groupby('Hero').agg({
                    'Winner': lambda x: (x == 'Winner').mean() * 100,
                    'Hero': 'count'
                }).round(2)
                hero_stats.columns = ['Win Rate (%)', 'Games']
                
                # Filtrar héroes con al menos 5 partidas
                hero_stats_filtered = hero_stats[hero_stats['Games'] >= 5]
                hero_stats_filtered = hero_stats_filtered.sort_values('Win Rate (%)', ascending=False).head(15)
                
                fig_winrate = px.bar(
                    x=hero_stats_filtered['Win Rate (%)'],
                    y=hero_stats_filtered.index,
                    orientation='h',
                    title="🏆 Win Rate por Héroe (Min. 5 partidas)",
                    template="plotly_dark",
                    color=hero_stats_filtered['Win Rate (%)'],
                    color_continuous_scale="RdYlGn"
                )
                fig_winrate.update_layout(
                    xaxis_title="Tasa de Victoria (%)",
                    yaxis_title="Héroe",
                    height=500
                )
                st.plotly_chart(fig_winrate, use_container_width=True)
        
        # Análisis de combinaciones de roles
        st.markdown("##### 🎭 Combinaciones de Roles por Partida")
        
        # Agrupar por algún identificador de partida (si existe)
        if 'Date' in data.columns:
            # Usar fecha + hora como proxy para identificar partidas
            if 'Hour' in data.columns:
                data['Game_ID'] = data['Date'].astype(str) + '_' + data['Hour'].astype(str)
            else:
                data['Game_ID'] = data['Date'].astype(str)
            
            # Obtener combinaciones de roles por partida
            role_combinations = data.groupby('Game_ID')['Role'].apply(list).reset_index()
            role_combinations['Role_Combo'] = role_combinations['Role'].apply(
                lambda x: ', '.join(sorted(Counter(x).keys()))
            )
            
            combo_counts = role_combinations['Role_Combo'].value_counts().head(10)
            
            if len(combo_counts) > 0:
                fig_combo = px.bar(
                    x=combo_counts.values,
                    y=combo_counts.index,
                    orientation='h',
                    title="🎯 Combinaciones de Roles Más Comunes",
                    template="plotly_dark",
                    color=combo_counts.values,
                    color_continuous_scale="viridis"
                )
                fig_combo.update_layout(
                    xaxis_title="Frecuencia",
                    yaxis_title="Combinación de Roles",
                    height=400
                )
                st.plotly_chart(fig_combo, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error en análisis de sinergias: {e}")


def create_meta_analysis(data):
    """Análisis del meta actual."""
    st.markdown("#### 🎯 Análisis del Meta")
    
    try:
        # Métricas del meta
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_heroes = data['Hero'].nunique()
            st.metric("🦸‍♂️ Héroes Únicos", total_heroes)
        
        with col2:
            if 'Role' in data.columns:
                total_roles = data['Role'].nunique()
                st.metric("🎭 Roles Únicos", total_roles)
            else:
                st.metric("🎭 Roles Únicos", "N/A")
        
        with col3:
            most_popular_hero = data['Hero'].mode().iloc[0] if len(data) > 0 else "N/A"
            st.metric("⭐ Héroe Más Popular", most_popular_hero)
        
        with col4:
            if 'Winner' in data.columns:
                overall_winrate = (data['Winner'] == 'Winner').mean() * 100
                st.metric("🎯 Win Rate General", f"{overall_winrate:.1f}%")
            else:
                st.metric("🎯 Win Rate General", "N/A")
        
        # Tier list visual
        st.markdown("##### 🏆 Tier List de Héroes")
        
        if 'Winner' in data.columns:
            # Calcular estadísticas por héroe
            hero_meta_stats = data.groupby('Hero').agg({
                'Winner': lambda x: (x == 'Winner').mean() * 100,
                'Hero': 'count',
                'HeroDmg': 'mean'
            }).round(2)
            hero_meta_stats.columns = ['Win Rate (%)', 'Pick Rate', 'Avg Damage']
            
            # Solo héroes con al menos 3 partidas
            hero_meta_stats = hero_meta_stats[hero_meta_stats['Pick Rate'] >= 3]
            
            if len(hero_meta_stats) > 0:
                # Crear tiers basados en win rate
                hero_meta_stats['Tier'] = pd.cut(
                    hero_meta_stats['Win Rate (%)'],
                    bins=[0, 40, 50, 60, 70, 100],
                    labels=['D', 'C', 'B', 'A', 'S']
                )
                
                # Gráfico de dispersión: Pick Rate vs Win Rate
                fig_meta = px.scatter(
                    hero_meta_stats.reset_index(),
                    x='Pick Rate',
                    y='Win Rate (%)',
                    size='Avg Damage',
                    color='Tier',
                    hover_name='Hero',
                    title="🎯 Meta Analysis: Pick Rate vs Win Rate",
                    template="plotly_dark",
                    color_discrete_map={
                        'S': '#FFD700',  # Dorado
                        'A': '#32CD32',  # Verde
                        'B': '#1E90FF',  # Azul
                        'C': '#FFA500',  # Naranja
                        'D': '#FF6347'   # Rojo
                    }
                )
                
                fig_meta.update_layout(
                    xaxis_title="Pick Rate (Número de Partidas)",
                    yaxis_title="Win Rate (%)",
                    height=500
                )
                
                st.plotly_chart(fig_meta, use_container_width=True)
                
                # Tabla de tiers
                st.markdown("##### 📊 Tabla de Tiers")
                
                tier_summary = hero_meta_stats.groupby('Tier').size().reset_index(name='Número de Héroes')
                tier_summary = tier_summary.sort_values('Tier')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(tier_summary, use_container_width=True)
                
                with col2:
                    # Mostrar detalles por tier
                    selected_tier = st.selectbox(
                        "Ver héroes por tier:",
                        ['S', 'A', 'B', 'C', 'D'],
                        help="Selecciona un tier para ver los héroes"
                    )
                    
                    if selected_tier:
                        tier_heroes = hero_meta_stats[hero_meta_stats['Tier'] == selected_tier]
                        tier_heroes = tier_heroes.sort_values('Win Rate (%)', ascending=False)
                        
                        if len(tier_heroes) > 0:
                            st.dataframe(
                                tier_heroes[['Win Rate (%)', 'Pick Rate', 'Avg Damage']],
                                use_container_width=True
                            )
                        else:
                            st.info(f"No hay héroes en el tier {selected_tier}")
        
    except Exception as e:
        st.error(f"Error en análisis del meta: {e}")


def create_team_statistics(data):
    """Estadísticas de equipo y rendimiento conjunto."""
    st.markdown("#### 📊 Estadísticas de Equipo")
    
    try:
        # Análisis temporal si hay datos de fecha
        if 'Date' in data.columns:
            st.markdown("##### 📅 Evolución del Meta")
            
            # Convertir fecha si es necesario
            try:
                data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
                data['Month'] = data['Date'].dt.to_period('M').astype(str)
                
                # Evolución de uso de héroes por mes
                monthly_hero_usage = data.groupby(['Month', 'Hero']).size().reset_index(name='Usage')
                
                # Top 5 héroes por mes
                top_heroes_monthly = (
                    monthly_hero_usage.groupby('Month')
                    .apply(lambda x: x.nlargest(5, 'Usage'))
                    .reset_index(drop=True)
                )
                
                if len(top_heroes_monthly) > 0:
                    fig_evolution = px.line(
                        top_heroes_monthly,
                        x='Month',
                        y='Usage',
                        color='Hero',
                        title="📈 Evolución de Uso de Héroes Top 5 por Mes",
                        template="plotly_dark",
                        markers=True
                    )
                    
                    fig_evolution.update_layout(
                        xaxis_title="Mes",
                        yaxis_title="Número de Partidas",
                        height=400
                    )
                    
                    st.plotly_chart(fig_evolution, use_container_width=True)
                
            except Exception as e:
                st.warning(f"No se pudo procesar el análisis temporal: {e}")
        
        # Análisis de rendimiento por rol y daño
        st.markdown("##### ⚔️ Análisis de Daño por Rol")
        
        if 'Role' in data.columns and 'HeroDmg' in data.columns:
            role_damage_stats = data.groupby('Role')['HeroDmg'].agg([
                'mean', 'median', 'std', 'min', 'max'
            ]).round(2)
            
            role_damage_stats.columns = ['Media', 'Mediana', 'Desv. Estándar', 'Mínimo', 'Máximo']
            
            st.dataframe(role_damage_stats, use_container_width=True)
            
            # Box plot de daño por rol
            fig_damage_box = px.box(
                data,
                x='Role',
                y='HeroDmg',
                title="📦 Distribución de Daño por Rol",
                template="plotly_dark",
                color='Role'
            )
            
            fig_damage_box.update_layout(
                xaxis_title="Rol",
                yaxis_title="Daño a Héroes",
                height=400
            )
            
            st.plotly_chart(fig_damage_box, use_container_width=True)
        
        # Correlaciones entre métricas de equipo
        st.markdown("##### 🔗 Correlaciones de Rendimiento")
        
        team_metrics = ['HeroDmg', 'Deaths', 'Assists', 'HeroKills']
        available_metrics = [col for col in team_metrics if col in data.columns]
        
        if len(available_metrics) >= 2:
            corr_matrix = data[available_metrics].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="🔗 Correlaciones entre Métricas de Rendimiento",
                template="plotly_dark",
                color_continuous_scale="RdBu_r"
            )
            
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Resumen final
        st.markdown("##### 📋 Resumen del Análisis")
        
        summary_data = {
            'Métrica': [
                'Total de Partidas Analizadas',
                'Héroes Únicos en el Meta',
                'Roles Diferentes',
                'Periodo de Análisis'
            ],            'Valor': [
                data['File'].nunique() if 'File' in data.columns else len(data),
                data['Hero'].nunique(),
                data['Role'].nunique() if 'Role' in data.columns else 'N/A',
                f"{data['Date'].min().strftime('%d/%m/%Y')} - {data['Date'].max().strftime('%d/%m/%Y')}" 
                if 'Date' in data.columns else 'N/A'
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error en estadísticas de equipo: {e}")
