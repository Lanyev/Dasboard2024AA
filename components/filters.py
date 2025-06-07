import streamlit as st
import pandas as pd


def create_filters(data):
    """Genera los filtros en la barra lateral de Streamlit."""
    filters = {}
    filter_config = {
        "Date": {"type": "date_range", "label": "Rango de Fechas"},
        "Player": {"type": "multiselect", "label": "Jugadores", "searchable": True},
        "Role": {"type": "multiselect", "label": "Roles", "searchable": False},
        "Map": {"type": "multiselect", "label": "Mapas", "searchable": True},
        "Hero": {"type": "multiselect", "label": "Héroes", "searchable": True},
    }

    with st.sidebar:
        st.markdown("### 🎯 Filtros")
        
        # Mostrar información de calidad de datos
        total_rows = len(data)
        clean_rows = len(data.dropna())
        if total_rows > clean_rows:
            st.info(f"ℹ️ Datos: {clean_rows:,}/{total_rows:,} filas completas")
        
        for column, config in filter_config.items():
            if column in data.columns:
                # Limpiar datos y obtener valores únicos
                column_data = data[column].dropna()
                if len(column_data) == 0:
                    st.warning(f"⚠️ No hay datos válidos para {config['label']}")
                    continue
                
                unique_values = column_data.astype(str).unique()
                unique_values = [v for v in unique_values if v not in ['nan', 'None', '']]
                
                if config["type"] == "date_range" and len(unique_values) > 0:
                    try:
                        min_date = data[column].min()
                        max_date = data[column].max()
                        if pd.notna(min_date) and pd.notna(max_date):
                            filters[column] = st.date_input(
                                config["label"],
                                value=(min_date.date(), max_date.date()),
                                key=f"{column}_filter",
                            )
                    except Exception:
                        st.warning(f"⚠️ Error procesando fechas en {config['label']}")
                        
                elif config["type"] == "multiselect" and len(unique_values) > 0:
                    sorted_values = sorted(unique_values)
                    
                    # Para datasets grandes, limitar opciones iniciales
                    if len(sorted_values) > 100:
                        st.info(f"📊 {len(sorted_values)} opciones disponibles en {config['label']}")
                        
                        # Opción de búsqueda para datasets grandes
                        if config.get("searchable", False):
                            search_term = st.text_input(
                                f"🔍 Buscar en {config['label']}", 
                                key=f"{column}_search"
                            )
                            if search_term:
                                filtered_values = [v for v in sorted_values 
                                                if search_term.lower() in v.lower()]
                                sorted_values = filtered_values[:50]  # Limitar a 50 resultados
                            else:
                                sorted_values = sorted_values[:50]  # Mostrar solo los primeros 50
                        else:
                            sorted_values = sorted_values[:50]
                    
                    filters[column] = st.multiselect(
                        config["label"],
                        options=sorted_values,
                        key=f"{column}_filter",
                        help=f"Total disponible: {len(unique_values)}" if len(unique_values) > len(sorted_values) else None
                    )
                    
    return filters


def apply_filters(data, filters):
    """Aplica los filtros seleccionados al DataFrame."""
    filtered_data = data.copy()
    
    for column, filter_vals in filters.items():
        if filter_vals and column in filtered_data.columns:
            try:
                if column == "Date":
                    # Manejar filtro de fechas
                    if hasattr(filter_vals, '__len__') and len(filter_vals) == 2:
                        start_date, end_date = filter_vals
                        date_column = filtered_data["Date"]
                        if date_column.dtype == 'object':
                            date_column = pd.to_datetime(date_column, errors='coerce')
                        
                        mask = (date_column.dt.date >= start_date) & (date_column.dt.date <= end_date)
                        filtered_data = filtered_data[mask]
                        
                elif isinstance(filter_vals, (list, tuple)) and filter_vals:
                    # Manejar filtros multiselect
                    # Convertir tanto los datos como los filtros a string para comparación consistente
                    column_str = filtered_data[column].astype(str)
                    filter_vals_str = [str(v) for v in filter_vals]
                    
                    # Excluir valores NaN/None explícitamente
                    mask = column_str.isin(filter_vals_str) & (column_str.notna()) & (column_str != 'nan')
                    filtered_data = filtered_data[mask]
                    
            except Exception as e:
                st.warning(f"⚠️ Error aplicando filtro {column}: {str(e)}")
                continue
                
    return filtered_data
