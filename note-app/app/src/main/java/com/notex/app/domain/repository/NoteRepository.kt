package com.notex.app.domain.repository

import com.notex.app.domain.model.Note
import kotlinx.coroutines.flow.Flow

interface NoteRepository {
    fun getAllNotes(): Flow<List<Note>>
    fun getNotesByCategory(categoryId: String): Flow<List<Note>>
    fun searchNotes(query: String): Flow<List<Note>>
    fun getPinnedNotes(): Flow<List<Note>>
    fun getArchivedNotes(): Flow<List<Note>>
    suspend fun getNoteById(id: String): Note?
    suspend fun insertNote(note: Note)
    suspend fun updateNote(note: Note)
    suspend fun deleteNote(id: String)
    suspend fun togglePin(id: String)
    suspend fun toggleArchive(id: String)
    suspend fun syncNotes()
}
