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
        tabs = st.tabs(["Top 5", "Bottom 5"])

        with tabs[0]:  # Top 5
            create_ranking_section(df, category_columns, "top")

        with tabs[1]:  # Bottom 5
            create_ranking_section(df, category_columns, "bottom")


def create_ranking_section(df, columns, rank_type="top"):
    """
    Función auxiliar para generar rankings top o bottom 5
    """
    for column in columns:
        icon = "📈" if rank_type == "top" else "📉"
        metric_name = get_metric_description(column)
        st.markdown(f"#### {icon} {rank_type.title()} 5 en {metric_name}")

        # Obtener top/bottom 5
        if rank_type == "top":
            ranked_data = df.nlargest(5, column)[["Player", "Hero", "Role", column]]
        else:
            ranked_data = df.nsmallest(5, column)[["Player", "Hero", "Role", column]]

        # Eliminar filas con valores nulos
        ranked_data = ranked_data.dropna()

        col1, col2 = st.columns([3, 1])

        with col1:
            # Ordenar los datos de mayor a menor antes de graficar
            plot_data = ranked_data.copy()
            plot_data = plot_data.sort_values(by=column, ascending=False)

            # Crear una columna para los valores formateados sin modificar los numéricos
            plot_data["valor_formateado"] = plot_data[column].apply(
                lambda x: format_value(x, column)
            )

            # Crear una nueva columna que combine Jugador y Héroe
            plot_data["Player_Hero"] = (
                plot_data["Player"] + " (" + plot_data["Hero"] + ")"
            )

            fig = px.bar(
                plot_data,
                x="Player_Hero",  # Eje x con la combinación de Jugador y Héroe
                y=column,  # Usar los valores numéricos originales para la altura
                color="Hero",
                text="valor_formateado",  # Usar la columna con valores formateados para las etiquetas
                title=f"{rank_type.title()} 5 {metric_name}",
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
                xaxis_title="Jugador (Héroe)",
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Crear copia para tabla y formatear los valores en la columna
            table_data = ranked_data.copy()
            table_data[column] = table_data[column].apply(
                lambda x: format_value(x, column)
            )
            styled_df = table_data.style.set_properties(
                **{"background-color": "#1f1f1f", "color": "white"}
            )
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
