package com.notex.app.di

import android.content.Context
import androidx.room.Room
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.notex.app.BuildConfig
import com.notex.app.data.local.NoteXDatabase
import com.notex.app.data.local.dao.CategoryDao
import com.notex.app.data.local.dao.NoteDao
import com.notex.app.data.remote.AuthInterceptor
import com.notex.app.data.remote.NoteXApi
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = true
    }

    // ── Database ──────────────────────────────
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): NoteXDatabase =
        Room.databaseBuilder(
            context,
            NoteXDatabase::class.java,
            NoteXDatabase.DATABASE_NAME
        ).build()

    @Provides
    fun provideNoteDao(database: NoteXDatabase): NoteDao = database.noteDao()

    @Provides
    fun provideCategoryDao(database: NoteXDatabase): CategoryDao = database.categoryDao()

    // ── Network ───────────────────────────────
    @Provides
    @Singleton
    fun provideOkHttpClient(authInterceptor: AuthInterceptor): OkHttpClient {
        val builder = OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)

        if (BuildConfig.DEBUG) {
            val loggingInterceptor = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }
            builder.addInterceptor(loggingInterceptor)
        }

        return builder.build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl(BuildConfig.BASE_URL + "/")
            .client(okHttpClient)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()

    @Provides
    @Singleton
    fun provideNoteXApi(retrofit: Retrofit): NoteXApi =
        retrofit.create(NoteXApi::class.java)
}
