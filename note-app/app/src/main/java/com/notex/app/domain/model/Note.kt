package com.notex.app.domain.model

import java.util.UUID

data class Note(
    val id: String = UUID.randomUUID().toString(),
    val userId: String = "",
    val categoryId: String? = null,
    val title: String = "",
    val content: String = "",
    val contentFormat: String = "rich_text",
    val color: String = "#FFFFFF",
    val isPinned: Boolean = false,
    val isArchived: Boolean = false,
    val isDeleted: Boolean = false,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis(),
    val deletedAt: Long? = null,
    val isSynced: Boolean = false
)
