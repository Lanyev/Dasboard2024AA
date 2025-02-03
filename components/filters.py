import streamlit as st
import pandas as pd


def create_filters(data):
    """Genera los filtros en la barra lateral de Streamlit."""
    filters = {}
    filter_config = {
        "Date": {"type": "date_range", "label": "Rango de Fechas"},
        "Player": {"type": "multiselect", "label": "Jugadores"},
        "Role": {"type": "multiselect", "label": "Roles"},
        "Map": {"type": "multiselect", "label": "Mapas"},
        "Hero": {"type": "multiselect", "label": "Héroes"},
    }

    with st.sidebar:
        st.markdown("### 🎯 Filtros")
        for column, config in filter_config.items():
            if column in data.columns:
                column_data = (
                    data[column].dropna().astype(str).unique()
                )  # 🔹 Evitar NaN y convertir a str
                if config["type"] == "date_range":
                    filters[column] = st.date_input(
                        config["label"],
                        value=(
                            data[column].min(),
                            data[column].max(),
                        ),
                        key=f"{column}_filter",
                    )
                elif config["type"] == "multiselect":
                    filters[column] = st.multiselect(
                        config["label"],
                        options=sorted(column_data),  # 🔹 Ahora es seguro ordenar
                    )
    return filters


def apply_filters(data, filters):
    """Aplica los filtros seleccionados al DataFrame."""
    filtered_data = data.copy()
    for column, filter_vals in filters.items():
        if filter_vals:
            if column == "Date":
                filtered_data = filtered_data[
                    (filtered_data["Date"].dt.date >= filter_vals[0])
                    & (filtered_data["Date"].dt.date <= filter_vals[1])
                ]
            elif isinstance(filter_vals, (list, tuple)) and filter_vals:
                filtered_data = filtered_data[
                    filtered_data[column].astype(str).isin(filter_vals)
                ]  # 🔹 Convertir a str antes de filtrar
    return filtered_data
