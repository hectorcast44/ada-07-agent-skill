# Third-Party Skill Pre-Install Audit

Auditoría que realicé antes de instalar la skill comunitaria en mi workspace, tratándola como cualquier otra dependencia externa.

Repository: https://github.com/addyosmani/agent-skills  
Selected skill: code-review-and-quality  
Version / commit inspected: commit 1401c8b8030e023baeebb31781a6653fe8e93026 (Blob SHA: 08209ff2208d2883d48d945f7754c428b77f8d87)

## Purpose
Darle al agente un marco completo de revisión de código previa al merge (*multi-axis code review*). Evalúa cinco áreas clave: corrección (*correctness*), legibilidad y simplicidad (*readability & simplicity*), arquitectura (*architecture*), seguridad (*security*) y rendimiento (*performance*). Además, define quality gates, reglas para clasificar severidades y verificación basada en evidencia.

## Trigger / Description
- **Nombre:** `code-review-and-quality`
- **Descripción en frontmatter:**  
  `Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch. Use when asked to review a diff or a pull request, even when the diff is pasted inline.`
- **Tareas que la activan:**  
  Cualquier solicitud de revisión antes de un merge, al terminar de programar una funcionalidad o corrección de bug, cuando se pide evaluar código escrito por otro agente o humano, o cuando se le pasa un diff o PR para inspección.
- **Tareas que quedan fuera:**  
  No escribe código de producción, no ejecuta `git push` ni `git merge`, y delega auditorías profundas de seguridad y rendimiento a otras skills (`security-and-hardening` y `performance-optimization`).

## Supporting References
Revisé los archivos que cita y encontré referencias a documentos compartidos en el repo de origen:
- `../../references/security-checklist.md`
- `../../references/performance-checklist.md`
- Skills complementarias: `security-and-hardening`, `performance-optimization` y `constraint-driven-development`.

## Tools / Commands / Permissions
- **Permisos requeridos:** Solo lectura de archivos del proyecto y del historial de Git (`git diff`, lectura de código y tests).
- **Herramientas y comandos:** Sugiere correr la suite de tests del proyecto (`pytest`, `npm test`) y propone una técnica de pruebas de mutación manual (cambiar una condición lógica en el código para verificar que los tests fallen y luego restaurar el archivo).
- **Acceso externo:** No pide tokens de escritura en GitHub ni acceso a servicios de red externos.

## Potential Risks
Al leer el archivo identifiqué tres aspectos a tomar en cuenta:
1. **Riesgo en pruebas de mutación:** La skill sugiere modificar temporalmente una condición en el código para ver si la suite de tests falla. Si el agente no restaura el archivo con cuidado, podría dejar código alterado en el proyecto.
2. **Referencias rotas por rutas relativas:** Apunta a carpetas en `../../references/`. Si instalas solo la carpeta de esta skill sin el resto del repositorio, esos enlaces quedan rotos.
3. **Consumo de contexto:** Es un archivo muy largo (casi 400 líneas, ~21 KB). Mete todo en un solo `SKILL.md`, lo que carga muchos tokens cada vez que se invoca.
4. **Seguridad de supply chain:** Revisé el archivo línea por línea; no contiene scripts ejecutables ocultos, binarios ni llamadas a APIs extrañas. Proviene de una fuente confiable (Addy Osmani).

## Decision
[X] Install  
[ ] Do not install  

Reason:
La skill es segura, viene de un autor reconocido en la comunidad y su contenido técnico es de excelente nivel. Decidí instalarla congelando el commit exacto (`1401c8b8030e023baeebb31781a6653fe8e93026`) dentro de mi carpeta local `.agents/skills/code-review-and-quality/SKILL.md` para poder compararla contra mi skill sin depender de la red ni arriesgarme a cambios no controlados.
