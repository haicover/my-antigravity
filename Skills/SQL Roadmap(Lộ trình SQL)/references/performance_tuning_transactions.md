# Mastery Chapter: Performance Tuning & Transactions (2026)

In 2026, data volume is massive. Query optimization is the difference between a responsive app and a system crash.

## 1. The Art of Indexing

An index is a pointer to data. Used correctly, it makes lookups `O(log n)`. Used incorrectly, it kills `INSERT` performance.

### Index Types
- **B-Tree (Default)**: Best for equality and range queries (`=`, `<`, `>`).
- **GIN (Generalized Inverted Index)**: Best for full-text search and JSONB.
- **BRIN (Block Range Index)**: Best for very large, naturally ordered tables (e.g., Log timestamps).

### Multi-Column Indexes
The order of columns matters!
- **Rule**: Put the column with highest **Cardinality** (most unique values) or the one used in `=` filters first.

---

## 2. Mastery of EXPLAIN ANALYZE

Don't guess. Ask the database.

- **EXPLAIN**: Shows the plan chosen by the Query Optimizer.
- **EXPLAIN ANALYZE**: Runs the query and shows real timing.

### What to look for:
- **Sequential Scan**: Reading every row. Bad for large tables.
- **Index Scan**: Good. Using the index.
- **Hash Join / Nested Loop**: Understanding how tables are merged.
- **Cost**: The relative resource usage estimation.

---

## 3. Transactions & ACID

The database ensures data is saved reliably via the **ACID** properties:
- **Atomicity**: All or nothing.
- **Consistency**: The DB moves from one valid state to another.
- **Isolation**: Concurrent transactions don't interfere.
- **Durability**: Once saved, it stays saved even after a crash.

### Isolation Levels (The Tradeoffs)
1.  **Read Uncommitted**: Fast, but "Dirty Reads" are possible.
2.  **Read Committed** (Default): Prevents dirty reads.
3.  **Repeatable Read**: Prevents "Non-repeatable reads."
4.  **Serializable**: Total isolation, but slowest (Highest contention).

---

## ⚡ Performance Optimization Checklist
- [ ] Have I checked the Query Execution Plan?
- [ ] Is there an index on my `FOREIGN KEY` columns?
- [ ] Am I avoiding `LIKE '%word%'`? (Use Full-Text Search or Trigrams instead).
- [ ] Have I avoided N+1 queries by joining efficiently?
- [ ] Are my transactions as short as possible?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/SQL%20Roadmap%28L%E1%BB%99%20tr%C3%ACnh%20SQL%29/SKILL.md)*
