import streamlit as st
import plotly.express as px


def create_hero_analysis(filtered_data):
    st.markdown("### 🦸‍♂️ Análisis de Héroes")

    col1, col2 = st.columns(2)

    with col1:
        hero_stats = (
            filtered_data.groupby("Hero")
            .agg(
                {
                    "Winner": lambda x: (x == "Winner").mean() * 100,
                    "HeroDmg": "mean",
                    "Assists": "mean",
                }
            )
            .round(2)
        )

        fig = px.scatter(
            hero_stats.reset_index(),
            x="HeroDmg",
            y="Winner",
            size="Assists",
            color="Winner",
            hover_name="Hero",
            title="Relación Daño vs. Winrate por Héroe",
            template="plotly_dark",
            color_continuous_scale="RdYlBu",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "Role" in filtered_data.columns:
            role_hero_stats = (
                filtered_data.groupby(["Role", "Hero"])
                .agg(
                    {
                        "Winner": lambda x: (x == "Winner").mean() * 100,
                        "HeroDmg": "mean",
                    }
                )
                .round(2)
            )

            fig = px.treemap(
                role_hero_stats.reset_index(),
                path=[px.Constant("Todos"), "Role", "Hero"],
                values="HeroDmg",
                color="Winner",
                title="Distribución de Héroes por Rol",
                template="plotly_dark",
                color_continuous_scale="RdYlBu",
            )
            st.plotly_chart(fig, use_container_width=True)
