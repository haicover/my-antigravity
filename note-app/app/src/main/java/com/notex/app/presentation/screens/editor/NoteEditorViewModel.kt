package com.notex.app.presentation.screens.editor

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.notex.app.data.remote.TokenManager
import com.notex.app.domain.model.Note
import com.notex.app.domain.repository.NoteRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class EditorUiState(
    val note: Note? = null,
    val isNew: Boolean = true,
    val isSaved: Boolean = false,
    val isLoading: Boolean = false
)

@HiltViewModel
class NoteEditorViewModel @Inject constructor(
    private val noteRepository: NoteRepository,
    private val tokenManager: TokenManager
) : ViewModel() {

    private val _uiState = MutableStateFlow(EditorUiState())
    val uiState: StateFlow<EditorUiState> = _uiState

    fun loadNote(noteId: String?) {
        if (noteId == null) {
            viewModelScope.launch {
                val userId = tokenManager.getUserId() ?: ""
                _uiState.update {
                    it.copy(
                        note = Note(userId = userId),
                        isNew = true,
                        isLoading = false
                    )
                }
            }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            val note = noteRepository.getNoteById(noteId)
            _uiState.update {
                it.copy(
                    note = note ?: Note(),
                    isNew = note == null,
                    isLoading = false
                )
            }
        }
    }

    fun updateTitle(title: String) {
        _uiState.update { it.copy(note = it.note?.copy(title = title)) }
    }

    fun updateContent(content: String) {
        _uiState.update { it.copy(note = it.note?.copy(content = content)) }
    }

    fun updateColor(color: String) {
        _uiState.update { it.copy(note = it.note?.copy(color = color)) }
    }

    fun updateCategory(categoryId: String?) {
        _uiState.update { it.copy(note = it.note?.copy(categoryId = categoryId)) }
    }

    fun togglePin() {
        _uiState.update { it.copy(note = it.note?.copy(isPinned = !(it.note.isPinned))) }
    }

    fun saveNote() {
        val note = _uiState.value.note ?: return
        if (note.title.isBlank() && note.content.isBlank()) return

        viewModelScope.launch {
            val updatedNote = note.copy(updatedAt = System.currentTimeMillis())
            if (_uiState.value.isNew) {
                noteRepository.insertNote(updatedNote)
            } else {
                noteRepository.updateNote(updatedNote)
            }
            _uiState.update { it.copy(isSaved = true) }
        }
    }

    fun deleteNote() {
        val note = _uiState.value.note ?: return
        viewModelScope.launch {
            noteRepository.deleteNote(note.id)
            _uiState.update { it.copy(isSaved = true) }
        }
    }
}
