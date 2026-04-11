# Mastery Chapter: Domain-Driven Design (DDD) 2026

DDD is the primary tool for managing complexity in the **Core Domain**. It bridges the gap between technical implementation and business reality.

## 1. Strategic DDD: Working with the Business

### The Ubiquitous Language
A language shared by everyone on the team (Devs, POs, Stakeholders). 
- **Rule**: If the business calls it a "Subscription," the class name MUST be `Subscription`, not `UserPackage` or `PaymentPlan`.

### Bounded Contexts & Context Mapping
A large system is composed of multiple sub-domains.
- **Bounded Context**: A boundary where a specific model applies.
- **Context Maps**: Defining relationships between contexts (Customer/Supplier, Conformist, ACL - Anti-Corruption Layer).

---

## 2. Tactical DDD: Building the Core

### Entities vs. Value Objects
- **Entity**: Has a unique identity that persists over time (e.g., `User`, `Order`). Even if attributes change, the identity remains.
- **Value Object**: Defined solely by its attributes. It is **Immutable**. If you change an attribute, you get a new Value Object (e.g., `Money`, `Address`, `Color`).

### Aggregates & Roots
An Aggregate is a cluster of domain objects that can be treated as a single unit for data changes.
- **Aggregate Root**: The only entry point for external calls. It maintains **Invariants** (Consistency Rules).
- **Rule**: References between aggregates should be by **ID**, not by object reference.

### Domain Events
Something that happened in the domain that other parts of the system care about (e.g., `OrderPlaced`, `AccountLocked`). 
- **Pattern**: Publish events from the Aggregate Root after a state change.

---

## 3. DDD in the AI Era
AI models excel at extracting **Domain Knowledge** but fail at maintaining **Consistency**.
- **Role for Architects**: Use AI to draft the ubiquitous language and map contexts, but use the code structure (Aggregates) to enforce the rules that AI might hallucinate.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Software%20Design%20and%20Architecture%28Thi%E1%BA%BFt%20k%E1%BA%BF%20v%C3%A0%20Ki%E1%BA%BFn%20tr%C3%BAc%20Ph%E1%BA%A7n%20m%E1%BB%81m%29/SKILL.md)*
