# Anatomía y Reverse Engineering de una Skill Profesional

Análisis de la Skill: `code-review-and-quality`  
Autor/Origen: Addy Osmani (`addyosmani/agent-skills`)  
Commit: `1401c8b8030e023baeebb31781a6653fe8e93026`  

---

## 1. Routing (Frontmatter & Description)
- **Mecanismo de detección**: La propiedad `description` está redactada para capturar una amplia variedad de intenciones de revisión previas al merge. Emplea patrones fraseológicos como:
  - *"Conducts multi-axis code review"*
  - *"Use before merging any change"*
  - *"Use when reviewing code written by yourself, another agent, or a human"*
  - *"Use when asked to review a diff or a pull request, even when the diff is pasted inline"*
- **Estrategia**: Es una descripción proactiva y centrada en el momento del ciclo de vida del desarrollo ("before merging any change"). A diferencia de un enrutamiento restrictivo, abarca tanto diffs pegados en el chat como ramas completas, pero carece de cláusulas negativas explícitas (anti-triggers negativos como "Do NOT merge" o "Do NOT refactor"), confiando en que su verbo rector ("Conducts review") delimite el alcance.

---

## 2. Workflow & Quality Gates
El flujo de revisión se estructura en 5 pasos secuenciales y disciplinados:
1. **Step 1: Understand the Context**: Comprender qué intenta lograr el cambio, la especificación o tarea que implementa, y el cambio de comportamiento esperado antes de juzgar el código.
2. **Step 2: Review the Tests First**: Inspección de pruebas unitarias previo a la lectura de la implementación. Propone una técnica activa de verificación heurística: inducir una mutación temporal (invertir una condición lógica) para comprobar si la suite falla; si los tests siguen pasando, existe una brecha de cobertura.
3. **Step 3: Review the Implementation**: Evaluación archivo por archivo a través de los cinco ejes.
4. **Step 4: Categorize Findings**: Etiquetado estricto de cada hallazgo con su severidad correspondiente antes de redactar comentarios.
5. **Step 5: Verify the Verification**: Comprobación rigurosa de la evidencia empírica aportada por el autor (pruebas ejecutadas, compilación exitosa, pruebas manuales).

**Quality Gates previas al veredicto**:
- Exige que todos los problemas críticos y requeridos estén resueltos o justificados formalmente.
- Cero tolerancia a "lo limpiamos después" (*"We'll clean it up later" is a fallacy*).

---

## 3. Review Axes (Los Cinco Ejes de Revisión)
La Skill organiza el escrutinio técnico en 5 dimensiones exhaustivas:
- **Correctness (Corrección)**: ¿El código cumple la especificación? Manejo de valores nulos, vacíos y casos de frontera; manejo de caminos de error; detección de errores off-by-one, condiciones de carrera e inconsistencias de estado.
- **Readability & Simplicity (Legibilidad y Simplicidad)**: Nombres descriptivos alineados al proyecto; flujo de control directo (sin ternarios anidados o callbacks profundos); control del tamaño de archivos e implementaciones (¿podría hacerse en menos líneas?); detección de código muerto o shims innecesarios.
- **Architecture (Arquitectura)**: Respeto a límites de módulos; ausencia de dependencias circulares; evitar relocalizar complejidad en lugar de reducirla; evitar que lógica específica de un feature contamine módulos genéricos compartidos.
- **Security (Seguridad)**: Validación y sanitización en fronteras; cero secretos o credenciales en código o logs; consultas SQL parametrizadas; tratamiento de datos externos como no confiables.
- **Performance (Rendimiento)**: Detección de patrones N+1; bucles o consultas no acotadas; operaciones síncronas bloqueantes en hilos principales; paginación ausente en endpoints.

---

## 4. Severity Model (Modelo de Severidad)
La Skill introduce una taxonomía explícita de prefijos para evitar que los desarrolladores malgasten esfuerzo en sugerencias opcionales:

| Prefijo | Significado | Acción para el Autor |
|---|---|---|
| *(Sin prefijo)* | **Required change** | Obligatorio resolver antes del merge |
| `Critical:` | **Blocks merge** | Vulnerabilidad grave de seguridad, pérdida de datos o funcionalidad rota |
| `Nit:` | **Minor / Optional** | Preferencia de estilo o detalle menor; el autor puede ignorarlo |
| `Optional:` / `Consider:` | **Suggestion** | Sugerencia técnica valiosa pero no bloqueante |
| `FYI` | **Informational only** | Contexto o nota para referencia futura; no requiere acción |

**Principio de ordenamiento**: Ordenar los hallazgos por apalancamiento (*leverage*): Corrección y Seguridad primero, seguidos de regresiones estructurales, y finalmente detalles cosméticos.

---

## 5. Verification (Verificación Empírica)
- Exige evidencia observable antes de emitir un veredicto de aprobación:
  - Pruebas unitarias/integración pasando con exit code 0.
  - Compilación (build) exitosa.
  - Validación de disciplina de dependencias (revisar el diff del lockfile, no solo el `package.json`).
  - Lista explícita de código muerto identificado (`DEAD CODE IDENTIFIED`) solicitando confirmación antes de borrar.

---

## 6. Composition (Composición y Modularidad)
- La Skill no intenta resolver todo en un solo prompt monolítico. Aplica composición modular delegando a otras skills especializadas:
  - Remite a `security-and-hardening` para auditorías de seguridad avanzadas y triaje de vulnerabilidades (`npm audit`).
  - Remite a `performance-optimization` para perfilado y optimizaciones complejas de CPU/memoria.
  - Remite a `constraint-driven-development` para métricas avanzadas de mutation testing.
  - Referencia archivos compartidos a nivel de repositorio (`../../references/security-checklist.md`, `../../references/performance-checklist.md`).

---

## 7. Boundaries (Límites y Autoridad Humana)
- **Decisión final humana**: Incluye el patrón *Multi-Model Review Pattern* y establece explícitamente: *"Human makes the final call"*.
- **Acciones prohibidas de forma silenciosa**:
  - No aprueba ni hace merge automático sin revisión del autor.
  - No elimina silenciosamente código muerto sin preguntar primero (*"Ask before deleting: Should I remove these now-unused elements?"*).
  - Preserva el principio de que los desacuerdos técnicos se resuelven mediante datos y guías de estilo, pero la decisión final corresponde a la autoridad humana.
