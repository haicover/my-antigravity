# Agentic Deployment & Environment — Elite 2026

Elite skills are built to be executed by Agents. In 2026, this means mastery of the Model Context Protocol (MCP) and multi-agent coordination.

---

## 🔌 1. Integrating MCP Tools
Don't rely solely on basic file manipulation.
- **Tool Discovery**: Use `mcp` tools to browse directories, run commands, and call external APIs.
- **Context injection**: Use MCP resources to provide deep context to your skills (e.g., exposing a codebase's documentation to a `code-reviewer` skill).

## 🤝 2. Multi-Agent Coordination
Advanced skill workflows often involve specialized "Internal Agents":
- **The Grader**: Responsible for objective verification of assertions.
- **The Comparator**: Performs blind A/B comparisons between skill versions.
- **The Analyzer**: Performs meta-analysis on benchmark patterns to suggest architectural fixes.

## 📦 3. Packaging & Versioning
- **Skill Bundling**: Use `scripts.package_skill` to create portable `.skill` files.
- **Version Control**: Every skill iteration should be snapshotted (`cp -r <skill> /tmp/skill_v1.0/`) before applying major architectural changes.

## 🌍 4. Environmental Adaptation
A skill must adapt to different working environments:
- **Claude Code**: Full access to subagents, browser, and parallel execution.
- **Claude.ai**: Limited to safe, single-thread execution; skip benchmarking/optimization.
- **Cowork**: Full subagent support but limited interactivity; use static HTML viewers.

---

## ⚡ Elite Insight
> "A skill is a product. Packaging is the difference between a 'cool experiment' and a 'reliable tool'. Always include a `LICENSE.txt` and a clear `README.md` (or high-quality SKILL.md) in your bundles."
