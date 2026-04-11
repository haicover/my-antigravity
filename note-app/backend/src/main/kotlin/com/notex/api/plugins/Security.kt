package com.notex.api.plugins

import com.auth0.jwt.JWT
import com.auth0.jwt.algorithms.Algorithm
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.auth.*
import io.ktor.server.auth.jwt.*
import io.ktor.server.response.*
import java.util.*

object JwtConfig {
    val secret: String = System.getenv("JWT_SECRET") ?: "notex-dev-secret-key-change-in-production"
    val issuer: String = System.getenv("JWT_ISSUER") ?: "notex-api"
    val audience: String = System.getenv("JWT_AUDIENCE") ?: "notex-app"
    private val algorithm = Algorithm.HMAC256(secret)
    private val accessTokenExpiry = 24 * 60 * 60 * 1000L // 24 hours
    private val refreshTokenExpiry = 30 * 24 * 60 * 60 * 1000L // 30 days

    fun generateAccessToken(userId: String, email: String): String = JWT.create()
        .withIssuer(issuer)
        .withAudience(audience)
        .withClaim("user_id", userId)
        .withClaim("email", email)
        .withExpiresAt(Date(System.currentTimeMillis() + accessTokenExpiry))
        .sign(algorithm)

    fun generateRefreshToken(userId: String): String = JWT.create()
        .withIssuer(issuer)
        .withAudience(audience)
        .withClaim("user_id", userId)
        .withClaim("type", "refresh")
        .withExpiresAt(Date(System.currentTimeMillis() + refreshTokenExpiry))
        .sign(algorithm)

    fun getVerifier() = JWT.require(algorithm)
        .withIssuer(issuer)
        .withAudience(audience)
        .build()
}

fun Application.configureSecurity() {
    install(Authentication) {
        jwt("auth-jwt") {
            verifier(JwtConfig.getVerifier())
            validate { credential ->
                val userId = credential.payload.getClaim("user_id").asString()
                val type = credential.payload.getClaim("type")?.asString()
                if (userId != null && type == null) {
                    JWTPrincipal(credential.payload)
                } else null
            }
            challenge { _, _ ->
                call.respond(HttpStatusCode.Unauthorized, mapOf("message" to "Token expired or invalid"))
            }
        }
    }
}

fun JWTPrincipal.getUserId(): String =
    payload.getClaim("user_id").asString()
