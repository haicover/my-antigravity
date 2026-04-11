package com.notex.app.presentation.screens.categories

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.notex.app.data.remote.TokenManager
import com.notex.app.domain.model.Category
import com.notex.app.domain.repository.CategoryRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CategoriesUiState(
    val categories: List<Category> = emptyList(),
    val isLoading: Boolean = true
)

@HiltViewModel
class CategoriesViewModel @Inject constructor(
    private val categoryRepository: CategoryRepository,
    private val tokenManager: TokenManager
) : ViewModel() {

    val uiState: StateFlow<CategoriesUiState> = categoryRepository.getAllCategories()
        .map { CategoriesUiState(categories = it, isLoading = false) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = CategoriesUiState()
        )

    fun addCategory(name: String, color: String) {
        viewModelScope.launch {
            val userId = tokenManager.getUserId() ?: ""
            categoryRepository.insertCategory(
                Category(userId = userId, name = name, color = color)
            )
        }
    }

    fun deleteCategory(id: String) {
        viewModelScope.launch {
            categoryRepository.deleteCategory(id)
        }
    }
}
