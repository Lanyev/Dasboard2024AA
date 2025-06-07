import streamlit as st
import pandas as pd
import os


@st.cache_data
def get_available_datasets():
    """Obtiene la lista de datasets disponibles"""
    datasets = {}
    # Buscar archivos CSV en el directorio actual
    for file in os.listdir('.'):
        if file.startswith('hots_cleaned_data_modified') and file.endswith('.csv'):
            if '2025_1' in file:
                datasets['🌟 Alan Awards 2025 Summer Edition'] = file
            elif file == 'hots_cleaned_data_modified.csv':
                datasets['🏆 Alan Awards 2024 Complete'] = file
    return datasets


@st.cache_data
def load_data(file_path=None):
    """Carga los datos desde el archivo especificado"""
    if file_path is None:
        file_path = "hots_cleaned_data_modified.csv"
    
    data = pd.read_csv(file_path)
    
    # Normalizar estructura según el tipo de archivo
    if '2025_1' in file_path:
        # Nuevo formato 2025
        data = normalize_2025_format(data)
    else:
        # Formato original 2024
        data = normalize_2024_format(data)
    
    # Aplicar limpieza de datos
    data = clean_data(data)
    
    return data


def normalize_2024_format(data):
    """Normaliza el formato de datos de 2024"""
    data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
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
    
    # Normalizar columna Winner
    if 'Winner' in df.columns:
        # Convertir valores booleanos y numéricos a texto consistente
        df['Winner'] = df['Winner'].astype(str).str.strip().str.lower()
        winner_mapping = {
            'true': 'Winner', '1': 'Winner', '1.0': 'Winner',
            'false': 'Loser', '0': 'Loser', '0.0': 'Loser',
            'nan': 'Unknown', 'none': 'Unknown', '': 'Unknown'
        }
        df['Winner'] = df['Winner'].replace(winner_mapping)
        # Si no coincide con ningún mapeo, marcar como Unknown
        valid_values = ['Winner', 'Loser', 'Unknown']
        df.loc[~df['Winner'].isin(valid_values), 'Winner'] = 'Unknown'
    
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
                st.warning(f"⚠️ Se encontraron {short_games_mask.sum()} partidas anómalamente cortas (< 3 min) que serán marcadas para revisión")
                # En lugar de eliminar, marcar con una etiqueta
                df.loc[short_games_mask, 'DataQuality'] = 'Short Game'
    
    return df
