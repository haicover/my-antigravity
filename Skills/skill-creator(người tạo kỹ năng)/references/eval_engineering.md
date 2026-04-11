# Evaluation Engineering — Elite 2026

In 2026, "it looks okay to me" is no longer the standard for skill verification. Elite Skill Engineering requires **Quantitative Evaluation**.

---

## 🧪 1. Designing Test Cases (Eval Prompts)
Every skill should have 3–5 representative test cases stored in `evals/evals.json`.
- **Realistic Prompts**: Use complex, multi-layered prompts that a real user would type.
- **Edge Cases**: Include inputs that might "break" the skill or cause ambiguity.
- **Expected Output**: Define the ground truth against which the output will be measured.

## ⚖️ 2. Assertion Logic
Assertions are objective "binary" checks used to grade a skill's performance.
- **Verification Types**:
    - **Format Check**: "Does it output valid JSON?"
    - **Content Check**: "Does the report contain the 'Key Findings' section?"
    - **Tool Use Check**: "Did the skill use the `read_file` tool?"
    - **Logic Check**: "Is the total revenue calculated correctly?"

## 📊 3. Quantitative Metrics (The Grader)
Elite skills are graded using an automated **Grader Agent**.
- **Pass Rate**: The percentage of assertions that passed.
- **Cost/Token Efficiency**: Measuring the token usage per run (Efficiency is a feature).
- **Duration**: Measuring execution time (20.3s vs 25s).

## 🧩 4. JSON Schema (Reference)
Refer to the standard 2026 Evaluation Schema:
```json
{
  "eval_id": 1,
  "prompt": "Task description...",
  "assertions": [
    {
      "type": "javascript",
      "value": "output.includes('# Summary')",
      "description": "Output must have a Summary header."
    }
  ],
  "expected_output": "Description of the perfect result"
}
```

---

## ⚡ Elite Insight
> "Assertions should be discriminating. If an assertion passes even when the skill isn't used, your test isn't measuring the skill — it's measuring the base model. Build tests that only pass when the skill is executed perfectly."
