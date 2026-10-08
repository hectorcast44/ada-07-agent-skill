# Reflexión Académica e Ingeniería de Software — ADA-07

Respuestas detalladas a las 14 preguntas de reflexión sobre diseño, implementación, evaluación y adopción de Agent Skills.

---

### 1. ¿Qué parte del workflow pertenece al juicio del LLM y cuál debe ser determinista?
- **Juicio del LLM**:
  - Comprensión semántica y contractual: Mapear descripciones en lenguaje natural de los requisitos (`REQUIREMENTS.md`) contra ramas condicionales, clases y métodos en el código.
  - Análisis de suficiencia de pruebas: Evaluar si los tests ejercitan casos de borde reales (ej. valor exacto en el umbral) o solo caminos felices nominales.
  - Clasificación de severidad y razonamiento contextual: Discriminar si una discrepancia representa un bloqueador crítico (`MUST FIX`), una deuda técnica estructural (`SHOULD FIX`) o un detalle de estilo (`OPTIONAL`).
- **Comportamiento Determinista**:
  - Extracción de datos del repositorio: Comandos Git (`git diff`, `git status`, `git checkout`).
  - Ejecución de suites de prueba y captura de códigos de retorno (`pytest -v`).
  - Validación estructural del reporte: El script `validate_review_report.py` verifica la presencia obligatoria de secciones, marcadores y contadores numéricos.

---

### 2. ¿Qué información moviste de SKILL.md a references/ y por qué?
- **Información movida**:
  - La lista exhaustiva de verificación (`references/review_checklist.md`), que incluye directrices detalladas sobre requisitos, código, pruebas, arquitectura y seguridad.
  - La guía de criterios de severidad (`references/severity_guide.md`), que desglosa las condiciones precisas para clasificar un hallazgo como `MUST FIX`, `SHOULD FIX` u `OPTIONAL`.
- **Razón técnica**: Para aplicar el principio de **Progressive Disclosure** (revelación progresiva). Si se incluye toda esa información en `SKILL.md`, el archivo se vuelve un prompt monolítico pesado que satura la ventana de contexto (*context window*) en cada activación. Al aislarla en `references/`, `SKILL.md` se mantiene compacto (~60 líneas) y el agente carga el conocimiento especializado únicamente cuando el flujo de trabajo lo requiere.

---

### 3. ¿Qué función cumple la description del frontmatter en el routing?
- La propiedad `description` actúa como el **algoritmo de clasificación y enrutamiento (routing)** para el orquestador del agente.
- Cuando el usuario formula un prompt, el orquestador compara la intención del usuario contra las descripciones de las skills indexadas sin cargar el cuerpo completo de los archivos.
- Una buena descripción define claramente:
  1. Qué hace la habilidad (revisión de preparación para revisión humana).
  2. Cuáles son sus frases gatillo de activación (*triggers*).
  3. Cuándo **NO** debe usarse (*anti-triggers* explícitos). Esto previene falsos positivos en tareas de codificación general, merge o preguntas teóricas.

---

### 4. ¿Qué prompt negativo fue más difícil de evitar que activara la Skill?
- El caso límite compuesto: `"Review PR #42 and merge it if everything looks good."` (`boundary_01`).
- **Dificultad**: Contiene simultáneamente una intención positiva legítima ("Review PR #42") y una acción estrictamente prohibida ("merge it").
- Si el anti-trigger solo decía "Do NOT use to merge PRs", el agente podía rechazar la tarea completa o activar la habilidad e intentar realizar la acción prohibida.
- **Solución**: Refinar la descripción y las fronteras de seguridad para indicar que ante solicitudes combinadas, la Skill debe ejecutar exclusivamente la revisión de preparación en modo de solo lectura, rechazar formalmente la operación de merge y delegar la decisión final a la intervención humana.

---

