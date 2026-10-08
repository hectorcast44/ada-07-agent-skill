# Comparativa de Skills: `reviewing-pull-requests` vs `code-review-and-quality`

**Caso evaluado**: PR #42 (`feature/pr-42-tiered-discounts` -> `main`)  
**Repositorio**: Order & Discount Service (`ada-07-skills`)

---

## 1. Matriz Comparativa por Dimensiones

| Dimensión | Tu Skill (`reviewing-pull-requests`) | Skill Profesional (`code-review-and-quality`) | Conclusión / Aprendizaje |
|---|---|---|---|
| **Trigger / routing** | Específico y delimitado por anti-triggers claros ("Do NOT use to implement, merge, approve"). Enfoque en "PR readiness". | Amplio y proactivo ("before merging any change", "when reviewing code written by yourself, another agent, or human"). | La Skill profesional tiene mayor alcance general; nuestra Skill previene mejor activaciones erróneas en flujos no relacionados gracias a anti-triggers explícitos. |
| **Scope / boundaries** | Estrictamente Draft-Only. Solo genera un artefacto local y se detiene solicitando decisión humana explícita. | Quality Gate consultivo ("Approve standard"). Orienta el veredicto pero no prohíbe de forma tan rígida la interacción en el chat. | La delimitación estricta de fronteras de nuestra Skill reduce el riesgo de alucinación de acciones no deseadas (como intentar hacer push o comentar en GitHub). |
| **Workflow depth** | Lineal de 10 pasos con énfasis en lectura de spec normativa (`REQUIREMENTS.md`) y validación determinista por script. | Heurístico de 5 pasos con énfasis en inspección de tests primero y pruebas de mutación manual. | La profesional profundiza más en la dinámica de revisión del código en sí; nuestra Skill sobresale en la trazabilidad formal de requisitos normativos. |
| **Correctness** | Mapea directamente cada Acceptance Criterion (AC-01 a AC-04) contra el diff de código. | Evalúa cumplimiento de spec, casos nulos, off-by-one, y caminos de error. | Ambas detectaron el bug en `SILVER` tier ($50.00 exacto). La profesional contextualizó el error en términos de deuda técnica y ramificación redundante. |
| **Architecture** | Verifica cumplimiento de directrices en `ARCHITECTURE.md` y aislamiento de capas. | Enfatiza si el cambio reduce complejidad o solo la relocaliza; vigila tamaño de archivos (~1000 líneas) y acoplamiento. | La profesional aporta heurísticas arquitectónicas de alto nivel muy valiosas para proyectos maduros. |
| **Security** | Checklist general (secretos, permisos, validación de entrada externa). | Eje de seguridad dedicado y composición delegando a `security-and-hardening`. | La profesional integra seguridad dentro de un ecosistema modular de habilidades especializadas. |
| **Performance** | Checklist básico dentro de `references/review_checklist.md`. | Eje explícito de rendimiento (N+1 queries, bucles no acotados, operaciones síncronas) y delegación a `performance-optimization`. | La profesional institucionaliza el análisis de performance con criterios de cuantificación de impacto (ms por ítem). |
| **Tests / verification** | Comprueba que los tests pasen (`pytest -v`) y que la suite no se debilite (detección de tests eliminados). | Técnica de mutation testing heurístico (invertir condición y comprobar que falle la suite); verificación de lockfiles. | La técnica de mutación de la profesional añade rigor empírico que expone falsos positivos donde la suite es "verde" pero inútil. |
| **Severity model** | 3 niveles: `MUST FIX`, `SHOULD FIX`, `OPTIONAL`. | 5 niveles con prefijos estrictos: `Critical:`, `Required` (sin prefijo), `Nit:`, `Optional:`, `FYI`. | El modelo de la profesional discrimina con mayor sutileza entre detalles cosméticos e información contextual. |
| **Human review** | Gate determinista con variable obligatoria: `Human decision required: YES`. | Principio filosófico *"Human makes the final call"* en patrón Multi-Model. | Nuestra Skill garantiza cumplimiento determinista; la profesional aporta un modelo mental de colaboración entre modelos y humanos. |
| **References / composition** | Progressive disclosure estructurado en subcarpetas (`references/`, `assets/`, `scripts/`). | SKILL.md monolítico que referencia checklists externos compartidos a nivel de monorepo. | La estructura de nuestra Skill cumple mejor con progressive disclosure autónomo sin asumir rutas padre fuera del paquete. |
| **Reusability** | Altamente reusable y autocontenida para cualquier proyecto con requisitos formales y pytest. | Reusable en cualquier stack de software general sin importar el lenguaje de programación. | La profesional es agnóstica de lenguaje; nuestra Skill incluye validación mecánica específica que garantiza la uniformidad del reporte. |

---

## 2. Preguntas de Análisis Comparativo

