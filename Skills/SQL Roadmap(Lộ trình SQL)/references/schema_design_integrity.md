# Mastery Chapter: Schema Design & Data Integrity (2026)

A bad query can be fixed. A bad schema is a life sentence. In 2026, we design for **Performance** and **Multi-tenancy**.

## 1. Normalization (The Science of Cleanup)

The goal is to eliminate redundancy and prevent data anomalies.

- **1NF**: Atomic values. No repeating groups.
- **2NF**: All non-key attributes must depend on the *entire* primary key.
- **3NF**: All attributes must depend *directly* on the primary key (No transitive dependencies).

### Pragmatic De-normalization
In high-performance systems, we sometimes break 3NF to avoid expensive joins.
- **Rule**: Only de-normalize after you have identified a bottleneck and documented the synchronization strategy (e.g., using triggers or application-level logic).

---

## 2. Advanced Integrity: Row-Level Security (RLS)

In modern SaaS applications, we use **RLS** (standard in PostgreSQL) to ensure a user/tenant can only see their own data, even if the query is `SELECT * FROM orders`.

```sql
-- Enabling RLS on a table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Creating a policy: Only owner can see their rows
CREATE POLICY order_isolation_policy ON orders
FOR SELECT USING (user_id = current_setting('app.current_user_id')::UUID);
```

---

## 3. ERD Modeling Best Practices

1.  **Immutability**: Prefer UUIDs over auto-increment IDs for distributed systems.
2.  **Audit Logs**: Every table should have `created_at` and `updated_at` timestamps.
3.  **Naming Convention**: Use `snake_case`. Table names should be **plural** (e.g., `users`, `products`).
4.  **Soft Deletes**: Use a `deleted_at` timestamp instead of deleting rows, to preserve history.

## 🗄️ Design Assessment
- [ ] Is my schema in at least 3NF?
- [ ] Have I handled multi-tenancy correctly?
- [ ] Are all my relationships documented with Foreign Keys?
- [ ] Do I have `updated_at` triggers?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/SQL%20Roadmap%28L%E1%BB%99%20tr%C3%ACnh%20SQL%29/SKILL.md)*
