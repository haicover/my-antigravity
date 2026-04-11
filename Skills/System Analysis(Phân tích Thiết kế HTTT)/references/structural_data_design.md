# Mastery Chapter: Structural Data Design (2026)

Data is the lifeblood of a system. A poorly designed data structure will haunt the system's performance and scalability forever.

## 1. Entity Relationship Diagram (ERD)

The ERD is the blueprint for the database. We use the **Crow's Foot Notation** for professional modeling.

### Core Concepts:
- **Entities**: The objects we store data about (e.g., User, Product, Order).
- **Attributes**: The specific information (e.g., Name, Price, Date).
- **Relationships**: 1:1, 1:N, or M:N.

### Elite Checklist:
- [ ] Are all Primary Keys (PK) defined? (Prefer UUID in distributed systems).
- [ ] Are Foreign Keys (FK) explicitly mapped?
- [ ] Is "Participation" mandatory or optional?

---

## 2. Database Normalization

Normalization avoids data redundancy and ensures data integrity.

- **1NF**: Atomic values. No repeating groups.
- **2NF**: In 1NF + All non-key attributes depend on the *entire* PK. (Removes Partial Dependencies).
- **3NF**: In 2NF + No transitive dependencies. (e.g., City depends on ZipCode, not directly on UserID).
- **BCNF**: A stronger version of 3NF for complex keys.

---

## 3. Data Integrity & Constraints

System Analysis isn't just about drawing boxes; it's about defining the rules.

- **Domain Integrity**: Correct data types and ranges.
- **Entity Integrity**: PK must be unique and not null.
- **Referential Integrity**: FK must match a valid PK.
- **Business Rule Constraints**: e.g., "Order total cannot be negative" (implemented via `CHECK` constraints).

---

## 🏗️ Design Workflow
1.  **Identify Entities** from SRS nouns.
2.  **Define Cardinality** between entities.
3.  **Apply Normalization** to keep it clean.
4.  **Enforce Integrity** via technical constraints.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/System%20Analysis%28Ph%C3%A2n%20t%C3%ADch%20Thi%E1%BA%BFt%20k%E1%BA%BF%20HTTT%29/SKILL.md)*
