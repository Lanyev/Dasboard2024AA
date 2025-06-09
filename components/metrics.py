import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.hero_roles import get_hero_roles, get_all_roles


def create_metrics(filtered_data, original_data):
    """Crea métricas clave"""
    
    st.markdown("### 📊 Métricas Clave")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Calcular partidas únicas usando File/FileName
        file_col = 'File' if 'File' in filtered_data.columns else 'FileName'
        if file_col in filtered_data.columns:
            total_games = filtered_data[file_col].nunique()
            original_games = original_data[file_col].nunique() if file_col in original_data.columns else 0
            delta_games = total_games - original_games
        else:
            total_games = len(filtered_data)
            delta_games = total_games - len(original_data)
        
        st.metric(
            "Total Partidas",
            f"{total_games:,}",
            delta=f"{delta_games:+,} filtradas" if delta_games != 0 else None,
        )

    with col2:
        if len(filtered_data) > 0 and "HeroDmg" in filtered_data.columns:
            avg_damage = filtered_data["HeroDmg"].mean()
            original_avg = original_data["HeroDmg"].mean() if "HeroDmg" in original_data.columns else 0
            delta_dmg = avg_damage - original_avg
            st.metric(
                "Daño Promedio",
                f"{avg_damage:,.0f}",
                delta=f"{delta_dmg:+,.0f}" if abs(delta_dmg) > 100 else None,
            )
        else:
            st.metric("Daño Promedio", "N/A", delta="Sin datos")

    with col3:
        if len(filtered_data) > 0 and "Winner" in filtered_data.columns:
            win_rate = (filtered_data["Winner"] == "Winner").mean() * 100
            original_win_rate = (original_data["Winner"] == "Winner").mean() * 100 if "Winner" in original_data.columns else 50
            delta_wr = win_rate - original_win_rate
            st.metric(
                "Tasa de Victoria",
                f"{win_rate:.1f}%",
                delta=f"{delta_wr:+.1f}%" if abs(delta_wr) > 0.1 else None,
            )
        else:
            st.metric("Tasa de Victoria", "N/A", delta="Sin datos")

    with col4:
        if len(filtered_data) > 0 and "GameTime" in filtered_data.columns:
            try:
                avg_time = filtered_data["GameTime"].mean()
                # Manejar diferentes tipos de datos de tiempo
                if hasattr(avg_time, 'total_seconds'):
                    # Es un timedelta
                    total_seconds = int(avg_time.total_seconds())
                elif isinstance(avg_time, str):
                    # Es un string, intentar convertir
                    avg_time_td = pd.to_timedelta(avg_time, errors='coerce')
                    total_seconds = int(avg_time_td.total_seconds()) if not pd.isna(avg_time_td) else 0
                else:
                    # Asumir que es un número (segundos)
                    total_seconds = int(avg_time) if not pd.isna(avg_time) else 0
                
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time_str = f"{minutes}m {seconds}s"
                st.metric("Tiempo Promedio", time_str, delta_color="off")
            except Exception as e:
                st.metric("Tiempo Promedio", "Error", delta_color="off")
        else:
            st.metric("Tiempo Promedio", "N/A", delta_color="off")    # Nuevas métricas basadas en roles
    st.markdown("### 🎭 Métricas por Rol")
    
    # Obtener mapeo de héroes a roles
    hero_roles = get_hero_roles()
    
    # Agregar columna de roles al dataset
    filtered_data_with_roles = filtered_data.copy()
    filtered_data_with_roles['Role'] = filtered_data_with_roles['Hero'].map(hero_roles)
    
    # Filtrar solo los registros que tienen rol asignado
    role_data = filtered_data_with_roles[filtered_data_with_roles['Role'].notna()]
    
    if len(role_data) > 0:
        # Calcular métricas por rol
        role_metrics = []
        
        for role in get_all_roles():
            role_subset = role_data[role_data['Role'] == role]
            
            if len(role_subset) > 0:
                # Verificar que las columnas necesarias existen
                file_col = 'File' if 'File' in role_subset.columns else 'FileName'
                total_games_role = role_subset[file_col].nunique() if file_col in role_subset.columns else len(role_subset)
                
                # Calcular métricas seguras
                avg_damage_role = role_subset["HeroDmg"].mean() if "HeroDmg" in role_subset.columns else 0
                win_rate_role = (role_subset["Winner"] == "Yes").mean() * 100 if "Winner" in role_subset.columns else 0
                
                role_metrics.append({
                    'Rol': role,
                    'Total Partidas': total_games_role,
                    'Daño Promedio': avg_damage_role,
                    'Tasa de Victoria': win_rate_role
                })
        
        if role_metrics:
            # Crear DataFrame y mostrar métricas
            metrics_df = pd.DataFrame(role_metrics)
            metrics_df = metrics_df.sort_values(by="Tasa de Victoria", ascending=False)
            
            # Mostrar en columnas
            cols = st.columns(min(len(role_metrics), 5))
            for i, (_, row) in enumerate(metrics_df.iterrows()):
                with cols[i % len(cols)]:
                    st.metric(
                        f"{row['Rol']}",
                        f"{row['Tasa de Victoria']:.1f}%",
                        delta=f"{row['Total Partidas']} partidas"
                    )
            
            # Gráfico de barras para Tasa de Victoria por Rol
            if len(metrics_df) > 1:
                fig = px.bar(
                    metrics_df,
                    x='Rol',
                    y='Tasa de Victoria',
                    title="📊 Tasa de Victoria por Rol",
                    labels={"Rol": "Rol", "Tasa de Victoria": "Tasa de Victoria (%)"},
                    color='Tasa de Victoria',
                    color_continuous_scale=px.colors.sequential.Viridis,
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Gráfico de dispersión para Daño vs Winrate si hay suficientes datos
                if len(metrics_df) > 2 and metrics_df['Daño Promedio'].max() > 0:
                    fig2 = px.scatter(
                        metrics_df,
                        x='Daño Promedio',
                        y='Tasa de Victoria',
                        text='Rol',
                        title="💥 Daño Promedio vs Tasa de Victoria por Rol",
                        labels={"Daño Promedio": "Daño Promedio", "Tasa de Victoria": "Tasa de Victoria (%)"},
                    )
                    fig2.update_traces(marker=dict(size=12))
                    fig2.update_traces(textposition="top center")
                    fig2.update_layout(height=400)
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("ℹ️ No hay suficientes datos para mostrar métricas por rol.")
    else:
        st.info("ℹ️ No se encontraron héroes con roles asignados en los datos filtrados.")
