import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def create_friendly_date_filter(date_series, label):
    """Crea un filtro de fechas más amigable con botones por año y mes"""
    
    # Obtener rango completo de fechas
    min_date = date_series.min()
    max_date = date_series.max()
    
    if pd.isna(min_date) or pd.isna(max_date):
        return None
    
    # Convertir a datetime si es necesario
    if isinstance(min_date, str):
        min_date = pd.to_datetime(min_date)
    if isinstance(max_date, str):
        max_date = pd.to_datetime(max_date)
    
    # Extraer años y meses disponibles
    date_series_clean = pd.to_datetime(date_series.dropna())
    available_years = sorted(date_series_clean.dt.year.unique())
    
    st.markdown(f"#### 📅 {label}")
    
    # Inicializar session_state para el filtro de fechas si no existe
    if f"{label}_date_filter" not in st.session_state:
        st.session_state[f"{label}_date_filter"] = (min_date.date(), max_date.date())
    
    # Opciones rápidas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Todo el tiempo", key=f"{label}_all_time"):
            st.session_state[f"{label}_date_filter"] = (min_date.date(), max_date.date())
            st.rerun()
    
    with col2:
        if st.button("📅 Último año", key=f"{label}_last_year"):
            start_date = max_date - timedelta(days=365)
            st.session_state[f"{label}_date_filter"] = (max(start_date.date(), min_date.date()), max_date.date())
            st.rerun()
    
    with col3:
        if st.button("🗓️ Últimos 6 meses", key=f"{label}_last_6m"):
            start_date = max_date - timedelta(days=180)
            st.session_state[f"{label}_date_filter"] = (max(start_date.date(), min_date.date()), max_date.date())
            st.rerun()
    
    # Selector por año
    if len(available_years) > 1:
        st.markdown("**Por Año:**")
        year_cols = st.columns(min(len(available_years), 4))
        
        for i, year in enumerate(available_years):
            with year_cols[i % 4]:
                if st.button(f"{year}", key=f"{label}_year_{year}"):
                    start_date = datetime(year, 1, 1)
                    end_date = datetime(year, 12, 31)
                    # Ajustar al rango disponible
                    start_date = max(start_date, min_date)
                    end_date = min(end_date, max_date)
                    st.session_state[f"{label}_date_filter"] = (start_date.date(), end_date.date())
                    st.rerun()
    
    # Selector por meses del último año
    current_year = max_date.year
    months_in_last_year = date_series_clean[date_series_clean.dt.year == current_year].dt.month.unique()
    
    if len(months_in_last_year) > 1:
        st.markdown(f"**Meses de {current_year}:**")
        month_names = {
            1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
        }
        
        month_cols = st.columns(min(len(months_in_last_year), 6))
        
        for i, month in enumerate(sorted(months_in_last_year)):
            with month_cols[i % 6]:
                if st.button(f"{month_names[month]}", key=f"{label}_month_{month}"):
                    start_date = datetime(current_year, month, 1)
                    if month == 12:
                        end_date = datetime(current_year, 12, 31)
                    else:
                        end_date = datetime(current_year, month + 1, 1) - timedelta(days=1)
                    
                    # Ajustar al rango disponible
                    start_date = max(start_date, min_date)
                    end_date = min(end_date, max_date)
                    st.session_state[f"{label}_date_filter"] = (start_date.date(), end_date.date())
                    st.rerun()
    
    # Selector manual como fallback
    st.markdown("**Rango personalizado:**")
    current_start, current_end = st.session_state[f"{label}_date_filter"]
    
    start_date_input = st.date_input(
        "Fecha inicio",
        value=current_start,
        min_value=min_date.date(),
        max_value=max_date.date(),
        key=f"{label}_start"
    )
    
    end_date_input = st.date_input(
        "Fecha fin",
        value=current_end,
        min_value=min_date.date(),
        max_value=max_date.date(),
        key=f"{label}_end"
    )
    
    # Validar que la fecha de inicio no sea mayor que la de fin
    if start_date_input > end_date_input:
        st.error("❌ La fecha de inicio no puede ser mayor que la fecha de fin")
        return st.session_state[f"{label}_date_filter"]
    
    # Actualizar session_state si las fechas cambiaron manualmente
    new_range = (start_date_input, end_date_input)
    if new_range != st.session_state[f"{label}_date_filter"]:
        st.session_state[f"{label}_date_filter"] = new_range
    
    return st.session_state[f"{label}_date_filter"]


