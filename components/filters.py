import streamlit as st


def create_filters(data):
    filters = {}
    with st.sidebar:
        st.markdown("### 🎯 Filtros")

        if "Date" in data.columns:
            date_range = st.date_input(
                "Rango de Fechas",
                value=(data["Date"].min(), data["Date"].max()),
                key="date_filter",
            )
            filters["Date"] = date_range

        with st.expander("Filtros de Jugador", expanded=False):
            if "Player" in data.columns:
                filters["Player"] = st.multiselect(
                    "Jugadores", options=sorted(data["Player"].unique())
                )

            if "Role" in data.columns:
                filters["Role"] = st.multiselect(
                    "Roles", options=sorted(data["Role"].unique())
                )

        with st.expander("Filtros de Partida", expanded=False):
            if "Map" in data.columns:
                filters["Map"] = st.multiselect(
                    "Mapas", options=sorted(data["Map"].unique())
                )

            if "Hero" in data.columns:
                filters["Hero"] = st.multiselect(
                    "Héroes", options=sorted(data["Hero"].unique())
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
