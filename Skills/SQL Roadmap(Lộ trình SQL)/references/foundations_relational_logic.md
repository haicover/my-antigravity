# Mastery Chapter: SQL Foundations & Relational Logic (2026)

SQL is a declarative language based on **Set Theory**. To master SQL, you must stop thinking in "loops" and start thinking in "sets."

## 1. The Real Order of Execution
SQL code is written in one order but executed by the RDBMS in another. Understanding this is critical for debugging and optimization.

1.  **FROM / JOIN**: Database identifies the tables and combines them.
2.  **WHERE**: Filters rows based on conditions.
3.  **GROUP BY**: Groups filtered rows into buckets.
4.  **HAVING**: Filters the buckets/groups.
5.  **SELECT**: Selects columns and calculated values.
6.  **ORDER BY**: Sorts the results.
7.  **LIMIT / OFFSET**: Clips the result set.

---

## 2. Mastery of JOINs

Think of tables as Circles in a Venn Diagram.

### Inner Join (Intersection)
Only returns rows that have matches in both tables.
```sql
SELECT orders.id, customers.name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```

### Left Join (The Default for Safety)
Returns all rows from the left table, and matching rows from the right. If no match, returns `NULL`.
- **Use case**: Finding "Customers who have never placed an order." 
- `WHERE orders.id IS NULL`

### Self Join
Joining a table to itself.
- **Use case**: Finding connections in a hierarchy (e.g., Employees and their Managers).

---

## 3. Data Integrity & Constraints

The database is the "Source of Truth." Use constraints to enforce rules at the lowest level.

- **Primary Key**: Unique identifier.
- **Foreign Key**: Ensures a value in one table exists in another (Referential Integrity).
- **Check Constraint**: `CHECK (age >= 18)` - Enforces business rules in the schema.
- **Not Null**: Prevents empty fields where data is mandatory.

## 📝 Foundations Checklist
- [ ] Do I understand the difference between `WHERE` and `HAVING`?
- [ ] Can I visualize a `LEFT JOIN` without a diagram?
- [ ] Am I using explicit names for my constraints?
- [ ] Do I know when to use `UNION ALL` vs `UNION`? (Answer: Always prefer `ALL` unless you truly need distinct values, for performance).

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/SQL%20Roadmap%28L%E1%BB%99%20tr%C3%ACnh%20SQL%29/SKILL.md)*
