# Mastery Chapter: Microservices & Messaging (2026)

In 2026, systems are distributed by default. Success depends on how well these distributed components talk to each other.

## 1. Microservices Architecture Patterns

Converting a Monolith into Microservices requires solving new challenges:
- **Service Discovery**: How services find each other (Consul, Eureka).
- **Circuit Breaker**: Preventing a single failed service from cascading (Resilience4j).
- **API Gateway**: A single entry point for clients (Kong, AWS API Gateway).
- **Sidecar Pattern**: Offloading infrastructure tasks (logging, security) to a helper container (Istio/Envoy).

---

## 2. Communication Protocols

| Protocol | Type | Best For | Pros/Cons |
|----------|------|----------|-----------|
| **REST** | Sync | Public APIs, Browser comms. | Simple, widely used / Text-based (slow). |
| **gRPC** | Sync | Inter-service comms. | Binary (fast), strongly typed / Hard to debug. |
| **Messaging** | Async | De-coupling, long-running tasks. | High throughput / Eventual consistency. |
| **WebSockets** | Real-time | Chat, Notifications. | Bi-directional / Hard to scale. |

---

## 3. The Power of Asynchronous Messaging

### Why use Message Queues (Kafka, RabbitMQ, SQS)?
1. **Decoupling**: Producer doesn't need to know who the Consumer is.
2. **Buffering**: Handle traffic spikes by queueing requests.
3. **Resilience**: If a consumer is down, the message stays in the queue until it's back.

### The Saga Pattern (Distributed Transactions)
Since we can't use traditional DB transactions across services, we use Sagas:
- **Choreography**: Each service produces an event that triggers the next service.
- **Orchestration**: A central manager tells each service what to do.
- **Compensating Transactions**: If Step 3 fails, triggers a "Rollback" action in Steps 1 and 2.

---

## 🚀 Design Checklist
- [ ] Is my service "Bounded Context" well-defined?
- [ ] Have I implemented Retries and Timeouts for every network call?
- [ ] Am I using Asynchronous messaging for non-critical paths?
- [ ] Does my system handle "Idempotency" (processing the same message twice safely)?

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/System%20Design%28L%E1%BB%99%20tr%C3%ACnh%20Thi%E1%BA%BFt%20k%E1%BA%BF%20H%E1%BB%87%20th%E1%BB%91ng%20Quy%20m%C3%B4%20l%E1%BB%9Bn%29/SKILL.md)*
