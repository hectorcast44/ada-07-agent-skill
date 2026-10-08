# Anatomía y Reverse Engineering de una Skill Profesional

Análisis que hice de la skill `code-review-and-quality` de Addy Osmani (`addyosmani/agent-skills`, commit `1401c8b8030e023baeebb31781a6653fe8e93026`).

---

## 1. Routing (Cómo decide activarse)
Al analizar el frontmatter de su `SKILL.md`, me di cuenta de que su descripción busca ser muy proactiva. Utiliza frases clave como:
- *"Conducts multi-axis code review"*
- *"Use before merging any change"*
- *"Use when reviewing code written by yourself, another agent, or a human"*
- *"Use when asked to review a diff or a pull request, even when the diff is pasted inline"*

A diferencia de mi skill, que usa anti-triggers muy explícitos para no tocar código ni hacer merge, Addy confía en redactar una descripción amplia orientada al momento de integración ("antes de cualquier merge"). No pone restricciones negativas en el frontmatter, lo que le da un rango de acción más amplio pero podría hacer que se dispare en situaciones donde solo se pedía explicar código.

---

## 2. Workflow y Quality Gates
Desarmando su flujo de trabajo, identifiqué 5 pasos bien estructurados:
1. **Entender el contexto:** Antes de tocar el código, entender qué problema resuelve el cambio y qué comportamiento promete la especificación.
2. **Revisar los tests primero:** Esto me pareció brillante: pide inspeccionar las pruebas antes que la implementación para entender la intención real. Incluso propone una técnica práctica: invertir una condición en el código para ver si los tests fallan; si la suite sigue en verde, hay un caso de prueba faltante.
3. **Revisar la implementación con 5 ejes:** Analizar los archivos con una lupa de cinco dimensiones.
4. **Categorizar los hallazgos con severidad:** Etiquetar cada comentario antes de presentarlo al autor.
5. **Verificar la evidencia:** Confirmar que los tests pasen, que el build compile y que no quede código muerto.

Su estándar de aprobación es pragmático: *"Aprueba un cambio cuando mejore la salud general del código, aunque no sea perfecto. El código perfecto no existe."* Pero es implacable con los quality gates: no acepta excusas de *"lo limpiamos después"*.

---

## 3. Review Axes (Los Cinco Ejes de Revisión)
La skill estructura la revisión técnica en 5 áreas muy completas:
- **Correctness (Corrección):** Que cumpla los requisitos, maneje casos nulos, entradas vacías, límites y caminos de error. Busca bugs como off-by-one o estados inconsistentes.
- **Readability & Simplicity (Legibilidad):** Nombres claros sin variables genéricas (`temp`, `data`), control de flujo plano (sin ternarios anidados) y control de tamaño (pregunta directamente: *"¿podría hacerse en menos líneas?"*).
- **Architecture (Arquitectura):** Que respete los límites de módulos, evite acoplamientos innecesarios y aplique una regla de oro: un refactor debe reducir la cantidad de conceptos que el lector tiene en mente, no solo mover la complejidad a otro archivo. También vigila que ningún archivo pase de ~1,000 líneas.
- **Security (Seguridad):** Validación de datos externos en las fronteras del sistema, cero secretos o contraseñas en el código, consultas parametrizadas y prevención de inyecciones.
- **Performance (Rendimiento):** Detección de consultas N+1, bucles infinitos, operaciones síncronas bloqueantes y falta de paginación en listas.

---

## 4. Severity Model (Modelo de Severidad)
Su taxonomía de severidades me pareció mucho más rica que la mía. Usa prefijos estandarizados para que el desarrollador sepa qué es obligatorio y qué puede ignorar:

| Prefijo | Significado | Qué debe hacer el autor |
|---|---|---|
| *(Sin prefijo)* | **Required change** | Obligatorio corregirlo antes del merge |
| `Critical:` | **Blocks merge** | Bloquea el PR (fallo de seguridad, pérdida de datos, funcionalidad rota) |
| `Nit:` | **Minor / Optional** | Detalle menor de estilo o preferencia; el autor puede ignorarlo |
| `Optional:` / `Consider:` | **Suggestion** | Sugerencia técnica que vale la pena pero no bloquea |
| `FYI` | **Informational only** | Información o contexto para referencia futura; no requiere cambios |

Además, establece una regla de priorización: poner primero los problemas de corrección y seguridad, luego los defectos estructurales y al final los nits cosméticos.

---

## 5. Verification (Verificación)
Antes de cerrar cualquier revisión, exige evidencia observable:
- Que los tests pasen con código de salida limpio.
- Que el build del proyecto compile sin errores.
- Que las actualizaciones de dependencias se hagan de una en una y se revise el diff del lockfile, no solo el `package.json`.
- Si detecta código muerto (`DEAD CODE IDENTIFIED`), lo lista explícitamente y pregunta antes de sugerir borrarlo.

---

## 6. Composition (Composición Modular)
Addy no intentó resolver toda la ingeniería de software en una sola skill. Su diseño delega tareas especializadas a otras skills:
- Para auditorías de seguridad a fondo y análisis de dependencias vulnerables, delega a `security-and-hardening`.
- Para análisis de rendimiento y perfilado de recursos, delega a `performance-optimization`.
- Para métricas formales de mutation testing, delega a `constraint-driven-development`.
- Cita checklists compartidos en el repositorio (`security-checklist.md`, `performance-checklist.md`).

---

## 7. Boundaries (Límites y Control Humano)
- **Decisión humana final:** En su sección sobre patrones de revisión con múltiples modelos (*Multi-Model Review Pattern*), deja en claro que los agentes revisan y señalan problemas, pero *"Human makes the final call"*.
- **Cero cambios destructivos silenciosos:** Prohíbe que el agente borre código huérfano sin preguntar primero (*"Ask before deleting"*).
- **Límites de autoridad:** La skill actúa como un auditor y consejero técnico, no como un bot que mergea ramas automáticamente.
