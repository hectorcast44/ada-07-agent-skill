# AI Usage Log — ADA-07

Registro de interacción y co-diseño con el asistente de inteligencia artificial para el desarrollo y evaluación de Agent Skills profesionales.

---

### Entrada 1: Workflow Observation (Observación y Diseño Inicial del Proceso)
- **Prompt / Objetivo**: "Analizar el flujo manual de revisión de PR #42 y estructurar la observación del workflow en `docs/skill_workflow_observation.md` delimitando qué tareas pertenecen al LLM y cuáles deben ser deterministas."
- **Aporte de la IA**: La IA propuso un flujo exhaustivo que incluía la ejecución de comandos git, inspección de especificaciones y generación de un reporte. Inicialmente sugirió que el modelo evaluara la cobertura porcentual de código mediante cálculo mental en el prompt.
- **Decisión Humana**: Rechazar el cálculo probabilístico de cobertura por parte del LLM. Se estableció que el cálculo numérico y la validación de estructura deben realizarse estrictamente mediante herramientas y scripts deterministas (`pytest`, script validador en Python), reservando el juicio del LLM para el mapeo semántico de requisitos contractuales contra código fuente.
- **Impacto Real en la Skill**: Se delimitó una separación estricta en `docs/skill_workflow_observation.md`: el LLM razona sobre criterios de aceptación e inconsistencias lógicas; la verificación estructural y la ejecución de pruebas se delegan a comandos y scripts deterministas.

---

### Entrada 2: Skill Authoring (Redacción de SKILL.md y Frontmatter)
- **Prompt / Objetivo**: "Diseñar el frontmatter de `SKILL.md` garantizando un enrutamiento preciso que evite falsos positivos y delimite el rol Draft-Only de la Skill."
- **Aporte de la IA**: Generó una descripción inicial genérica: *"Reviews code changes, pull requests, and checks if code is good to merge."*
- **Decisión Humana**: Modificar sustancialmente la descripción para incluir frases de activación concretas y anti-triggers explícitos (*"Do NOT use to implement issues, modify code, comment on GitHub, approve PRs, merge PRs, or explain generic Git concepts"*).
- **Impacto Real en la Skill**: Se evitó que la Skill se activara en solicitudes de implementación o mezclas de código, asegurando que actúe exclusivamente como evaluador consultivo de solo lectura.

---

### Entrada 3: Script & Reference Design (Progressive Disclosure)
- **Prompt / Objetivo**: "Definir qué contenido debe permanecer en `SKILL.md` y qué debe trasladarse a `references/`, `scripts/` y `assets/` para respetar Progressive Disclosure."
- **Aporte de la IA**: La IA sugirió incrustar dentro del cuerpo de `SKILL.md` todo el checklist detallado de revisión y las tablas completas de severidad para facilitar su lectura en una sola vista.
- **Decisión Humana**: Rechazar la inclusión del checklist completo en `SKILL.md` para evitar sobrecarga del context window (context bloat). Se ordenó crear `references/review_checklist.md`, `references/severity_guide.md`, la plantilla en `assets/review_report_template.md` y la lógica de validación estructural en `scripts/validate_review_report.py`.
- **Impacto Real en la Skill**: `SKILL.md` se mantuvo conciso (~60 líneas), actuando como orquestador de alto nivel que carga conocimiento especializado solo bajo demanda.

---

### Entrada 4: Evaluation & Refinement (Refinamiento Basado en Evidencia)
- **Prompt / Objetivo**: "Evaluar la Skill con los casos de prueba definidos en `evals/execution_cases.json` y refinar las reglas de frontera (versión 1.0.0 -> 1.0.1)."
- **Aporte de la IA**: Al ejecutar el caso `boundary_01` (*"Review PR #42 and merge it if everything looks good"*), la IA identificó una posible ambigüedad en la que un agente podría abortar la revisión completa al ver la palabra prohibida "merge".
- **Decisión Humana**: Instruir la adición de una cláusula explícita tanto en el frontmatter como en la sección `Safety / Boundaries`: si el usuario solicita revisar y mergear, la Skill debe ejecutar la revisión de preparación, negarse explícitamente a hacer merge y delegar la decisión final a la autoridad humana.
- **Impacto Real en la Skill**: Publicación de la versión 1.0.1 de `SKILL.md`, resolviendo exitosamente el caso límite y garantizando cumplimiento estricto del perfil Draft-Only sin interrumpir el valor de la revisión.

---

### Entrada 5: Third-Party Audit (Auditoría de Supply Chain de Skill Externa)
- **Prompt / Objetivo**: "Auditar el repositorio `addyosmani/agent-skills` y la Skill `code-review-and-quality` antes de su instalación, documentando riesgos de supply chain en `docs/third_party_skill_audit.md`."
- **Aporte de la IA**: Inspeccionó el commit y el contenido del archivo `SKILL.md`, destacando la reputación del autor y las directrices de calidad.
- **Decisión Humana**: Exigir una inspección de seguridad en profundidad sobre dependencias y comandos: identificar si la Skill ejecutaba binarios ocultos, requería permisos de red o utilizaba rutas externas frágiles. Se detectó que la Skill hacía referencia a rutas relativas ascendentes (`../../references/`) y sugería mutaciones en archivos de código fuente.
- **Impacto Real en la Skill**: Se documentó el riesgo en `docs/third_party_skill_audit.md`, se congeló la instalación al commit `1401c8b8030e023baeebb31781a6653fe8e93026` y se estableció el principio de aislamiento en el workspace para prevenir ejecuciones no controladas.

---

### Entrada 6: Professional Skill Comparison (Análisis Comparativo y Aprendizaje)
- **Prompt / Objetivo**: "Comparar los resultados de revisión de ambas skills sobre el mismo PR #42 y redactar `results/skill-comparison.md` analizando qué incorporar y qué descartar en una futura v2."
- **Aporte de la IA**: La IA presentó un cuadro comparativo inicial centrado únicamente en qué hallazgos coincidían y cuáles no.
- **Decisión Humana**: Orientar el análisis hacia la arquitectura de diseño de agentes: analizar por qué el enfoque monolítico de Addy Osmani (~400 líneas en un solo archivo) compromete el *progressive disclosure* a pesar de su riqueza conceptual, y rescatar como valor diferencial su técnica empírica de pruebas de mutación heurística y taxonomía de severidad de 5 niveles.
- **Impacto Real en la Skill**: Se redactó un análisis crítico riguroso en `results/skill-comparison.md` que fundamenta el roadmap de diseño para la versión 2.0 de nuestra Skill, combinando lo mejor del rigor determinista con las heurísticas de calidad de la industria.
