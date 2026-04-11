# Benchmarking & Optimization — Elite 2026

Elite Skill Engineering is an iterative process. In 2026, we use parallel execution and automated optimization loops to ensure peak performance.

---

## 🚀 1. Parallel Execution (Subagents)
Stop testing skills one by one. Use subagents to run multiple evaluation cases in parallel.
- **Workflow**: Create a workspace -> Spawn subagents for each test prompt -> Aggregate results.
- **Baseline Comparison**: Always run a **Baseline** (either without the skill or using the previous version) to measure the delta of improvement.

## 🖼️ 2. The Eval Viewer
Documentation and terminal logs aren't enough for qualitative review.
- **Visual Review**: Generate an HTML/standalone Viewer to compare outputs side-by-side.
- **Human-in-the-Loop**: Use the viewer's feedback loop to capture user critiques (`feedback.json`) and feed them back into the next iteration.

## 🔄 3. Description Optimization Loop
The `description` in the skill's frontmatter is the "API signature" for triggering.
1. **Trigger Eval Set**: Create 10–20 realistic queries (should-trigger vs. should-not-trigger).
2. **Automated Loop**: Run an optimization script that evaluates the current description and iteratively improves it based on "false positives" and "false negatives."
3. **Overfitting Check**: Avoid "training" your description on the same queries you test on.

## 📈 4. Analyzing Benchmark Results
Look behind the numbers:
- **Non-Discriminating Assertions**: If assertions pass for both baseline and skill, delete them. They don't measure the skill's value.
- **High Variance**: If a test case is flaky, it points to ambiguous instructions in `SKILL.md`.
- **Trade-offs**: Is the extra token cost of the skill worth the 5% quality improvement?

---

## ⚡ Elite Insight
> "A skill is a variable. Optimization is the process of reducing the variance of that variable. Your goal is for the skill to perform perfectly every time, regardless of how lazy the user's prompt is."
