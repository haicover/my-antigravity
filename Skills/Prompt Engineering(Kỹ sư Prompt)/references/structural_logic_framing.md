# Structural Logic & Context Framing — Elite 2026

Structural logic is what separates a "Chat" from a "Tool." In 2026, we focus on high-fidelity information separation to maximize model reasoning capabilities.

---

## 🏗️ 1. XML Tagging (The Gold Standard)
Using XML tags is the most effective way to separate instructions from data blocks. It reduces "semantic noise" and prevents the model from getting confused.
```xml
<instructions>
  Do X according to Y.
</instructions>

<context>
  Current environment is Z.
</context>

<data_to_process>
  {{INPUT_DATA}}
</data_to_process>
```

## 📝 2. Markdown Hierarchies as Logic Gates
- **H1/H2 Headers**: Act as "Logical Chapters" for the model.
- **Bold/Italics**: Used for emphasis on critical constraints.
- **Lists**: Used for sequential steps or parallel requirements.

## 🎭 3. System Role & Context Engineering
- **Identity Framing**: Don't just say "You are a coder." Say "You are a Senior Principal Engineer specializing in Rust memory safety."
- **Internal Monologue (`<thought>`)**: Forcing the model to "think" before generating an answer. This significantly improves performance on complex reasoning tasks.
- **Variable Injection**: Using `{{PLACEHOLDERS}}` to create reusable, programmatic templates.

## 🖼️ 4. Multimodal Context
- **Image-to-Context**: Providing visual screenshots to ground the model in a UI state.
- **Audio/Video Context**: Using timestamps and transcripts to coordinate temporal reasoning.

---

## 💡 Expert Rule: "Separation of Concerns"
Never mix your metadata with your content. Use clear delimiters (like `---` or XML tags) so the model knows exactly where the user input ends and the next instruction begins.
