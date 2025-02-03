import streamlit as st


def create_filters(data):
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
                if config["type"] == "date_range":
                    filters[column] = st.date_input(
                        config["label"],
                        value=(data[column].min(), data[column].max()),
                        key=f"{column}_filter",
                    )
                elif config["type"] == "multiselect":
                    filters[column] = st.multiselect(
                        config["label"], options=sorted(data[column].unique())
                    )
    return filters


def apply_filters(data, filters):
    filtered_data = data.copy()
    for column, filter_vals in filters.items():
        if filter_vals:
            if column == "Date":
                filtered_data = filtered_data[
                    (filtered_data["Date"].dt.date >= filter_vals[0])
                    & (filtered_data["Date"].dt.date <= filter_vals[1])
                ]
            elif isinstance(filter_vals, (list, tuple)) and filter_vals:
                filtered_data = filtered_data[filtered_data[column].isin(filter_vals)]
    return filtered_data
