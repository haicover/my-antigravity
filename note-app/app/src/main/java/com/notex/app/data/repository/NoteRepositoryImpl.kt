package com.notex.app.data.repository

import com.notex.app.data.local.dao.NoteDao
import com.notex.app.data.local.mapper.toDomain
import com.notex.app.data.local.mapper.toEntity
import com.notex.app.data.remote.NoteXApi
import com.notex.app.data.remote.toDto
import com.notex.app.data.remote.toEntity
import com.notex.app.domain.model.Note
import com.notex.app.domain.repository.NoteRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class NoteRepositoryImpl @Inject constructor(
    private val noteDao: NoteDao,
    private val api: NoteXApi
) : NoteRepository {

    override fun getAllNotes(): Flow<List<Note>> =
        noteDao.getAllNotes().map { entities -> entities.map { it.toDomain() } }

    override fun getNotesByCategory(categoryId: String): Flow<List<Note>> =
        noteDao.getNotesByCategory(categoryId).map { entities -> entities.map { it.toDomain() } }

    override fun searchNotes(query: String): Flow<List<Note>> =
        noteDao.searchNotes(query).map { entities -> entities.map { it.toDomain() } }

    override fun getPinnedNotes(): Flow<List<Note>> =
        noteDao.getPinnedNotes().map { entities -> entities.map { it.toDomain() } }

    override fun getArchivedNotes(): Flow<List<Note>> =
        noteDao.getArchivedNotes().map { entities -> entities.map { it.toDomain() } }

    override suspend fun getNoteById(id: String): Note? =
        noteDao.getNoteById(id)?.toDomain()

    override suspend fun insertNote(note: Note) {
        noteDao.insertNote(note.toEntity())
    }

    override suspend fun updateNote(note: Note) {
        noteDao.updateNote(
            note.copy(updatedAt = System.currentTimeMillis(), isSynced = false).toEntity()
        )
    }

    override suspend fun deleteNote(id: String) {
        noteDao.softDeleteNote(id)
    }

    override suspend fun togglePin(id: String) {
        noteDao.togglePin(id)
    }

    override suspend fun toggleArchive(id: String) {
        noteDao.toggleArchive(id)
    }

    override suspend fun syncNotes() {
        try {
            // Upload unsynced local notes
            val unsyncedNotes = noteDao.getUnsyncedNotes()
            if (unsyncedNotes.isNotEmpty()) {
                val response = api.syncNotes(unsyncedNotes.map { it.toDto() })
                if (response.success) {
                    unsyncedNotes.forEach { noteDao.markAsSynced(it.id) }
                }
            }

            // Download remote notes
            val remoteResponse = api.getNotes()
            if (remoteResponse.success && remoteResponse.data != null) {
                val remoteEntities = remoteResponse.data.map { it.toEntity(isSynced = true) }
                noteDao.insertAll(remoteEntities)
            }
        } catch (e: Exception) {
            // Offline mode - sync will retry later
            e.printStackTrace()
        }
    }
}
