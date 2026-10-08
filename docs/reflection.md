# Reflexión Académica — ADA-07

Respuestas a las 14 preguntas de reflexión sobre el diseño, evaluación y adopción de Agent Skills en procesos de ingeniería de software.

---

### 1. ¿Qué parte del workflow pertenece al juicio del LLM y cuál debe ser determinista?
- **Juicio del LLM:** El modelo debe encargarse del razonamiento semántico. En mi proyecto, esto fue comparar los requerimientos de `REQUIREMENTS.md` contra el diff en `src/services/pricing.py`. El LLM es bueno para entender que la condición `subtotal > min_threshold` rompía la regla de negocio de "mayor o igual que $50.00" para clientes SILVER, o para darse cuenta de que en `tests/test_pricing.py` se habían borrado los tests negativos que validaban precios inválidos. Ese criterio para clasificar la severidad (`MUST FIX` vs `SHOULD FIX`) necesita comprensión del contexto.
- **Determinista:** Todo lo que sea medible, ejecutable o estructurado debe ser código determinista. Correr los tests con `pytest -v`, sacar el diff con `git diff`, contar archivos modificados y validar que el reporte final tenga todas las secciones obligatorias (`validate_review_report.py`) debe hacerlo la terminal o un script. Pedirle al LLM que cuente líneas o valide mentalmente el formato es gastar tokens y arriesgarse a alucinaciones.

---

### 2. ¿Qué información moviste de SKILL.md a references/ y por qué?
Moví dos cosas principales:
1. El checklist completo de revisión a `references/review_checklist.md` (criterios de código, pruebas, arquitectura y seguridad).
2. La guía detallada de severidad a `references/severity_guide.md` (definiciones de `MUST FIX`, `SHOULD FIX` y `OPTIONAL`).

Hice esto para seguir el principio de *progressive disclosure*. Si dejaba todo ese texto dentro de `SKILL.md`, el archivo pasaba de 60 a más de 300 líneas. Cada vez que el agente activa la skill, se come contexto útil del modelo con instrucciones que solo necesita en pasos específicos. Al separarlo en `references/`, el agente lee `SKILL.md` como una guía rápida y solo consulta los archivos de referencia cuando llega a clasificar hallazgos o revisar puntos concretos.

---

### 3. ¿Qué función cumple la description del frontmatter en el routing?
La `description` es el filtro que usa el orquestador del agente para decidir si carga o no la skill sin tener que leer todo su contenido. Funciona como una regla de enrutamiento:
- Le dice qué sabe hacer ("Reviews a Pull Request for engineering readiness...").
- Le da frases clave de activación ("Use when the user asks to review a PR, assess PR readiness...").
- Le define anti-triggers claros ("Do NOT use to implement issues, modify code, comment on GitHub, approve PRs, merge PRs...").

Si la descripción es vaga (como poner solo "code review helper"), el agente la dispararía ante cualquier duda de código o intentaría usarla para escribir cambios.

---

### 4. ¿Qué prompt negativo fue más difícil de evitar que activara la Skill?
El caso mixto: `"Review PR #42 and merge it if everything looks good."` (`boundary_01`).

Fue el más difícil porque viene con dos intenciones opuestas: una permitida ("Review PR #42") y una prohibida ("merge it"). Si solo ponía en los anti-triggers "no usar para merge", el agente podía rechazar la petición completa sin hacer nada, o al revés, hacer la revisión y luego intentar hacer `git merge` para complacer al usuario. Tuve que refinar la instrucción en el frontmatter y en `Safety / Boundaries` para que hiciera la revisión normalmente, pero se negara de forma explícita a hacer el merge y dejara el reporte esperando decisión humana.

---

