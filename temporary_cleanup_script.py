import os
import shutil

# Obtener la ruta base del script para construir rutas absolutas
base_path = os.path.dirname(os.path.abspath(__file__))

files_to_delete = [
    # Scripts de análisis y corrección obsoletos
    "analyze_hero_roles.py",
    "fix_hero_column.py", # Asumiendo que la corrección ya se aplicó permanentemente

    # Scripts de limpieza y depuración de un solo uso o ya no necesarios
    "remove_duplicates.py",
    "debug_unknown_roles.py",
    "check_vip_players.py",
    "cleanup_markdown.py",
    "cleanup_unused_files.py",
    "debug_processing.py",
    "debug_roles.py",
    "find_unused_files.py",
    "project_cleanup.py",
    "validate_duplicates.py",
    "test_friendly_date_filter.py", # Si las pruebas unitarias cubren esto, o es obsoleto

    # Documentación de desarrollo o temporal
    "README_DEV.md",

    # Archivos .md de reportes específicos (revisar si su contenido es vital o ya está en CHANGELOG/PROJECT_SUMMARY)
    "CLEANUP_REPORT.md",
    "DOCUMENTATION_UPDATE.md",
    "DUPLICATE_CLEANUP_REPORT.md",
    "FINAL_CLEANUP_REPORT.md",
    "FINAL_PROJECT_STATUS.md",
    "FINAL_VALIDATION_REPORT.md",
    "FRIENDLY_DATE_FILTER_COMPLETED.md",
    "FRIENDLY_DATE_FILTER_DOCUMENTATION.md",
    "GEEKO_FILTER_UPDATE.md",
    "ROLE_METRICS_UPDATE.md",
    "VIP_FILTER_DOCUMENTATION.md"
]

# Archivos CSV de datos que podrían ser obsoletos si structured_data.csv es el único en uso
# Comentados por precaución, descomentar si se confirma que no son necesarios.
# "hots_cleaned_data_modified_2025_1_with_roles_fixed.csv",
# "hots_cleaned_data_modified.csv",

# Scripts originales o versiones antiguas
# "moba_dashboard_original.py", # Si moba_dashboard.py es la versión final
# "analyze_hero_roles_updated.py", # Si la lógica está en utils o en otro script

dirs_to_delete = [
    # Cachés de Python
    "__pycache__", # Raíz del proyecto
    os.path.join("components", "__pycache__"),
    os.path.join("utils", "__pycache__"),
    os.path.join("tests", "__pycache__"), # Si existe

    # Directorio de backups temporales (evaluar si aún se necesitan)
    # "temp_backup_csv" # Comentado por precaución
]

print("Iniciando limpieza de archivos y directorios...")
print(f"Ruta base: {base_path}")

for file_name in files_to_delete:
    f_path = os.path.join(base_path, file_name)
    if os.path.exists(f_path):
        try:
            os.remove(f_path)
            print(f"Archivo eliminado: {f_path}")
        except Exception as e:
            print(f"Error eliminando archivo {f_path}: {e}")
    else:
        print(f"Archivo no encontrado, omitiendo: {f_path}")

for dir_name in dirs_to_delete:
    d_path = os.path.join(base_path, dir_name)
    if os.path.exists(d_path):
        try:
            shutil.rmtree(d_path)
            print(f"Directorio eliminado: {d_path}")
        except Exception as e:
            print(f"Error eliminando directorio {d_path}: {e}")
    else:
        print(f"Directorio no encontrado, omitiendo: {d_path}")

print("Limpieza completada.")