### 5. ¿Qué diferencia práctica observaste entre una Skill y un MCP Server?
- **MCP Server (Model Context Protocol)**: Proporciona **alcance y capacidades externas (reach & capabilities)**. Expone herramientas primitivas tipadas (ej. leer un PR en GitHub, listar ramas, buscar archivos, ejecutar llamadas API). Un MCP Server no sabe qué proceso de negocio seguir ni qué orden de operaciones tiene sentido.
- **Agent Skill**: Proporciona **know-how y procedimiento profesional reusable**. Define el protocolo, los pasos secuenciales, los criterios de juicio, los quality gates, las plantillas y las condiciones de parada para utilizar las herramientas de forma segura y consistente.
- **Relación**: El MCP proporciona el acceso; la Skill proporciona el procedimiento de ingeniería para utilizar ese acceso.

---

### 6. ¿Qué aporta el script que no conviene resolver con instrucciones de lenguaje natural?
- **Garantía determinista y coste cero de tokens de razonamiento**: Un script en Python (`validate_review_report.py`) verifica en 10 milisegundos si existen todos los encabezados requeridos, si el archivo no está vacío y si la bandera de intervención humana está presente.
- **Inmunidad a la complacencia del LLM**: Un LLM puede convencerse a sí mismo de que "el reporte está suficientemente completo" aunque falte una sección crucial. El script evalúa con lógica booleana estricta y emite un código de salida (`exit code 0` o `1`), forzando al agente a corregir el artefacto si falló la validación estructural.

---

### 7. ¿Qué riesgo existiría si esta Skill pudiera comentar o hacer merge en GitHub?
- **Riesgos críticos de seguridad e integridad del software**:
  - **Auto-aprobación y merge no supervisado**: Si el modelo sufriera una alucinación o pasara por alto un error sutil (como la condición de frontera en SILVER), fusionaría código con bugs a la rama productiva sin supervisión humana.
  - **Spam o comentarios prematuros**: Podría inundar los hilos de GitHub con comentarios provisionales o reportes defectuosos ante fallas intermedias del flujo.
  - **Falsa sensación de seguridad**: Los equipos podrían asumir que el código fue validado por un ingeniero humano cuando en realidad fue aprobado por un agente autónomo.
- Por ello, la política **Draft-Only / Human Review** es indispensable en entornos profesionales.

---

### 8. ¿Qué cambió entre la primera y la última versión de tu Skill?
- **Versión 1.0.0**: Contaba con anti-triggers simples que prohibían el merge, pero carecía de instrucciones explícitas para procesar solicitudes mixtas de revisión + merge.
- **Versión 1.0.1**:
  - Se incorporó la regla de frontera para solicitudes mixtas en la descripción del frontmatter y en la sección `Safety / Boundaries`: ante un prompt como "Review and merge", ejecutar solo la revisión de solo lectura y rechazar explícitamente el merge.
  - Se reforzó la consistencia entre los hallazgos y el resumen numérico validado por script.

---

### 9. ¿Qué evidencia te permite afirmar que la Skill es reutilizable?
1. **Desacoplamiento del repositorio**: El procedimiento en `SKILL.md` no contiene nombres de ramas o PRs "hardcodeados"; opera sobre cualquier diff, rama o PR que el usuario suministre.
2. **Estructura modular estandarizada**: Utiliza una plantilla estándar (`assets/review_report_template.md`) y referencias genéricas de ingeniería de software (`references/review_checklist.md`, `references/severity_guide.md`) aplicables a proyectos Python, TypeScript, Go, etc.
3. **Casos de prueba de evaluación (`evals/`)**: La suite de pruebas de activación (`trigger_cases.json`) y ejecución (`execution_cases.json`) verificó que la habilidad responde consistentemente a diversas frases de entrada.

---

### 10. ¿Qué otro proceso profesional de Ingeniería de Software convertirías en una Skill?
- **Database Migration Safety & Zero-Downtime Review**:
  - *Propósito*: Revisar scripts de migración de base de datos (SQL, Alembic, Prisma) antes de su aplicación en producción.
  - *Procedimiento*: Verificar que las migraciones no bloqueen tablas grandes (locks exclusivos), comprueben índices creados concurrentemente (`CONCURRENTLY`), sean reversibles (rollback testeable) y respeten la estrategia de compatibilidad hacia atrás en despliegues con cero tiempo de inactividad (zero-downtime deployments).
  - *Artefactos y Scripts*: Script determinista para parsear comandos SQL prohibidos (`ALTER TABLE DROP COLUMN` sin fase deprecada) y plantilla de reporte de riesgo de migración.

