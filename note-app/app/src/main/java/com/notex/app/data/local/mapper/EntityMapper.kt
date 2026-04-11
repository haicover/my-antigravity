package com.notex.app.data.local.mapper

import com.notex.app.data.local.entity.CategoryEntity
import com.notex.app.data.local.entity.NoteEntity
import com.notex.app.domain.model.Category
import com.notex.app.domain.model.Note

fun NoteEntity.toDomain(): Note = Note(
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

fun Note.toEntity(): NoteEntity = NoteEntity(
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

fun CategoryEntity.toDomain(): Category = Category(
    id = id,
    userId = userId,
    name = name,
    color = color,
    createdAt = createdAt
)

fun Category.toEntity(): CategoryEntity = CategoryEntity(
    id = id,
    userId = userId,
    name = name,
    color = color,
    createdAt = createdAt
)
