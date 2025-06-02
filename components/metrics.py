import streamlit as st


def create_metrics(filtered_data, original_data):
    st.markdown("### 📊 Métricas Clave")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_games = len(filtered_data)
        st.metric(
            "Total Partidas",
            f"{total_games:,}",
            delta=f"{total_games - len(original_data):+,} filtradas",
        )

    with col2:
        if len(filtered_data) > 0 and "HeroDmg" in filtered_data.columns:
            avg_damage = filtered_data["HeroDmg"].mean()
            original_avg = original_data["HeroDmg"].mean() if "HeroDmg" in original_data.columns else 0
            st.metric(
                "Daño Promedio",
                f"{avg_damage:,.0f}",
                delta=f"{(avg_damage - original_avg):+,.0f}",
            )
        else:
            st.metric("Daño Promedio", "N/A", delta="Sin datos")

    with col3:
        if len(filtered_data) > 0 and "Winner" in filtered_data.columns:
            win_rate = (filtered_data["Winner"] == "Winner").mean() * 100
            original_win_rate = (original_data["Winner"] == "Winner").mean() * 100 if "Winner" in original_data.columns else 50
            st.metric(
                "Tasa de Victoria",
                f"{win_rate:.1f}%",
                delta=f"{win_rate - original_win_rate:+.1f}%",
            )
        else:
            st.metric("Tasa de Victoria", "N/A", delta="Sin datos")

    with col4:
        if len(filtered_data) > 0 and "GameTime" in filtered_data.columns:
            avg_time = filtered_data["GameTime"].mean()
            st.metric("Tiempo Promedio", str(avg_time).split(".")[0], delta_color="off")
        else:
            st.metric("Tiempo Promedio", "N/A", delta_color="off")
