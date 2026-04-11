package com.notex.app.domain.model

data class User(
    val id: String = "",
    val email: String = "",
    val displayName: String = "",
    val avatarUrl: String? = null,
    val authProvider: String = "email",
    val token: String? = null
)
