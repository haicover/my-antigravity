package com.notex.app.data.repository

import com.notex.app.data.remote.NoteXApi
import com.notex.app.data.remote.TokenManager
import com.notex.app.data.remote.dto.GoogleAuthRequest
import com.notex.app.data.remote.dto.LoginRequest
import com.notex.app.data.remote.dto.RegisterRequest
import com.notex.app.data.remote.dto.TokenRefreshRequest
import com.notex.app.data.remote.toDomain
import com.notex.app.domain.model.User
import com.notex.app.domain.repository.AuthRepository
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val api: NoteXApi,
    private val tokenManager: TokenManager
) : AuthRepository {

    override suspend fun login(email: String, password: String): Result<User> {
        return try {
            val response = api.login(LoginRequest(email, password))
            if (response.success && response.data != null) {
                val authData = response.data
                tokenManager.saveTokens(authData.token, authData.refreshToken)
                tokenManager.saveUser(
                    id = authData.user.id,
                    email = authData.user.email,
                    name = authData.user.displayName,
                    avatar = authData.user.avatarUrl,
                    provider = authData.user.authProvider
                )
                Result.success(authData.user.toDomain(authData.token))
            } else {
                Result.failure(Exception(response.message ?: "Login failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun register(
        email: String,
        password: String,
        displayName: String
    ): Result<User> {
        return try {
            val response = api.register(RegisterRequest(email, password, displayName))
            if (response.success && response.data != null) {
                val authData = response.data
                tokenManager.saveTokens(authData.token, authData.refreshToken)
                tokenManager.saveUser(
                    id = authData.user.id,
                    email = authData.user.email,
                    name = authData.user.displayName,
                    avatar = authData.user.avatarUrl,
                    provider = authData.user.authProvider
                )
                Result.success(authData.user.toDomain(authData.token))
            } else {
                Result.failure(Exception(response.message ?: "Registration failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun loginWithGoogle(idToken: String): Result<User> {
        return try {
            val response = api.loginWithGoogle(GoogleAuthRequest(idToken))
            if (response.success && response.data != null) {
                val authData = response.data
                tokenManager.saveTokens(authData.token, authData.refreshToken)
                tokenManager.saveUser(
                    id = authData.user.id,
                    email = authData.user.email,
                    name = authData.user.displayName,
                    avatar = authData.user.avatarUrl,
                    provider = "google"
                )
                Result.success(authData.user.toDomain(authData.token))
            } else {
                Result.failure(Exception(response.message ?: "Google login failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun refreshToken(): Result<String> {
        return try {
            val refreshToken = tokenManager.getRefreshToken()
                ?: return Result.failure(Exception("No refresh token"))
            val response = api.refreshToken(TokenRefreshRequest(refreshToken))
            if (response.success && response.data != null) {
                tokenManager.saveTokens(response.data.token, response.data.refreshToken)
                Result.success(response.data.token)
            } else {
                Result.failure(Exception("Token refresh failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun logout() {
        tokenManager.clearAll()
    }

    override suspend fun getCurrentUser(): User? {
        val id = tokenManager.getUserId() ?: return null
        val email = tokenManager.getUserEmail() ?: return null
        val name = tokenManager.getUserName() ?: return null
        return User(
            id = id,
            email = email,
            displayName = name,
            avatarUrl = tokenManager.getUserAvatar(),
            authProvider = tokenManager.getAuthProvider() ?: "email",
            token = tokenManager.getAccessToken()
        )
    }

    override suspend fun isLoggedIn(): Boolean = tokenManager.isLoggedIn()
}
