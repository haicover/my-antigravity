package com.notex.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.notex.app.data.local.dao.CategoryDao
import com.notex.app.data.local.dao.NoteDao
import com.notex.app.data.local.entity.CategoryEntity
import com.notex.app.data.local.entity.NoteEntity

@Database(
    entities = [NoteEntity::class, CategoryEntity::class],
    version = 1,
    exportSchema = true
)
abstract class NoteXDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
    abstract fun categoryDao(): CategoryDao

    companion object {
        const val DATABASE_NAME = "notex_db"
    }
}
