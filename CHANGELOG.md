# 📝 Changelog - Heroes Analytics Dashboard

## 🧹 Versión 2.1.1 (Enero 2025) - Filtro de Fechas Amigable

### 🆕 Nuevas Funcionalidades

#### 📅 Filtro de Fechas Mejorado
- **Botones rápidos**: "Todo el tiempo", "Último año", "Últimos 6 meses"
- **Selector por año**: Botones dinámicos para cada año disponible
- **Selector por meses**: Navegación mensual del año más reciente
- **Rango personalizado**: Selector manual como opción alternativa
- **Estado persistente**: Uso de session_state para mantener selecciones
- **Validación robusta**: Manejo de fechas inválidas y rangos incorrectos
- **Interfaz intuitiva**: Diseño con iconos y organización clara

#### 🎯 Mejoras de UX/UI
- **Navegación simplificada**: Botones claros para períodos comunes
- **Feedback visual**: Estados y mensajes informativos
- **Diseño responsivo**: Columnas adaptables según contenido
- **Compatibilidad completa**: Integración con filtros VIP y multiselect

### 📁 Archivos Modificados
- `components/filters.py`: Implementación completa del filtro amigable
- `CHANGELOG.md`: Documentación de cambios

### 📚 Documentación Nueva
- `FRIENDLY_DATE_FILTER_DOCUMENTATION.md`: Guía completa de la nueva funcionalidad

## 🧹 Versión 2.1.0 (Junio 2025) - Optimización y Limpieza

### 🚀 Optimizaciones Principales

#### 📊 Migración a Dataset Único
- **Consolidación completa**: Migración total a `structured_data.csv`
- **Eliminación de redundancias**: Headers duplicados y métricas innecesarias removidas
- **Optimización de columnas**: Normalización y limpieza de nombres de columnas
- **Performance mejorada**: Carga más rápida y uso eficiente de memoria

#### � Curación de Métricas
- **Rankings optimizados**: Lista curada de 13 métricas relevantes
- **Nombres descriptivos**: Interfaz completamente en español
- **Eliminación de duplicados**: No más métricas repetidas en selectores
- **Filtros inteligentes**: Detección automática de métricas disponibles

#### 🧹 Limpieza del Proyecto
- **18 archivos eliminados**: Scripts temporales, backups y duplicados
- **Estructura simplificada**: Solo archivos esenciales y activos
- **Documentación actualizada**: READMEs y documentación reflejando estado actual

### ✅ Correcciones Críticas

#### 🏆 Sistema de Rankings
- **Rankings de jugadores**: Métricas curadas sin duplicados
- **Rankings de héroes**: Consistencia con nombres descriptivos
- **Agregaciones múltiples**: Promedio, Total, Máximo funcionando correctamente
- **Manejo de tipos**: Corrección para métricas temporales como GameTime

#### 🦸‍♂️ Análisis de Héroes  
- **Filtro HeroKills**: Implementación y validación del filtro de asesinatos
- **Métricas clave**: Solo métricas relevantes para análisis de héroes
- **Nombres correctos**: Uso consistente de nombres de columnas del dataset

### 🗂️ Archivos Eliminados
- Análisis temporales: `analyze_*.py` (8 archivos)
- Backups y duplicados: `*_original.py`, `*_backup.py` (5 archivos)  
- Documentación temporal: `MIGRATION_*.md`, `OPTIMIZATION_*.md` (5 archivos)

