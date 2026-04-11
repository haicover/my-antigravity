package com.notex.app.domain.repository

import com.notex.app.domain.model.User

interface AuthRepository {
    suspend fun login(email: String, password: String): Result<User>
    suspend fun register(email: String, password: String, displayName: String): Result<User>
    suspend fun loginWithGoogle(idToken: String): Result<User>
    suspend fun refreshToken(): Result<String>
    suspend fun logout()
    suspend fun getCurrentUser(): User?
    suspend fun isLoggedIn(): Boolean
}
