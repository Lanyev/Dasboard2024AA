import streamlit as st
import pandas as pd
import plotly.express as px


def create_rankings(filtered_data):
    st.markdown("### 🏆 Rankings Top 5 y Bottom 5")

    # Crear una copia y convertir columnas de tiempo
    df = filtered_data.copy()
    time_columns = ["SpentDead", "GameTime"]
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col])

    # Obtener columnas numéricas
    exclude_columns = ["Hour", "Date"]
    numeric_columns = df.select_dtypes(
        include=["int64", "float64", "timedelta64"]
    ).columns.difference(exclude_columns).tolist()

    if not numeric_columns:
        st.warning("No hay métricas numéricas disponibles para crear rankings")
        return

    # Selector de métrica
    col1, col2 = st.columns(2)
    with col1:
        selected_metric = st.selectbox("Selecciona una métrica:", numeric_columns)
    with col2:
        aggregation = st.selectbox("Agregación:", ["Promedio", "Total", "Máximo"])

    if len(df) == 0:
        st.warning("No hay datos para mostrar")
        return

    # Agrupar por jugador y calcular estadísticas
    if aggregation == "Promedio":
        stats = df.groupby("Player")[selected_metric].mean().sort_values(ascending=False)
    elif aggregation == "Total":
        stats = df.groupby("Player")[selected_metric].sum().sort_values(ascending=False)
    else:  # Máximo
        stats = df.groupby("Player")[selected_metric].max().sort_values(ascending=False)

    # Crear dos columnas para Top 5 y Bottom 5
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### 🥇 Top 5 - {selected_metric}")
        top_5 = stats.head(5).reset_index()
        
        if len(top_5) > 0:
            # Crear gráfico de barras para Top 5
            fig_top = px.bar(
                top_5,
                x="Player",
                y=selected_metric,
                title=f"Top 5 Jugadores - {selected_metric} ({aggregation})",
                color=selected_metric,
                color_continuous_scale="Blues",
                template="plotly_white"
            )
            fig_top.update_layout(height=400)
            st.plotly_chart(fig_top, use_container_width=True)
            
            # Mostrar tabla
            st.dataframe(top_5.style.highlight_max(axis=0), use_container_width=True)

    with col2:
        st.markdown(f"#### 📉 Bottom 5 - {selected_metric}")
        bottom_5 = stats.tail(5).reset_index()
        
        if len(bottom_5) > 0:
            # Crear gráfico de barras para Bottom 5
            fig_bottom = px.bar(
                bottom_5,
                x="Player",
                y=selected_metric,
                title=f"Bottom 5 Jugadores - {selected_metric} ({aggregation})",
                color=selected_metric,
                color_continuous_scale="Reds",
                template="plotly_white"
            )
            fig_bottom.update_layout(height=400)
            st.plotly_chart(fig_bottom, use_container_width=True)
            
            # Mostrar tabla
            st.dataframe(bottom_5.style.highlight_min(axis=0), use_container_width=True)

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
