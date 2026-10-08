# ADA-07: Build an Agent Skill

**Ingeniería de Software asistida por IA · UADY**  
**Estudiante:** Hector Castro (`hectorcast44`)  
**Actividad:** ADA-07 · Build an Agent Skill (Workflow profesional reutilizable)

---

## 🎯 Objetivo de la Actividad
Diseñar, implementar y evaluar una **Agent Skill** que encapsule un proceso profesional de Ingeniería de Software: **Pull Request Readiness Review**.
La Skill permite a un coding agent revisar si un Pull Request o rama de características está lista para revisión humana antes del merge, inspeccionando requisitos, cambios de código y evidencia de pruebas sin escribir en GitHub, sin aprobar y sin hacer merge (*Draft-Only / Human Review*).

---

## 📁 Estructura del Repositorio

```text
ada-07-skills/
├── .agents/
│   └── skills/
│       ├── reviewing_pull_requests/              # Skill construida en Parte I
│       │   ├── SKILL.md                          # Frontmatter + Workflow v1.0.1
│       │   ├── references/                       # Progressive Disclosure
│       │   │   ├── review_checklist.md           # Checklist de ingeniería
│       │   │   └── severity_guide.md             # Guía de severidad
│       │   ├── scripts/
│       │   │   └── validate_review_report.py     # Validador determinista (exit code 0/1)
│       │   ├── assets/
│       │   │   └── review_report_template.md     # Plantilla estandarizada
│       │   └── evals/                            # Evaluation-Driven Design
│       │       ├── trigger_cases.json            # Casos de activación (+3 positivos, +3 negativos)
│       │       └── execution_cases.json          # Casos de ejecución y boundary
│       └── code-review-and-quality/              # Skill profesional adoptada en Parte II
│           └── SKILL.md                          # De Addy Osmani (commit 1401c8b8)
├── docs/
│   ├── skill_workflow_observation.md             # Observación del flujo manual
│   ├── third_party_skill_audit.md                # Auditoría de supply chain previa
│   ├── professional_skill_anatomy.md             # Reverse engineering (5 ejes)
│   └── reflection.md                             # Respuestas a las 14 preguntas de reflexión
├── results/
│   ├── pr-readiness-review.md                    # Reporte de revisión de PR #42
│   ├── skill-evaluation-report.md                # Evaluación, matrices y refinamiento (v1.0.0 -> v1.0.1)
│   ├── professional-skill-review.md              # Reporte generado con la skill profesional
│   └── skill-comparison.md                       # Matriz comparativa entre ambas skills
├── src/                                          # Código del servicio (Order & Pricing)
├── tests/                                        # Pruebas con pytest
├── REQUIREMENTS.md                               # Especificación contractual (AC-01 a AC-04)
├── ARCHITECTURE.md                               # Directrices de arquitectura
└── AI_USAGE_LOG.md                               # Registro de uso de IA (6 etapas)
```

---

## 🧪 Verificación Rápida

### 1. Ejecutar Pruebas Automatizadas
```bash
pytest -v
```

### 2. Validar Reporte de Revisión de Forma Determinista
```bash
python .agents/skills/reviewing_pull_requests/scripts/validate_review_report.py results/pr-readiness-review.md
# Expected: VALID: PR readiness review structure is complete. (exit code 0)
```
