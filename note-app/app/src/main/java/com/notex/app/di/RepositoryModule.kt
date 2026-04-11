package com.notex.app.di

import com.notex.app.data.repository.AuthRepositoryImpl
import com.notex.app.data.repository.CategoryRepositoryImpl
import com.notex.app.data.repository.NoteRepositoryImpl
import com.notex.app.domain.repository.AuthRepository
import com.notex.app.domain.repository.CategoryRepository
import com.notex.app.domain.repository.NoteRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindNoteRepository(impl: NoteRepositoryImpl): NoteRepository

    @Binds
    @Singleton
    abstract fun bindCategoryRepository(impl: CategoryRepositoryImpl): CategoryRepository

    @Binds
    @Singleton
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository
}
