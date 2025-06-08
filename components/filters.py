import streamlit as st
import pandas as pd


def create_filters(data):
    """Genera los filtros en la barra lateral de Streamlit."""
    filters = {}
    
    # Lista de jugadores VIP (filtro especial)
    VIP_PLAYERS = [
        "Deathmask", "Zombicioso", "Indigente", "Rampage15th", "Omarman",
        "Raizenser", "ChapelHots", "Ticoman", "Swift", "Watchdogman", "Malenfant"
    ]
    
    filter_config = {
        "Date": {"type": "date_range", "label": "Rango de Fechas"},
        "PlayerName": {"type": "multiselect", "label": "Jugadores", "searchable": True},
        "Role": {"type": "multiselect", "label": "Roles", "searchable": False},
        "Map": {"type": "multiselect", "label": "Mapas", "searchable": True},
        "HeroName": {"type": "multiselect", "label": "Héroes", "searchable": True},
    }

    with st.sidebar:
        st.markdown("### 🎯 Filtros")
        
        # FILTRO ESPECIAL VIP - Activado por defecto
        st.markdown("#### ⭐ Filtro Especial VIP")
          # Verificar cuántos jugadores VIP están en los datos
        if 'PlayerName' in data.columns:
            available_vip_players = [p for p in VIP_PLAYERS if p in data['PlayerName'].values]
            vip_count = len(available_vip_players)
            
            if vip_count > 0:
                # Checkbox para activar/desactivar filtro VIP
                use_vip_filter = st.checkbox(
                    f"🌟 Mostrar solo jugadores VIP ({vip_count} disponibles)",
                    value=True,  # Activado por defecto
                    help=f"Jugadores VIP disponibles: {', '.join(available_vip_players[:5])}{'...' if len(available_vip_players) > 5 else ''}"
                )
                
                # Añadir el filtro VIP
                filters['_vip_filter'] = use_vip_filter
                filters['_vip_players'] = available_vip_players
                  # Mostrar estadísticas del filtro VIP
                if use_vip_filter:
                    vip_data = data[data['PlayerName'].isin(available_vip_players)]
                    st.success(f"✅ Mostrando {len(vip_data):,} partidas de jugadores VIP")
                else:
                    st.info(f"ℹ️ Mostrando todos los {len(data):,} registros")
            else:
                st.warning("⚠️ No se encontraron jugadores VIP en el dataset actual")
        
        st.markdown("---")  # Separador visual
        
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
      # APLICAR FILTRO VIP PRIMERO (si está activo)
    if filters.get('_vip_filter', False) and filters.get('_vip_players'):
        vip_players = filters['_vip_players']
        if 'PlayerName' in filtered_data.columns:
            # Filtrar solo jugadores VIP
            filtered_data = filtered_data[filtered_data['PlayerName'].isin(vip_players)]
    
    # Aplicar filtros regulares
    for column, filter_vals in filters.items():
        # Saltar filtros especiales internos
        if column.startswith('_'):
            continue
            
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
