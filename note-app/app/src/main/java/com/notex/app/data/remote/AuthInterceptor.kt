package com.notex.app.data.remote

import kotlinx.coroutines.runBlocking
import okhttp3.Interceptor
import okhttp3.Response
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()

        // Skip auth for login/register endpoints
        val path = originalRequest.url.encodedPath
        if (path.contains("/auth/login") ||
            path.contains("/auth/register") ||
            path.contains("/auth/google") ||
            path.contains("/health")
        ) {
            return chain.proceed(originalRequest)
        }

        val token = runBlocking { tokenManager.getAccessToken() }

        val authenticatedRequest = if (token != null) {
            originalRequest.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            originalRequest
        }

        return chain.proceed(authenticatedRequest)
    }
}
