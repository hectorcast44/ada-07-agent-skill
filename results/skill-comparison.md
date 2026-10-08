# Comparativa de Skills: `reviewing-pull-requests` vs `code-review-and-quality`

Análisis comparativo que realicé al probar ambas skills sobre el mismo cambio: el PR #42 en la rama `feature/pr-42-tiered-discounts`.

---

## 1. Matriz Comparativa por Dimensiones

| Dimensión | Mi Skill (`reviewing-pull-requests`) | Skill Profesional (`code-review-and-quality`) | Mi Conclusión y Aprendizaje |
|---|---|---|---|
| **Trigger / routing** | Enfoque acotado a "PR readiness", con anti-triggers explícitos para no tocar código ni hacer merge. | Muy amplia y proactiva ("before merging any change", diffs pegados en el chat, código de agentes o humanos). | La de Addy cubre más escenarios de integración; la mía previene mejor que el agente se active cuando le piden implementar o fusionar ramas. |
| **Scope / boundaries** | Estrictamente *Draft-Only*. Solo genera un markdown local y se detiene pidiendo decisión humana obligatoria. | Define un estándar de aprobación consultivo. Orienta el veredicto pero no prohíbe de forma tan tajante la interacción en chat. | Mis límites estrictos reducen el riesgo de que el agente alucine y quiera correr comandos de Git no autorizados. |
| **Workflow depth** | Flujo lineal de 10 pasos con lectura de especificaciones normativas (`REQUIREMENTS.md`) y validación por script. | Flujo de 5 pasos centrado en revisar tests primero, aplicar 5 ejes de calidad y probar mutaciones en el código. | La mía es más fuerte en trazabilidad contractual contra requerimientos; la de Addy profundiza mucho más en la calidad interna del código. |
| **Correctness** | Mapea directamente cada criterio de aceptación (AC-01 a AC-04) contra las líneas del diff. | Revisa cumplimiento de especificación, valores nulos, límites numéricos, caminos de error y off-by-one. | Ambas atraparon el bug del umbral en `SILVER` ($50.00). Addy además explicó cómo simplificar la estructura condicional redundante. |
| **Architecture** | Revisa que se respeten las capas descritas en `ARCHITECTURE.md`. | Evalúa si el cambio reduce la complejidad o solo la mueve de lugar, y cuida el tamaño del archivo (~1,000 líneas). | Las reglas de Addy sobre no relocalizar deuda técnica aportan un criterio de diseño más maduro. |
| **Security** | Checklist general de seguridad (secretos, permisos, validación de entradas). | Eje dedicado de seguridad y delega auditorías profundas a `security-and-hardening`. | Addy maneja la seguridad como parte de un ecosistema de skills especializadas. |
| **Performance** | Puntos básicos en el checklist de referencia. | Eje dedicado de rendimiento (consultas N+1, operaciones síncronas bloqueantes, paginación) y delega a `performance-optimization`. | Addy formaliza el rendimiento con preguntas concretas sobre el impacto en milisegundos. |
| **Tests / verification** | Corre `pytest -v` y verifica que los tests pasen y no se hayan borrado pruebas existentes. | Revisa tests primero, pide pruebas de mutación (invertir una condición para ver si fallan) y cuida el diff de lockfiles. | La técnica de mutación de Addy es superior para encontrar huecos donde la suite está en verde pero no prueba los límites. |
| **Severity model** | 3 niveles simples: `MUST FIX`, `SHOULD FIX`, `OPTIONAL`. | 5 niveles con prefijos: `Critical:`, `Required` (sin prefijo), `Nit:`, `Optional:`, `FYI`. | La escala de Addy separa mucho mejor los comentarios cosméticos de los bloqueadores del PR. |
| **Human review** | Gate determinista obligatorio: la línea `Human decision required: YES` la valida un script en Python. | Filosofía *"Human makes the final call"* en un patrón multi-modelo. | Mi enfoque garantiza que el gate se cumpla de forma programática; el de Addy da un marco mental de colaboración. |
| **References / composition** | Estructura modular limpia con *progressive disclosure* (`references/`, `assets/`, `scripts/`). | Archivo `SKILL.md` monolítico que apunta a checklists compartidos fuera de la carpeta (`../../references/`). | Mi estructura es más autónoma y fácil de empaquetar sin enlaces rotos a carpetas superiores. |
| **Reusability** | Reusable para cualquier proyecto con requisitos formales y tests automatizados. | Reusable para cualquier lenguaje o stack en tareas de revisión general de software. | La de Addy es agnóstica de lenguaje; la mía incluye validación mecánica específica que garantiza la uniformidad del reporte. |

---

## 2. Preguntas de Análisis Comparativo

### 1. ¿Qué hace la Skill profesional que tu Skill no contempló?
- **Pruebas de mutación heurística:** Me pareció una idea genial. Sugiere invertir una condición en el código (por ejemplo, cambiar un `>=` por un `>` o quitar una negación) y correr los tests. Si los tests siguen pasando en verde, acabas de demostrar empíricamente que falta un caso de prueba.
- **Disciplina con los lockfiles y dependencias:** Tiene reglas claras para no hacer "bump deps" a ciegas; exige revisar paquetes de uno en uno y mirar el diff del lockfile, no solo el `package.json`.
- **Regla contra relocalizar complejidad:** Exige evaluar si un refactor realmente reduce la cantidad de conceptos que el desarrollador debe recordar, o si solo escondió la misma complejidad detrás de capas innecesarias.

