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
        avg_damage = filtered_data["HeroDmg"].mean()
        st.metric(
            "Daño Promedio",
            f"{avg_damage:,.0f}",
            delta=f"{(avg_damage - original_data['HeroDmg'].mean()):+,.0f}",
        )

    with col3:
        win_rate = (filtered_data["Winner"] == "Winner").mean() * 100
        st.metric(
            "Tasa de Victoria",
            f"{win_rate:.1f}%",
            delta=f"{win_rate - ((original_data['Winner'] == 'Winner').mean() * 100):+.1f}%",
        )

    with col4:
        avg_time = filtered_data["GameTime"].mean()
        st.metric("Tiempo Promedio", str(avg_time).split(".")[0], delta_color="off")
