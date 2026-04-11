# Mastery Chapter: Data Persistence & Web API (2026)

Building robust data layers and elegant APIs is the cornerstone of Spring Boot development.

## 1. Spring Data JPA Mastery

The most common trap in Spring development is the **N+1 Query Problem**.

### Solving N+1 with EntityGraphs
Instead of multiple queries, fetch all associations in a single SQL operation.
```java
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    @EntityGraph(attributePaths = {"items", "customer"})
    List<Order> findAllWithDetails();
}
```

### Transaction Management
Use `@Transactional(readOnly = true)` for query methods to optimize Hibernate performance by disabling dirty checking.

### Projections for Performance
Don't fetch whole entities when you only need a few fields. Use **DTO Projections**.
```java
public interface OrderSummary {
    String getOrderNumber();
    BigDecimal getTotal();
}
```

---

## 2. Advanced Web API Design

### Global Exception Handling
Clean APIs don't leak stack traces. Use `@RestControllerAdvice`.
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    }
}
```
*Note: Use Spring 3+ `ProblemDetail` (RFC 7807) for standardized error responses.*

### Bean Validation (JSR 303)
Enforce data integrity at the Controller level using `@Valid`.
```java
public record CreateUserRequest(
    @NotBlank String username,
    @Email String email,
    @Size(min = 8) String password
) {}
```

---

## 3. Best Practices (Web & Data)
1.  **Immutability**: Use **Java Records** for DTOs and Request bodies.
2.  **Pagination**: Never return all records. Always use `Pageable`.
3.  **HATEOAS**: Consider using Spring HATEOAS for self-describing APIs.
4.  **OpenAPI**: Document everything using `springdoc-openapi` (Swagger).

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Spring%20Boot%28L%E1%BA%ADp%20tr%C3%ACnh%20Spring%20Boot%29/SKILL.md)*
