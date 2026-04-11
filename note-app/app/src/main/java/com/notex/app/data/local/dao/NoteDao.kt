package com.notex.app.data.local.dao

import androidx.room.*
import com.notex.app.data.local.entity.NoteEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface NoteDao {

    @Query("SELECT * FROM notes WHERE is_deleted = 0 AND is_archived = 0 ORDER BY is_pinned DESC, updated_at DESC")
    fun getAllNotes(): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE category_id = :categoryId AND is_deleted = 0 AND is_archived = 0 ORDER BY is_pinned DESC, updated_at DESC")
    fun getNotesByCategory(categoryId: String): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE (title LIKE '%' || :query || '%' OR content LIKE '%' || :query || '%') AND is_deleted = 0 ORDER BY updated_at DESC")
    fun searchNotes(query: String): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE is_pinned = 1 AND is_deleted = 0 ORDER BY updated_at DESC")
    fun getPinnedNotes(): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE is_archived = 1 AND is_deleted = 0 ORDER BY updated_at DESC")
    fun getArchivedNotes(): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE id = :id")
    suspend fun getNoteById(id: String): NoteEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertNote(note: NoteEntity)

    @Update
    suspend fun updateNote(note: NoteEntity)

    @Query("UPDATE notes SET is_deleted = 1, deleted_at = :deletedAt, is_synced = 0 WHERE id = :id")
    suspend fun softDeleteNote(id: String, deletedAt: Long = System.currentTimeMillis())

    @Query("UPDATE notes SET is_pinned = NOT is_pinned, is_synced = 0 WHERE id = :id")
    suspend fun togglePin(id: String)

    @Query("UPDATE notes SET is_archived = NOT is_archived, is_synced = 0 WHERE id = :id")
    suspend fun toggleArchive(id: String)

    @Query("SELECT * FROM notes WHERE is_synced = 0")
    suspend fun getUnsyncedNotes(): List<NoteEntity>

    @Query("UPDATE notes SET is_synced = 1 WHERE id = :id")
    suspend fun markAsSynced(id: String)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(notes: List<NoteEntity>)
}
