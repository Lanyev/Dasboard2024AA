# Pipeline de Datos: Heroes of the Storm Analytics Dashboard

## 1. Resumen

Este documento detalla el proceso de transformación de los datos crudos de Heroes of the Storm hasta llegar al dataset optimizado `structured_data.csv` que utiliza la aplicación. Es crucial entender este pipeline para asegurar la calidad y reproducibilidad de los análisis.

## 2. Fuentes de Datos Originales

El proyecto parece haber manejado varias versiones o estados de los datos, como se infiere de los archivos en `temp_backup_csv/` y nombres como `structured_data_original_backup.csv`. Las fuentes primarias podrían ser:

*   **Archivos CSV de partidas**: Exportaciones de bases de datos de replays o APIs de juegos.
    *   Ejemplo inferido: `hots_cleaned_data_modified.csv`
    *   Ejemplo inferido: `hots_cleaned_data_modified_2025_1_with_roles_fixed.csv`
*   **Datos de referencia**: Posiblemente archivos o tablas con información de héroes, mapas, etc. (aunque `utils/hero_roles.py` sugiere que parte de esto se maneja en código).

## 3. Proceso de ETL (Extract, Transform, Load)

El objetivo es producir `structured_data.csv`. Los pasos generales, basados en las mejores prácticas y la estructura del proyecto, serían:

### 3.1. Extracción (Extract)

*   **Identificación de la fuente canónica**: Determinar cuál de los archivos de backup (`structured_data_original_backup.csv`, archivos en `temp_backup_csv/`) representa el punto de partida más completo o relevante.
*   **Carga inicial**: Cargar los datos crudos en un DataFrame de Pandas.

### 3.2. Transformación (Transform)

Esta es la fase más crítica y probablemente incluye:

*   **Limpieza de Datos**:
    *   **Manejo de Nulos (NaN)**: Imputar valores faltantes o eliminar filas/columnas según sea apropiado.
    *   **Corrección de Tipos de Datos**: Asegurar que las columnas numéricas sean numéricas, las fechas sean datetime, etc. (El `PROJECT_SUMMARY.md` menciona "Manejo correcto de métricas de tiempo").
    *   **Eliminación de Duplicados**: El `PROJECT_SUMMARY.md` destaca una "optimización tras eliminar duplicados (32,038 filas vs 51K originales)". Este es un paso clave.
    *   **Estandarización de Nombres**: Unificar nombres de héroes, mapas, jugadores si hay variaciones.
    *   **Normalización de Columnas**: "Headers consistentes sin duplicados" (mencionado en `PROJECT_SUMMARY.md`).

*   **Ingeniería de Características (Feature Engineering)**:
    *   **Creación de Nuevas Métricas**: Calcular métricas derivadas que no están en los datos crudos (ej. KDA, tasas de participación, etc.).
    *   **Asignación de Roles**: Utilizar la lógica de `utils/hero_roles.py` para asignar roles a los héroes en cada partida. Esto puede incluir el manejo de multi-rol y roles especiales como "Mages".
    *   **Agregaciones**: Calcular estadísticas agregadas si es necesario (aunque la mayoría de las agregaciones parecen ocurrir dinámicamente en el dashboard).

*   **Filtrado Específico**:
    *   Aplicar filtros para excluir partidas irrelevantes (ej. partidas muy cortas, modos de juego no deseados si aplica).

*   **Optimización del Dataset**:
    *   Seleccionar solo las columnas necesarias para el dashboard.
    *   Optimizar tipos de datos para reducir el uso de memoria (ej. usar `category` para columnas con baja cardinalidad).

### 3.3. Carga (Load)

*   **Guardado del Dataset Procesado**: Guardar el DataFrame transformado en `structured_data.csv`.
    ```python
    # Ejemplo conceptual en un script de procesamiento
    # import pandas as pd
    # df_processed.to_csv('structured_data.csv', index=False)
    ```

## 4. Scripts y Herramientas

*   **`temporary_cleanup_script.py`**: Este script podría contener parte de la lógica de transformación utilizada. Sería ideal refactorizar su contenido en funciones reutilizables y bien documentadas, posiblemente dentro de `utils/` o en un nuevo directorio `scripts/etl/`.
*   **`utils/data_loader.py`**: Aunque su función principal es cargar `structured_data.csv` para la app, podría extenderse o complementarse con scripts que *generen* este archivo.
*   **Jupyter Notebooks (Opcional)**: A menudo, la exploración de datos y el desarrollo inicial de los pasos de ETL se realizan en notebooks. Si se usaron, podrían limpiarse y guardarse en `documentation/notebooks/` o `scripts/etl/notebooks/` como referencia.

## 5. Reproducibilidad y Versionado

*   **Scripts Versionados**: Todo el código utilizado para generar `structured_data.csv` debe estar versionado en Git.
*   **Documentación Clara**: Los pasos y decisiones tomadas durante el ETL deben estar bien documentados aquí.
*   **Datos Originales**: Mantener una copia segura de los datos originales sin procesar. Si son muy grandes para Git, almacenarlos en una ubicación accesible y documentar cómo obtenerlos.
*   **Semillas (Seeds)**: Si se utilizan procesos aleatorios (ej. para imputación o muestreo), fijar las semillas para asegurar la reproducibilidad.

## 6. Mantenimiento del Pipeline

*   **Actualización de Datos**: Si se reciben nuevos datos de partidas, el pipeline de ETL debe poder ejecutarse sobre ellos para actualizar `structured_data.csv`.
*   **Cambios en la Lógica**: Si se modifican las definiciones de métricas, roles de héroes, o cualquier lógica de transformación, el pipeline debe re-ejecutarse para reflejar estos cambios en `structured_data.csv`.

## 7. Estado Actual y Recomendaciones

*   El `PROJECT_SUMMARY.md` indica que `structured_data.csv` ya está "limpio y optimizado".
*   **Recomendación**: Formalizar cualquier script o pasos manuales usados para crear `structured_data.csv` en un script de Python bien estructurado y versionado. Esto podría ser un `build_dataset.py` en la raíz o en una carpeta `scripts/`.
*   **Recomendación**: Documentar las fuentes exactas y las transformaciones específicas aplicadas con más detalle si es posible, incluyendo ejemplos de código o pseudocódigo de las transformaciones clave.

Este documento sirve como un esquema. Debería ser expandido con los detalles específicos del proceso de ETL implementado en el proyecto.
