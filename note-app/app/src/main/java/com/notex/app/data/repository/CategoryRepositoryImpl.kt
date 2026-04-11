package com.notex.app.data.repository

import com.notex.app.data.local.dao.CategoryDao
import com.notex.app.data.local.mapper.toDomain
import com.notex.app.data.local.mapper.toEntity
import com.notex.app.data.remote.NoteXApi
import com.notex.app.data.remote.toEntity
import com.notex.app.domain.model.Category
import com.notex.app.domain.repository.CategoryRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CategoryRepositoryImpl @Inject constructor(
    private val categoryDao: CategoryDao,
    private val api: NoteXApi
) : CategoryRepository {

    override fun getAllCategories(): Flow<List<Category>> =
        categoryDao.getAllCategories().map { entities -> entities.map { it.toDomain() } }

    override suspend fun getCategoryById(id: String): Category? =
        categoryDao.getCategoryById(id)?.toDomain()

    override suspend fun insertCategory(category: Category) {
        categoryDao.insertCategory(category.toEntity())
        try {
            api.createCategory(
                com.notex.app.data.remote.dto.CreateCategoryRequest(
                    name = category.name,
                    color = category.color
                )
            )
        } catch (_: Exception) { }
    }

    override suspend fun updateCategory(category: Category) {
        categoryDao.updateCategory(category.toEntity())
    }

    override suspend fun deleteCategory(id: String) {
        categoryDao.deleteCategory(id)
        try {
            api.deleteCategory(id)
        } catch (_: Exception) { }
    }
}
