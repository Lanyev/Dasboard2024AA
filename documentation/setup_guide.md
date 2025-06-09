# Guía de Configuración del Entorno de Desarrollo

Este documento proporciona instrucciones detalladas para configurar el entorno de desarrollo para el proyecto Heroes of the Storm Analytics Dashboard.

## 1. Prerrequisitos

*   **Python**: Versión 3.8 o superior. Puedes descargarlo desde [python.org](https://www.python.org/).
*   **Git**: Para clonar el repositorio y gestionar versiones. Puedes descargarlo desde [git-scm.com](https://git-scm.com/).
*   **Acceso a un Terminal/Shell**:
    *   Windows: PowerShell, Git Bash, o Command Prompt.
    *   macOS/Linux: Terminal.

## 2. Clonar el Repositorio

1.  Abre tu terminal.
2.  Navega al directorio donde deseas clonar el proyecto.
3.  Ejecuta el siguiente comando (reemplaza `<URL_DEL_REPOSITORIO>` con la URL real del repositorio Git):
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd heroes 
    ```
    (Si ya tienes el proyecto localmente, puedes omitir este paso y asegurarte de estar en la rama principal y con los últimos cambios: `git checkout main && git pull`)

## 3. Crear y Activar un Entorno Virtual

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

### Usando `venv` (incorporado en Python)

1.  **Crear el entorno virtual** (ejecutar desde la raíz del proyecto, `heroes/`):
    ```bash
    python -m venv .venv
    ```
    Esto creará una carpeta `.venv` en el directorio del proyecto.

2.  **Activar el entorno virtual**:
    *   **Windows (PowerShell)**:
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
        (Si encuentras un error de ejecución de scripts, puede que necesites ejecutar `Set-ExecutionPolicy Unrestricted -Scope Process` primero y luego intentar activar de nuevo).
    *   **Windows (Git Bash/Command Prompt)**:
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source .venv/bin/activate
        ```
    Una vez activado, deberías ver `(.venv)` al principio de tu prompt del terminal.

## 4. Instalar Dependencias

Con el entorno virtual activado, instala las dependencias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

Esto instalará Streamlit, Pandas, Plotly, NumPy y cualquier otra biblioteca necesaria.

## 5. Verificar la Instalación

1.  **Asegúrate de que el dataset principal esté presente**:
    El archivo `structured_data.csv` debe estar en la raíz del proyecto. Según el `README.md`, este archivo está incluido.

2.  **Ejecutar la aplicación Streamlit**:
    ```bash
    streamlit run moba_dashboard.py
    ```

3.  Abre tu navegador web y ve a la dirección que se muestra en el terminal (usualmente `http://localhost:8501`). Deberías ver el dashboard funcionando.

## 6. Herramientas de Desarrollo (Opcional pero Recomendado)

### Linters y Formateadores

Para mantener la calidad y consistencia del código, considera instalar y configurar:

*   **Flake8** (Linter):
    ```bash
    pip install flake8
    ```
    Puedes ejecutarlo con `flake8 .` desde la raíz del proyecto.

*   **Black** (Formateador de código):
    ```bash
    pip install black
    ```
    Puedes formatear archivos con `black .` o `black <nombre_del_archivo>.py`.

*   **autopep8** (Formateador de código alternativo):
    ```bash
    pip install autopep8
    ```
    Puedes formatear archivos con `autopep8 --in-place --recursive .`.


### Pre-commit Hooks

Para automatizar la ejecución de linters/formateadores antes de cada commit:

1.  Instala `pre-commit`:
    ```bash
    pip install pre-commit
    ```
2.  Crea un archivo de configuración `.pre-commit-config.yaml` en la raíz del proyecto. Ejemplo:
    ```yaml
    repos:
    -   repo: https://github.com/psf/black
        rev: 23.3.0 # Usa una versión estable reciente
        hooks:
        -   id: black
            language_version: python3.10 # Ajusta a tu versión de Python
    -   repo: https://github.com/pycqa/flake8
        rev: 6.0.0 # Usa una versión estable reciente
        hooks:
        -   id: flake8
    ```
3.  Instala los hooks:
    ```bash
    pre-commit install
    ```
    Ahora, Black y Flake8 se ejecutarán automáticamente en los archivos modificados antes de cada commit.

## 7. Ejecutar Pruebas

Para ejecutar las pruebas automatizadas (asumiendo que usan `pytest`, lo cual es común):

1.  Instala `pytest` si aún no está en `requirements.txt`:
    ```bash
    pip install pytest pytest-cov
    ```
2.  Ejecuta las pruebas desde la raíz del proyecto:
    ```bash
    pytest
    ```
    Para ver la cobertura de las pruebas:
    ```bash
    pytest --cov=.
    ```

## 8. Desactivar el Entorno Virtual

Cuando termines de trabajar en el proyecto, puedes desactivar el entorno virtual:

```bash
deactivate
```

## 9. Solución de Problemas Comunes

*   **Error `ModuleNotFoundError`**: Asegúrate de que el entorno virtual esté activado y que todas las dependencias de `requirements.txt` se hayan instalado correctamente.
*   **Problemas con `streamlit run`**: Verifica que Streamlit esté instalado (`pip show streamlit`) y que estés en el directorio correcto (`heroes/`) donde se encuentra `moba_dashboard.py`.
*   **Permisos de Ejecución de Scripts (PowerShell)**: Si `.\.venv\Scripts\Activate.ps1` falla, intenta `Set-ExecutionPolicy RemoteSigned -Scope Process` o `Set-ExecutionPolicy Unrestricted -Scope Process`.

Si sigues estos pasos, deberías tener un entorno de desarrollo funcional para contribuir o trabajar con el proyecto.
