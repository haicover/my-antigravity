# Mastery Chapter: Fundamentals & Trade-offs (2026)

System design is the art of making the right trade-offs. There is no "best" design, only the best design for a specific set of constraints.

## 1. The Core Laws

### CAP Theorem
In a distributed system, you can only pick two of these three:
- **Consistency**: Every read receives the most recent write or an error.
- **Availability**: Every request receives a (non-error) response.
- **Partition Tolerance**: The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network.

### PACELC Theorem
A refinement of CAP:
- If there is a **P**artition, how do you trade off **A**vailability and **C**onsistency?
- **E**lse (no partition), how do you trade off **L**atency and **C**onsistency?

---

## 2. Networking & Traffic Management

### Load Balancing
Distributing incoming network traffic across multiple servers.
- **Layer 4 (Transport)**: Basic (IP and TCP port).
- **Layer 7 (Application)**: Advanced (HTTP headers, Cookies, Path).
- **Consistent Hashing**: A technique to minimize reshuffling when a server is added or removed from a cluster.

### Content Delivery Network (CDN)
A geographically distributed group of servers which work together to provide fast delivery of Internet content.
- **Push vs. Pull**: Pull (Cache on demand) vs. Push (Pre-load content).

---

## 3. Performance Metrics

| Metric | Definition | Goal |
|--------|------------|------|
| **Latency** | Time taken for a single request. | Minimize (e.g., < 100ms) |
| **Throughput** | Number of requests handled per second (QPS/RPS). | Maximize |
| **Availability** | The "Nines" (e.g., 99.99% uptime). | High reliability |

## 📐 Trade-off Checklist
- [ ] Are we prioritizing Read performance or Write performance?
- [ ] Is strong consistency required, or is Eventual Consistency acceptable?
- [ ] What is the cost of a 1-second delay in our system?
- [ ] How does the system handle an 10x sudden increase in traffic?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/System%20Design%28L%E1%BB%99%20tr%C3%ACnh%20Thi%E1%BA%BFt%20k%E1%BA%BF%20H%E1%BB%87%20th%E1%BB%91ng%20Quy%20m%C3%B4%20l%E1%BB%9Bn%29/SKILL.md)*
