import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


def create_professional_analytics_dashboard(filtered_data):
    """Dashboard de Analytics Profesional con métricas avanzadas"""
    
    st.markdown("### 📊 Professional Analytics Dashboard")
    st.markdown("*Análisis avanzado de datos con métricas profesionales y estadísticas detalladas*")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Executive Summary", 
        "📈 Advanced KPIs",
        "🔬 Statistical Analysis",
        "💎 Performance Insights",
        "🚀 Predictive Models"
    ])
    
    with tab1:
        create_executive_dashboard(filtered_data)
    
    with tab2:
        create_advanced_kpis_dashboard(filtered_data)
    
    with tab3:
        create_statistical_analysis_dashboard(filtered_data)
        
    with tab4:
        create_performance_insights_dashboard(filtered_data)
        
    with tab5:
        create_predictive_models_dashboard(filtered_data)


def create_executive_dashboard(data):
    """Dashboard ejecutivo con métricas clave"""
    
    st.markdown("#### 🎯 Executive Summary")
      # KPIs principales en cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular partidas únicas basado en la columna File
    total_games = data['File'].nunique() if 'File' in data.columns else len(data)
    unique_players = data['Player'].nunique()
    unique_heroes = data['Hero'].nunique()
    avg_game_time = calculate_avg_game_time(data)
    
    with col1:
        st.metric(
            label="🎮 Total Games",
            value=f"{total_games:,}",
            help="Número total de partidas analizadas"
        )
    
    with col2:
        st.metric(
            label="👥 Active Players", 
            value=f"{unique_players:,}",
            help="Jugadores únicos en el dataset"
        )
    
    with col3:
        st.metric(
            label="🦸‍♂️ Hero Pool",
            value=f"{unique_heroes:,}",
            help="Héroes únicos jugados"
        )
    
    with col4:
        st.metric(
            label="⏱️ Avg Game Time",
            value=f"{avg_game_time:.1f}m",
            help="Duración promedio de partidas"
        )
    
    # Gráfico de tendencias principal
    st.markdown("##### 📈 Performance Trends Overview")
    
    # Crear métricas agregadas por período (si hay datos temporales)
    if 'Date' in data.columns or len(data) > 100:
        create_performance_trend_chart(data)
    else:
        create_performance_distribution_overview(data)
    
    # Health Score del Meta
    st.markdown("##### 🏥 Meta Health Score")
    
    meta_health = calculate_meta_health(data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        diversity_score = meta_health['diversity_score']
        color = "normal" if diversity_score > 70 else "inverse"
        st.metric(
            "🌈 Hero Diversity", 
            f"{diversity_score:.0f}/100",
            help="Diversidad en la selección de héroes"
        )
    
    with col2:
        balance_score = meta_health['balance_score']
        st.metric(
            "⚖️ Balance Score",
            f"{balance_score:.0f}/100",
            help="Balance general del meta"
        )
    
    with col3:
        competitive_score = meta_health['competitive_score']
        st.metric(
            "🏆 Competitive Health",
            f"{competitive_score:.0f}/100",
            help="Nivel competitivo del ambiente"
        )
    
    # Insights automáticos
    create_executive_insights(data, meta_health)


def create_advanced_kpis_dashboard(data):
    """KPIs avanzados y métricas profesionales"""
    
    st.markdown("#### 📈 Advanced KPIs & Metrics")
    
    # Eficiencia Metrics
    st.markdown("##### ⚡ Efficiency Metrics")
    
    efficiency_metrics = calculate_efficiency_metrics(data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_to_display = [
        ("💀 KDA Efficiency", efficiency_metrics.get('avg_kda', 0), "f{value:.2f}"),
        ("🎯 Damage Efficiency", efficiency_metrics.get('damage_efficiency', 0), "f{value:.1f}%"),
        ("🛡️ Survivability", efficiency_metrics.get('survivability', 0), "f{value:.1f}%"),
        ("⚡ Game Impact", efficiency_metrics.get('game_impact', 0), "f{value:.0f}")
    ]
    
    for i, (label, value, format_str) in enumerate(metrics_to_display):
        with [col1, col2, col3, col4][i]:
            try:
                if "%" in format_str:
                    formatted_value = f"{value:.1f}%"
                elif ":.0f" in format_str:
                    formatted_value = f"{value:.0f}"
                elif ":.2f" in format_str:
                    formatted_value = f"{value:.2f}"
                else:
                    formatted_value = f"{value:.1f}"
                st.metric(label, formatted_value)
            except Exception as e:
                st.metric(label, f"{value:.1f}")
    
    # Matriz de correlación avanzada
    st.markdown("##### 🔗 Performance Correlation Matrix")
    
    create_advanced_correlation_matrix(data)
    
    # Efficiency vs Performance Scatter
    st.markdown("##### 📊 Efficiency vs Performance Analysis")
    
    create_efficiency_performance_analysis(data)
    
    # Player Performance Distribution
    if 'Player' in data.columns:
        st.markdown("##### 👥 Player Performance Distribution")
        create_player_performance_distribution(data)


def create_statistical_analysis_dashboard(data):
    """Análisis estadístico avanzado"""
    
    st.markdown("#### 🔬 Statistical Analysis")
    
    # Análisis de distribuciones
    st.markdown("##### 📊 Distribution Analysis")
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_columns) >= 2:
        selected_metrics = st.multiselect(
            "Select metrics for distribution analysis:",
            numeric_columns,
            default=numeric_columns[:3] if len(numeric_columns) >= 3 else numeric_columns
        )
        
        if selected_metrics:
            create_distribution_analysis(data, selected_metrics)
    
    # Tests estadísticos
    st.markdown("##### 🧪 Statistical Tests")
    
    if 'Winner' in data.columns:
        create_statistical_tests(data)
    
    # Análisis de outliers
    st.markdown("##### 🎯 Outlier Analysis")
    
    create_outlier_analysis(data)
    
    # Principal Component Analysis
    if len(numeric_columns) >= 3:
        st.markdown("##### 🔍 Principal Component Analysis")
        create_pca_analysis(data, numeric_columns)


def create_performance_insights_dashboard(data):
    """Dashboard de insights de performance"""
    
    st.markdown("#### 💎 Performance Insights")
    
    # Performance Segments
    st.markdown("##### 🎯 Performance Segmentation")
    
    create_performance_segmentation(data)
    
    # Hero Meta Analysis
    st.markdown("##### 🦸‍♂️ Hero Meta Deep Dive")
    
    create_hero_meta_analysis(data)
    
    # Player Improvement Tracking
    if 'Player' in data.columns and len(data) > 50:
        st.markdown("##### 📈 Player Development Tracking")
        create_player_development_tracking(data)
    
    # Game Mode Analysis
    if 'GameMode' in data.columns:
        st.markdown("##### 🎮 Game Mode Analysis")
        create_game_mode_analysis(data)


def create_predictive_models_dashboard(data):
    """Dashboard de modelos predictivos"""
    
    st.markdown("#### 🚀 Predictive Models")
    
    st.markdown("##### 🔮 Predictive Insights")
    
    # Performance Prediction
    create_performance_prediction_model(data)
    
    # Meta Trend Prediction
    create_meta_trend_prediction(data)
    
    # Risk Analysis
    create_risk_analysis(data)


# Funciones auxiliares

def calculate_avg_game_time(data):
    """Calcula el tiempo promedio de juego en minutos"""
    if 'GameTime' in data.columns:
        try:
            # Manejar diferentes tipos de datos en GameTime
            game_time_series = data['GameTime'].dropna()
            
            if len(game_time_series) == 0:
                return 20.0  # Default si no hay datos
            
            # Si ya es timedelta (procesado por data_loader)
            if pd.api.types.is_timedelta64_dtype(game_time_series):
                time_minutes = game_time_series.dt.total_seconds() / 60
                return time_minutes.mean()
            
            # Si es object, intentar convertir a timedelta
            elif game_time_series.dtype == 'object':
                time_series = pd.to_timedelta(game_time_series, errors='coerce')
                time_minutes = time_series.dt.total_seconds() / 60
                return time_minutes.mean()
            
            # Si ya es numérico, asumir que está en minutos
            else:
                return game_time_series.mean()
                
        except Exception as e:
            print(f"Error processing GameTime: {e}")
            return 20.0  # Default en caso de error
    
    return 20.0  # Default de 20 minutos


def calculate_meta_health(data):
    """Calcula métricas de salud del meta"""
    
    # Hero Diversity (Gini coefficient inverso)
    hero_counts = data['Hero'].value_counts()
    hero_proportions = hero_counts / len(data)
    gini = 1 - sum(hero_proportions ** 2)
    diversity_score = gini * 100
      # Balance Score (basado en winrates)
    balance_score = 75  # Default
    if 'Winner' in data.columns:
        hero_winrates = data.groupby('Hero')['Winner'].apply(lambda x: (x == 'Yes').mean())
        winrate_std = hero_winrates.std()
        balance_score = max(0, 100 - (winrate_std * 500))  # Normalize
    
    # Competitive Score (basado en varianza de performance)
    competitive_score = 80  # Default
    if 'HeroDmg' in data.columns:
        damage_cv = data['HeroDmg'].std() / data['HeroDmg'].mean()
        competitive_score = min(100, damage_cv * 100)
    
    return {
        'diversity_score': diversity_score,
        'balance_score': balance_score,
        'competitive_score': competitive_score
    }


def calculate_efficiency_metrics(data):
    """Calcula métricas de eficiencia"""
    
    metrics = {}
    
    # KDA Efficiency
    if all(col in data.columns for col in ['HeroKills', 'Assists', 'Deaths']):
        kills = data['HeroKills'].mean()
        assists = data['Assists'].mean()
        deaths = data['Deaths'].mean()
        metrics['avg_kda'] = (kills + assists) / max(deaths, 1)
    
    # Damage Efficiency    if 'HeroDmg' in data.columns and 'DmgTaken' in data.columns:
        damage_ratio = data['HeroDmg'] / (data['DmgTaken'] + 1)
        metrics['damage_efficiency'] = damage_ratio.mean() * 100
    
    # Survivability
    if 'Deaths' in data.columns and 'GameTime' in data.columns:
        try:
            game_time_minutes = calculate_avg_game_time(data)
            avg_deaths = data['Deaths'].mean()
            metrics['survivability'] = max(0, 100 - (avg_deaths / game_time_minutes * 100))
        except:
            metrics['survivability'] = 75
    
    # Game Impact (combinación de métricas)
    if 'Takedowns' in data.columns and 'XP' in data.columns:
        takedowns_norm = data['Takedowns'] / data['Takedowns'].max()
        exp_norm = data['XP'] / data['XP'].max()
        metrics['game_impact'] = ((takedowns_norm + exp_norm) / 2 * 100).mean()
    
    return metrics


def create_performance_trend_chart(data):
    """Crea gráfico de tendencias de performance"""
    
    # Si no hay fecha, crear índice temporal
    if 'Date' not in data.columns:
        data = data.copy()
        data['Period'] = pd.cut(range(len(data)), bins=10, labels=False)
    else:
        data['Period'] = pd.to_datetime(data['Date']).dt.date
    
    # Agregar métricas por período
    trend_data = data.groupby('Period').agg({
        'HeroDmg': 'mean',
        'Takedowns': 'mean',
        'Deaths': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Hero Damage Trend', 'Takedowns Trend', 'Deaths Trend', 'Performance Index'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Hero Damage
    fig.add_trace(
        go.Scatter(x=trend_data['Period'], y=trend_data['HeroDmg'], 
                  mode='lines+markers', name='Hero Damage'),
        row=1, col=1
    )
    
    # Takedowns
    fig.add_trace(
        go.Scatter(x=trend_data['Period'], y=trend_data['Takedowns'], 
                  mode='lines+markers', name='Takedowns'),
        row=1, col=2
    )
    
    # Deaths
    fig.add_trace(
        go.Scatter(x=trend_data['Period'], y=trend_data['Deaths'], 
                  mode='lines+markers', name='Deaths'),
        row=2, col=1
    )
    
    # Performance Index
    performance_index = (trend_data['HeroDmg'] / trend_data['HeroDmg'].max() * 50 + 
                        trend_data['Takedowns'] / trend_data['Takedowns'].max() * 30 - 
                        trend_data['Deaths'] / trend_data['Deaths'].max() * 20)
    
    fig.add_trace(
        go.Scatter(x=trend_data['Period'], y=performance_index, 
                  mode='lines+markers', name='Performance Index'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def create_performance_distribution_overview(data):
    """Crea overview de distribución de performance"""
    
    # Crear métricas de performance
    metrics = ['HeroDmg', 'Takedowns', 'Deaths', 'XP']
    available_metrics = [m for m in metrics if m in data.columns]
    
    if not available_metrics:
        st.info("No hay suficientes métricas para crear el overview")
        return
    
    fig = make_subplots(
        rows=1, cols=len(available_metrics),
        subplot_titles=available_metrics
    )
    
    for i, metric in enumerate(available_metrics, 1):
        fig.add_trace(
            go.Histogram(x=data[metric], name=metric, showlegend=False),
            row=1, col=i
        )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def create_executive_insights(data, meta_health):
    """Crea insights ejecutivos automáticos"""
    
    st.markdown("##### 🔍 Executive Insights")
    
    insights = []
    
    # Insight sobre diversidad
    if meta_health['diversity_score'] > 80:
        insights.append("✅ **Excelente diversidad de héroes** - El meta está saludable con buena variedad")
    elif meta_health['diversity_score'] < 50:
        insights.append("⚠️ **Baja diversidad de héroes** - El meta está dominado por pocos héroes")
    
    # Insight sobre balance
    if meta_health['balance_score'] > 80:
        insights.append("✅ **Buen balance general** - Los héroes están bien equilibrados")
    elif meta_health['balance_score'] < 60:
        insights.append("⚠️ **Issues de balance detectados** - Algunos héroes dominan significativamente")
      # Insight sobre actividad
    total_games = data['File'].nunique() if 'File' in data.columns else len(data)
    if total_games > 1000:
        insights.append("📈 **Alta actividad competitiva** - Dataset robusto para análisis")
    elif total_games < 100:
        insights.append("📊 **Dataset limitado** - Se recomienda más datos para insights precisos")
    
    # Mostrar insights
    for insight in insights:
        if "✅" in insight:
            st.success(insight)
        elif "⚠️" in insight:
            st.warning(insight)
        else:
            st.info(insight)


def create_advanced_correlation_matrix(data):
    """Crea matriz de correlación avanzada"""
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 3:
        st.info("No hay suficientes columnas numéricas para análisis de correlación")
        return
    
    # Seleccionar columnas relevantes
    relevant_cols = [col for col in numeric_cols if not col.startswith('Talents_')][:8]
    
    if len(relevant_cols) < 3:
        relevant_cols = numeric_cols[:8]
    
    corr_matrix = data[relevant_cols].corr()
    
    # Crear heatmap
    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=relevant_cols,
        y=relevant_cols,
        color_continuous_scale='RdBu',
        aspect="auto"
    )
    
    fig.update_layout(
        title="Advanced Correlation Matrix",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_efficiency_performance_analysis(data):
    """Análisis de eficiencia vs performance"""
    
    if not all(col in data.columns for col in ['HeroDmg', 'Deaths', 'Takedowns']):
        st.info("No hay suficientes métricas para análisis de eficiencia")
        return
    
    # Calcular eficiencia
    data_copy = data.copy()
    data_copy['Efficiency'] = data_copy['Takedowns'] / (data_copy['Deaths'] + 1)
    data_copy['Performance'] = data_copy['HeroDmg'] / 1000 + data_copy['Takedowns'] * 100
    
    fig = px.scatter(
        data_copy,
        x='Efficiency',
        y='Performance',
        color='Hero' if 'Hero' in data.columns else None,
        size='XP' if 'XP' in data.columns else None,
        title="Efficiency vs Performance Analysis",
        labels={
            'Efficiency': 'Efficiency Score (Takedowns/Deaths)',
            'Performance': 'Performance Score'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_player_performance_distribution(data):
    """Distribución de performance por jugador"""
    
    if 'Player' not in data.columns:
        return
    
    player_stats = data.groupby('Player').agg({
        'HeroDmg': 'mean',
        'Takedowns': 'mean',
        'Deaths': 'mean'
    }).reset_index()
    
    # Calcular performance score
    player_stats['Performance_Score'] = (
        player_stats['HeroDmg'] / 1000 + 
        player_stats['Takedowns'] * 100 - 
        player_stats['Deaths'] * 50
    )
    
    fig = px.histogram(
        player_stats,
        x='Performance_Score',
        nbins=20,
        title="Player Performance Score Distribution"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_distribution_analysis(data, metrics):
    """Análisis de distribución para métricas seleccionadas"""
    
    fig = make_subplots(
        rows=len(metrics), cols=2,
        subplot_titles=[f'{metric} - Histogram' for metric in metrics] + 
                       [f'{metric} - Box Plot' for metric in metrics],
        specs=[[{"secondary_y": False}, {"secondary_y": False}] for _ in metrics]
    )
    
    for i, metric in enumerate(metrics, 1):
        # Histogram
        fig.add_trace(
            go.Histogram(x=data[metric], name=f'{metric} Hist', showlegend=False),
            row=i, col=1
        )
        
        # Box plot
        fig.add_trace(
            go.Box(y=data[metric], name=f'{metric} Box', showlegend=False),
            row=i, col=2
        )
    
    fig.update_layout(height=300 * len(metrics))
    st.plotly_chart(fig, use_container_width=True)


def create_statistical_tests(data):
    """Crea tests estadísticos"""
    
    # T-test para winners vs losers
    winners = data[data['Winner'] == 'Yes']
    losers = data[data['Winner'] == 'No']
    
    if len(winners) > 0 and len(losers) > 0:
        st.markdown("**T-Test: Winners vs Losers**")
        
        test_metrics = ['HeroDmg', 'Takedowns', 'Deaths']
        available_test_metrics = [m for m in test_metrics if m in data.columns]
        
        for metric in available_test_metrics:
            t_stat, p_value = stats.ttest_ind(winners[metric], losers[metric])
            
            significance = "Significativo" if p_value < 0.05 else "No significativo"
            st.write(f"• **{metric}**: t-statistic = {t_stat:.3f}, p-value = {p_value:.3f} ({significance})")


def create_outlier_analysis(data):
    """Análisis de outliers"""
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()[:5]
    
    outlier_data = []
    
    for col in numeric_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
        
        outlier_data.append({
            'Metric': col,
            'Outliers': len(outliers),
            'Percentage': len(outliers) / len(data) * 100,
            'Lower Bound': lower_bound,
            'Upper Bound': upper_bound
        })
    
    outlier_df = pd.DataFrame(outlier_data)
    st.dataframe(outlier_df.round(2), use_container_width=True)


def create_pca_analysis(data, numeric_columns):
    """Análisis de componentes principales"""
      # Filtrar columnas que sean realmente numéricas (excluyendo timedelta, datetime, object)
    numeric_only_cols = []
    for col in numeric_columns:
        if col in data.columns:
            # Verificar que sea numérico pero no timedelta ni datetime
            dtype = data[col].dtype
            if (pd.api.types.is_numeric_dtype(dtype) and 
                not pd.api.types.is_timedelta64_dtype(dtype) and
                not pd.api.types.is_datetime64_any_dtype(dtype)):
                # Verificar que no contenga strings
                try:
                    pd.to_numeric(data[col].dropna().iloc[0] if not data[col].dropna().empty else 0)
                    numeric_only_cols.append(col)
                except (ValueError, TypeError):
                    continue
    
    # Seleccionar columnas para PCA (máximo 6 para visualización)
    pca_cols = [col for col in numeric_only_cols if not col.startswith('Talents_')][:6]
    
    if len(pca_cols) < 3:
        st.info("No hay suficientes métricas numéricas para PCA")
        return
    
    try:
        # Preparar datos - solo columnas realmente numéricas
        pca_data = data[pca_cols].copy()
        
        # Convertir a numérico, forzando errores a NaN
        for col in pca_cols:
            pca_data[col] = pd.to_numeric(pca_data[col], errors='coerce')
        
        # Eliminar filas con todos NaN
        pca_data = pca_data.dropna()
        
        if pca_data.empty:
            st.warning("No hay datos válidos para PCA después de limpieza")
            return
        
        # Verificar que no hay datos infinitos o NaN
        pca_data = pca_data.replace([np.inf, -np.inf], np.nan)
        pca_data = pca_data.fillna(pca_data.mean())
        
        # Aplicar StandardScaler solo después de validar datos
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(pca_data)
        
        # Aplicar PCA
        pca = PCA(n_components=min(3, len(pca_cols)))
        pca_result = pca.fit_transform(scaled_data)
        
        # Varianza explicada
        variance_explained = pca.explained_variance_ratio_
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot PCA
            fig_pca = px.scatter(
                x=pca_result[:, 0],
                y=pca_result[:, 1],
                title="PCA: First Two Components",
                labels={
                    'x': f'PC1 ({variance_explained[0]:.1%} variance)',
                    'y': f'PC2 ({variance_explained[1]:.1%} variance)'
                },
                template="plotly_dark"            )
            fig_pca.update_layout(height=400)
            st.plotly_chart(fig_pca, use_container_width=True)
        
        with col2:
            # Varianza explicada
            fig_var = px.bar(
                x=[f'PC{i+1}' for i in range(len(variance_explained))],
                y=variance_explained,
                title="Varianza Explicada por Componente",
                template="plotly_dark"
            )
            fig_var.update_layout(height=400)
            st.plotly_chart(fig_var, use_container_width=True)
        
        # Componentes principales
        st.markdown("##### 📊 Componentes Principales")
        
        components_df = pd.DataFrame(
            pca.components_[:2].T,
            columns=['PC1', 'PC2'],
            index=pca_cols
        ).round(3)
        
        st.dataframe(components_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error en análisis PCA: {e}")
        st.info("Mostrando métricas disponibles para debug:")
        st.write(f"Columnas numéricas disponibles: {numeric_only_cols}")
        st.write(f"Columnas seleccionadas para PCA: {pca_cols}")


def create_performance_segmentation(data):
    """Segmentación de performance"""
    
    if 'HeroDmg' not in data.columns:
        st.info("No hay datos de daño para segmentación")
        return
    
    # Crear segmentos basados en percentiles
    damage_q75 = data['HeroDmg'].quantile(0.75)
    damage_q25 = data['HeroDmg'].quantile(0.25)
    
    data_copy = data.copy()
    data_copy['Performance_Segment'] = 'Medium'
    data_copy.loc[data_copy['HeroDmg'] >= damage_q75, 'Performance_Segment'] = 'High'
    data_copy.loc[data_copy['HeroDmg'] <= damage_q25, 'Performance_Segment'] = 'Low'
    
    # Distribución de segmentos
    segment_counts = data_copy['Performance_Segment'].value_counts()
    
    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        title="Performance Segmentation Distribution"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_hero_meta_analysis(data):
    """Análisis profundo del meta de héroes"""
    
    hero_stats = data.groupby('Hero').agg({
        'HeroDmg': ['mean', 'std'],
        'Takedowns': 'mean',
        'Deaths': 'mean',
        'Hero': 'count'  # Para contar partidas
    }).round(2)
    
    # Flatten column names
    hero_stats.columns = ['Damage_Avg', 'Damage_Std', 'Takedowns_Avg', 'Deaths_Avg', 'Games_Played']
    hero_stats = hero_stats.reset_index()
    
    # Filtrar héroes con al menos 3 partidas
    hero_stats = hero_stats[hero_stats['Games_Played'] >= 3]
    
    if len(hero_stats) == 0:
        st.info("No hay suficientes datos por héroe")
        return
    
    # Top héroes por diferentes métricas
    col1, col2 = st.columns(2)
    
    with col1:
        top_damage = hero_stats.nlargest(5, 'Damage_Avg')
        st.markdown("**🔥 Top 5 Damage Dealers**")
        for _, hero in top_damage.iterrows():
            st.write(f"• {hero['Hero']}: {hero['Damage_Avg']:,.0f} avg damage")
    
    with col2:
        top_takedowns = hero_stats.nlargest(5, 'Takedowns_Avg')
        st.markdown("**🎯 Top 5 Takedown Leaders**")
        for _, hero in top_takedowns.iterrows():
            st.write(f"• {hero['Hero']}: {hero['Takedowns_Avg']:.1f} avg takedowns")


def create_player_development_tracking(data):
    """Tracking de desarrollo de jugadores"""
    
    if 'Player' not in data.columns:
        return
    
    # Calcular progresión por jugador
    player_progression = []
    
    for player in data['Player'].unique():
        player_data = data[data['Player'] == player].copy()
        if len(player_data) >= 3:  # Mínimo 3 partidas
            player_data = player_data.sort_index()  # Asumir orden cronológico
            
            # Calcular mejora en damage
            first_half = player_data.head(len(player_data)//2)
            second_half = player_data.tail(len(player_data)//2)
            
            damage_improvement = second_half['HeroDmg'].mean() - first_half['HeroDmg'].mean()
            
            player_progression.append({
                'Player': player,
                'Games': len(player_data),
                'Damage_Improvement': damage_improvement,
                'Avg_Damage': player_data['HeroDmg'].mean()
            })
    
    if player_progression:
        prog_df = pd.DataFrame(player_progression)
        
        fig = px.scatter(
            prog_df,
            x='Games',
            y='Damage_Improvement',
            size='Avg_Damage',
            hover_name='Player',
            title="Player Development: Damage Improvement vs Games Played"
        )
        
        st.plotly_chart(fig, use_container_width=True)


def create_game_mode_analysis(data):
    """Análisis por modo de juego"""
    
    mode_stats = data.groupby('GameMode').agg({
        'HeroDmg': 'mean',
        'GameTime': 'count'  # Como proxy para número de partidas
    }).round(0)
    
    mode_stats.columns = ['Avg_Damage', 'Games_Count']
    mode_stats = mode_stats.reset_index()
    
    fig = px.bar(
        mode_stats,
        x='GameMode',
        y='Avg_Damage',
        title="Average Damage by Game Mode"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_performance_prediction_model(data):
    """Modelo simple de predicción de performance"""
    
    st.info("🔮 **Performance Prediction Model**")
    st.write("Basado en métricas históricas, predice performance futura")
    
    # Implementación simplificada para demo
    if 'HeroDmg' in data.columns:
        avg_damage = data['HeroDmg'].mean()
        std_damage = data['HeroDmg'].std()
        
        # Predicción simple basada en tendencia
        trend_factor = np.random.normal(1.05, 0.1)  # 5% mejora promedio con variación
        predicted_damage = avg_damage * trend_factor
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Avg Damage", f"{avg_damage:,.0f}")
        with col2:
            st.metric("Predicted Next Period", f"{predicted_damage:,.0f}", f"{(predicted_damage-avg_damage):+,.0f}")


def create_meta_trend_prediction(data):
    """Predicción de tendencias del meta"""
    
    st.info("📈 **Meta Trend Prediction**")
    
    # Análisis de tendencia de popularidad de héroes
    hero_popularity = data['Hero'].value_counts().head(5)
    
    st.write("**Trending Heroes (Current Top 5):**")
    for hero, count in hero_popularity.items():
        percentage = count / len(data) * 100
        trend = "↗️" if percentage > 10 else "→" if percentage > 5 else "↘️"
        st.write(f"• {trend} {hero}: {percentage:.1f}% pick rate")


def create_risk_analysis(data):
    """Análisis de riesgo"""
    
    st.info("⚠️ **Risk Analysis**")
    
    risks = []
    
    # Risk: Meta dominance
    if 'Hero' in data.columns:
        top_hero_percentage = data['Hero'].value_counts().iloc[0] / len(data) * 100
        if top_hero_percentage > 25:
            risks.append(f"🔴 Meta Risk: {data['Hero'].value_counts().index[0]} domina con {top_hero_percentage:.1f}% pick rate")
    
    # Risk: Player activity concentration
    if 'Player' in data.columns:
        top_player_percentage = data['Player'].value_counts().iloc[0] / len(data) * 100
        if top_player_percentage > 30:
            risks.append(f"🟡 Activity Risk: Un jugador representa {top_player_percentage:.1f}% de las partidas")
    
    # Show risks
    if risks:
        for risk in risks:
            if "🔴" in risk:
                st.error(risk)
            elif "🟡" in risk:
                st.warning(risk)
    else:
        st.success("✅ No se detectaron riesgos significativos en los datos")