### 2. ¿Qué elementos de tu Skill son más específicos al curso/proyecto y conviene conservar?
- **Mapeo directo contra `REQUIREMENTS.md` y `ARCHITECTURE.md`:** Citar el criterio de aceptación contractual exacto (por ejemplo `RF-01 -> AC-01`) es indispensable cuando trabajas con especificaciones formales de ingeniería.
- **Validación determinista por script (`validate_review_report.py`):** Un script en Python verifica en milisegundos que el reporte no tenga huecos ni le falten secciones obligatorias. El LLM no puede "olvidar" un encabezado porque el script le regresa exit code 1.
- **Gate determinista `Human decision required: YES`:** Garantiza que el agente no tome atribuciones que no le corresponden.

### 3. ¿Qué agregarías a una versión 2 de tu Skill?
1. La técnica de mutation testing heurístico en el paso de revisión de pruebas.
2. La escala de 5 niveles de severidad (`Critical`, `Required`, `Nit`, `Optional`, `FYI`) para no saturar al desarrollador con detalles menores.
3. El catálogo de soluciones estructurales con nombre (ej. "colapsar ramas condicionales", "extraer dispatcher") para que los hallazgos sean más constructivos.

### 4. ¿Qué NO copiarías y por qué?
- **Su `SKILL.md` monolítico:** El archivo de Addy tiene casi 400 líneas y pesa ~21 KB. Meter todo eso de golpe rompe el principio de *progressive disclosure* y desperdicia tokens del context window del modelo en cada invocación. Prefiero mil veces mantener `SKILL.md` en ~60 líneas y mandar el detalle a `references/`.
- **Rutas relativas ascendentes (`../../references/`):** Asumen que la skill vive dentro de un repositorio monorepo específico. Si la copias a otro proyecto de forma aislada, esos enlaces se rompen de inmediato.

### 5. ¿Cuál produjo hallazgos más accionables? Incluye dos ejemplos.
Ambas skills fueron muy efectivas sobre el PR #42, pero mostraron fortalezas distintas:

- **Ejemplo 1 (El bug del umbral en el tier SILVER):**
  - *Mi skill:* Fue muy precisa en señalar la violación contractual: citó `src/services/pricing.py#L35` y explicó que violaba directamente el criterio `AC-01`, dejando sin descuento a compras de exactamente $50.00.
  - *La profesional:* Además de marcar el bug, notó el problema de diseño: vio que la condición para SILVER estaba duplicada innecesariamente respecto al resto de los tiers y sugirió unificarla en un solo bloque limpio, reduciendo líneas de código.
- **Ejemplo 2 (Validación de entradas externas):**
  - *La profesional:* Identificó que el parámetro `coupon_discount` en `calculate_final_total` no validaba números negativos. Aplicó su eje de seguridad ("tratar datos externos como no confiables") y me dio el código exacto del guard statement a agregar (`if coupon_discount < Decimal("0.00"): raise ValueError(...)`).

---

## 3. Evaluación de la Skill como Dependencia (Supply Chain Hygiene)

| Control | Cómo lo evalué y qué encontré |
|---|---|
| **Source** | Proviene del repositorio público oficial `https://github.com/addyosmani/agent-skills`, mantenido por Addy Osmani (líder de ingeniería en Google Chrome). |
| **Pinning** | No usé la rama `main` flotante. Fijé la instalación exactamente en el commit `1401c8b8030e023baeebb31781a6653fe8e93026` (Blob SHA `08209ff2208d2883d48d945f7754c428b77f8d87`). |
| **Audit** | Leí el archivo `SKILL.md` completo antes de instalarlo. Confirmé que no contiene scripts ocultos, comandos `curl` a dominios sospechosos ni instrucciones maliciosas. |
| **Secrets** | Cero contraseñas, tokens de API o variables de entorno sensibles en el archivo. |
| **Commands** | Solo sugiere correr herramientas locales del proyecto (`pytest`, `npm test`) y pruebas de mutación manuales; no intenta bajar nada de internet. |
| **Permissions** | Solo necesita leer archivos locales (`git diff` y código fuente). No requiere permisos de red ni privilegios de administrador. |
| **Change Control** | La instalé de forma local y versionada en `.agents/skills/code-review-and-quality/SKILL.md`. Si el autor actualiza su repo mañana, mi entorno no sufrirá cambios sorpresa. |

---

## 4. Mi Conclusión
Hacer este ejercicio me demostró que diseñar una buena Skill para agentes no es solo redactar un prompt bonito; es construir una capacidad de ingeniería repetible y segura. 

La skill de Addy Osmani me enseñó heurísticas de revisión de código de primer nivel que reflejan años de experiencia en desarrollo de software, especialmente su técnica para probar mutaciones en los tests y su criterio para simplificar arquitecturas. Por otro lado, mi skill demostró que una estructura modular con *progressive disclosure* y validación mecánica con scripts en Python es mucho más eficiente en el uso de contexto y da mayores garantías de que el reporte final salga completo.

Para una versión 2.0, el camino ideal es combinar ambas: adoptar el criterio técnico y los 5 ejes de la skill profesional, pero empaquetados dentro de la arquitectura modular y determinista que construí en este proyecto.
