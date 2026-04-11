package com.notex.app.data.local.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "categories")
data class CategoryEntity(
    @PrimaryKey
    val id: String,
    @ColumnInfo(name = "user_id")
    val userId: String,
    val name: String,
    val color: String = "#4F46E5",
    @ColumnInfo(name = "created_at")
    val createdAt: Long
)
