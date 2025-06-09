# Guía de Contribución para Heroes of the Storm Analytics Dashboard

¡Gracias por tu interés en contribuir al proyecto! Agradecemos cualquier ayuda, desde la corrección de errores y la mejora de la documentación hasta la implementación de nuevas características.

## Cómo Contribuir

Hay muchas maneras de contribuir:

*   **Reportando Bugs**: Si encuentras un error, por favor, crea un "Issue" en el repositorio de GitHub detallando el problema, los pasos para reproducirlo y tu entorno.
*   **Sugiriendo Mejoras**: Si tienes ideas para nuevas características o mejoras a las existentes, crea un "Issue" describiendo tu propuesta.
*   **Escribiendo Código**: Si quieres corregir un bug o implementar una nueva característica.
*   **Mejorando la Documentación**: Si encuentras partes de la documentación que son confusas, incompletas o incorrectas.

## Proceso de Contribución de Código

1.  **Busca o Crea un Issue**: Antes de empezar a trabajar, revisa los Issues existentes para ver si alguien ya está trabajando en lo mismo o si ya se ha discutido. Si no existe un Issue relevante, crea uno nuevo para discutir tu propuesta o el bug que quieres solucionar.

2.  **Haz un Fork del Repositorio**: Haz clic en el botón "Fork" en la página del repositorio de GitHub para crear una copia personal del proyecto en tu cuenta.

3.  **Clona tu Fork**:
    ```bash
    git clone https://github.com/TU_USUARIO/heroes.git
    cd heroes
    ```

4.  **Crea una Rama (Branch)**: Crea una rama descriptiva para tus cambios.
    ```bash
    git checkout -b nombre-descriptivo-de-tu-rama
    ```
    Ejemplos: `fix/login-bug`, `feature/new-hero-filter`, `docs/update-readme`.

5.  **Configura tu Entorno de Desarrollo**: Sigue las instrucciones en `documentation/setup_guide.md`.

6.  **Realiza tus Cambios**:
    *   Escribe código claro, conciso y bien comentado.
    *   Sigue el estilo de código del proyecto (considera usar Black y Flake8).
    *   Añade pruebas unitarias para cualquier nueva funcionalidad o corrección de bug.
    *   Asegúrate de que todas las pruebas existentes pasen (`pytest`).

7.  **Haz Commits de tus Cambios**:
    *   Haz commits pequeños y lógicos.
    *   Escribe mensajes de commit claros y descriptivos. Sigue [buenas prácticas para mensajes de commit](https://cbea.ms/git-commit/).
    ```bash
    git add .
    git commit -m "feat: Implementa filtro por rol de héroe en análisis general"
    ```
    (Considera usar prefijos como `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).

8.  **Sincroniza tu Rama con el Repositorio Original (Upstream)**:
    Antes de hacer un Pull Request, es una buena práctica actualizar tu rama con los últimos cambios del repositorio original para evitar conflictos.
    ```bash
    git remote add upstream https://github.com/USUARIO_ORIGINAL/heroes.git # Solo la primera vez
    git fetch upstream
    git rebase upstream/main # O la rama principal del proyecto
    ```
    Resuelve cualquier conflicto que surja.

9.  **Empuja tus Cambios a tu Fork**:
    ```bash
    git push origin nombre-descriptivo-de-tu-rama
    ```

10. **Crea un Pull Request (PR)**:
    *   Ve a tu fork en GitHub.
    *   Haz clic en el botón "New pull request" o "Compare & pull request".
    *   Asegúrate de que la rama base sea la rama principal del repositorio original y la rama de comparación sea tu rama de cambios.
    *   Escribe un título claro y una descripción detallada de tus cambios en el PR. Enlaza el Issue que resuelve (ej. "Closes #123").
    *   Envía el PR.

11. **Revisión de Código**:
    *   Los mantenedores del proyecto revisarán tu PR.
    *   Estate atento a comentarios o solicitudes de cambios. Realiza los ajustes necesarios.
    *   Una vez aprobado, tu PR será fusionado (merged) en el proyecto.

## Estilo de Código

*   Sigue las convenciones de [PEP 8](https://www.python.org/dev/peps/pep-0008/).
*   Usa **Black** para el formateo automático del código.
*   Usa **Flake8** para el linting y la detección de problemas.
*   Escribe docstrings para todos los módulos, clases y funciones públicas.

## Pruebas

*   Todas las contribuciones de código deben incluir pruebas relevantes.
*   Utiliza `pytest` para escribir y ejecutar pruebas.
*   Asegúrate de que todas las pruebas pasen antes de enviar un PR.
*   Intenta mantener o aumentar la cobertura de pruebas del proyecto.

## Documentación

*   Si tus cambios afectan la forma en que los usuarios o desarrolladores interactúan con el proyecto, actualiza la documentación relevante (README, guías en `documentation/`, docstrings).

## Código de Conducta

Se espera que todos los contribuidores sigan el [Código de Conducta](CODE_OF_CONDUCT.md) del proyecto.

¡Gracias de nuevo por tu contribución!
