# Workflow Observation

## Trigger
¿Cuándo debería utilizarse este workflow?
- Cuando un desarrollador o agente solicita evaluar si un Pull Request o rama de características está lista para revisión humana antes del merge (`PR readiness review`).
- Cuando se desea verificar un diff de código frente a especificaciones normativas (`REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`) y evidencia de pruebas automatizadas.
- No debe utilizarse para implementar nuevas características, modificar código productivo directamente, aprobar o rechazar PRs en GitHub, ni ejecutar `git merge`.

## Inputs
¿Qué necesita para iniciar?
1. Identificador del PR o rama / diff base a comparar (ej. `feature/pr-42-tiered-discounts` contra `main` o PR #42).
2. Documentos de especificación técnica y arquitectura del repositorio (`REQUIREMENTS.md`, `ARCHITECTURE.md`).
3. Acceso de solo lectura al árbol de trabajo y archivos modificados (`git diff`, `git status`).
4. Entorno de pruebas disponible para inspeccionar o ejecutar la suite de pruebas automatizadas (`pytest -v`).

## Steps Performed
1. Identificación y checkout del PR/rama (`feature/pr-42-tiered-discounts`) y obtención del diff respecto a la rama base (`git diff main..HEAD`).
2. Lectura y análisis de especificaciones normativas en `REQUIREMENTS.md` (especialmente criterios AC-01 a AC-04) y directrices en `ARCHITECTURE.md`.
3. Inspección detallada del diff de archivos modificados (`src/services/pricing.py` y `tests/test_pricing.py`) y mapeo línea a línea contra los criterios de aceptación.
4. Identificación de pruebas relevantes y ejecución de la suite de pruebas (`pytest -v`), notando que los tests existentes pasan pero omiten casos de frontera críticos.
5. Descubrimiento de discrepancias entre especificación y código:
   - Detección de error de frontera en `src/services/pricing.py` para nivel SILVER (`subtotal > min_threshold` en vez de `>=`).
   - Detección de regresión en suite de pruebas (`tests/test_pricing.py` eliminó pruebas de validación de precios negativos y cantidades cero).
   - Verificación de cálculo determinista con `Decimal` y cumplimiento de límites máximos de descuento (AC-02).
6. Clasificación rigurosa de hallazgos según severidad:
   - `MUST FIX`: Violación de AC-01 (error de frontera en SILVER tier) y eliminación de pruebas unitarias negativas existentes.
   - `SHOULD FIX`: Falta de validación para `coupon_discount` negativo o no tipado en `calculate_final_total`.
   - `OPTIONAL`: Documentación interna o constantes finales en el mapeo de tasas.
7. Ensamblado del borrador del reporte estructurado (`results/pr-readiness-review.md`) sin alterar el código fuente ni publicar comentarios en repositorios remotos.
8. Validación determinista del reporte generado mediante un script para asegurar completitud de secciones y recuentos.
9. Detención del agente y presentación formal del reporte al revisor humano con la indicación explícita de decisión humana requerida (`Human decision required: YES`).

## Decisions
¿Qué decisiones requieren criterio del LLM?
- Mapeo semántico entre los requisitos en lenguaje natural (`REQUIREMENTS.md`) y las estructuras de control en el código fuente.
- Evaluación de suficiencia de pruebas: razonar si los tests cubren casos de borde (ej. valor exacto en el umbral) o solo caminos felices.
- Clasificación de severidad de cada hallazgo (`MUST FIX` vs `SHOULD FIX` vs `OPTIONAL`) analizando el impacto funcional, riesgo de regresión e integridad de datos.
- Determinación de límites de alcance del PR (si introduce refactorizaciones no justificadas o cambios no solicitados).

## Deterministic Work
¿Qué pasos deberían ser scripts/comandos?
- Obtención del diff y lista de archivos modificados (`git diff`, `git status`).
- Ejecución de la suite de pruebas unitarias y captura de resultados/exit code (`pytest -v`).
- Validación estructural del reporte de revisión (`validate_review_report.py`) verificando existencia de encabezados obligatorios, formato y contadores numéricos.
- Conteo de líneas modificadas y archivos afectados.

## Reference Knowledge
¿Qué checklist, criterios o convenciones se consultaron?
- Lista de verificación de Pull Requests de Ingeniería de Software (`references/review_checklist.md`), cubriendo requisitos, código, pruebas, arquitectura y seguridad.
- Guía de clasificación de severidad de hallazgos (`references/severity_guide.md`), diferenciando bloqueadores normativos de mejoras opcionales.
- Convenciones de codificación del proyecto y directrices de arquitectura (`ARCHITECTURE.md`).

## Output
¿Qué artefacto produce?
- Reporte estructurado en formato Markdown: `results/pr-readiness-review.md`.
- Contiene: contexto de revisión, requisitos analizados, evidencia de pruebas, hallazgos clasificados (MUST FIX, SHOULD FIX, OPTIONAL), preguntas abiertas, resumen final con contadores y confirmación de `Human decision required: YES`.

## Stop Conditions
¿Cuándo debe detenerse y pedir intervención humana?
- Al concluir la generación y validación del reporte: el agente nunca debe aprobar el PR, ni mergear la rama, ni comentar en GitHub.
- Si existe contradicción irreconciliable entre `REQUIREMENTS.md` y `ARCHITECTURE.md` o el PR description.
- Si faltan permisos o el diff excede los límites seguros para una revisión automatizada.
- Si la suite de pruebas produce fallos catastróficos que impiden el análisis determinista.
