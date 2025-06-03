#!/usr/bin/env python3
"""
Script para corregir los mapeos de roles de héroes que faltan
Mapea los héroes con problemas de encoding y nombres diferentes
"""

import pandas as pd

def fix_hero_role_mappings():
    """Corrige los mapeos de roles faltantes"""
    print("🔧 CORRECCIÓN DE MAPEOS DE ROLES")
    print("=" * 40)
    
    # Mapeos de corrección para héroes con problemas
    corrections = {
        'AzmodÃ¡n': 'Azmodan',      # Problema de encoding UTF-8
        'LÃºcio': 'Lucio',          # Problema de encoding UTF-8  
        'Mefisto': 'Mephisto',      # Traducción/nombre diferente
        'Cromi': 'Chromie',         # Traducción/nombre diferente
        'Teniente Morales': 'Lt. Morales',  # Traducción completa
        'Puntos': None              # Probablemente error de datos
    }
    
    # Roles conocidos para estos héroes
    hero_roles = {
        'Azmodan': 'Mage',
        'Lucio': 'Healer', 
        'Mephisto': 'Mage',
        'Chromie': 'Mage',
        'Lt. Morales': 'Healer'
    }
    
    print("📋 MAPEOS DE CORRECCIÓN:")
    for problema, solucion in corrections.items():
        if solucion:
            role = hero_roles.get(solucion, 'Unknown')
            print(f"   🔄 '{problema}' → '{solucion}' → {role}")
        else:
            print(f"   ❌ '{problema}' → ELIMINAR (probablemente error de datos)")
    
    return corrections, hero_roles

def apply_corrections_to_dataset():
    """Aplica las correcciones al dataset 2025 con roles"""
    print("\n🛠️  APLICANDO CORRECCIONES AL DATASET")
    print("=" * 45)
    
    try:
        # Cargar dataset
        df = pd.read_csv('hots_cleaned_data_modified_2025_1_with_roles.csv')
        print(f"✅ Dataset cargado: {len(df):,} registros")
        
        corrections, hero_roles = fix_hero_role_mappings()
        
        # Aplicar correcciones
        changes_made = 0
        
        for problema, solucion in corrections.items():
            # Contar registros con el problema
            mask = df['HeroName'] == problema
            count = mask.sum()
            
            if count > 0:
                if solucion:
                    # Corregir nombre del héroe
                    df.loc[mask, 'HeroName'] = solucion
                    # Asignar rol correcto
                    role = hero_roles.get(solucion, 'Unknown')
                    df.loc[mask, 'Role'] = role
                    print(f"   ✅ Corregidos {count} registros de '{problema}' → '{solucion}' ({role})")
                    changes_made += count
                else:
                    # Marcar para eliminar
                    df.loc[mask, 'Role'] = 'DELETE'
                    print(f"   🗑️  Marcados {count} registros de '{problema}' para eliminación")
        
        # Eliminar registros marcados como DELETE
        delete_mask = df['Role'] == 'DELETE'
        delete_count = delete_mask.sum()
        if delete_count > 0:
            df = df[~delete_mask]
            print(f"   🗑️  Eliminados {delete_count} registros erróneos")
            changes_made += delete_count
        
        # Verificar estado final
        unknown_heroes = df[df['Role'] == 'Unknown']['HeroName'].unique()
        print(f"\n📊 ESTADO FINAL:")
        print(f"   📈 Registros totales: {len(df):,}")
        print(f"   🔄 Cambios realizados: {changes_made}")
        print(f"   ❓ Héroes aún sin rol: {len(unknown_heroes)}")
        
        if len(unknown_heroes) > 0:
            print("   Lista de héroes sin rol:")
            for hero in sorted(unknown_heroes):
                count = (df['HeroName'] == hero).sum()
                print(f"      - {hero} ({count} registros)")
        
        # Guardar dataset corregido
        output_file = 'hots_cleaned_data_modified_2025_1_with_roles_fixed.csv'
        df.to_csv(output_file, index=False)
        print(f"\n💾 Dataset corregido guardado como: {output_file}")
        
        # Mostrar distribución final de roles
        print(f"\n🎭 DISTRIBUCIÓN FINAL DE ROLES:")
        roles_count = df['Role'].value_counts()
        for role, count in roles_count.items():
            percentage = (count / len(df)) * 100
            print(f"   {role}: {count:,} registros ({percentage:.1f}%)")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_data_loader():
    """Sugiere actualizaciones para el data_loader.py"""
    print("\n📝 SUGERENCIAS PARA ACTUALIZAR data_loader.py")
    print("=" * 50)
    
    print("Agregar estos mapeos al diccionario manual_mappings:")
    print("""
manual_mappings = {
    'AzmodÃ¡n': 'Mage',           # Azmodán con encoding issues
    'LÃºcio': 'Healer',          # Lúcio con encoding issues  
    'Teniente Morales': 'Healer', # Lt. Morales en español
    'Mefisto': 'Mage',           # Mephisto en español
    'Cromi': 'Mage',             # Chromie en español
    # Eliminar o filtrar 'Puntos' ya que es un error de datos
}
    """)

def main():
    """Función principal"""
    print("🎮 CORRECCIÓN DE ROLES DE HÉROES - HEROES OF THE STORM")
    print("=" * 60)
    print("Fecha:", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Analizar y corregir
    fix_hero_role_mappings()
    df_corrected = apply_corrections_to_dataset()
    
    if df_corrected is not None:
        update_data_loader()
    
    print("\n" + "=" * 60)
    print("✅ Proceso de corrección completado")

if __name__ == "__main__":
    main()
