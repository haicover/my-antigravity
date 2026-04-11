package com.notex.app.presentation.screens.notes

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.notex.app.domain.model.Note
import com.notex.app.domain.repository.NoteRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class NoteListUiState(
    val notes: List<Note> = emptyList(),
    val isLoading: Boolean = true,
    val searchQuery: String = "",
    val selectedCategoryId: String? = null,
    val isGridView: Boolean = true
)

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class NoteListViewModel @Inject constructor(
    private val noteRepository: NoteRepository
) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")
    private val _selectedCategoryId = MutableStateFlow<String?>(null)
    private val _isGridView = MutableStateFlow(true)

    val uiState: StateFlow<NoteListUiState> = combine(
        _searchQuery,
        _selectedCategoryId,
        _isGridView
    ) { query, categoryId, isGrid ->
        Triple(query, categoryId, isGrid)
    }.flatMapLatest { (query, categoryId, isGrid) ->
        val notesFlow = when {
            query.isNotBlank() -> noteRepository.searchNotes(query)
            categoryId != null -> noteRepository.getNotesByCategory(categoryId)
            else -> noteRepository.getAllNotes()
        }
        notesFlow.map { notes ->
            NoteListUiState(
                notes = notes,
                isLoading = false,
                searchQuery = query,
                selectedCategoryId = categoryId,
                isGridView = isGrid
            )
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = NoteListUiState()
    )

    init {
        viewModelScope.launch {
            noteRepository.syncNotes()
        }
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
    }

    fun onCategoryFilterChange(categoryId: String?) {
        _selectedCategoryId.value = categoryId
    }

    fun toggleViewMode() {
        _isGridView.value = !_isGridView.value
    }

    fun deleteNote(noteId: String) {
        viewModelScope.launch {
            noteRepository.deleteNote(noteId)
        }
    }

    fun togglePin(noteId: String) {
        viewModelScope.launch {
            noteRepository.togglePin(noteId)
        }
    }

    fun toggleArchive(noteId: String) {
        viewModelScope.launch {
            noteRepository.toggleArchive(noteId)
        }
    }
}
