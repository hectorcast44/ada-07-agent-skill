# Third-Party Skill Pre-Install Audit

Repository: https://github.com/addyosmani/agent-skills
Selected skill: code-review-and-quality
Version / commit inspected: commit 1401c8b8030e023baeebb31781a6653fe8e93026 (Blob SHA: 08209ff2208d2883d48d945f7754c428b77f8d87)

## Purpose
Proporcionar un marco integral y multidimensional de revisión de código (multi-axis code review) antes de realizar merge a la rama principal (`main`/`master`). Evalúa cinco ejes cardinales de ingeniería de software: corrección (correctness), legibilidad/simplicidad (readability & simplicity), arquitectura (architecture), seguridad (security) y rendimiento (performance). Incorpora quality gates, estándares de aprobación, categorización estricta de severidad y verificación empírica.

## Trigger / Description
- **Nombre**: `code-review-and-quality`
- **Descripción**:
  `Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch. Use when asked to review a diff or a pull request, even when the diff is pasted inline.`
- **Tareas que disparan la Skill**:
  - Antes de realizar merge de cualquier PR o cambio.
  - Al completar la implementación de un feature o bug fix.
  - Evaluación de código generado por otro agente o humano.
  - Solicitudes de revisión sobre diffs locales o pull requests.
- **Tareas que quedan fuera (Anti-triggers / Out of Scope)**:
  - Implementación o escritura directa de código productivo.
  - Realización automática de merge o push a ramas remotas sin control humano.
  - Análisis forense profundo de seguridad o profiling de rendimiento a bajo nivel (los delega explícitamente a `security-and-hardening` y `performance-optimization`).

## Supporting References
- Cita referencias externas y compartidas del repositorio:
  - `../../references/security-checklist.md`
  - `../../references/performance-checklist.md`
- Skills complementarias referenciadas en el ecosistema:
  - `security-and-hardening`
  - `performance-optimization`
  - `constraint-driven-development`

## Tools / Commands / Permissions
- **Permisos requeridos**: Acceso de solo lectura al sistema de archivos local y diffs de Git (`git diff`, lectura de archivos fuente y tests).
- **Herramientas**: Comandos para ejecutar suites de pruebas unitarias (`pytest`, `npm test`) y pruebas de mutación heurística (invertir una condición temporalmente para verificar si la suite falla).
- **Restricciones de autoridad**: La Skill está diseñada para revisión consultiva y quality gates; no requiere privilegios administrativos ni tokens de escritura a GitHub.

## Potential Risks
1. **Riesgo de modificación de archivos en pruebas de mutación**: La Skill sugiere modificar temporalmente una condición en el código para validar la efectividad de las pruebas y luego restaurarla. Si el agente falla al restaurar el archivo, podría dejar código roto.
2. **Dependencias de referencias cruzadas**: Hace referencia a archivos en `../../references/`, lo cual puede provocar enlaces rotos si solo se instala la carpeta de la Skill aislada.
3. **Sobrecarga de contexto (Context bloat)**: `SKILL.md` es extenso (~400 líneas, ~21 KB) y combina filosofía, checklists, anti-patrones y procesos en un único archivo, a diferencia del diseño de progressive disclosure estricto donde el detalle reside en subcarpetas.
4. **Seguridad / Supply Chain**: Al ser código markdown declarativo de un autor reconocido (Addy Osmani) sin scripts ejecutables maliciosos ni binarios embebidos, el riesgo de ejecución de código arbitrario es mínimo tras la auditoría manual.

## Decision
[X] Install
[ ] Do not install

Reason:
La Skill proviene de una fuente reputada en ingeniería de software, no contiene scripts maliciosos ni solicita credenciales sensibles, y proporciona una metodología de revisión de alta calidad (5 ejes) que permite un contraste enriquecedor con nuestra Skill interna `reviewing-pull-requests`. Se instalará de forma aislada y controlada en `.agents/skills/code-review-and-quality/` fijada al commit auditado (`1401c8b8030e023baeebb31781a6653fe8e93026`).
