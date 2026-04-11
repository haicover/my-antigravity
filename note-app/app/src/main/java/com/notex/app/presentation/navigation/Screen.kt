package com.notex.app.presentation.navigation

import kotlinx.serialization.Serializable

sealed interface Screen {
    @Serializable
    data object Splash : Screen

    @Serializable
    data object Login : Screen

    @Serializable
    data object Register : Screen

    @Serializable
    data object NoteList : Screen

    @Serializable
    data class NoteEditor(val noteId: String? = null) : Screen

    @Serializable
    data object Categories : Screen

    @Serializable
    data object Settings : Screen

    @Serializable
    data object Profile : Screen
}