### 1. ¿Qué hace la Skill profesional que tu Skill no contempló?
- **Pruebas de mutación heurística**: Sugiere invertir una condición agregada por el cambio y correr la suite de pruebas; si la suite continúa en verde, demuestra empíricamente que falta un test de regresión.
- **Disciplina de dependencias y lockfiles**: Incorpora reglas específicas para revisar upgrades de librerías paquete por paquete y auditar el diff del lockfile.
- **Regla de simplificación estructural**: Plantea que si un refactor deja igual el número de conceptos que un lector debe memorizar, no es una mejora sino mera relocalización de complejidad.

### 2. ¿Qué elementos de tu Skill son más específicos al curso/proyecto y conviene conservar?
- **Mapeo normativo contra `REQUIREMENTS.md` y `ARCHITECTURE.md`**: Vincula de forma inequívoca cada hallazgo a un criterio de aceptación contractual (ej. RF-01 -> AC-01), lo cual es crítico en ingeniería de software formal.
- **Validación determinista por script (`validate_review_report.py`)**: Garantiza que ningún modelo de lenguaje entregue un reporte incompleto o sin los encabezados y conteos exigidos.
- **Gate explícito `Human decision required: YES`**: Asegura que el pipeline no se automatice indebidamente hacia acciones no autorizadas.

### 3. ¿Qué agregarías a una versión 2 de tu Skill?
- La verificación de cobertura por mutación heurística en el paso de tests.
- La taxonomía de 5 niveles de severidad (`Critical`, `Required`, `Nit`, `Optional`, `FYI`).
- El principio de recomendación de soluciones estructurales con nombre (ej. "Collapse duplicate branches", "Extract dispatcher").

### 4. ¿Qué NO copiarías y por qué?
- **El tamaño monolítico de `SKILL.md`**: El archivo de Addy Osmani tiene ~400 líneas y ~21 KB en un solo documento. Esto viola el principio de *progressive disclosure* y satura el context window del agente en cada activación. Conviene mantener `SKILL.md` corto y delegar los detalles a `references/`.
- **Rutas relativas ascendentes frágiles (`../../references/`)**: Dependen de la estructura del repositorio global y fallan al instalar la Skill de forma aislada.

### 5. ¿Cuál produjo hallazgos más accionables? Incluye dos ejemplos.
Ambas skills fueron altamente efectivas, pero se complementaron:
- **Ejemplo 1 (Hallazgo de Corrección en SILVER tier)**: Nuestra Skill fue más precisa al citar directamente la violación contractual de AC-01 (`src/services/pricing.py#L35`), mientras que la profesional además propuso la solución arquitectónica ("eliminar la bifurcación condicional duplicada y unificarla en un solo bloque").
- **Ejemplo 2 (Hallazgo de Validación de Entradas Externas)**: La Skill profesional detectó que `coupon_discount` en `calculate_final_total` no validaba números negativos desde una perspectiva de principio de seguridad defensiva ("tratar datos externos como no confiables"), aportando el snippet de código exacto para el guard statement.

---

## 3. Evaluación de la Skill como Dependencia (Supply Chain Hygiene)

| Control | Evidencia y Evaluación |
|---|---|
| **Source** | Repositorio público oficial `https://github.com/addyosmani/agent-skills`, mantenido por Addy Osmani (líder de ingeniería en Google Chrome). |
| **Pinning** | Commit fijado exactamente a `1401c8b8030e023baeebb31781a6653fe8e93026` y SHA de blob `08209ff2208d2883d48d945f7754c428b77f8d87`. |
| **Audit** | Inspección completa línea por línea del archivo `SKILL.md`. No contiene scripts binarios, URLs de descarga dinámicas ni instrucciones de ofuscación. |
| **Secrets** | Cero tokens, variables de entorno sensibles o claves privadas embebidas ni solicitadas. |
| **Commands** | Sugiere ejecución de suites de pruebas (`pytest`, `npm test`) y pruebas de mutación locales; no descarga ejecutables de internet. |
| **Permissions** | Opera exclusivamente en modo lectura del workspace (`git diff`, lectura de archivos locales). No requiere acceso de red ni privilegios de superusuario. |
| **Change Control** | Se instaló de forma local congelada dentro del repositorio del proyecto (`.agents/skills/code-review-and-quality/SKILL.md`), garantizando que actualizaciones remotas no alteren el comportamiento en tiempo de ejecución. |

---

## 4. Conclusión Humana
La adopción de una Skill profesional existente demuestra el inmenso valor de estandarizar procesos de ingeniería de software para agentes. Mientras que la Skill comunitaria aporta heurísticas de diseño avanzadas y una visión holística de calidad, nuestra Skill personalizada aporta un anclaje determinista y verificación estricta de requisitos. La combinación ideal para una versión 2 consiste en adoptar la taxonomía y técnicas heurísticas de la Skill profesional preservando la arquitectura modular con *progressive disclosure* y validación mecánica determinista de nuestra Skill.
