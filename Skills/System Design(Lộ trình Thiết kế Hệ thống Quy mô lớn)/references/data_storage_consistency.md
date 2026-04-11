# Mastery Chapter: Data Storage & Consistency (2026)

In 2026, data storage is more than just SQL vs. NoSQL. It's about selecting the right specialized engine for the right data model.

## 1. Database Paradigms

| Type | Best For | Example Tech |
|------|----------|--------------|
| **Relational (SQL)** | Structured data, ACID transactions. | PostgreSQL, MySQL. |
| **NoSQL (Document)** | Flexible schema, rapid dev. | MongoDB, DynamoDB. |
| **Key-Value** | Caching, Simple sessions. | Redis, Memcached. |
| **Graph** | Complex relationships (Social nets). | Neo4j. |
| **Vector DB** | AI/LLM context, Embeddings. | Pinecone, Milvus, Weaviate. |

---

## 2. Scaling Data

As traffic grows, a single database instance will eventually become a bottleneck.

### Replication
Copying data to multiple servers to improve availability and read performance.
- **Leader-Follower**: Write to leader, read from followers.
- **Multi-Leader**: Multiple nodes handle writes (complex conflict resolution).

### Sharding (Horizontal Partitioning)
Breaking a large database into smaller, faster, more easily managed parts called shards.
- **Key-based**: Hashing a key (e.g., UserID).
- **Directory-based**: Using a lookup service to find data location.

---

## 3. Consistency Models

- **Strong Consistency**: After a write, every subsequent read will see that write. (CP system).
- **Eventual Consistency**: After a write, the system will eventually converge to the same value across all nodes. (AP system).
- **Read-Your-Writes**: A user will always see the data they just wrote, even if others don't yet.

---

## 🏗️ Storage Checklist
- [ ] Have I selected the right DB for the data access pattern (Read-heavy vs. Write-heavy)?
- [ ] Is the Sharding Key distributed evenly (Avoid "hot partitions")?
- [ ] How do we handle double-writes in a distributed environment?
- [ ] Are we using Caching properly to shield the DB from massive read traffic?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/System%20Design%28L%E1%BB%99%20tr%C3%ACnh%20Thi%E1%BA%BFt%20k%E1%BA%BF%20H%E1%BB%87%20th%E1%BB%91ng%20Quy%20m%C3%B4%20l%E1%BB%9Bn%29/SKILL.md)*
