package com.notex.app.data.remote

import com.notex.app.data.local.entity.CategoryEntity
import com.notex.app.data.local.entity.NoteEntity
import com.notex.app.data.remote.dto.CategoryDto
import com.notex.app.data.remote.dto.NoteDto
import com.notex.app.domain.model.User
import com.notex.app.data.remote.dto.UserDto

// ── Note DTO ↔ Entity ─────────────────────────
fun NoteDto.toEntity(isSynced: Boolean = true): NoteEntity = NoteEntity(
    id = id,
    userId = userId,
    categoryId = categoryId,
    title = title,
    content = content,
    contentFormat = contentFormat,
    color = color,
    isPinned = isPinned,
    isArchived = isArchived,
    isDeleted = isDeleted,
    createdAt = createdAt,
    updatedAt = updatedAt,
    deletedAt = deletedAt,
    isSynced = isSynced
)

fun NoteEntity.toDto(): NoteDto = NoteDto(
    id = id,
    userId = userId,
    categoryId = categoryId,
    title = title,
    content = content,
    contentFormat = contentFormat,
    color = color,
    isPinned = isPinned,
    isArchived = isArchived,
    isDeleted = isDeleted,
    createdAt = createdAt,
    updatedAt = updatedAt,
    deletedAt = deletedAt
)

// ── Category DTO ↔ Entity ─────────────────────
fun CategoryDto.toEntity(): CategoryEntity = CategoryEntity(
    id = id,
    userId = userId,
    name = name,
    color = color,
    createdAt = createdAt
)

// ── User DTO → Domain ─────────────────────────
fun UserDto.toDomain(token: String? = null): User = User(
    id = id,
    email = email,
    displayName = displayName,
    avatarUrl = avatarUrl,
    authProvider = authProvider,
    token = token
)
