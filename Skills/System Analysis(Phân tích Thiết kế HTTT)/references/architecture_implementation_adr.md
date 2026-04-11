# Mastery Chapter: Modern Architecture & ADRs (2026)

Architecture is about the big decisions—decisions that are expensive to change later.

## 1. Architecture Decision Records (ADR)

An ADR is a document that captures an important architectural decision, including its context and the consequences.

### Template:
- **Title**: Short and descriptive.
- **Status**: Proposed, Accepted, Rejected, Deprecated.
- **Context**: Why are we making this decision?
- **Decision**: What is the choice?
- **Consequences**: What are the trade-offs (The good and the bad)?

---

## 2. The C4 Model

A lean graphical notation technique for modeling the architecture of software systems.

- **Level 1 (Context)**: How the system fits into the world.
- **Level 2 (Containers)**: High-level technical building blocks (Web App, Database, API).
- **Level 3 (Components)**: The internal parts of a container.
- **Level 4 (Code)**: Detailed class/object structure (rarely needed).

---

## 3. Evolutionary Architecture

Designing systems that can change without breaking.

- **Fitness Functions**: Automated checks that verify the system maintains key architectural characteristics (e.g., Performance, Security).
- **Loose Coupling**: Minimizing dependencies between modules or services.
- **AI-Actor Integration**: Treat AI agents as standard system actors but with a "probabilistic output" state.

---

## 4. Implementation Strategy

| Layer | Responsibility | Pattern |
|-------|----------------|---------|
| **Presentation** | UI / API Gateways | Backend-for-Frontend (BFF) |
| **Application** | Use Case Coordination | Command/Query (CQRS) |
| **Domain** | Business Logic | Domain-Driven Design (DDD) |
| **Infrastructure** | Persistence / Messaging | Repository / Message Bus |

## 🚀 Architect's Checklist
- [ ] Have I documented the "Why" via an ADR?
- [ ] Is the system horizontally scalable?
- [ ] Are we monitoring the "Golden Signals" (Latency, Traffic, Errors, Saturation)?
- [ ] Is the data partitioned correctly for growth?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/System%20Analysis%28Ph%C3%A2n%20t%C3%ADch%20Thi%E1%BA%BFt%20k%E1%BA%BF%20HTTT%29/SKILL.md)*
