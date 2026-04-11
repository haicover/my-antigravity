# Mastery Chapter: Modern Patterns & Principles (2026)

In the era of AI-native development and high-concurrency systems, design patterns and principles have evolved from "rules to follow" to "strategies for managing entropy."

## 1. Advanced SOLID & GRASP
Beyond the basics, 2026 engineering focuses on the **Cost of Change**.

### The Liskov Substitution Paradox
In modern systems, we favor **Composition over Inheritance** almost exclusively. Substitution is strictly enforced via **Protocols (TypeScript/Python)** or **Traits (Rust)** rather than class hierarchies.

### Single Responsibility (SRPx)
SRP is now interpreted at the **Functional Level**. A module shouldn't just do "one thing"; it should have "one reason to change" relative to the **Business Context**, not just the code structure.

### GRASP (General Responsibility Assignment Software Patterns)
We emphasize **Information Expert** and **Low Coupling**:
- **Information Expert**: Assign responsibility to the class that has the information necessary to fulfill it.
- **Pure Fabrication**: Creating classes that don't represent a domain concept but help achieve low coupling/high cohesion (e.g., Service objects, Repositories).

---

## 2. Design Patterns for the AI Era

### The Agentic Interface Pattern
When designing for AI agents to consume your code:
1.  **Strict Typing**: Every input/output must be typed and validated (Pydantic, Zod).
2.  **Self-Explaining APIs**: Use docstrings as a "Manual for the Agent."
3.  **Command Pattern**: Encapsulate actions as objects to allow AI to queue, undo, and log operations easily.

### The Strategy Pattern (Hyper-Dynamic)
Use the Strategy pattern to swap out AI models, database implementations, or UI rendering logic at runtime without breaking the core system.

### Functional Composition
Favor chaining pure functions over complex stateful objects. 
- **Pattern**: `Pipe`, `FMap`, and `Compose`.

---

## 3. The 2026 Design Checklist
- [ ] Is this code **Testable** without a database? (DIP)
- [ ] Is the **Boundary** between Domain and Infrastructure clear?
- [ ] Does it follow the **Principle of Least Astonishment** for both humans and AI?
- [ ] Is there **Zero Global State**?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Software%20Design%20and%20Architecture%28Thi%E1%BA%BFt%20k%E1%BA%BF%20v%C3%A0%20Ki%E1%BA%BFn%20tr%C3%BAc%20Ph%E1%BA%A7n%20m%E1%BB%81m%29/SKILL.md)*