## 🆕 Versión 2.0.0 (Mayo 2025) - Multi-Dataset
- Colores: Verde (#00D4AA) y azul (#58A6FF)
- Estilo: Futurista con gradientes
- Efectos: Animaciones glow y transiciones suaves
- Enfoque: Análisis en tiempo real 2025

### 📋 Compatibilidad
- ✅ Streamlit >= 1.10.0
- ✅ Pandas >= 1.3.0
- ✅ Plotly >= 5.5.0
- ✅ Python 3.11+

### 🚀 Uso
```bash
# Ejecutar la aplicación
streamlit run moba_dashboard.py

# Acceder a http://localhost:8501
# Seleccionar dataset en la barra lateral
# El tema cambiará automáticamente
```

### 🎮 Estructura de Datasets Soportada

#### Formato 2024 (Alan Awards)
```
Player, Hero, Role, Winner, File, Map, Date, GameTime, ...
```

#### Formato 2025 (Nueva Temporada)
```
PlayerName, HeroName, Winner, FileName, Map, GameTime, ...
```

### 🔮 Próximas Funcionalidades
- [ ] Soporte para más formatos de datos
- [ ] Temas personalizables por el usuario
- [ ] Comparación lado a lado entre datasets
- [ ] Exportación de análisis en PDF
- [ ] Dashboard en tiempo real con WebSockets

---
**Desarrollado por**: Alan Yeverino (@Lanyev)  
**Repositorio**: https://github.com/Lanyev/Dasboard2024AA  
**Versión**: 2.0.0

## [v2.3.0] - 2025-06-08 🎭 Actualización de Métricas por Rol

### ✨ Nuevas Funcionalidades Principales
- **🎭 Métricas por Rol**: Sistema completo de análisis por roles con 7 categorías principales
- **🛡️ Análisis de Composiciones de Equipo**: Nueva sección interactiva para analizar y crear composiciones
- **📊 Visualizaciones por Rol**: Gráficos de winrate y daño promedio por rol
- **🎯 Composición Personalizada**: Herramienta para crear y analizar composiciones custom

### 🔧 Mejoras Técnicas
- **Corrección de Columna Winner**: Solucionado problema que mostraba 0% en métricas de winrate
- **Sistema de Roles Mejorado**: Mapeo completo de 85 héroes en 7 roles (Tank, Bruiser, Melee Assassin, Ranged Assassin, Mage, Healer, Support)
- **Procesamiento de Datos Optimizado**: Mejor manejo de transformaciones de datos
- **Cache Management**: Limpieza automática de cache para actualizaciones en tiempo real

### 📈 Componentes Actualizados
- `components/metrics.py`: Agregadas métricas por rol con visualizaciones
- `components/team_composition_analysis.py`: Nuevo componente completo para análisis de composiciones
- `utils/hero_roles.py`: Sistema centralizado de gestión de roles
- `utils/data_loader.py`: Corrección de mapeo de columna Winner (Yes/No)

### 🎮 Nuevas Secciones del Dashboard
- **🛡️ Composiciones de Equipo**: 4 tabs con análisis completo
  - 🔍 Explorar Composiciones Existentes
  - 📊 Estadísticas por Roles
  - 🎯 Composición Personalizada
  - 📈 Tendencias de Meta

### 🐛 Correcciones de Bugs
- **CRITICAL**: Solucionado problema donde todas las métricas por rol mostraban 0.0%
- **Mapeo de Winner**: Corregido mapeo erróneo de Yes/No → Winner/Loser → Unknown
- **Referencias de Columnas**: Corregido uso de 'HeroName' vs 'Hero' en componentes

### 📊 Métricas Implementadas
- **Por Rol**: Winrate, partidas jugadas, daño promedio, popularidad
- **Por Composición**: Análisis de sinergia, balance de equipo, recomendaciones
- **Visualizaciones**: Gráficos de barras, dispersión y tendencias temporales

## [2025-01-08] - Limpieza de Duplicados y Optimización Final

### ✅ Añadido
- **Limpieza automática de duplicados**: Script `remove_duplicates.py` que elimina duplicados basándose en StructureDamage, TotalSiegeDamage y HeroDamage
- **Backup automático**: Creación automática de backup antes de eliminar duplicados
- **Sistema de verificación**: Validación de integridad del dataset después de la limpieza
- **Estadísticas detalladas**: Análisis completo de patrones de duplicados encontrados

### 🔧 Mejorado
- **Reducción del dataset**: 37.93% de reducción (de 51,619 a 32,038 filas)
- **Calidad de datos**: Eliminación de 19,581 filas duplicadas manteniendo la integridad
- **Rendimiento**: Mejora significativa en velocidad de carga y procesamiento
- **Filtro de fechas**: Interfaz más amigable con botones por año, mes y opciones rápidas

### 📊 Estadísticas de Limpieza
- **Filas originales**: 51,619
- **Filas duplicadas eliminadas**: 19,581
- **Filas finales**: 32,038
- **Grupos duplicados**: 15,437 grupos identificados
- **Grupo más grande**: 46 filas duplicadas
- **Backup creado**: `structured_data_original_backup.csv`
