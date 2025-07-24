import streamlit as st
import pandas as pd
import os


@st.cache_data
def get_available_datasets():
    """Obtiene la lista de datasets disponibles"""
    datasets = {}
    
    # Dataset principal actual
    if os.path.exists('structured_data.csv'):
        datasets['🌟 HotS Complete Data 2025'] = 'structured_data.csv'
    
    # Datasets de backup si existen en la carpeta temporal
    if os.path.exists('temp_backup_csv'):
        for file in os.listdir('temp_backup_csv'):
            if file.startswith('hots_cleaned_data_modified') and file.endswith('.csv'):
                if '2025_1' in file:
                    datasets['📦 Backup: Alan Awards 2025 Summer'] = f'temp_backup_csv/{file}'
                elif file == 'hots_cleaned_data_modified.csv':
                    datasets['📦 Backup: Alan Awards 2024 Complete'] = f'temp_backup_csv/{file}'
    
    return datasets


@st.cache_data
def load_data(file_path=None):
    """Carga los datos desde el archivo especificado"""
    if file_path is None:
        file_path = "structured_data.csv"
    
    data = pd.read_csv(file_path)
    
    # Normalizar estructura según el tipo de archivo
    if 'structured_data.csv' in file_path:
        # Nuevo formato structured_data (formato estándar)
        data = normalize_structured_format(data)
    elif '2025_1' in file_path:
        # Formato backup 2025
        data = normalize_2025_format(data)
    else:
        # Formato backup 2024
        data = normalize_2024_format(data)
    
    # Unificar jugadores
    data = unify_players(data)
    
    # Aplicar limpieza de datos
    data = clean_data(data)
    
    return data


def normalize_2024_format(data):
    """Normaliza el formato de datos de 2024"""
    data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    return data


def normalize_structured_format(data):
    """Normaliza el formato de structured_data.csv (formato principal actual)"""
    # Mapear columnas del formato structured_data al formato esperado
    column_mapping = {
        'PlayerName': 'Player',           # PlayerName → Player
        'HeroName': 'Hero',               # HeroName → Hero
        'FileName': 'File',               # FileName → File
        'HeroDamage': 'HeroDmg',         # HeroDamage → HeroDmg
        'StructureDamage': 'SiegeDmg',    # StructureDamage → SiegeDmg
        'HealingShielding': 'Healing',    # HealingShielding → Healing
        'DamageTaken': 'DmgTaken'         # DamageTaken → DmgTaken
    }
    
    # Aplicar mapeo de columnas si existen
    for old_col, new_col in column_mapping.items():
        if old_col in data.columns and new_col not in data.columns:
            data[new_col] = data[old_col]
    
    # Optimizar dataset eliminando redundancias
    data = optimize_dataset(data)
    
    # Crear columna Date a partir de FileName
    if 'FileName' in data.columns or 'File' in data.columns:
        file_col = 'File' if 'File' in data.columns else 'FileName'
        # Extraer fecha del nombre del archivo (formato esperado: YYYY-MM-DD)
        data['Date'] = pd.to_datetime(data[file_col].str.extract(r'(\d{4}-\d{2}-\d{2})')[0], errors='coerce')
        
        # Extraer hora de inicio si está disponible
        time_match = data[file_col].str.extract(r'(\d{2}\.\d{2}\.\d{2})')
        if not time_match[0].isna().all():
            data['StartTime'] = pd.to_datetime(time_match[0], format='%H.%M.%S', errors='coerce').dt.time
    
    # Convertir GameTime a timedelta
    data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
      # Crear columna Role basada en el mapeo automático
    data = apply_role_mapping(data)
    
    # No normalizar Winner aquí - se hace en clean_data()
    
    return data


def normalize_2025_format(data):
    """Normaliza el formato de datos de 2025 y mapea a estructura compatible"""
    # Mapear columnas del nuevo formato al formato esperado por la aplicación
    column_mapping = {
        'PlayerName': 'Player',           # Nuevo: PlayerName → Player
        'HeroName': 'Hero',               # Nuevo: HeroName → Hero
        'FileName': 'File',               # Nuevo: FileName → File
    }
    
    # Aplicar mapeo de columnas si existen
    for old_col, new_col in column_mapping.items():
        if old_col in data.columns and new_col not in data.columns:
            data[new_col] = data[old_col]
    
    # Crear columna Date y StartTime a partir de FileName
    if 'FileName' in data.columns or 'File' in data.columns:
        file_col = 'File' if 'File' in data.columns else 'FileName'
        # Extraer fecha del nombre del archivo (formato esperado: YYYY-MM-DD_HH-MM-SS)
        data['Date'] = pd.to_datetime(data[file_col].str.extract(r'(\d{4}-\d{2}-\d{2})')[0], errors='coerce')
        data['StartTime'] = data[file_col].str.extract(r'(\d{2}-\d{2}-\d{2})')[0]
        data['StartTime'] = pd.to_datetime(data['StartTime'], format='%H-%M-%S', errors='coerce').dt.time
    
    # Aplicar role mapping y limpieza
    data = apply_role_mapping(data)
    
    # Convertir GameTime a timedelta
    data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
    
    return data