---

### 11. ¿Qué diferencia de diseño fue más evidente entre tu Skill y code-review-and-quality?
- **Estructura y Progressive Disclosure**:
  - Nuestra Skill utiliza una arquitectura modular limpia: `SKILL.md` corto + subcarpetas `references/`, `scripts/`, `assets/`, `evals/`.
  - `code-review-and-quality` de Addy Osmani utiliza un documento `SKILL.md` único, masivo y autosuficiente (~400 líneas), combinando filosofía, checklists de 5 ejes, patrones multi-modelo y anti-patrones en el cuerpo principal.
- **Metodología de validación**: Nuestra Skill confía en scripts deterministas en Python para validar el artefacto final; la profesional confía en directrices heurísticas ricas y en la técnica activa de pruebas de mutación.

---

### 12. ¿Qué ventaja y qué costo observaste al usar una Skill mucho más extensa y opinionated?
- **Ventaja**: Proporciona un criterio de ingeniería extraordinariamente profundo y sofisticado (reglas contra mover complejidad en lugar de reducirla, límite de 1000 líneas por archivo, disciplina de actualización de dependencias paquete por paquete, y prueba de mutación mental).
- **Costo**:
  - **Consumo elevado de tokens**: Inyecta ~21 KB (~5,000 tokens) directamente al contexto en cada llamada, encareciendo la ejecución y reduciendo el espacio disponible para diffs de código extensos.
  - **Riesgo de rigidez o sobre-ingeniería**: Puede emitir recomendaciones excesivamente prescriptivas para cambios pequeños o scripts internos que no requieren la misma complejidad arquitectónica.

---

### 13. ¿Qué controles aplicarías antes de adoptar una Skill de terceros en un repositorio empresarial?
1. **Auditoría de Supply Chain y Reputación**: Verificar autoría, repositorio oficial, historial de commits y licencias compatibles.
2. **Congelamiento de Versión (Pinning)**: Fijar la Skill a un commit hash específico e inmutable (ej. `1401c8b8...`), evitando referencias a ramas móviles (`main`/`master`) que puedan cambiar silenciosamente.
3. **Análisis de Scripts y Binarios**: Inspeccionar cualquier ejecutable o script incluido en `scripts/` para descartar código malicioso, conexiones de red externas o extracción de telemetría.
4. **Verificación de Secretos y Permisos**: Garantizar que la Skill no solicite ni exponga variables de entorno con tokens, claves de API o accesos administrativos a la infraestructura corporativa.
5. **Evaluación de Aislamiento (Sandbox)**: Probar la Skill en un entorno aislado con herramientas de solo lectura antes de desplegarla en los flujos de integración continua del equipo.

---

### 14. Después de estudiar la Skill profesional, ¿qué cambiarías en una versión 2 de tu Skill y cómo evaluarías que realmente mejoró?
- **Cambios para la Versión 2.0**:
  1. **Incorporar el paso de prueba de mutación heurística** en el flujo de trabajo: ordenar al agente que identifique qué pruebas fallarían si invierte la condición añadida, detectando pruebas que son falsos positivos.
  2. **Adoptar la taxonomía de 5 niveles de severidad** (`Critical`, `Required`, `Nit`, `Optional`, `FYI`) para afinar la priorización de los hallazgos.
  3. **Añadir el eje de simplificación estructural**: requerir que el reporte señale si un cambio redujo conceptos o solo trasladó complejidad.
- **Cómo evaluar la mejora**:
  - Añadir nuevos casos de prueba en `evals/execution_cases.json` con suites de pruebas incompletas (como nuestro PR #42) y medir si la Skill identifica automáticamente la ausencia de casos de borde mediante el criterio de mutación.
  - Verificar que el porcentaje de hallazgos accionables aumente sin incrementar la tasa de falsos positivos en el script validador.
