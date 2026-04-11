# Mastery Chapter: Advanced Analytical SQL (2026)

Analytical SQL is where the database stops being a "bucket of rows" and starts being an "engine for insights."

## 1. Window Functions (The Powerhouse)

Window functions perform a calculation across a set of table rows that are somehow related to the current row.

### Core Syntax
`FUNCTION() OVER (PARTITION BY ... ORDER BY ...)`

### Top 3 Most Used Functions
1.  **ROW_NUMBER() / RANK()**: Ranking items within a category (e.g., Top 5 customers per country).
2.  **LEAD() / LAG()**: Accessing the next or previous row (e.g., Calculating Month-over-Month growth).
3.  **SUM() OVER**: Running totals.

```sql
-- Running total of sales per product
SELECT product_id, sale_date, amount,
       SUM(amount) OVER (PARTITION BY product_id ORDER BY sale_date) as running_total
FROM sales;
```

---

## 2. Common Table Expressions (CTE)

CTEs make complex queries readable and maintainable.

### Recursive CTEs
Used for hierarchical data like organizational charts or bill-of-materials.
```sql
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id FROM employees WHERE id = 1  -- Root
    UNION ALL
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    INNER JOIN subordinates s ON s.id = e.manager_id
)
SELECT * FROM subordinates;
```

---

## 3. Semi-Structured Data: JSONB (PostgreSQL)

In 2026, many relational tables contain a JSONB column for flexibility.

- **Storage**: Binary format, indexed, fast.
- **Queries**: Use the `->>` (extract text) or `@>` (contains) operators.
```sql
-- Finding users with a specific tag in a JSONB column
SELECT * FROM users WHERE metadata @> '{"tags": ["premium"]}';
```

## 📊 Analytical Checklist
- [ ] Am I using Window Functions instead of slow self-joins?
- [ ] Are my CTE names descriptive (Business-focused)?
- [ ] Am I avoiding `SELECT *` inside my CTEs?
- [ ] Do I know when to use `RANK()` vs `DENSE_RANK()`?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/SQL%20Roadmap%28L%E1%BB%99%20tr%C3%ACnh%20SQL%29/SKILL.md)*
