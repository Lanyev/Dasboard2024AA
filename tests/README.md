# 🧪 Tests del Dashboard MOBA

Esta carpeta contiene todos los tests para verificar el funcionamiento del dashboard Heroes of the Storm Analytics.

## 📁 Archivos de Test

### Tests Principales
- **`test_dashboard.py`** - Test principal que verifica todas las funcionalidades básicas ✅
- **`test_basic.py`** - Tests básicos de importación y estructura ✅
- **`test_role_mapping.py`** - Test específico para verificar el mapeo automático de roles ✅
- **`test_dashboard_final.py`** - Test completo con análisis detallado (en desarrollo)
- **`test_dashboard_clean.py`** - Test limpio para verificación rápida

### Utilidades
- **`analyze_roles.py`** - Herramienta de análisis de roles entre datasets

### Scripts de Ejecución
- **`run_tests.bat`** - Script para Windows (PowerShell/CMD)
- **`run_tests.sh`** - Script para Linux/macOS (Bash)

## 🚀 Cómo Ejecutar los Tests

### Opción 1: Script Automático (Recomendado)
```bash
# Windows
cd tests
.\run_tests.bat

# Linux/macOS
cd tests
chmod +x run_tests.sh
./run_tests.sh
```

### Opción 2: Ejecución Manual
```bash
# Test principal
python test_dashboard.py

# Test de mapeo de roles
python test_role_mapping.py

# Test completo
python test_dashboard_final.py
```

## 📊 Que Verifican los Tests

### 1. **Imports y Dependencias**
- ✅ Todas las librerías necesarias
- ✅ Componentes del dashboard
- ✅ Utilidades y helpers

### 2. **Carga de Datos**
- ✅ Lectura de datasets CSV
- ✅ Normalización de formatos
- ✅ Mapeo automático de roles

### 3. **Funcionalidades del Dashboard**
- ✅ 8 secciones principales
- ✅ Filtros y navegación
- ✅ Visualizaciones y métricas

### 4. **Análisis de Roles**
- ✅ Mapeo Héroe→Rol automático
- ✅ Sincronización entre datasets
- ✅ Consistencia de datos

## 📋 Interpretación de Resultados

### ✅ **Test Exitoso**
```
🎉 ¡TODOS LOS TESTS BÁSICOS PASARON!
📊 Resultados: 21/21 tests pasaron
```

### ❌ **Test Fallido**
```
💥 TESTS FALLIDOS ENCONTRADOS
❌ Fallidos: X
```

### ⚠️ **Advertencias**
- Warnings de Streamlit son normales
- Mensajes de cache son informativos
- ScriptRunContext warnings pueden ignorarse

## 🔧 Solución de Problemas

### Error de Imports
```bash
# Verificar que estás en el directorio correcto
cd c:\Users\lanye\OneDrive\Escritorio\Proyectos Personales\streamlite\heroes
python -m tests.test_dashboard
```

### Error de Datasets
```bash
# Verificar que los archivos CSV existen
ls *.csv
```

### Error de Streamlit
```bash
# Instalar dependencias
pip install -r requirements.txt
```

## 📝 Notas Importantes

1. **Ejecutar desde la raíz del proyecto**, no desde la carpeta tests
2. **Los tests NO inician el servidor Streamlit**, solo verifican funcionalidad
3. **Algunos warnings son normales** y pueden ignorarse
4. **Si un test falla**, verificar que todos los archivos estén presentes

## 🎯 Tests por Implementar

- [ ] Tests de rendimiento
- [ ] Tests de interfaz de usuario
- [ ] Tests de carga de datos masivos
- [ ] Tests de compatibilidad entre navegadores
