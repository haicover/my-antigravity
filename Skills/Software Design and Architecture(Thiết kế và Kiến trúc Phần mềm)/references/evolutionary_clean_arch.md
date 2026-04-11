# Mastery Chapter: Clean & Evolutionary Architecture (2026)

Architecture in 2026 is no longer about "being right" at once; it's about "being easy to change when you're wrong."

## 1. The Clean Trio: Hexagonal, Onion, and Clean

While they go by different names, they share 80% of the same DNA.

### Hexagonal Architecture (Ports & Adapters)
- **Concept**: The core application logic is at the center, surrounded by "Ports" (Interfaces).
- **Adapters**: Concrete implementations (PostgreSQL, AWS S3, React UI) that plug into these ports.
- **Benefit**: Zero coupling to external technology. You can swap a database or a transport protocol in minutes.

### The Dependency Rule
> "Source code dependencies can only point inwards, towards higher-level policies."

1.  **Frameworks/Drivers** (Outer) -> **Interface Adapters** -> **Application Services** -> **Domain Entities** (Inner).

---

## 2. Evolutionary Architecture & Fitness Functions

Static diagrams fail. 2026 architects use **Fitness Functions** to automate architectural governance.

### What is a Fitness Function?
A programmatic test that fails if an architectural constraint is violated.

#### Example (ArchUnit in Java or pytest-archon in Python):
```python
# Rule: Application layer cannot import from Infrastructure
def test_architecture():
    (archrule()
     .match("myapp.application.*")
     .should_not()
     .import_from("myapp.infrastructure.*")
     .check(root_package))
```

### Decoupling Patterns
- **Database-per-Service**: Ensuring logical boundaries aren't bridged at the data layer.
- **In-Process vs. Out-of-Process**: Knowing when to use an Interface and when to use a Network boundary.

---

## 3. Practical Implementation Guidelines

### The "Screaming" Architecture
Your folder structure should reveal **what the app does**, not what framework it uses.
- ❌ `/controllers`, `/models`, `/views`
- ✅ `/orders`, `/billing`, `/shipping`

### Invariants over DTOs
Don't just pass data. Ensure that every object in the inner layers is **Always Valid**. If an object exists, it must satisfy all domain rules.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Software%20Design%20and%20Architecture%28Thi%E1%BA%BFt%20k%E1%BA%BF%20v%C3%A0%20Ki%E1%BA%BFn%20tr%C3%BAc%20Ph%E1%BA%A7n%20m%E1%BB%81m%29/SKILL.md)*
