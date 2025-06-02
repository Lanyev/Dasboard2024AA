# 📝 Changelog - Heroes Analytics Dashboard

## 🆕 Versión 2.0.0 (Junio 2025)

### ✨ Nuevas Funcionalidades

#### 🎯 Selector Multi-Dataset
- **Soporte para múltiples archivos de datos**: Ahora puedes alternar entre diferentes datasets
- **Dataset 2024**: `hots_cleaned_data_modified.csv` (Original Alan Awards 2024)
- **Dataset 2025**: `hots_cleaned_data_modified_2025_1.csv` (Nueva temporada)
- **Detección automática**: La aplicación encuentra automáticamente todos los datasets disponibles

#### 🎨 Temas Dinámicos
- **Tema Alan Awards 2024**: Diseño clásico con colores rojos y dorados
- **Tema Temporada 2025**: Diseño futurista con gradientes verde/azul y efectos visuales avanzados
- **Cambio automático**: El tema se adapta automáticamente según el dataset seleccionado

#### 🔄 Normalización de Datos
- **Mapeo automático**: Convierte estructuras de datos diferentes a un formato común
- **Compatibilidad total**: Todos los componentes funcionan con ambos formatos
- **Mapeo de roles mejorado**: Más de 50 héroes clasificados correctamente

### 🛠 Mejoras Técnicas

#### 📊 Data Loader Mejorado
- Función `get_available_datasets()` para detección automática
- Función `normalize_2025_format()` para conversión de estructura
- Función `normalize_2024_format()` para compatibilidad retroactiva
- Cache optimizado para mejor rendimiento

#### 🎨 Sistema de Estilos Renovado
- CSS modular con variables personalizables
- Animaciones y efectos visuales avanzados
- Gradientes y sombras dinámicas
- Responsive design mejorado

#### 🏗 Arquitectura Mejorada
- Header dinámico que se adapta al dataset
- Footer con información contextual
- Indicadores visuales del tema activo
- Métricas básicas del dataset en tiempo real

### 🎯 Funcionalidades Específicas por Tema

#### Tema Alan Awards 2024 🏆
- Colores: Rojo (#FF4B4B) y dorado
- Estilo: Clásico y elegante
- Enfoque: Análisis retrospectivo 2024

#### Tema Temporada 2025 🚀
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
