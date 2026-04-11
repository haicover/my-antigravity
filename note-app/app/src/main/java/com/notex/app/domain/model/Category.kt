package com.notex.app.domain.model

import java.util.UUID

data class Category(
    val id: String = UUID.randomUUID().toString(),
    val userId: String = "",
    val name: String = "",
    val color: String = "#4F46E5",
    val createdAt: Long = System.currentTimeMillis()
)
