# Mastery Chapter: Security & Identity Flows (2026)

Spring Security 6 introduced a modernized, functional approach to securing applications. In 2026, we focus on **Stateless JWT** and **OAuth2/OIDC**.

## 1. Modern Security Configuration (V6+)

We no longer use `WebSecurityConfigurerAdapter`. Everything is configured via `@Bean` and Lambda expressions.

### The Stateless Security Filter Chain
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable)
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults())) // For JWT-based APIs
            .build();
    }
}
```

---

## 2. JWT (JSON Web Token) Integration

In a microservices architecture, JWT is the standard for identity propagation.

### Best Practices for JWT in 2026
- **RS256 (Asymmetric)**: Use public/private keys instead of HS256 (Symmetric) to increase security across service boundaries.
- **Short-lived tokens**: Use Access Tokens with 15-minute expirations and **Refresh Tokens** for renewal.
- **Claims**: Include `roles` and `permissions` in the JWT body to avoid extra DB lookups in downstream services.

---

## 3. Secure Identity Management

### Password Hashing
Spring Security defaults to `BCrypt`, but for 2026, **Argon2** is recommended for its memory-hard resistance to GPU cracking.
```java
@Bean
public PasswordEncoder passwordEncoder() {
    return Argon2PasswordEncoder.defaultsForSpringSecurity_v5_8();
}
```

### Method-Level Security
Secure your Service layer, not just your Controllers.
```java
@Service
public class SalaryService {
    @PreAuthorize("hasRole('HR') or #userId == principal.id")
    public BigDecimal getSalary(Long userId) {
        // ...
    }
}
```

## 🛡️ Security Pro-Tips
1.  **Never** store sensitive data in JWT claims (it's encoded, not encrypted).
2.  **Always** use HTTPS (TLS).
3.  **Disable CSRF** only for truly stateless APIs.
4.  Implement **Rate Limiting** using Spring Cloud Gateway or Redis to prevent Brute Force.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/Spring%20Boot%28L%E1%BA%ADp%20tr%C3%ACnh%20Spring%20Boot%29/SKILL.md)*
