# MatCom AI Skills

Conjunto de *skills* para Claude Code (y otros agentes compatibles) pensado para estudiantes y profesores de la Facultad de Matemática y Computación de la Universidad de La Habana. Resuelve el ciclo completo de investigación y escritura académica asistida por IA: recolectar fuentes, sintetizarlas en una wiki, destilar notas atómicas, generar un estado del arte estructurado y auditar el documento final antes de la defensa o el envío.

## ¿Qué problema resuelve?

Un estudiante que escribe su tesis o un paper enfrenta cuatro tareas que la IA puede acelerar sin sustituir el juicio del autor:

1. **Recoger fuentes**: bajar artículos, papers, blogs, PDFs, transcripciones — y guardarlos en un lugar citable.
2. **Sintetizarlas**: convertir un montón de fuentes en una wiki cross-linked con conceptos, métodos y debates.
3. **Destilar**: extraer claims atómicos para los apuntes propios.
4. **Estructurar el estado del arte**: producir el capítulo o sección de Estado del Arte de la tesis, organizado por dimensiones relevantes (no como lista cronológica de papers).
5. **Auditar**: revisión profunda del documento final antes de imprimir o someter, con hallazgos descriptivos sobre estructura, metodología, novedad, integridad bibliográfica y reproducibilidad.

Cada uno de estos pasos corresponde a un *skill* en este repositorio.

## Los skills

| Skill | Función |
|---|---|
| **`pull`** | Bajar webpages, PDFs, papers, blogs o cualquier documento externo a `./sources/` como markdown con frontmatter de procedencia. Usa `markitdown` por debajo. |
| **`ingest`** | Compila las fuentes de `./sources/` en una wiki cross-linked bajo `./wiki/`. Genera resúmenes por fuente y páginas de síntesis por concepto/método/debate. |
| **`distill`** | Extrae claims atómicos de un corpus para notas estilo Zettelkasten. Salida a `./notes/atomic/`. |
| **`sota`** | Genera un estado del arte estructurado por dimensiones a partir de un corpus de fuentes / páginas de wiki ya recolectadas. Salida: un reporte Markdown con introducción, una sección por dimensión, matriz comparativa y bibliografía con citas Pandoc-friendly (`^[N](#ref-N)^`). |
| **`review`** | Auditoría forense de un documento académico (tesis de diploma, maestría, doctorado o paper). Produce un reporte narrativo (5–18 páginas según nivel) más una asamblea forense estructurada como artefacto hermano. |

El flujo típico para un capítulo de Estado del Arte es:

```
pull (n veces) → ingest → sota → escribir el capítulo → review
```

## Instalación

Requisitos:

- Claude Code o un agente compatible con el formato Anthropic *skills* (Cursor, Codex, Gemini CLI, etc.).
- Python 3.10+ (para algunos scripts vendoreados).
- `markitdown` instalado vía `pipx` o `uv tool install` (solo para `pull`).

Pasos:

```bash
# Clonar el repo en cualquier carpeta
git clone https://github.com/matcom/ai-skills.git
cd ai-skills

# Instalar todos los skills en ~/.claude/skills/
./install.sh

# (Alternativa) Instalar solo en un proyecto específico
SKILLS_DEST=./mi-proyecto/.claude/skills ./install.sh
```

El script de instalación copia cada skill a su carpeta destino. Si la carpeta ya existe, la salta (no sobrescribe; usa `--force` si querés re-instalar).

## Uso típico — un Estado del Arte de cero

Supongamos que querés escribir el capítulo de Estado del Arte sobre *razonamiento agéntico* para tu tesis. Asumiendo que los 5 skills están instalados:

```bash
# 1. Crear carpeta del proyecto
mkdir -p ~/tesis-sota-razonamiento && cd ~/tesis-sota-razonamiento

# 2. Bajar fuentes (una por una, en la sesión interactiva con el agente)
/pull https://arxiv.org/abs/2201.11903    # CoT (Wei 2022)
/pull https://arxiv.org/abs/2305.10601    # Tree of Thoughts
/pull https://arxiv.org/abs/2303.11366    # Reflexion
# ... 20-30 papers más

# 3. Sintetizar en wiki
/ingest todas las fuentes que descargué, una página por método de razonamiento

# 4. Generar el SOTA por dimensiones
/sota razonamiento agéntico

# 5. Escribir el capítulo a mano usando el reporte SOTA como guía
#    (el SOTA es input para tu escritura, no tu escritura final)

# 6. Auditar el capítulo escrito
/review estado-del-arte.md
```

Cada skill es interactivo: te propone un plan, lo aprobás o modificás, y entonces ejecuta. No hace nada irreversible sin tu visto bueno.

## Convención de carpetas

Los skills asumen una estructura simple, relativa al directorio de trabajo:

```
mi-proyecto/
├── sources/        # fuentes bajadas por `pull`
├── wiki/           # síntesis cross-linked construida por `ingest`
├── notes/atomic/   # notas atómicas extraídas por `distill`
├── sota/           # reportes de estado del arte generados por `sota`
└── reviews/        # auditorías producidas por `review`
```

Ningún skill depende de Obsidian, de un *vault* específico, de Notion ni de ningún otro sistema externo. Todo vive en carpetas planas con archivos Markdown.

## Filosofía

Estas son las decisiones de diseño compartidas por los cinco skills:

1. **Plan primero, fan-out después.** Ningún skill arranca trabajo costoso sin presentar un plan que el usuario aprueba o modifica en lenguaje natural.
2. **Descriptivo, nunca prescriptivo.** Los reportes no dicen "esto está bien" o "esto está mal", solo "esta afirmación está aquí, la evidencia que cita está allá, esta brecha existe, esta novedad está cubierta por trabajo previo". El lector interpreta.
3. **Markdown como sustrato.** Todo entrada y salida es Markdown. Renderizable con Quarto/Pandoc/Typst sin herramientas adicionales.
4. **Sin lock-in.** No hay dependencia de un proveedor de almacenamiento, sincronización o renderizado. El estudiante elige sus herramientas.
5. **Multilingüe.** Los prompts internos están en inglés (donde los modelos funcionan mejor); las observaciones, reportes y artefactos se generan en el idioma del documento auditado o del corpus consultado.

## Contribuir

Pull requests bienvenidas, especialmente para:

- Nuevos skills que cierren huecos del flujo académico.
- Traducciones de los skills a otros idiomas (los prompts ya soportan multilenguaje en sus outputs; lo que falta es traducir los prompts mismos a otros idiomas si fuese útil).
- Mejoras a los scripts vendoreados.

Convención: un skill por carpeta bajo `skills/`. Cada skill tiene su propio `SKILL.md` como punto de entrada, opcionalmente `tools/` con scripts vendoreados, y subagent prompts como archivos hermanos.

## Licencia

MIT. Ver `LICENSE`.

## Créditos

Construido con Claude Code en colaboración con la facultad de MatCom. Diseñado y mantenido por Alejandro Piad Morffis (`@apiad`).
