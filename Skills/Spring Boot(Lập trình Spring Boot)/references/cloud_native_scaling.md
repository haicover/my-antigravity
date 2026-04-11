# Mastery Chapter: Cloud Native & Scaling (2026)

In 2026, Spring Boot is lean, fast, and optimized for the Cloud using **GraalVM Native Image** and **Event-Driven Architectures**.

## 1. Spring Native (GraalVM)

Transform your Spring Boot app into a standalone executable that starts in milliseconds.

### Benefits of Native Images
- **Startup Time**: ~0.05s vs ~5-15s (JVM).
- **RAM Footprint**: ~50-80MB vs ~300-500MB (JVM).
- **Ideal for**: Serverless (AWS Lambda), Scale-to-zero K8s pods.

### Building a Native Image
Use the `native` profile and your build tool (Maven/Gradle):
```bash
./mvnw native:compile -Pnative
```
*Note: Some libraries require **Hinting** to support reflection in the native environment.*

---

## 2. Event-Driven Architecture (Messaging)

Decouple services using asynchronous messaging.

### Spring for Apache Kafka
```java
@Service
public class NotificationProducer {
    private final KafkaTemplate<String, String> kafkaTemplate;

    public void sendMessage(String topic, String message) {
        kafkaTemplate.send(topic, message);
    }
}

@Service
public class NotificationConsumer {
    @KafkaListener(topics = "order-placed", groupId = "notifications")
    public void listen(String message) {
        // Process message
    }
}
```

---

## 3. Microservice Orchestration (Spring Cloud)

Managing a fleet of services requires robust infrastructure patterns.

### The Spring Cloud 2026 Stack
- **Spring Cloud Gateway**: The entry point. Handles rate limiting, filtering, and routing.
- **Config Server**: Centralized configuration management via Git.
- **Service Discovery (Eureka/Consul)**: Keeping track of service instances.
- **OpenFeign**: Declarative REST clients for inter-service communication.
- **Resilience4j**: Circuit breakers, retries, and rate limiting.

---

## ☁️ Cloud Native Best Practices
1.  **Twelve-Factor App**: Follow the 12-factor methodology for cloud apps.
2.  **Graceful Shutdown**: Ensure your app handles termination signals correctly for K8s.
    - Set `server.shutdown=graceful` in `application.yml`.
3.  **Liveness & Readiness**: Use **Spring Actuator** health endpoints to inform K8s of pod status.
4.  **Distributed Tracing**: Use **Micrometer Tracing** with OpenTelemetry collectors.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Spring%20Boot%28L%E1%BA%ADp%20tr%C3%ACnh%20Spring%20Boot%29/SKILL.md)*
