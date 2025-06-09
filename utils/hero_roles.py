"""
Sistema de roles de héroes para Heroes of the Storm
Maneja la clasificación de héroes y análisis de composiciones
"""

def get_hero_roles():
    """Retorna un diccionario con los roles de cada héroe.
    Para héroes multi-rol, se usa el rol principal, pero se documentan los alternativos.
    """
    
    hero_roles = {
        # TANKS
        'Anub\'arak': 'Tank',
        'Arthas': 'Tank', 
        'Blaze': 'Tank',
        'Diablo': 'Tank',
        'E.T.C.': 'Tank',
        'Garrosh': 'Tank',
        'Johanna': 'Tank',
        'Mal\'Ganis': 'Tank',
        'Mei': 'Tank',
        'Muradin': 'Tank',
        'Stitches': 'Tank',
        'Tyrael': 'Tank',
        'Varian': 'Tank',
        
        # BRUISERS
        'Artanis': 'Bruiser',
        'Chen': 'Bruiser',
        'Dehaka': 'Bruiser',
        'Gazlowe': 'Bruiser',
        'Hogger': 'Bruiser',
        'Imperius': 'Bruiser',
        'Leoric': 'Bruiser',
        'Malthael': 'Bruiser',
        'Ragnaros': 'Bruiser',
        'Rexxar': 'Bruiser',
        'Sonya': 'Bruiser',
        'Thrall': 'Bruiser',
        'Yrel': 'Bruiser',
        'D.Va': 'Bruiser',
        'Xul': 'Bruiser',
        'Zarya': 'Bruiser',
        
        # MELEE ASSASSINS
        'Alarak': 'Melee Assassin',
        'Illidan': 'Melee Assassin',
        'Kerrigan': 'Melee Assassin',
        'Maiev': 'Melee Assassin',
        'Murky': 'Melee Assassin',
        'Qhira': 'Melee Assassin',
        'Samuro': 'Melee Assassin',
        'The Butcher': 'Melee Assassin',
        'Valeera': 'Melee Assassin',
        'Zeratul': 'Melee Assassin',
        'Genji': 'Melee Assassin',
        'Tracer': 'Melee Assassin',
        
        # MAGES
        'Azmodan': 'Mage',
        'Chromie': 'Mage',
        'Gul\'dan': 'Mage',
        'Jaina': 'Mage',
        'Kael\'thas': 'Mage',
        'Kel\'Thuzad': 'Mage',
        'Li-Ming': 'Mage',
        'Mephisto': 'Mage',
        'Nazeebo': 'Mage',
        'Orphea': 'Mage',
        'Probius': 'Mage',
        'Tassadar': 'Mage',
        'Deathwing': 'Mage',
        
        # RANGED ASSASSINS
        'Cassia': 'Ranged Assassin',
        'Falstad': 'Ranged Assassin',
        'Fenix': 'Ranged Assassin',
        'Greymane': 'Ranged Assassin',
        'Hanzo': 'Ranged Assassin',
        'Junkrat': 'Ranged Assassin',
        'Lunara': 'Ranged Assassin',
        'Nova': 'Ranged Assassin',
        'Raynor': 'Ranged Assassin',
        'Sylvanas': 'Ranged Assassin',
        'Tychus': 'Ranged Assassin',
        'Valla': 'Ranged Assassin',
        'Zagara': 'Ranged Assassin',
        'Zul\'jin': 'Ranged Assassin',
        
        # HEALERS
        'Alexstrasza': 'Healer',
        'Ana': 'Healer',
        'Anduin': 'Healer',
        'Auriel': 'Healer',
        'Brightwing': 'Healer',
        'Deckard': 'Healer',
        'Kharazim': 'Healer',
        'Li Li': 'Healer',
        'Lt. Morales': 'Healer',
        'Lúcio': 'Healer',
        'Malfurion': 'Healer',
        'Rehgar': 'Healer',
        'Stukov': 'Healer',
        'Tyrande': 'Healer',
        'Uther': 'Healer',
        'Whitemane': 'Healer',
        
        # SUPPORTS
        'Medivh': 'Support',
    }
    
    return hero_roles

def get_multi_role_heroes():
    """Retorna un diccionario con héroes que pueden desempeñar múltiples roles"""
    
    multi_role_heroes = {
        'Varian': ['Tank', 'Bruiser'],
        'Dehaka': ['Bruiser', 'Tank'],
        'Zarya': ['Bruiser', 'Support'],
        'Xul': ['Bruiser', 'Support'],
        'Kharazim': ['Healer', 'Melee Assassin'],
        'Tyrande': ['Healer', 'Support'],
        'Medivh': ['Support', 'Mage'],
        'Tassadar': ['Mage', 'Support'],
        'Chen': ['Bruiser', 'Tank'],
        'Blaze': ['Tank', 'Bruiser'],
        'Yrel': ['Bruiser', 'Tank'],
        'Artanis': ['Bruiser', 'Tank'],
    }
    
    return multi_role_heroes

def get_hero_role(hero_name):
    """Obtiene el rol de un héroe específico"""
    hero_roles = get_hero_roles()
    return hero_roles.get(hero_name, 'Unknown')

def get_all_roles():
    """Retorna lista de todos los roles disponibles"""
    return ['Tank', 'Bruiser', 'Melee Assassin', 'Ranged Assassin', 'Mage', 'Healer', 'Support']

def get_heroes_by_role(role):
    """Retorna lista de héroes para un rol específico"""
    hero_roles = get_hero_roles()
    return [hero for hero, hero_role in hero_roles.items() if hero_role == role]

def classify_composition(heroes):
    """Clasifica una composición de 5 héroes y retorna análisis de roles"""
    if len(heroes) != 5:
        return None
    
    hero_roles = get_hero_roles()
    composition = {}
    
    for hero in heroes:
        role = hero_roles.get(hero, 'Unknown')
        if role not in composition:
            composition[role] = 0
        composition[role] += 1
    
    return composition

def get_composition_type(composition_dict):
    """Determina el tipo de composición basado en los roles"""
    if not composition_dict:
        return "Unknown"
    
    # Composiciones estándar
    if composition_dict.get('Tank', 0) >= 1 and composition_dict.get('Healer', 0) >= 1:
        if composition_dict.get('Tank', 0) == 1:
            return "Standard (1 Tank)"
        else:
            return "Double Tank"
    
    elif composition_dict.get('Bruiser', 0) >= 2:
        return "Double Bruiser"
    
    elif composition_dict.get('Healer', 0) >= 2:
        return "Double Support"
    
    elif composition_dict.get('Healer', 0) == 0:
        return "No Support"
    
    elif composition_dict.get('Tank', 0) == 0 and composition_dict.get('Bruiser', 0) >= 1:
        return "No Tank (Bruiser Solo)"
    
    else:
        return "Unusual Composition"
