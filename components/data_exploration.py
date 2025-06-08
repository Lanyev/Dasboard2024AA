import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_data_exploration(filtered_data):
    """Crea una sección de exploración interactiva de datos."""
    st.markdown("### 🔍 Exploración de Datos")
    
    # Pestañas para diferentes tipos de exploración
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Resumen Estadístico", 
        "🔗 Correlaciones", 
        "📈 Distribuciones",
        "🎮 Datos Brutos"
    ])
    
    with tab1:
        create_statistical_summary(filtered_data)
    
    with tab2:
        create_correlation_analysis(filtered_data)
    
    with tab3:
        create_distribution_analysis(filtered_data)
    
    with tab4:
        create_raw_data_view(filtered_data)


def create_statistical_summary(data):
    """Muestra un resumen estadístico detallado."""
    st.markdown("#### 📊 Resumen Estadístico")
    
    # Obtener solo columnas numéricas
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("No se encontraron columnas numéricas para analizar.")
        return
    
    # Estadísticas descriptivas
    st.markdown("##### 📈 Estadísticas Descriptivas")
    
    try:
        stats = data[numeric_cols].describe()
        st.dataframe(stats.round(2), use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar estadísticas: {e}")
        return
    
    # Métricas clave en columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            total_registros = len(data)
            st.metric("📊 Total Registros", f"{total_registros:,}")
        except:
            st.metric("📊 Total Registros", "N/A")
    
    with col2:
        try:
            columnas_numericas = len(numeric_cols)
            st.metric("🔢 Columnas Numéricas", columnas_numericas)
        except:
            st.metric("🔢 Columnas Numéricas", "N/A")
    
    with col3:
        try:
            if 'Player' in data.columns:
                jugadores_unicos = data['Player'].nunique()
                st.metric("👥 Jugadores Únicos", jugadores_unicos)
            else:
                st.metric("👥 Jugadores Únicos", "N/A")
        except:
            st.metric("👥 Jugadores Únicos", "N/A")
    
    with col4:
        try:
            if 'Hero' in data.columns:
                heroes_unicos = data['Hero'].nunique()
                st.metric("🦸‍♂️ Héroes Únicos", heroes_unicos)
            else:
                st.metric("🦸‍♂️ Héroes Únicos", "N/A")
        except:
            st.metric("🦸‍♂️ Héroes Únicos", "N/A")


def create_correlation_analysis(data):
    """Análisis de correlaciones entre variables."""
    st.markdown("#### 🔗 Análisis de Correlaciones")
    
    # Obtener solo columnas numéricas
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Se necesitan al menos 2 columnas numéricas para análisis de correlación.")
        return
    
    try:
        # Calcular matriz de correlación
        corr_matrix = data[numeric_cols].corr()
        
        # Gráfico de matriz de correlación
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="🔗 Matriz de Correlación",
            template="plotly_dark",
            color_continuous_scale="RdBu_r"
        )
        
        fig.update_layout(
            height=600,
            title_x=0.5
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlaciones
        st.markdown("##### 🔝 Correlaciones Más Altas")
        
        # Obtener correlaciones en formato lista
        correlation_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                
                if not pd.isna(corr_value):
                    correlation_pairs.append({
                        'Variable 1': col1,
                        'Variable 2': col2,
                        'Correlación': round(corr_value, 3)
                    })
        
        if correlation_pairs:
            corr_df = pd.DataFrame(correlation_pairs)
            corr_df = corr_df.reindex(corr_df['Correlación'].abs().sort_values(ascending=False).index)
            
            # Mostrar top 10
            st.dataframe(corr_df.head(10), use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al calcular correlaciones: {e}")


def create_distribution_analysis(data):
    """Análisis de distribuciones de variables."""
    st.markdown("#### 📈 Distribuciones de Variables")
    
    # Obtener columnas numéricas
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("No se encontraron columnas numéricas para analizar distribuciones.")
        return
    
    # Selector de variable
    selected_var = st.selectbox(
        "Selecciona una variable para analizar:",
        numeric_cols,
        help="Elige una variable numérica para ver su distribución"
    )
    
    if selected_var:
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                # Histograma
                fig_hist = px.histogram(
                    data,
                    x=selected_var,
                    title=f"📊 Histograma - {selected_var}",
                    template="plotly_dark",
                    nbins=30
                )
                
                fig_hist.update_layout(height=400)
                st.plotly_chart(fig_hist, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error al crear histograma: {e}")
        
        with col2:
            try:
                # Box plot
                fig_box = px.box(
                    data,
                    y=selected_var,
                    title=f"📦 Box Plot - {selected_var}",
                    template="plotly_dark"
                )
                
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error al crear box plot: {e}")
        
        # Estadísticas de la variable seleccionada
        st.markdown(f"##### 📋 Estadísticas Detalladas - {selected_var}")
        try:
            # Obtener estadísticas básicas
            variable_stats = data[selected_var].describe()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Media", f"{variable_stats['mean']:.2f}")
            with col2:
                st.metric("📈 Mediana", f"{variable_stats['50%']:.2f}")
            with col3:
                st.metric("📏 Desv. Estándar", f"{variable_stats['std']:.2f}")
            with col4:
                st.metric("🎯 Rango", f"{variable_stats['max'] - variable_stats['min']:.2f}")
                
        except Exception as e:
            st.error(f"Error al calcular estadísticas: {e}")
            # Mostrar información de debug
            st.info(f"Tipo de datos: {data[selected_var].dtype}")
            st.info(f"Columna: {selected_var}")
            if len(data[selected_var].dropna()) > 0:
                st.info(f"Ejemplo de valores: {list(data[selected_var].dropna().head(3))}")


def create_raw_data_view(data):
    """Vista de datos brutos con filtros y búsqueda."""
    st.markdown("#### 🎮 Vista de Datos Brutos")
    
    # Información del dataset
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Filas", len(data))
    with col2:
        st.metric("📋 Total Columnas", len(data.columns))
    with col3:
        memory_usage = data.memory_usage(deep=True).sum() / 1024**2
        st.metric("💾 Memoria (MB)", f"{memory_usage:.2f}")
    
    # Filtros para la vista
    st.markdown("##### 🔍 Filtros de Vista")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtro por número de filas
        max_rows = min(len(data), 1000)  # Limitar a 1000 para rendimiento
        num_rows = st.slider(
            "Número de filas a mostrar:",
            min_value=10,
            max_value=max_rows,
            value=min(100, max_rows),
            step=10
        )
    
    with col2:
        # Filtro por columnas
        all_columns = data.columns.tolist()
        selected_columns = st.multiselect(
            "Columnas a mostrar:",
            all_columns,
            default=all_columns[:10],  # Mostrar primeras 10 por defecto
            help="Selecciona las columnas que quieres visualizar"
        )
    
    # Búsqueda en datos
    search_term = st.text_input(
        "🔍 Buscar en datos:",
        placeholder="Introduce un término para buscar...",
        help="Busca en todas las columnas de texto"
    )
    
    try:
        # Aplicar filtros
        display_data = data.copy()
        
        if selected_columns:
            display_data = display_data[selected_columns]
        
        if search_term:
            # Buscar en columnas de texto
            text_columns = display_data.select_dtypes(include=['object']).columns
            if len(text_columns) > 0:
                mask = False
                for col in text_columns:
                    mask |= display_data[col].astype(str).str.contains(
                        search_term, case=False, na=False
                    )
                display_data = display_data[mask]
        
        # Limitar número de filas
        display_data = display_data.head(num_rows)
        
        # Mostrar datos
        if len(display_data) > 0:
            st.dataframe(
                display_data,
                use_container_width=True,
                height=400
            )
            
            # Opción de descarga
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="📥 Descargar datos filtrados (CSV)",
                data=csv,
                file_name=f"datos_filtrados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No se encontraron datos con los filtros aplicados.")
            
    except Exception as e:
        st.error(f"Error al mostrar datos: {e}")


# Importar y mostrar explicación al final
def add_data_exploration_explanation():
    """Añade explicación detallada para la sección de Exploración de Datos"""
    from .explanations import create_explanation_section
    create_explanation_section('data_exploration')