def create_filters(data):
    """Genera los filtros en la barra lateral de Streamlit."""
    filters = {}
    
    # Lista de jugadores Geekos (filtro especial)
    GEEKO_PLAYERS = [
        "Deathmask", "Zombicioso", "Indigente", "Rampage15th", "Omarman",
        "Raizenser", "ChapelHots", "Ticoman", "WatchdogMan", "Malenfant"
    ]
    
    filter_config = {
        "Date": {"type": "date_range", "label": "Rango de Fechas"},
        "Player": {"type": "multiselect", "label": "Jugadores", "searchable": True},
        "Role": {"type": "multiselect", "label": "Roles", "searchable": False},
        "Map": {"type": "multiselect", "label": "Mapas", "searchable": True},
        "Hero": {"type": "multiselect", "label": "Héroes", "searchable": True},
    }

    with st.sidebar:
        st.markdown("### 🎯 Filtros")
        
        # FILTRO ESPECIAL GEEKOS - Activado por defecto
        st.markdown("#### 🎮 Filtro Especial Geekos")
        
        # Verificar cuántos jugadores Geekos están en los datos
        if 'Player' in data.columns:
            available_geeko_players = [p for p in GEEKO_PLAYERS if p in data['Player'].values]
            geeko_count = len(available_geeko_players)
            
            if geeko_count > 0:
                # Crear botones individuales para cada Geeko
                st.markdown("**🎯 Seleccionar Geekos:**")
                
                # Inicializar estado si no existe
                if 'selected_geekos' not in st.session_state:
                    st.session_state.selected_geekos = available_geeko_players.copy()  # Todos seleccionados por defecto
                
                # Botones de control rápido
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Todos", key="select_all_geekos"):
                        st.session_state.selected_geekos = available_geeko_players.copy()
                        st.rerun()
                with col2:
                    if st.button("❌ Ninguno", key="select_none_geekos"):
                        st.session_state.selected_geekos = []
                        st.rerun()
                
                # Crear botones individuales para cada Geeko
                geeko_cols = st.columns(2)  # 2 columnas para los botones
                for i, player in enumerate(available_geeko_players):
                    with geeko_cols[i % 2]:
                        is_selected = player in st.session_state.selected_geekos
                        button_text = f"{'✅' if is_selected else '⬜'} {player}"
                        
                        if st.button(button_text, key=f"geeko_{player}"):
                            if is_selected:
                                st.session_state.selected_geekos.remove(player)
                            else:
                                st.session_state.selected_geekos.append(player)
                            st.rerun()
                
                # Checkbox general para activar/desactivar filtro Geekos
                use_geeko_filter = st.checkbox(
                    f"🌟 Aplicar filtro Geekos ({len(st.session_state.selected_geekos)}/{geeko_count} seleccionados)",
                    value=len(st.session_state.selected_geekos) > 0,  # Activado si hay alguno seleccionado
                    help=f"Geekos disponibles: {', '.join(available_geeko_players)}"
                )
                
                # Añadir el filtro Geekos
                filters['_geeko_filter'] = use_geeko_filter and len(st.session_state.selected_geekos) > 0
                filters['_geeko_players'] = st.session_state.selected_geekos if use_geeko_filter else []
                  # Mostrar estadísticas del filtro Geekos
                if use_geeko_filter and st.session_state.selected_geekos:
                    geeko_data = data[data['Player'].isin(st.session_state.selected_geekos)]
                    st.success(f"✅ Mostrando {len(geeko_data):,} partidas de {len(st.session_state.selected_geekos)} Geekos")
                else:
                    st.info(f"ℹ️ Mostrando todos los {len(data):,} registros")
            else:
                st.warning("⚠️ No se encontraron jugadores Geekos en el dataset actual")
        
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
                            filters[column] = create_friendly_date_filter(data[column], config["label"])
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
    
    # APLICAR FILTRO GEEKOS PRIMERO (si está activo)
    if filters.get('_geeko_filter', False) and filters.get('_geeko_players'):
        geeko_players = filters['_geeko_players']
        if 'Player' in filtered_data.columns:
            # Filtrar solo jugadores Geekos seleccionados
            filtered_data = filtered_data[filtered_data['Player'].isin(geeko_players)]
    
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