def clean_hero_names(data):
    """Limpia y corrige nombres de héroes con problemas de encoding"""
    name_corrections = {
        'Puntos': 'Stitches',
        'AzmodÃ¡n': 'Azmodan',
        'LÃºcio': 'Lucio', 
        'Mefisto': 'Mephisto',
        'Cromi': 'Chromie',
        'Teniente Morales': 'Lt. Morales'
    }
    
    if 'Hero' in data.columns:
        data['Hero'] = data['Hero'].replace(name_corrections)
    if 'HeroName' in data.columns:
        data['HeroName'] = data['HeroName'].replace(name_corrections)
    
    return data


def unify_players(data):
    """Unifica jugadores que deben ser tratados como uno solo en todas las columnas relevantes."""
    # Definir todas las variantes a unificar
    player_unify_map = {
        'Swift': 'WatchdogMan',
    }
    for col in ['PlayerName', 'Player']:
        if col in data.columns:
            data[col] = data[col].replace(player_unify_map)
    return data


def get_automatic_role_mapping():
    """Obtiene mapeo automático de héroes a roles"""
    # Mapeo manual para casos especiales y correcciones
    manual_mappings = {
        # Correcciones de nombres con problemas de encoding
        'Azmodan': 'Assassin',
        'Lucio': 'Support', 
        'Mephisto': 'Assassin',
        'Chromie': 'Assassin',
        'Lt. Morales': 'Support',
        'Stitches': 'Tank',  # Corrección para "Puntos"
        
        # Héroes estándar por rol
        'Abathur': 'Specialist',
        'Alarak': 'Assassin',
        'Alexstrasza': 'Support',
        'Ana': 'Support',
        'Anduin': 'Support',
        'Anub\'arak': 'Tank',
        'Artanis': 'Bruiser',
        'Arthas': 'Tank',
        'Auriel': 'Support',
        'Azmodan': 'Assassin',
        'Blaze': 'Tank',
        'Brightwing': 'Support',
        'Cassia': 'Assassin',
        'Chen': 'Tank',
        'Cho': 'Tank',
        'Chromie': 'Assassin',
        'D.Va': 'Tank',
        'Deckard': 'Support',
        'Deathwing': 'Bruiser',
        'Dehaka': 'Bruiser',
        'Diablo': 'Tank',
        'E.T.C.': 'Tank',
        'Falstad': 'Assassin',
        'Fenix': 'Assassin',
        'Gall': 'Assassin',
        'Garrosh': 'Tank',
        'Gazlowe': 'Bruiser',
        'Genji': 'Assassin',
        'Greymane': 'Assassin',
        'Gul\'dan': 'Assassin',
        'Hanzo': 'Assassin',
        'Hogger': 'Bruiser',
        'Illidan': 'Assassin',
        'Imperius': 'Bruiser',
        'Jaina': 'Assassin',
        'Johanna': 'Tank',
        'Junkrat': 'Assassin',
        'Kael\'thas': 'Assassin',
        'Kel\'Thuzad': 'Assassin',
        'Kerrigan': 'Assassin',
        'Kharazim': 'Support',
        'Leoric': 'Bruiser',
        'Li Li': 'Support',
        'Li-Ming': 'Assassin',
        'Lt. Morales': 'Support',
        'Lucio': 'Support',
        'Lunara': 'Assassin',
        'Maiev': 'Assassin',
        'Mal\'Ganis': 'Tank',
        'Malfurion': 'Support',
        'Malthael': 'Bruiser',
        'Medivh': 'Support',
        'Mei': 'Tank',
        'Mephisto': 'Assassin',
        'Muradin': 'Tank',
        'Murky': 'Specialist',
        'Nazeebo': 'Assassin',
        'Nova': 'Assassin',
        'Orphea': 'Assassin',
        'Probius': 'Specialist',
        'Qhira': 'Assassin',
        'Ragnaros': 'Bruiser',
        'Raynor': 'Assassin',
        'Rehgar': 'Support',
        'Rexxar': 'Bruiser',
        'Samuro': 'Assassin',
        'Sgt. Hammer': 'Specialist',
        'Sonya': 'Bruiser',
        'Stitches': 'Tank',
        'Stukov': 'Support',
        'Sylvanas': 'Specialist',
        'Tassadar': 'Assassin',
        'The Butcher': 'Assassin',
        'The Lost Vikings': 'Specialist',
        'Thrall': 'Assassin',
        'Tracer': 'Assassin',
        'Tyrael': 'Tank',
        'Tyrande': 'Support',
        'Tychus': 'Assassin',
        'Uther': 'Support',
        'Valeera': 'Assassin',
        'Valla': 'Assassin',
        'Varian': 'Tank',
        'Whitemane': 'Support',
        'Xul': 'Specialist',
        'Yrel': 'Tank',
        'Zagara': 'Specialist',
        'Zarya': 'Bruiser',
        'Zeratul': 'Assassin',
        'Zuljin': 'Assassin'
    }
    
    return manual_mappings


