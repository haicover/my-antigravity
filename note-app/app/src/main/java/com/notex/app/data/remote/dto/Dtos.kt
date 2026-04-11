package com.notex.app.data.remote.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class NoteDto(
    val id: String,
    @SerialName("user_id") val userId: String,
    @SerialName("category_id") val categoryId: String? = null,
    val title: String,
    val content: String,
    @SerialName("content_format") val contentFormat: String = "rich_text",
    val color: String = "#FFFFFF",
    @SerialName("is_pinned") val isPinned: Boolean = false,
    @SerialName("is_archived") val isArchived: Boolean = false,
    @SerialName("is_deleted") val isDeleted: Boolean = false,
    @SerialName("created_at") val createdAt: Long,
    @SerialName("updated_at") val updatedAt: Long,
    @SerialName("deleted_at") val deletedAt: Long? = null
)

@Serializable
data class CreateNoteRequest(
    val title: String,
    val content: String,
    @SerialName("content_format") val contentFormat: String = "rich_text",
    val color: String = "#FFFFFF",
    @SerialName("category_id") val categoryId: String? = null
)

@Serializable
data class UpdateNoteRequest(
    val title: String? = null,
    val content: String? = null,
    @SerialName("content_format") val contentFormat: String? = null,
    val color: String? = null,
    @SerialName("category_id") val categoryId: String? = null,
    @SerialName("is_pinned") val isPinned: Boolean? = null,
    @SerialName("is_archived") val isArchived: Boolean? = null
)

@Serializable
data class CategoryDto(
    val id: String,
    @SerialName("user_id") val userId: String,
    val name: String,
    val color: String = "#4F46E5",
    @SerialName("created_at") val createdAt: Long
)

@Serializable
data class CreateCategoryRequest(
    val name: String,
    val color: String = "#4F46E5"
)

@Serializable
data class LoginRequest(
    val email: String,
    val password: String
)

@Serializable
data class RegisterRequest(
    val email: String,
    val password: String,
    @SerialName("display_name") val displayName: String
)

@Serializable
data class GoogleAuthRequest(
    @SerialName("id_token") val idToken: String
)

@Serializable
data class AuthResponse(
    val token: String,
    @SerialName("refresh_token") val refreshToken: String,
    val user: UserDto
)

@Serializable
data class UserDto(
    val id: String,
    val email: String,
    @SerialName("display_name") val displayName: String,
    @SerialName("avatar_url") val avatarUrl: String? = null,
    @SerialName("auth_provider") val authProvider: String = "email"
)

@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val message: String? = null
)

@Serializable
data class TokenRefreshRequest(
    @SerialName("refresh_token") val refreshToken: String
)

@Serializable
data class TokenResponse(
    val token: String,
    @SerialName("refresh_token") val refreshToken: String
)
