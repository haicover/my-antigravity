# Skill Design & Architecture — Elite 2026

Skill creation in 2026 is an engineering discipline. It's about designing a cognitive module that an AI can load and execute with precision.

---

## 🎯 1. Capturing Intent
Before writing a single line of a skill, you must define its core mission.
- **Intent Extraction**: What specific problem does this skill solve?
- **Context Cues**: In what specific scenarios should this skill be triggered? (e.g., "whenever user mentions database migration").
- **Expected Outcome**: Define the "Perfect Output" format (Markdown, JSON, code structure).

## 🏗️ 2. Skill Structure & Progressive Disclosure
Elite skills are modular. Don't dump everything into `SKILL.md`. Use a 3-layer loading pattern:
1. **Metadata Layer**: The name and description in the frontmatter. Used for triggering (High efficiency).
2. **Instruction Layer**: The `SKILL.md` body. Contains workflows and logic (Medium weight).
3. **Resource Layer**: The `references/` and `scripts/` directories. Loaded only when needed (On-demand).

## ✍️ 3. Elite Instruction Principles
- **Imperative Clarity**: Use direct commands (`Read the file`, `Validate the schema`).
- **Explain the "Why"**: Modern LLMs have a strong theory of mind. Explaining the reasoning behind an instruction often yields better results than blind obedience.
- **Avoid Over-Fitting**: Don't build a skill that only works for your current example. Generalize the patterns so it survives varied user inputs.
- **Structural Framing**: Use Markdown headers to create a "Table of Contents" for the LLM's attention.

## 📁 4. Standard Directory Layout
```text
skill-name/
├── SKILL.md                ← The entry point (Command Center)
└── Bundled Resources/
    ├── scripts/            ← Deterministic logic (Python/JS)
    ├── references/         ← Deep documentation & schemas
    └── assets/             ← Templates, binary files
```

---

## ⚡ Elite Insight
> "A skill is a cognitive shortcut. If it takes the AI more energy to read the skill than to perform the task without it, your architecture has failed. Keep it lean, keep it modular."
