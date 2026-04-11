package com.notex.api.models.db

import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.javatime.timestamp

object Users : Table("users") {
    val id = varchar("id", 36)
    val email = varchar("email", 255).uniqueIndex()
    val passwordHash = varchar("password_hash", 255).default("")
    val displayName = varchar("display_name", 255)
    val avatarUrl = varchar("avatar_url", 500).nullable()
    val authProvider = varchar("auth_provider", 20).default("email")
    val googleId = varchar("google_id", 255).nullable()
    val createdAt = timestamp("created_at")
    val updatedAt = timestamp("updated_at")

    override val primaryKey = PrimaryKey(id)
}

object Notes : Table("notes") {
    val id = varchar("id", 36)
    val userId = varchar("user_id", 36).references(Users.id)
    val categoryId = varchar("category_id", 36).references(Categories.id).nullable()
    val title = varchar("title", 500).default("")
    val content = text("content").default("")
    val contentFormat = varchar("content_format", 50).default("rich_text")
    val color = varchar("color", 20).default("#FFFFFF")
    val isPinned = bool("is_pinned").default(false)
    val isArchived = bool("is_archived").default(false)
    val isDeleted = bool("is_deleted").default(false)
    val createdAt = timestamp("created_at")
    val updatedAt = timestamp("updated_at")
    val deletedAt = timestamp("deleted_at").nullable()

    override val primaryKey = PrimaryKey(id)
}

object Categories : Table("categories") {
    val id = varchar("id", 36)
    val userId = varchar("user_id", 36).references(Users.id)
    val name = varchar("name", 100)
    val color = varchar("color", 20).default("#4F46E5")
    val createdAt = timestamp("created_at")

    override val primaryKey = PrimaryKey(id)
}
