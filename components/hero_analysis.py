import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .explanations import create_explanation_section


def create_hero_analysis(filtered_data):
    """Genera un análisis visual de los héroes basado en las métricas seleccionadas."""
    
    st.markdown("### 🦸‍♂️ Análisis de Héroes")
    
    # Métricas clave disponibles (adaptadas a structured_data.csv)
    key_metrics = {
        "HeroDamage": "Daño a Héroes",
        "HeroKills": "Asesinatos",
        "Assists": "Asistencias", 
        "Takedowns": "Takedowns",
        "DamageTaken": "Daño Recibido",
        "Experience": "Experiencia",
        "HealingShielding": "Curación/Escudos",
        "Deaths": "Muertes",
        "GameTime": "Tiempo de Juego",
        "StructureDamage": "Daño a Estructuras",
        "SelfHealing": "Auto-curación"
    }
    
    # Filtrar métricas disponibles en el dataset
    available_metrics = {k: v for k, v in key_metrics.items() if k in filtered_data.columns}
    
    if not available_metrics:
        st.warning("No hay métricas disponibles para el análisis")
        return
    
    # Filtro de métricas clave
    st.markdown("#### 📊 Métricas Clave")
    default_metrics = ["HeroDamage", "HeroKills", "HealingShielding", "Deaths", "GameTime"]
    default_selection = [m for m in default_metrics if m in available_metrics]
    if not default_selection:
        default_selection = list(available_metrics.keys())[:5]
    
    selected_metrics = st.multiselect(
        "Selecciona las métricas que deseas visualizar:",
        options=list(available_metrics.keys()),
        default=default_selection,
        format_func=lambda x: available_metrics.get(x, x)
    )
    
    if not selected_metrics:
        st.info("Selecciona al menos una métrica para visualizar el análisis.")
        return
        
    # Obtener nombres de columnas relevantes para los selectbox
    available_columns = selected_metrics
    
    if not available_columns:
        st.warning("No hay columnas numéricas disponibles para el análisis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_x = st.selectbox("Métrica X (Horizontal):", available_columns, index=0,
                               format_func=lambda x: available_metrics.get(x, x))
    
    with col2:
        metric_y = st.selectbox("Métrica Y (Vertical):", available_columns, 
                               index=1 if len(available_columns) > 1 else 0,
                               format_func=lambda x: available_metrics.get(x, x))

    if len(filtered_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Análisis por héroe agregado
            st.markdown("#### Análisis por Héroe (Promedio)")
            hero_col = "HeroName" if "HeroName" in filtered_data.columns else "Hero"
            hero_stats = filtered_data.groupby(hero_col)[available_columns].mean().reset_index()
            
            fig_hero = px.scatter(
                hero_stats,
                x=metric_x,
                y=metric_y,
                hover_name=hero_col,
                title=f"Relación entre {available_metrics.get(metric_x, metric_x)} y {available_metrics.get(metric_y, metric_y)} por Héroe",
                template="plotly_dark",
                color_discrete_sequence=['#1f77b4']
            )
            
            fig_hero.update_traces(
                marker=dict(
                    size=10,
                    color='#1f77b4',
                    line=dict(width=2, color='#ffffff')
                )
            )
            
            fig_hero.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(color='white', size=14)
            )
            
            st.plotly_chart(fig_hero, use_container_width=True)

        with col2:
            # Análisis de distribución de roles (si está disponible)
            role_col = "Role" if "Role" in filtered_data.columns else None
            if role_col and filtered_data[role_col].nunique() > 1:
                st.markdown(f"#### Análisis por Rol ({available_metrics.get(metric_y, metric_y)})")
                role_stats = filtered_data.groupby(role_col)[available_columns].mean().reset_index()
                
                fig_role = px.bar(
                    role_stats,
                    x=role_col,
                    y=metric_y,
                    title=f"Promedio de {available_metrics.get(metric_y, metric_y)} por Rol",
                    template="plotly_dark",
                    color=metric_y,
                    color_continuous_scale='viridis'
                )
                
                fig_role.update_traces(
                    texttemplate='%{y:.0f}',
                    textposition='outside',
                    marker=dict(
                        line=dict(width=1, color='white')
                    )
                )
                
                fig_role.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    title_font=dict(color='white', size=14),
                    legend=dict(
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='white',
                        borderwidth=1
                    )
                )
                
                st.plotly_chart(fig_role, use_container_width=True)
            else:
                # Mostrar top 10 héroes por la métrica Y seleccionada
                st.markdown(f"#### Top 10 Héroes por {available_metrics.get(metric_y, metric_y)}")
                top_heroes = hero_stats.nlargest(10, metric_y)
                
                fig_top = px.bar(
                    top_heroes,
                    x=hero_col,
                    y=metric_y,
                    title=f"Top 10 Héroes por {available_metrics.get(metric_y, metric_y)}",
                    template="plotly_dark",
                    color_discrete_sequence=['#2ca02c']
                )
                
                fig_top.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    title_font=dict(color='white', size=14),
                    xaxis_tickangle=-45
                )
                
                st.plotly_chart(fig_top, use_container_width=True)

        # Estadísticas adicionales
        st.markdown("#### 📈 Estadísticas de Rendimiento")
        
        col1, col2, col3 = st.columns(3)
          with col1:
            hero_col = "HeroName" if "HeroName" in filtered_data.columns else "Hero"
            st.metric(
                "Héroes Únicos",
                filtered_data[hero_col].nunique()
            )
        
        with col2:
            if "Winner" in filtered_data.columns:
                win_rate = (filtered_data["Winner"] == "Yes").mean() * 100
                st.metric(
                    "Tasa de Victoria",
                    f"{win_rate:.1f}%"
                )
            else:
                st.metric("Tasa de Victoria", "N/A")
        
        with col3:
            if metric_y in filtered_data.columns:
                avg_metric = filtered_data[metric_y].mean()
                # Manejar diferentes tipos de datos
                try:
                    if hasattr(avg_metric, 'total_seconds'):
                        # Es un timedelta
                        total_seconds = int(avg_metric.total_seconds())
                        minutes = total_seconds // 60
                        seconds = total_seconds % 60
                        metric_str = f"{minutes}m {seconds}s"
                    elif pd.api.types.is_numeric_dtype(filtered_data[metric_y]):
                        # Es numérico
                        metric_str = f"{avg_metric:,.0f}" if avg_metric > 10 else f"{avg_metric:.2f}"
                    else:
                        # Otro tipo
                        metric_str = str(avg_metric)
                except:
                    metric_str = str(avg_metric)
                
                st.metric(
                    f"Promedio {available_metrics.get(metric_y, metric_y)}",
                    metric_str
                )
    else:
        st.info("No hay datos para mostrar con los filtros aplicados.")

    # Añadir explicación detallada al final
    st.markdown("---")
    create_explanation_section('hero_analysis')
