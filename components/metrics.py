import streamlit as st
import pandas as pd


def create_metrics(filtered_data, original_data):
    """Crea métricas clave"""
    
    st.markdown("### 📊 Métricas Clave")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Calcular partidas únicas usando File/FileName
        file_col = 'File' if 'File' in filtered_data.columns else 'FileName'
        if file_col in filtered_data.columns:
            total_games = filtered_data[file_col].nunique()
            original_games = original_data[file_col].nunique() if file_col in original_data.columns else 0
            delta_games = total_games - original_games
        else:
            total_games = len(filtered_data)
            delta_games = total_games - len(original_data)
        
        st.metric(
            "Total Partidas",
            f"{total_games:,}",
            delta=f"{delta_games:+,} filtradas" if delta_games != 0 else None,
        )

    with col2:
        if len(filtered_data) > 0 and "HeroDmg" in filtered_data.columns:
            avg_damage = filtered_data["HeroDmg"].mean()
            original_avg = original_data["HeroDmg"].mean() if "HeroDmg" in original_data.columns else 0
            delta_dmg = avg_damage - original_avg
            st.metric(
                "Daño Promedio",
                f"{avg_damage:,.0f}",
                delta=f"{delta_dmg:+,.0f}" if abs(delta_dmg) > 100 else None,
            )
        else:
            st.metric("Daño Promedio", "N/A", delta="Sin datos")

    with col3:
        if len(filtered_data) > 0 and "Winner" in filtered_data.columns:
            win_rate = (filtered_data["Winner"] == "Winner").mean() * 100
            original_win_rate = (original_data["Winner"] == "Winner").mean() * 100 if "Winner" in original_data.columns else 50
            delta_wr = win_rate - original_win_rate
            st.metric(
                "Tasa de Victoria",
                f"{win_rate:.1f}%",
                delta=f"{delta_wr:+.1f}%" if abs(delta_wr) > 0.1 else None,
            )
        else:
            st.metric("Tasa de Victoria", "N/A", delta="Sin datos")

    with col4:
        if len(filtered_data) > 0 and "GameTime" in filtered_data.columns:
            try:
                avg_time = filtered_data["GameTime"].mean()
                # Manejar diferentes tipos de datos de tiempo
                if hasattr(avg_time, 'total_seconds'):
                    # Es un timedelta
                    total_seconds = int(avg_time.total_seconds())
                elif isinstance(avg_time, str):
                    # Es un string, intentar convertir
                    avg_time_td = pd.to_timedelta(avg_time, errors='coerce')
                    total_seconds = int(avg_time_td.total_seconds()) if not pd.isna(avg_time_td) else 0
                else:
                    # Asumir que es un número (segundos)
                    total_seconds = int(avg_time) if not pd.isna(avg_time) else 0
                
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time_str = f"{minutes}m {seconds}s"
                st.metric("Tiempo Promedio", time_str, delta_color="off")
            except Exception as e:
                st.metric("Tiempo Promedio", "Error", delta_color="off")
        else:
            st.metric("Tiempo Promedio", "N/A", delta_color="off")