### 5. ¿Qué diferencia práctica observaste entre una Skill y un MCP Server?
Lo resumiría así:
- **MCP Server:** Da acceso y herramientas (capabilities/reach). Por ejemplo, un GitHub MCP permite leer un PR, listar commits o ver archivos remotos. Pero el MCP no sabe en qué orden usar esas herramientas ni bajo qué reglas de ingeniería evaluar el código.
- **Skill:** Da el procedimiento y el criterio (know-how). Define el flujo paso a paso: primero lee la spec, luego revisa el diff, corre tests, consulta el checklist, clasifica hallazgos y valida el reporte.

El MCP es la herramienta y la Skill es el manual de procedimiento que le dice al agente cómo usarla de forma profesional.

---

### 6. ¿Qué aporta el script que no conviene resolver con instrucciones de lenguaje natural?
Un script (`validate_review_report.py`) aporta certeza total y velocidad sin gastar tokens. 
En menos de medio segundo comprueba con código Python real que el archivo exista, que los encabezados obligatorios estén presentes y que la línea `Human decision required: YES` esté escrita. Si intentas validar eso con puro prompt diciéndole al modelo "asegúrate de incluir todas las secciones", el modelo a veces se confía, da por hecho que el reporte está completo aunque le falte un bloque, o inventa el formato. El script devuelve un `exit code 0` o `1`, y si falla, obliga al agente a corregir el archivo antes de terminar.

---

### 7. ¿Qué riesgo existiría si esta Skill pudiera comentar o hacer merge en GitHub?
El riesgo principal es meter errores a producción sin supervisión humana. En mi prueba, el PR #42 tenía un bug sutil en la condición del tier SILVER (`>` en vez de `>=`). Si la skill tuviera permisos de escritura y el modelo se equivocara o tuviera una alucinación considerando que "los 5 tests pasaron, entonces todo bien", podría aprobar y mergear código roto a `main`. 

También existe el riesgo de que comente borradores incompletos o haga spam en los PRs de GitHub si el proceso falla a la mitad. Por eso mantener la skill en modo *Draft-Only* y dejar el merge en manos humanas es la decisión correcta.

---

### 8. ¿Qué cambió entre la primera y la última versión de tu Skill?
- En la versión **1.0.0**, el frontmatter solo decía que no se usara la skill para hacer merge o modificar código, pero no explicaba qué hacer si el usuario pedía revisar y mergear en el mismo mensaje.
- En la versión **1.0.1**, ajusté la `description` y la sección `Safety / Boundaries`: agregué la regla explícita de que ante peticiones mixtas, el agente debe hacer la revisión de solo lectura, rechazar formalmente la acción de merge y delegar la decisión final al revisor humano. También aseguré que el validador en Python revisara la consistencia del resumen.

---

### 9. ¿Qué evidencia te permite afirmar que la Skill es reutilizable?
1. **No depende de este proyecto en específico:** El procedimiento en `SKILL.md` no tiene nombres de ramas ni variables fijas; habla en términos genéricos de inspeccionar requisitos normativos, diffs y suites de prueba.
2. **Usa assets y referencias estándar:** El checklist y la plantilla de reporte aplican a cualquier proyecto que use control de versiones y tests automatizados.
3. **Casos de prueba verificados:** Pasó los 6 casos de `evals/trigger_cases.json` y los 3 escenarios de `evals/execution_cases.json`, respondiendo adecuadamente tanto a ramas locales como a PRs.

---

### 10. ¿Qué otro proceso profesional de Ingeniería de Software convertirías en una Skill?
Crearía una skill para **Revisión de Migraciones de Base de Datos (Database Migration Review)**.

Sería muy útil para revisar scripts de SQLAlchemy/Alembic o SQL puro antes de aplicarlos en producción. El workflow revisaría que la migración no bloquee tablas grandes (sin `ACCESS EXCLUSIVE` innecesario), que agregue índices de forma concurrente, que incluya función de rollback testeable y que mantenga compatibilidad hacia atrás para despliegues sin caída (*zero-downtime*). Un script determinista podría analizar el archivo SQL buscando sentencias peligrosas como `ALTER TABLE DROP COLUMN` directo.

