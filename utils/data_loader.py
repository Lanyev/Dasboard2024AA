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
                datasets['🆕 Temporada 2025 - Parte 1'] = file
            elif file == 'hots_cleaned_data_modified.csv':
                datasets['🏆 Alan Awards 2024'] = file
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
        'PlayerName': 'Player',
        'HeroName': 'Hero',
        'HeroDamage': 'HeroDmg',          # Correcto: HeroDamage → HeroDmg
        'DamageTaken': 'DmgTaken',        # Correcto: DamageTaken → DmgTaken
        'MinionDamage': 'MinionDmg',
        'SummonDamage': 'SummonDmg',
        'StructureDamage': 'StructDmg',
        'TotalSiegeDamage': 'SiegeDmg',   # Correcto: TotalSiegeDamage → SiegeDmg
        'Experience': 'XP',               # Correcto: Experience → XP
        'HealingShielding': 'HealShield', # Correcto: HealingShielding → HealShield
        'SelfHealing': 'SelfHeal',
        'MinionKills': 'MinionKills',
        'RegenGlobes': 'Regen',
        'MercCampCaptures': 'MercCaptures',
        'SpellDamage': 'SpellDmg',
        'PhysicalDamage': 'PhysDmg',
        'MercDamage': 'MercDmg',
        'RootingHeroes': 'Rooting',
        'SilenceHeroes': 'Silence',
        'StunHeroes': 'Stun',
        'CCHeroes': 'CC',                 # Correcto: CCHeroes → CC
        'FileName': 'File',               # Nuevo: FileName → File
    }    
    # Renombrar columnas
    data = data.rename(columns=column_mapping)
    
    # Crear columnas faltantes que necesita la aplicación
    
    # Crear columna Date y StartTime a partir de FileName
    if 'File' in data.columns and 'Date' not in data.columns:
        # Extraer fecha del nombre del archivo (formato: "2025-03-10 00.06.56...")
        data['Date'] = pd.to_datetime(data['File'].str[:10], errors="coerce")
        data['StartTime'] = data['File'].str[11:19].str.replace('.', ':', regex=False)
    
    # Procesar GameTime
    if 'GameTime' in data.columns:
        data["GameTime"] = pd.to_timedelta(data["GameTime"], errors="coerce")
      # Convertir Winner de Yes/No a Winner/Loser
    if 'Winner' in data.columns:
        data['Winner'] = data['Winner'].map({'Yes': 'Winner', 'No': 'Loser'})
    
    # Limpiar nombres de héroes erróneos
    data = clean_hero_names(data)
    
    # Crear columna Role basada en mapeo automático desde dataset 2024
    role_mapping = get_automatic_role_mapping()
    data['Role'] = data['Hero'].map(role_mapping).fillna('Unknown')
    
    # Filtrar registros con datos erróneos
    invalid_heroes = ['Puntos', 'nan', '']
    data = data[~data['Hero'].isin(invalid_heroes)]
    data = data[data['Hero'].notna()]
    
    return data


@st.cache_data
def get_automatic_role_mapping():
    """Obtiene mapeo automático de Hero→Role desde el dataset 2024"""
    try:
        # Cargar dataset de referencia (2024) que ya tiene roles
        df_2024 = pd.read_csv("hots_cleaned_data_modified.csv")
        
        if 'Role' not in df_2024.columns or 'Hero' not in df_2024.columns:
            return get_fallback_role_mapping()
        
        # Crear mapeo basado en el rol más frecuente para cada héroe
        hero_role_mapping = df_2024.groupby('Hero')['Role'].agg(
            lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'
        ).to_dict()          # Agregar mapeos manuales para héroes con nombres diferentes
        manual_mappings = {
            'AzmodÃ¡n': 'Mage',           # Azmodán con encoding issues
            'LÃºcio': 'Healer',          # Lúcio con encoding issues  
            'Teniente Morales': 'Healer', # Lt. Morales en español
            'Mefisto': 'Mage',           # Mephisto en español
            'Cromi': 'Mage',             # Chromie en español
            'Puntos': 'Tank',            # Stitches con datos erróneos
        }
        
        hero_role_mapping.update(manual_mappings)
        
        return hero_role_mapping
        
    except Exception as e:
        print(f"Error en mapeo automático: {e}")
        return get_fallback_role_mapping()


def get_fallback_role_mapping():
    """Mapeo de respaldo en caso de error"""
    return {
        # Assassins
        'Cassia': 'Ranged Assassin', 'Thrall': 'Melee Assassin', 'Genji': 'Melee Assassin',
        'Fenix': 'Ranged Assassin', 'Gazlowe': 'Ranged Assassin', 'Samuro': 'Melee Assassin',
        'Greymane': 'Ranged Assassin', 'Nazeebo': 'Ranged Assassin', 'Valla': 'Ranged Assassin',
        'Raynor': 'Ranged Assassin', 'Jaina': 'Mage', 'Kael\'thas': 'Mage',
        'Nova': 'Ranged Assassin', 'Zeratul': 'Melee Assassin', 'Illidan': 'Melee Assassin',
        'Kerrigan': 'Melee Assassin', 'Butcher': 'Melee Assassin', 'Sonya': 'Bruiser',
        'Alarak': 'Melee Assassin', 'Malthael': 'Melee Assassin', 'Qhira': 'Melee Assassin',
          # Tanks
        'E.T.C.': 'Tank', 'Diablo': 'Tank', 'Muradin': 'Tank', 'Johanna': 'Tank',
        'Anub\'arak': 'Tank', 'Arthas': 'Tank', 'Tyrael': 'Tank', 'Varian': 'Tank',
        'Garrosh': 'Tank', 'Blaze': 'Tank', 'Mal\'Ganis': 'Tank', 'Imperius': 'Tank',
        'Deathwing': 'Tank', 'Hogger': 'Tank', 'Stitches': 'Tank',
        
        # Healers/Support
        'Malfurion': 'Healer', 'Anduin': 'Healer', 'Rehgar': 'Healer', 'Li Li': 'Healer',
        'Brightwing': 'Healer', 'Uther': 'Healer', 'Tyrande': 'Support', 'Tassadar': 'Support',
        'Kharazim': 'Healer', 'Morales': 'Healer', 'Auriel': 'Healer', 'Lucio': 'Healer',
        'Ana': 'Healer', 'Deckard': 'Healer', 'Whitemane': 'Healer', 'Stukov': 'Healer',
        'Alexstrasza': 'Healer',
        
        # Bruisers
        'Artanis': 'Bruiser', 'Dehaka': 'Bruiser', 'Leoric': 'Bruiser',
        'Ragnaros': 'Bruiser', 'D.Va': 'Bruiser', 'Yrel': 'Bruiser',
        
        # Mages/Specialists
        'Abathur': 'Support', 'Azmodan': 'Mage', 'Murky': 'Melee Assassin',
        'The Lost Vikings': 'Support', 'Zagara': 'Ranged Assassin', 'Sylvanas': 'Ranged Assassin',
        'Xul': 'Melee Assassin', 'Probius': 'Ranged Assassin'
    }


def clean_hero_names(data):
    """Limpia nombres de héroes erróneos en los datos"""
    if 'Hero' not in data.columns:
        return data
    
    # Mapeo de nombres erróneos a nombres correctos
    name_corrections = {
        'Puntos': 'Stitches',  # Error de datos: "Puntos" es realmente Stitches
        # Aquí se pueden agregar más correcciones si se encuentran otros errores
    }
    
    # Aplicar correcciones
    data['Hero'] = data['Hero'].replace(name_corrections)
    
    return data

