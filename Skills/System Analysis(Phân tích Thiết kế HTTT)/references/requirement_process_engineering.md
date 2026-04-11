# Mastery Chapter: Requirement & Process Engineering (2026)

System analysis starts with empathy and ends with precision. This chapter covers the translation of business chaos into engineering logic.

## 1. Requirements Engineering (The "What")

Requirements are the foundation of any system. If the foundation is cracked, the system will fail.

### SMART Requirements
- **Specific**: "User receives an email" vs. "User sees a message".
- **Measurable**: "Load time < 200ms" vs. "Fast loading".
- **Achievable**: Technically feasible with current tech stack.
- **Relevant**: Solves a legitimate business problem.
- **Time-bound**: Defined within a project scope.

### The 5 Whys Technique
Used to find the root cause of an requirement request.
- *Request*: "We need a faster checkout."
- *Why 1*: Users are dropping off.
- *Why 2*: The form is too long.
- *Why 3*: It asks for address every time.
- *Why 4*: We don't save user profiles.
- *Why 5*: Security concerns about data storage.
- **Result**: Requirement changes from "Faster checkout" to "Encrypted User Profile Storage".

---

## 2. Process Modeling (The "How")

### BPMN 2.0 (Business Process Model and Notation)
The standard for visual communication between business and technical teams.

| Element | Description |
|---------|-------------|
| **Pools/Lanes** | Separates different departments or actors. |
| **Gateways** | Decisions (Exclusive, Parallel, Inclusive). |
| **Events** | Start, Intermediate, End (e.g., Message received, Timer). |

### Data Flow Diagram (DFD)
Focuses on the movement of data between external entities, processes, and stores.

- **Level 0 (Context Diagram)**: The system as a single bubble.
- **Level 1**: Breaking down the main functional areas.
- **Level 2**: Detailed data flows for specific processes.

---

## 📋 Best Practices
- [ ] Always validate requirements with stakeholders twice.
- [ ] Use BPMN 2.0 for strategic workflows; Use Activity Diagrams for detailed logic.
- [ ] Avoid "Scope Creep" by strictly defining what is *out* of scope.
- [ ] Document the "Implicit Requirements" (e.g., Logging, Error handling).

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/System%20Analysis%28Ph%C3%A2n%20t%C3%ADch%20Thi%E1%BA%BFt%20k%E1%BA%BF%20HTTT%29/SKILL.md)*
