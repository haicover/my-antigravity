package com.notex.app.data.remote

import com.notex.app.data.remote.dto.*
import retrofit2.http.*

interface NoteXApi {

    // ── Auth ──────────────────────────────────
    @POST("api/v1/auth/register")
    suspend fun register(@Body request: RegisterRequest): ApiResponse<AuthResponse>

    @POST("api/v1/auth/login")
    suspend fun login(@Body request: LoginRequest): ApiResponse<AuthResponse>

    @POST("api/v1/auth/google")
    suspend fun loginWithGoogle(@Body request: GoogleAuthRequest): ApiResponse<AuthResponse>

    @POST("api/v1/auth/refresh")
    suspend fun refreshToken(@Body request: TokenRefreshRequest): ApiResponse<TokenResponse>

    // ── Notes ─────────────────────────────────
    @GET("api/v1/notes")
    suspend fun getNotes(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 50,
        @Query("category_id") categoryId: String? = null,
        @Query("search") search: String? = null
    ): ApiResponse<List<NoteDto>>

    @GET("api/v1/notes/{id}")
    suspend fun getNoteById(@Path("id") id: String): ApiResponse<NoteDto>

    @POST("api/v1/notes")
    suspend fun createNote(@Body request: CreateNoteRequest): ApiResponse<NoteDto>

    @PUT("api/v1/notes/{id}")
    suspend fun updateNote(
        @Path("id") id: String,
        @Body request: UpdateNoteRequest
    ): ApiResponse<NoteDto>

    @DELETE("api/v1/notes/{id}")
    suspend fun deleteNote(@Path("id") id: String): ApiResponse<Unit>

    // ── Categories ────────────────────────────
    @GET("api/v1/categories")
    suspend fun getCategories(): ApiResponse<List<CategoryDto>>

    @POST("api/v1/categories")
    suspend fun createCategory(@Body request: CreateCategoryRequest): ApiResponse<CategoryDto>

    @DELETE("api/v1/categories/{id}")
    suspend fun deleteCategory(@Path("id") id: String): ApiResponse<Unit>

    // ── Sync ──────────────────────────────────
    @POST("api/v1/sync")
    suspend fun syncNotes(@Body notes: List<NoteDto>): ApiResponse<List<NoteDto>>
}
