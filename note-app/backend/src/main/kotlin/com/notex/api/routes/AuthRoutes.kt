package com.notex.api.routes

import at.favre.lib.crypto.bcrypt.BCrypt
import com.auth0.jwt.JWT
import com.notex.api.models.*
import com.notex.api.models.db.Users
import com.notex.api.plugins.JwtConfig
import io.ktor.http.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import java.time.Instant
import java.util.*

fun Route.authRoutes() {
    route("/api/v1/auth") {

        post("/register") {
            val request = call.receive<RegisterRequest>()

            if (request.email.isBlank() || request.password.isBlank() || request.displayName.isBlank()) {
                call.respond(HttpStatusCode.BadRequest, ApiResponse<Unit>(false, message = "All fields are required"))
                return@post
            }

            if (request.password.length < 6) {
                call.respond(HttpStatusCode.BadRequest, ApiResponse<Unit>(false, message = "Password must be at least 6 characters"))
                return@post
            }

            val existingUser = transaction { Users.selectAll().where { Users.email eq request.email }.firstOrNull() }
            if (existingUser != null) {
                call.respond(HttpStatusCode.Conflict, ApiResponse<Unit>(false, message = "Email already registered"))
                return@post
            }

            val userId = UUID.randomUUID().toString()
            val hashedPassword = BCrypt.withDefaults().hashToString(12, request.password.toCharArray())
            val now = Instant.now()

            transaction {
                Users.insert {
                    it[id] = userId
                    it[email] = request.email
                    it[passwordHash] = hashedPassword
                    it[displayName] = request.displayName
                    it[authProvider] = "email"
                    it[createdAt] = now
                    it[updatedAt] = now
                }
            }

            val token = JwtConfig.generateAccessToken(userId, request.email)
            val refreshToken = JwtConfig.generateRefreshToken(userId)

            call.respond(HttpStatusCode.Created, ApiResponse(
                success = true,
                data = AuthResponse(
                    token = token,
                    refreshToken = refreshToken,
                    user = UserDto(userId, request.email, request.displayName)
                )
            ))
        }

        post("/login") {
            val request = call.receive<LoginRequest>()

            val user = transaction {
                Users.selectAll().where { Users.email eq request.email }.firstOrNull()
            }

            if (user == null) {
                call.respond(HttpStatusCode.Unauthorized, ApiResponse<Unit>(false, message = "Invalid credentials"))
                return@post
            }

            val result = BCrypt.verifyer().verify(request.password.toCharArray(), user[Users.passwordHash])
            if (!result.verified) {
                call.respond(HttpStatusCode.Unauthorized, ApiResponse<Unit>(false, message = "Invalid credentials"))
                return@post
            }

            val token = JwtConfig.generateAccessToken(user[Users.id], user[Users.email])
            val refreshToken = JwtConfig.generateRefreshToken(user[Users.id])

            call.respond(ApiResponse(
                success = true,
                data = AuthResponse(
                    token = token,
                    refreshToken = refreshToken,
                    user = UserDto(
                        id = user[Users.id],
                        email = user[Users.email],
                        displayName = user[Users.displayName],
                        avatarUrl = user[Users.avatarUrl],
                        authProvider = user[Users.authProvider]
                    )
                )
            ))
        }

        post("/google") {
            val request = call.receive<GoogleAuthRequest>()

            // Decode Google ID token to get user info
            // In production, verify with Google's API
            val decoded = try {
                JWT.decode(request.idToken)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.BadRequest, ApiResponse<Unit>(false, message = "Invalid Google token"))
                return@post
            }

            val googleEmail = decoded.getClaim("email")?.asString() ?: ""
            val googleName = decoded.getClaim("name")?.asString() ?: "User"
            val googleAvatar = decoded.getClaim("picture")?.asString()
            val googleId = decoded.subject ?: ""

            // Find or create user
            val existingUser = transaction {
                Users.selectAll().where { Users.email eq googleEmail }.firstOrNull()
            }

            val userId: String
            if (existingUser != null) {
                userId = existingUser[Users.id]
                transaction {
                    Users.update({ Users.id eq userId }) {
                        it[googleId] = googleId
                        it[avatarUrl] = googleAvatar
                        it[updatedAt] = Instant.now()
                    }
                }
            } else {
                userId = UUID.randomUUID().toString()
                transaction {
                    Users.insert {
                        it[id] = userId
                        it[email] = googleEmail
                        it[displayName] = googleName
                        it[avatarUrl] = googleAvatar
                        it[authProvider] = "google"
                        it[Users.googleId] = googleId
                        it[createdAt] = Instant.now()
                        it[updatedAt] = Instant.now()
                    }
                }
            }

            val token = JwtConfig.generateAccessToken(userId, googleEmail)
            val refreshToken = JwtConfig.generateRefreshToken(userId)

            call.respond(ApiResponse(
                success = true,
                data = AuthResponse(
                    token = token,
                    refreshToken = refreshToken,
                    user = UserDto(userId, googleEmail, googleName, googleAvatar, "google")
                )
            ))
        }

        post("/refresh") {
            val request = call.receive<TokenRefreshRequest>()
            try {
                val decoded = JwtConfig.getVerifier().verify(request.refreshToken)
                val userId = decoded.getClaim("user_id").asString()
                val type = decoded.getClaim("type").asString()

                if (type != "refresh") {
                    call.respond(HttpStatusCode.BadRequest, ApiResponse<Unit>(false, message = "Invalid token type"))
                    return@post
                }

                val user = transaction { Users.selectAll().where { Users.id eq userId }.firstOrNull() }
                if (user == null) {
                    call.respond(HttpStatusCode.Unauthorized, ApiResponse<Unit>(false, message = "User not found"))
                    return@post
                }

                val newToken = JwtConfig.generateAccessToken(userId, user[Users.email])
                val newRefreshToken = JwtConfig.generateRefreshToken(userId)

                call.respond(ApiResponse(
                    success = true,
                    data = TokenResponse(newToken, newRefreshToken)
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.Unauthorized, ApiResponse<Unit>(false, message = "Invalid refresh token"))
            }
        }
    }
}
