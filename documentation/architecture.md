# Arquitectura del Proyecto: Heroes of the Storm Analytics Dashboard

## 1. Resumen

Este documento describe la arquitectura del Dashboard de Análisis de Heroes of the Storm. El proyecto está construido principalmente en Python, utilizando Streamlit para la interfaz de usuario, Pandas para la manipulación de datos y Plotly para las visualizaciones.

## 2. Componentes Principales

El proyecto se organiza en los siguientes directorios y archivos clave:

```
heroes/
├── moba_dashboard.py           # Aplicación principal de Streamlit. Orquesta la interfaz y los componentes.
├── structured_data.csv         # Dataset principal, limpio y optimizado.
│
├── components/                 # Módulos de UI y lógica para cada sección del dashboard.
│   ├── __init__.py
│   ├── advanced_analytics.py   # Lógica para la sección de métricas avanzadas.
│   ├── composition_analysis.py # Lógica para el análisis de composición de equipos.
│   ├── data_exploration.py     # Lógica para la exploración interactiva de datos.
│   ├── explanations.py         # Componentes para mostrar explicaciones o información.
│   ├── filters.py              # Lógica para los filtros dinámicos de la aplicación.
│   ├── header.py               # Componente para el encabezado del dashboard.
│   ├── hero_analysis.py        # Lógica para el análisis detallado de héroes.
│   ├── metrics.py              # Lógica para las métricas generales.
│   ├── professional_analytics.py # Lógica para dashboards ejecutivos y KPIs.
│   ├── rankings_hero.py        # Lógica para los rankings de héroes.
│   ├── rankings.py             # Lógica para los rankings de jugadores.
│   ├── team_composition_analysis.py # (Posiblemente redundante o fusionado con composition_analysis.py)
│   └── time_analysis.py        # Lógica para el análisis de tendencias temporales.
│
├── utils/                      # Utilidades y funciones auxiliares.
│   ├── __init__.py
│   ├── data_loader.py          # Funciones para cargar y preprocesar `structured_data.csv`.
│   └── hero_roles.py           # Lógica o mapeos relacionados con los roles de los héroes.
│
├── tests/                      # Pruebas automatizadas.
│   ├── test_dashboard_complete_coverage.py
│   ├── test_dashboard_comprehensive.py
│   ├── test_filters_validation.py
│   └── test_user_interactions.py
│
├── documentation/              # Esta carpeta. Documentación del proyecto.
│   ├── architecture.md         # Este archivo.
│   └── ...                     # Otros documentos de guía.
│
├── images/                     # Imágenes utilizadas en el dashboard o documentación.
│   └── ss.png                  # Captura de pantalla del dashboard.
│
├── temp_backup_csv/            # Backups de datos (no versionados en Git).
│
├── .gitignore                  # Especifica archivos y directorios ignorados por Git.
├── CHANGELOG.md                # Historial de cambios del proyecto.
├── PROJECT_SUMMARY.md          # Resumen detallado del estado y características del proyecto.
├── README.md                   # Guía principal del proyecto, cómo empezar.
├── requirements.txt            # Dependencias de Python.
└── temporary_cleanup_script.py # Script para tareas de limpieza puntuales (considerar integrar o eliminar).
```

## 3. Flujo de la Aplicación

1.  **Inicio**: El usuario ejecuta `streamlit run moba_dashboard.py`.
2.  **Carga de Datos**: `moba_dashboard.py` utiliza `utils/data_loader.py` para cargar `structured_data.csv` en un DataFrame de Pandas. Se pueden aplicar cachés de Streamlit (`@st.cache_data`) para optimizar cargas repetidas.
3.  **Interfaz de Usuario (UI)**:
    *   `moba_dashboard.py` define la estructura principal de la aplicación, incluyendo la barra lateral de navegación y el área de contenido principal.
    *   Se utilizan los módulos dentro de `components/` para renderizar las diferentes secciones de análisis seleccionadas por el usuario.
    *   El componente `components/filters.py` gestiona la lógica de los filtros (por héroe, jugador, fecha, etc.) que se aplican a los datos.
    *   El componente `components/header.py` muestra información dinámica o títulos.
4.  **Procesamiento y Visualización**:
    *   Cada módulo en `components/` toma los datos (potencialmente filtrados), realiza los cálculos y análisis necesarios (usando Pandas, NumPy), y genera visualizaciones (usando Plotly).
    *   Los resultados se muestran en la interfaz de Streamlit.

## 4. Gestión de Datos

*   **Fuente Principal**: `structured_data.csv` es el dataset curado y optimizado que alimenta todas las analíticas.
*   **Preprocesamiento**: La lógica para limpiar, transformar y validar los datos originales para producir `structured_data.csv` debería estar documentada (ver `data_pipeline.md`) y, si es posible, automatizada en scripts dentro de `utils/` o una carpeta dedicada a ETL.
*   **Roles de Héroes**: `utils/hero_roles.py` probablemente contiene la lógica para asignar y gestionar los roles de los héroes, lo cual es crucial para muchos análisis.

## 5. Pruebas

*   La carpeta `tests/` contiene pruebas para validar la funcionalidad del dashboard, la lógica de los filtros y las interacciones del usuario. Se recomienda el uso de `pytest` y medir la cobertura.

## 6. Consideraciones de Diseño

*   **Modularidad**: Los componentes en `components/` están diseñados para ser modulares, permitiendo que cada sección del dashboard se desarrolle y mantenga de forma independiente.
*   **Eficiencia**: Se utilizan técnicas de caching de Streamlit y optimizaciones de Pandas para asegurar un buen rendimiento, especialmente con un dataset considerable.
*   **Configuración**: No parece haber archivos de configuración explícitos (ej. `.yaml`, `.ini`). Las configuraciones podrían estar hardcodeadas o gestionadas mediante variables de entorno si fuera necesario para despliegues.

## 7. Posibles Mejoras Arquitecturales

*   **Gestión de Estado**: Para dashboards más complejos, explorar las capacidades de gestión de estado más avanzadas de Streamlit (`st.session_state`) si aún no se utilizan extensivamente.
*   **Pipeline de Datos Formal**: Formalizar el proceso de ETL para `structured_data.csv` en scripts versionados.
*   **API (Opcional)**: Si los datos o análisis necesitaran ser consumidos por otros servicios, se podría considerar exponer una API (ej. con FastAPI). Para este proyecto, parece no ser necesario.
*   **Logging y Monitorización**: Implementar un sistema de logging estructurado.

Este documento proporciona una visión general. Para detalles específicos, referirse al código fuente y a otros documentos en esta carpeta.
