import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_hero_analysis(filtered_data):
    """Genera un análisis visual de los héroes basado en las métricas seleccionadas."""
    
    st.markdown("### 🦸‍♂️ Análisis de Héroes")
    
    # Obtener nombres de columnas relevantes
    numeric_columns = [
        "HeroDmg",
        "DmgTaken", 
        "XP",
        "Healing",
        "TakeDowns",
        "Deaths",
        "KDA",
        "LifeTimeCC",
        "GameTime",
        "SiegeDmg",
        "SelfHealing"
    ]
    
    # Filtrar las columnas que realmente existen en el dataframe
    available_columns = [col for col in numeric_columns if col in filtered_data.columns]
    
    if not available_columns:
        st.warning("No hay columnas numéricas disponibles para el análisis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_x = st.selectbox("Métrica X (Horizontal):", available_columns, index=0)
    
    with col2:
        metric_y = st.selectbox("Métrica Y (Vertical):", available_columns, 
                               index=1 if len(available_columns) > 1 else 0)

    if len(filtered_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Análisis por héroe agregado
            st.markdown("#### Análisis por Héroe (Promedio)")
            hero_stats = filtered_data.groupby("Hero")[available_columns].mean().reset_index()
            
            fig_hero = px.scatter(
                hero_stats,
                x=metric_x,
                y=metric_y,
                hover_name="Hero",
                title=f"Relación entre {metric_x} y {metric_y} por Héroe",
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
            if "Role" in filtered_data.columns:
                st.markdown("#### Análisis por Rol")
                role_stats = filtered_data.groupby("Role")[available_columns].mean().reset_index()
                
                fig_role = px.scatter(
                    role_stats,
                    x=metric_x,
                    y=metric_y,
                    color="Role",
                    hover_name="Role",
                    title=f"Relación entre {metric_x} y {metric_y} por Rol",
                    template="plotly_dark",
                    color_discrete_sequence=['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
                )
                
                fig_role.update_traces(
                    marker=dict(
                        size=12,
                        line=dict(width=2, color='#ffffff')
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
                st.markdown(f"#### Top 10 Héroes por {metric_y}")
                top_heroes = hero_stats.nlargest(10, metric_y)
                
                fig_top = px.bar(
                    top_heroes,
                    x="Hero",
                    y=metric_y,
                    title=f"Top 10 Héroes por {metric_y}",
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
            st.metric(
                "Héroes Únicos",
                filtered_data["Hero"].nunique()
            )
        
        with col2:
            if "Winner" in filtered_data.columns:
                win_rate = (filtered_data["Winner"] == "Winner").mean() * 100
                st.metric(
                    "Tasa de Victoria",
                    f"{win_rate:.1f}%"
                )
            else:
                st.metric("Tasa de Victoria", "N/A")
        
        with col3:
            if metric_y in filtered_data.columns:
                avg_metric = filtered_data[metric_y].mean()
                st.metric(
                    f"Promedio {metric_y}",
                    f"{avg_metric:,.0f}" if avg_metric > 10 else f"{avg_metric:.2f}"
                )
    else:
        st.info("No hay datos para mostrar con los filtros aplicados.")
