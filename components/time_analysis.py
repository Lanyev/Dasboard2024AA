import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_time_analysis(filtered_data):
    if "Date" in filtered_data.columns:
        st.markdown("### 📅 Análisis Temporal")

        # 🔹 Convertir la columna Date a formato datetime especificando el formato correcto
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"], format="%d/%m/%Y")

        # 🔹 Extraer el mes en formato YYYY-MM para una mejor agrupación
        filtered_data["Month"] = filtered_data["Date"].dt.to_period("M").astype(str)

        col1, col2 = st.columns(2)

        with col1:
            daily_stats = (
                filtered_data.groupby("Date")
                .agg(
                    {
                        "HeroDmg": "mean",
                        "Assists": "mean",
                        "Winner": lambda x: (x == "Winner").mean() * 100,
                    }
                )
                .round(2)
            )

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=daily_stats.index,
                    y=daily_stats["HeroDmg"],
                    name="Daño",
                    line=dict(color="#FF4B4B"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=daily_stats.index,
                    y=daily_stats["Winner"],
                    name="Winrate",
                    yaxis="y2",
                    line=dict(color="#4B4BFF"),
                )
            )

            fig.update_layout(
                title="Tendencias Diarias",
                template="plotly_dark",
                yaxis2=dict(title="Winrate (%)", overlaying="y", side="right"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            if "Hour" in filtered_data.columns:
                hourly_games = filtered_data.groupby("Hour").size()

                fig = px.bar(
                    hourly_games,
                    title="Distribución de Partidas por Hora",
                    template="plotly_dark",
                    color=hourly_games.values,
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(fig, use_container_width=True)

        # 🔹 Nuevo gráfico: Partidas jugadas por mes
        monthly_games = filtered_data.groupby("Month").size().reset_index()
        monthly_games.columns = ["Month", "Games Played"]

        fig = px.line(
            monthly_games,
            x="Month",
            y="Games Played",
            title="📊 Partidas Jugadas por Mes",
            markers=True,
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)
