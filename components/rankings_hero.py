import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data  # Importación corregida


def create_hero_rankings(filtered_data):
    st.markdown("### 🏆 Rankings de Héroes (Top 5 y Bottom 5)")
    # Crear una copia y convertir columnas de tiempo
    df = filtered_data.copy()
    time_columns = ["SpentDead", "GameTime"]
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col])

    # Obtener columnas numéricas
    exclude_columns = ["Hour", "Date", "Player", "Role"]
    numeric_columns = df.select_dtypes(
        include=["int64", "float64", "timedelta64"]
    ).columns
    numeric_columns = [col for col in numeric_columns if col not in exclude_columns]

    # Categorías de métricas
    metric_categories = {
        "Combate": [
            "HeroDmg",
            "SiegeDmg",
            "HeroKills",
            "Deaths",
            "Assists",
            "DmgTaken",
            "Takedowns",
        ],
        "Economía": ["XP", "MercCaptures", "MinionKills", "Regen"],
        "Objetivos": ["SpentDead", "GameTime", "MercDmg", "StructDmg"],
        "Soporte": ["HealShield", "SelfHeal", "Assists"],
        "Daño": ["MinionDmg", "SummonDmg", "SpellDmg", "PhysDmg"],
    }

    selected_category = st.selectbox(
        "Selecciona categoría de métricas", options=list(metric_categories.keys())
    )
    category_columns = [
        col for col in metric_categories[selected_category] if col in df.columns
    ]

    if category_columns:
        tabs = st.tabs(["Top 5 Héroes", "Bottom 5 Héroes"])
        with tabs[0]:  # Top 5 Héroes
            create_hero_ranking_section(df, category_columns, "top")
        with tabs[1]:  # Bottom 5 Héroes
            create_hero_ranking_section(df, category_columns, "bottom")


def create_hero_ranking_section(df, columns, rank_type="top"):
    """
    Función auxiliar para generar rankings top o bottom 5 de héroes.
    """
    for column in columns:
        icon = "📈" if rank_type == "top" else "📉"
        metric_name = get_metric_description(column)
        st.markdown(f"#### {icon} {rank_type.title()} 5 Héroes en {metric_name}")

        # Agrupar por héroe y calcular la media de la métrica
        hero_data = df.groupby("Hero")[column].mean().reset_index()

        # Contar el número de partidas por héroe
        match_counts = df.groupby("Hero").size().reset_index(name="Matches")

        # Combinar los datos de promedio con el conteo de partidas
        hero_data = hero_data.merge(match_counts, on="Hero")

        # Filtrar héroes con al menos 5 partidas jugadas
        hero_data = hero_data[hero_data["Matches"] >= 5]

        # Obtener top/bottom 5 héroes
        if rank_type == "top":
            ranked_data = hero_data.nlargest(5, column)
        else:
            ranked_data = hero_data.nsmallest(5, column)

        # Eliminar filas con valores nulos
        ranked_data = ranked_data.dropna()

        if ranked_data.empty:
            st.warning(
                f"No hay suficientes datos para mostrar {rank_type} 5 héroes en {metric_name}."
            )
            continue

        col1, col2 = st.columns([3, 1])
        with col1:
            # Ordenar los datos de mayor a menor antes de graficar
            plot_data = ranked_data.copy()
            plot_data = plot_data.sort_values(
                by=column, ascending=False
            )  # Orden descendente

            # Formatear valores para la visualización
            plot_data[column] = plot_data[column].apply(
                lambda x: format_value(x, column)
            )

            fig = px.bar(
                plot_data,
                x="Hero",
                y=column,
                color="Hero",
                text=column,
                title=f"{rank_type.title()} 5 Héroes en {metric_name}",
                template="plotly_dark",
                barmode="group",
            )
            # Ajustar el tamaño del texto y evitar que se solape
            fig.update_traces(
                texttemplate="%{text}",
                textposition="inside",  # Mueve el texto dentro de la barra
                textfont_size=12,  # Reduce el tamaño del texto
                width=0.5,  # Ajusta el ancho de las barras
            )
            fig.update_layout(
                height=300,
                margin=dict(t=30, b=0, l=0, r=0),
                yaxis_title=metric_name,
                xaxis_title="Héroe",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Crear copia para tabla
            table_data = ranked_data.copy()
            table_data[column] = table_data[column].apply(
                lambda x: format_value(x, column)
            )
            cmap = "Reds" if rank_type == "top" else "Blues"
            styled_df = table_data.style.set_properties(
                **{"background-color": "#1f1f1f", "color": "white"}
            )
            # Asegúrate de usar use_container_width=True aquí
            st.dataframe(styled_df, height=500, use_container_width=True)


def get_metric_description(metric):
    """
    Retorna una descripción más legible para cada métrica.
    """
    descriptions = {
        "HeroDmg": "Daño a Héroes",
        "SiegeDmg": "Daño de Asedio",
        "HeroKills": "Eliminaciones",
        "Deaths": "Muertes",
        "Assists": "Asistencias",
        "XP": "Experiencia",
        "MercCaptures": "Campamentos Capturados",
        "SpentDead": "Tiempo Muerto",
        "GameTime": "Duración del Juego",
        "MinionDmg": "Daño a Minions",
        "SummonDmg": "Daño a Invocaciones",
        "StructDmg": "Daño a Estructuras",
        "DmgTaken": "Daño Recibido",
        "HealShield": "Curación y Escudos",
        "SelfHeal": "Auto-Curación",
        "Takedowns": "Derribos",
        "Regen": "Regeneración",
        "SpellDmg": "Daño Mágico",
        "PhysDmg": "Daño Físico",
        "MercDmg": "Daño a Mercenarios",
    }
    return descriptions.get(metric, metric)


def format_value(value, column):
    """
    Formatea los valores según su tipo.
    """
    if pd.api.types.is_timedelta64_dtype(value):
        return str(value).split(".")[0]  # Formato HH:MM:SS para tiempos
    if isinstance(value, float):
        return f"{value:.2f}"  # Formato con 2 decimales
    return value