def apply_role_mapping(data):
    """Aplica mapeo de roles automático a los datos"""
    if 'Hero' not in data.columns:
        return data
    
    # Primero limpiar nombres de héroes
    data = clean_hero_names(data)
    
    # Obtener mapeo automático
    role_mapping = get_automatic_role_mapping()
    
    # Aplicar mapeo automático donde no hay Role o donde Role es Unknown/NaN
    if 'Role' not in data.columns:
        data['Role'] = 'Unknown'
    
    # Mapear roles donde no están definidos o son Unknown
    mask = (data['Role'].isna()) | (data['Role'] == 'Unknown') | (data['Role'] == '')
    data.loc[mask, 'Role'] = data.loc[mask, 'Hero'].map(role_mapping).fillna('Unknown')
    
    # Filtrar registros con datos válidos
    data = data.dropna(subset=['Hero'])
    
    return data


@st.cache_data
def clean_data(data):
    """Limpia los datos mejorando la calidad y consistencia"""
    df = data.copy()
    
    # Limpiar valores NaN críticos
    if 'Player' in df.columns:
        # Rellenar jugadores vacíos con "Jugador Desconocido"
        df['Player'] = df['Player'].fillna('Jugador Desconocido')
        df['Player'] = df['Player'].replace('', 'Jugador Desconocido')
    
    if 'Hero' in df.columns:
        # Rellenar héroes vacíos con "Héroe Desconocido"
        df['Hero'] = df['Hero'].fillna('Héroe Desconocido')
        df['Hero'] = df['Hero'].replace('', 'Héroe Desconocido')
      # Normalizar columna Winner - mantener formato original Yes/No
    if 'Winner' in df.columns:
        # Simplemente limpiar valores inválidos, manteniendo Yes/No
        valid_winner_values = ['Yes', 'No']
        df.loc[~df['Winner'].isin(valid_winner_values), 'Winner'] = 'Unknown'
    
    # Limpiar métricas numéricas
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        # Reemplazar valores infinitos con NaN
        df[col] = df[col].replace([float('inf'), float('-inf')], pd.NA)
        # Para métricas que no pueden ser negativas, reemplazar negativos con 0
        if col in ['HeroDmg', 'SiegeDmg', 'Healing', 'SelfHealing', 'DmgTaken']:
            df.loc[df[col] < 0, col] = 0
    
    # Limpiar duplicados
    if 'File' in df.columns or 'FileName' in df.columns:
        file_col = 'File' if 'File' in df.columns else 'FileName'
        # Identificar duplicados por archivo, jugador y héroe
        subset_cols = [file_col, 'Player', 'Hero']
        subset_cols = [col for col in subset_cols if col in df.columns]
        df = df.drop_duplicates(subset=subset_cols, keep='first')
      # Limpiar partidas anómalamente cortas (menos de 3 minutos)
    if 'GameTime' in df.columns:
        if df['GameTime'].dtype == 'timedelta64[ns]':
            # Filtrar partidas muy cortas (probablemente errores)
            min_game_time = pd.Timedelta(minutes=3)
            short_games_mask = df['GameTime'] < min_game_time
            if short_games_mask.sum() > 0:
                # Guardar mensaje para mostrar al final
                if 'footer_messages' not in st.session_state:
                    st.session_state.footer_messages = []
                st.session_state.footer_messages.append(
                    f"⚠️ Se encontraron {short_games_mask.sum()} partidas anómalamente cortas (< 3 min) que serán marcadas para revisión"
                )
                # En lugar de eliminar, marcar con una etiqueta
                df.loc[short_games_mask, 'DataQuality'] = 'Short Game'
    
    return df


def optimize_dataset(data):
    """Optimiza el dataset eliminando columnas redundantes identificadas"""
    df = data.copy()
    
    # Lista de columnas redundantes a eliminar
    redundant_columns = [
        'Takedowns',     # Duplicado: Takedowns = HeroKills + Assists
        'SummonDamage'   # Redundante: Siempre 0 en los datos
    ]
      # Eliminar columnas redundantes si existen
    columns_removed = []
    for col in redundant_columns:
        if col in df.columns:
            df = df.drop(columns=[col])
            columns_removed.append(col)
    
    # Crear columna Takedowns calculada dinámicamente si se necesita
    if 'Takedowns' in redundant_columns and 'HeroKills' in df.columns and 'Assists' in df.columns:
        df['Takedowns'] = df['HeroKills'] + df['Assists']
    
    if columns_removed:
        # Guardar mensaje para mostrar al final
        if 'footer_messages' not in st.session_state:
            st.session_state.footer_messages = []
        st.session_state.footer_messages.append(
            f"🔧 Optimización aplicada: Eliminadas columnas redundantes: {', '.join(columns_removed)}"
        )
    
    return df
