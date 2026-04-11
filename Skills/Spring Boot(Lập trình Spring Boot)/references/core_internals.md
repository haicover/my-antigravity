# Mastery Chapter: Spring Core Internals & Performance (2026)

Mastering the Spring Container is the difference between a "Spring Boot Coder" and a "Java Engineer."

## 1. The Container Mechanics (IoC & DI)

### Constructor Injection (The Gold Standard)
In 2026, we avoid `@Autowired` on fields. Constructor injection ensures **Immutability** and makes **Unit Testing** trivial.
```java
@Service
public class OrderService {
    private final ProductClient productClient;
    // Spring automatically injects this because there is only one constructor
    public OrderService(ProductClient productClient) {
        this.productClient = productClient;
    }
}
```

### Bean Lifecycle & Scopes
Understand when a Bean is created and destroyed:
- **Singleton** (Default): One instance per container.
- **Prototype**: New instance every time it's requested.
- **Request/Session**: Web-scoped beans.

---

## 2. Advanced Performance: Virtual Threads (Loom)

Spring Boot 3.2+ allows you to handle thousands of concurrent requests with minimal RAM using **Virtual Threads**.

### Enabling Virtual Threads
Add this to your `application.yml`:
```yaml
spring:
  threads:
    virtual:
      enabled: true
```
This flag switches the underlying thread pool to use Project Loom. Instead of a 1:1 mapping between Java threads and OS threads (blocking), it uses lightweight threads that are scheduled by the JVM.

---

## 3. Aspect-Oriented Programming (AOP)

Decouple cross-cutting concerns (Logging, Performance Monitoring, Security) from your business logic.

### Custom Annotation Pattern
```java
@Aspect
@Component
public class PerformanceAspect {
    @Around("@annotation(LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object proceed = joinPoint.proceed();
        long executionTime = System.currentTimeMillis() - start;
        System.out.println(joinPoint.getSignature() + " executed in " + executionTime + "ms");
        return proceed;
    }
}
```

## 📝 2026 Core Checklist
- [ ] Use **Constructor Injection** for all dependencies.
- [ ] Keep Beans stateless.
- [ ] Enable **Virtual Threads** for I/O heavy applications.
- [ ] Leverage **Profiles** (`dev`, `prod`, `test`) to manage configurations.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Spring%20Boot%28L%E1%BA%ADp%20tr%C3%ACnh%20Spring%20Boot%29/SKILL.md)*
