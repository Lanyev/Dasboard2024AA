import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def create_time_analysis(filtered_data):
    if "Date" in filtered_data.columns:
        st.markdown("### 📅 Análisis Temporal")

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
