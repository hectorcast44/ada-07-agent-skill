# Workflow Observation

Registro de la observación que hice al ejecutar manualmente el flujo de revisión antes de empaquetarlo en la Skill.

## Trigger
¿Cuándo debería utilizarse este workflow?
- Cuando un desarrollador o un agente me pide revisar si un Pull Request o una rama con cambios está lista para que un humano la revise y apruebe (*PR readiness review*).
- Cuando necesito comparar el diff de código contra los requisitos del proyecto (`REQUIREMENTS.md`, `ARCHITECTURE.md`) y comprobar la evidencia de pruebas automatizadas.
- No debe usarse si lo que se busca es implementar nuevas funcionalidades, modificar código fuente directamente, comentar en GitHub o hacer `git merge`.

## Inputs
¿Qué necesita para iniciar?
1. El identificador del PR o la rama que quiero revisar (en mi prueba usé la rama `feature/pr-42-tiered-discounts` comparada contra `main`).
2. Los documentos con las reglas del proyecto (`REQUIREMENTS.md` para los criterios de aceptación y `ARCHITECTURE.md` para las reglas de diseño).
3. Acceso de solo lectura a los archivos locales y al historial de Git (`git diff`, `git status`).
4. La suite de pruebas lista para ejecutarse en la terminal (`pytest -v`).

## Steps Performed
1. Me pasé a la rama con los cambios (`git checkout feature/pr-42-tiered-discounts`) y saqué el diff contra `main` usando `git diff main..HEAD`.
2. Leí con calma `REQUIREMENTS.md` para entender qué prometía la funcionalidad: descuentos del 5%, 10% y 15% según el tier del cliente (AC-01) y un tope máximo del 30% en descuentos totales (AC-02). También revisé `ARCHITECTURE.md` para recordar las reglas de aislamiento de capas.
3. Inspeccioné los dos archivos tocados en el diff: `src/services/pricing.py` y `tests/test_pricing.py`.
4. Corrí los tests con `pytest -v` en mi terminal y vi que pasaban los 5.
5. Al comparar línea por línea el código contra los requisitos, encontré dos problemas importantes:
   - En `src/services/pricing.py`, la condición para el tier SILVER decía `subtotal > min_threshold` en vez de `>=`. Si un cliente SILVER gasta exactamente $50.00, el sistema le da $0.00 de descuento en lugar del 5% ($2.50).
   - En `tests/test_pricing.py`, noté que el autor borró los tests que validaban que no se pudieran meter precios negativos o cantidades en cero. Es decir, los tests pasaban pero la suite se había debilitado.
6. Clasifiqué los hallazgos según su impacto:
   - `MUST FIX`: El bug del umbral en SILVER (rompe AC-01) y el borrado de los tests negativos de validación.
   - `SHOULD FIX`: Falta validar que el parámetro opcional `coupon_discount` no reciba números negativos.
   - `OPTIONAL`: Marcar los diccionarios de configuración como inmutables (`Final`).
7. Armé un borrador del reporte siguiendo una estructura fija con los contadores de cada categoría.
8. Verifiqué que el reporte incluyera todas las secciones obligatorias y la confirmación explícita de que se requiere decisión humana (`Human decision required: YES`).
9. Me detuve ahí para presentar el reporte al revisor humano, sin tocar el código ni intentar hacer merge.

## Decisions
¿Qué decisiones requieren criterio del LLM?
- Entender la intención del código y contrastarla contra el texto en lenguaje natural de los requerimientos.
- Darse cuenta de si los tests son suficientes o si solo prueban caminos felices (por ejemplo, notar que probar $60.00 en SILVER no garantiza que el umbral de $50.00 funcione).
- Decidir la severidad de cada hallazgo: saber cuándo algo es un bloqueador crítico que rompe el negocio (`MUST FIX`) y cuándo es una sugerencia de arquitectura o estilo (`SHOULD FIX` u `OPTIONAL`).

## Deterministic Work
¿Qué pasos deberían ser scripts/comandos?
- Obtener el diff de Git (`git diff main..HEAD`).
- Ejecutar la suite de pruebas y capturar el resultado exacto (`pytest -v`).
- Validar la estructura del reporte final mediante un script en Python (`validate_review_report.py`) que revise la presencia de encabezados y contadores sin gastar tokens ni depender de la memoria del modelo.

## Reference Knowledge
¿Qué checklist, criterios o convenciones se consultaron?
- Un checklist de revisión de software (`references/review_checklist.md`) para no olvidar aspectos de seguridad, arquitectura y pruebas.
- Una guía de severidad (`references/severity_guide.md`) con definiciones claras para clasificar los problemas.
- Las pautas de diseño documentadas en `ARCHITECTURE.md`.

## Output
¿Qué artefacto produce?
- Un archivo Markdown local: `results/pr-readiness-review.md`.
- Contiene el contexto de la revisión, requisitos evaluados, evidencia de tests, hallazgos clasificados, preguntas abiertas, resumen numérico y la línea obligatoria `Human decision required: YES`.

## Stop Conditions
¿Cuándo debe detenerse y pedir intervención humana?
- Apenas termine de generar y validar el reporte. La skill nunca debe intentar aprobar el PR, hacer merge ni publicar comentarios por su cuenta.
- Si encuentro que `REQUIREMENTS.md` y `ARCHITECTURE.md` se contradicen y no sé cuál tiene prioridad.
- Si los tests se rompen por completo o falta información básica para evaluar el cambio.
