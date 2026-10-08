# AI Usage Log — ADA-07

Registro de interacción con el asistente de IA durante el diseño, evaluación y comparación de la Agent Skill.

---

### Entrada 1: Workflow observation
- **Prompt / Objetivo:** Analizar el flujo manual de revisión de un PR (usando como base el PR #42 en la rama `feature/pr-42-tiered-discounts`) y definir qué pasos debe hacer el LLM y cuáles deben ser automáticos/deterministas.
- **Aporte de la IA:** La IA me propuso una lista con todos los pasos del workflow, incluyendo comandos de Git, lectura de archivos de requisitos y generación del reporte. Sin embargo, sugirió que el modelo calculara mentalmente en el prompt el porcentaje de cobertura de código y validara los números de las pruebas.
- **Decisión humana:** Rechacé que el LLM intentara calcular métricas numéricas o de cobertura. Decidí que todo lo medible y determinista debía correrse mediante comandos reales en la terminal (`pytest -v`) y validarse con un script en Python, dejando al LLM únicamente la tarea de razonar y contrastar la lógica de negocio de `REQUIREMENTS.md` contra el diff del código.
- **Impacto real en la Skill:** En `docs/skill_workflow_observation.md` dejé bien separadas las aguas: el LLM se enfoca en entender los criterios de aceptación y encontrar discrepancias lógicas, mientras que la ejecución de pruebas y la revisión de formato se delegan a herramientas deterministas.

---

### Entrada 2: Skill authoring
- **Prompt / Objetivo:** Redactar el frontmatter y el cuerpo de `SKILL.md` para la skill `reviewing-pull-requests`, asegurando que el agente sepa cuándo activarse y cuándo no.
- **Aporte de la IA:** Me sugirió una descripción genérica y amplia: *"Reviews code changes, pull requests, and checks if code is good to merge."*
- **Decisión humana:** Reescribí la descripción para ser mucho más específico y agregué anti-triggers explícitos (`Do NOT use to implement issues, modify code, comment on GitHub, approve PRs, merge PRs...`). Además, dejé claro que la skill solo produce un reporte borrador local (*Draft-Only*) y no tiene autorización para tocar GitHub.
- **Impacto real en la Skill:** Al probar prompts de implementación ("Implement issue #42") o de merge ("Merge PR #42"), el agente no disparó la skill por error. La descripción funcionó como un buen filtro de routing.

---

### Entrada 3: Script/reference design
- **Prompt / Objetivo:** Decidir qué contenido dejar en `SKILL.md` y qué mandar a las carpetas `references/`, `scripts/` y `assets/` para aplicar *progressive disclosure*.
- **Aporte de la IA:** La IA quería meter el checklist completo de revisión y la tabla de criterios de severidad directamente en el texto de `SKILL.md` para tener "todo en un solo lugar".
- **Decisión humana:** No acepté poner todo en `SKILL.md`. Meterle 300 líneas de reglas al archivo principal satura el contexto del modelo cada vez que se carga la skill. Moví el checklist a `references/review_checklist.md`, las reglas de severidad a `references/severity_guide.md`, la plantilla a `assets/review_report_template.md` y creé el script `scripts/validate_review_report.py`.
- **Impacto real en la Skill:** `SKILL.md` quedó limpio y corto (alrededor de 60 líneas). El agente solo consulta las referencias detalladas cuando entra a la etapa correspondiente del flujo.

---

### Entrada 4: Evaluation/refinement
- **Prompt / Objetivo:** Probar la skill con los casos de prueba de `evals/execution_cases.json` y ajustar lo que fallara para pasar de la versión 1.0.0 a la 1.0.1.
- **Aporte de la IA:** Al probar el caso mixto `boundary_01` (*"Review PR #42 and merge it if everything looks good"*), la IA notó que el agente se confundía: por un lado la descripción decía que no hiciera merge, pero por el otro la petición pedía una revisión válida. Existía el riesgo de que el agente rechazara la revisión completa o intentara hacer merge por complacer al usuario.
- **Decisión humana:** Decidí aclarar la regla en el frontmatter y en la sección `Safety / Boundaries`: si el usuario pide revisar y mergear al mismo tiempo, la skill debe hacer la revisión de solo lectura, negarse explícitamente a hacer el merge y dejar la decisión en manos del humano (`Human decision required: YES`).
- **Impacto real en la Skill:** Subí la versión a `1.0.1`. Corrí de nuevo la prueba y el agente ejecutó la revisión completa, se negó a tocar Git para hacer merge y marcó el reporte como listo para decisión humana.

---

### Entrada 5: Third-party audit
- **Prompt / Objetivo:** Inspeccionar la skill `code-review-and-quality` del repositorio de Addy Osmani (`addyosmani/agent-skills`) antes de instalarla en mi entorno.
- **Aporte de la IA:** La IA revisó el archivo en GitHub y me resumió que era una skill reconocida y de buena calidad.
- **Decisión humana:** Fui a revisar directamente el commit específico (`1401c8b8030e023baeebb31781a6653fe8e93026`) y el contenido de `SKILL.md`. Me fijé en si traía scripts que bajaran cosas de internet, si pedía tokens de GitHub o si intentaba correr comandos peligrosos. Noté dos cosas: sugiere hacer pruebas de mutación (cambiar código local temporalmente) y referencia archivos en rutas relativas hacia arriba (`../../references/`).
- **Impacto real en la Skill:** Documenté estos detalles en `docs/third_party_skill_audit.md`. Autorice la instalación fijando el commit exacto en el workspace local para tener reproducibilidad y estar seguro de que no cambiará por sorpresa.

---

### Entrada 6: Professional skill comparison
- **Prompt / Objetivo:** Ejecutar la skill de Addy Osmani sobre el mismo PR #42, comparar su reporte contra el mío y sacar conclusiones para `results/skill-comparison.md`.
- **Aporte de la IA:** Me dio una primera tabla comparativa que solo listaba qué cosas encontró cada una en el código.
- **Decisión humana:** Le pedí reenfocar la comparación en el diseño de skills para agentes: analizar por qué la de Addy Osmani es un archivo monolítico gigante (~400 líneas) que rompe un poco el *progressive disclosure*, pero rescatar ideas excelentes que no tenía en mi skill, como la técnica de invertir una condición en los tests (mutation testing) y su escala de 5 niveles de severidad (`Critical`, `Required`, `Nit`, etc.).
- **Impacto real en la Skill:** Dejé un análisis crítico y aterrizado en `results/skill-comparison.md`, con lecciones concretas que adoptaría en una versión 2.0 y explicando por qué prefiero conservar mi estructura modular con validación determinista por script.