---

### 11. ¿Qué diferencia de diseño fue más evidente entre tu Skill y code-review-and-quality?
La diferencia más grande está en la arquitectura del archivo:
- Mi skill sigue una estructura modular con *progressive disclosure*: `SKILL.md` es corto y delega a carpetas separadas (`references/`, `scripts/`, `assets/`, `evals/`).
- La skill de Addy Osmani es un archivo monolítico de casi 400 líneas (~21 KB). Mete en un solo texto la filosofía de revisión, los 5 ejes, ejemplos de refactorización, anti-patrones y reglas de dependencias. 

Aunque la de Addy Osmani tiene un contenido técnico impresionante, cargar ese archivo completo en cada revisión consume mucho más contexto que un diseño modular.

---

### 12. ¿Qué ventaja y qué costo observaste al usar una Skill mucho más extensa y opinionated?
- **Ventaja:** El nivel de criterio técnico es altísimo. No se limita a revisar si el código compila; te enseña heurísticas reales como *"si un refactor no reduce la cantidad de conceptos que el lector debe recordar, solo estás moviendo la complejidad de lugar"*, o vigilar el límite de 1,000 líneas por archivo.
- **Costo:** El costo en tokens y contexto. Meter 400 líneas de golpe encarece la llamada y deja menos espacio en el context window para diffs grandes. Además, puede resultar demasiado estricta para cambios pequeños o scripts sencillos donde no se necesita tanta formalidad arquitectónica.

---

### 13. ¿Qué controles aplicarías antes de adoptar una Skill de terceros en un repositorio empresarial?
Aplicaría cinco controles básicos de seguridad y supply chain:
1. **Revisar autor y origen:** Verificar que venga de una fuente oficial o conocida y que tenga licencia compatible.
2. **Fijar el commit (Pinning):** Nunca referenciar la rama `main` directamente. Fijar el commit hash exacto (por ejemplo `1401c8b8...`) para que no cambie el código de la skill sin que me dé cuenta.
3. **Auditar scripts:** Leer línea por línea cualquier script en `scripts/` para asegurarme de que no baje binarios externos, no haga peticiones de red raras ni ejecute comandos riesgosos.
4. **Verificar permisos y secretos:** Confirmar que la skill no pida tokens con permisos de escritura ni variables de entorno sensibles.
5. **Probarla en un entorno aislado:** Correrla primero en una rama local o contenedor con acceso de solo lectura antes de ponerla en los flujos del equipo.

---

### 14. Después de estudiar la Skill profesional, ¿qué cambiarías en una versión 2 de tu Skill y cómo evaluarías que realmente mejoró?
Para una **versión 2.0**, le agregaría tres cosas que aprendí de la skill de Addy Osmani:
1. **Pruebas de mutación heurística:** En el paso de tests, pedirle al agente que invierta una condición en el código nuevo y corra los tests; si la suite sigue pasando en verde, significa que falta un test de regresión para ese caso de borde (justo lo que pasó con el 50.00 de SILVER en mi PR).
2. **Escala de 5 severidades:** Cambiar mi escala de 3 niveles a la suya (`Critical:`, `Required`, `Nit:`, `Optional:`, `FYI`) para separar mejor los detalles cosméticos de los bloqueadores reales.
3. **Recomendaciones con nombres de patrones:** En lugar de solo decir "esto está complejo", sugerir soluciones concretas como "extraer dispatcher" o "colapsar ramas duplicadas".

**Cómo evaluaría la mejora:**
Crearía un nuevo caso de prueba en `evals/execution_cases.json` con un PR donde los tests pasen en verde pero tengan huecos de cobertura. La métrica de éxito sería comprobar si la versión 2.0 detecta la falta de pruebas mediante la técnica de mutación sin necesitar que yo se lo señale manualmente en el prompt, y que el validador en Python confirme que el nuevo formato de reporte se mantiene consistente.
