package com.notex.app.presentation.navigation

import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute
import com.notex.app.presentation.screens.auth.LoginScreen
import com.notex.app.presentation.screens.auth.RegisterScreen
import com.notex.app.presentation.screens.categories.CategoriesScreen
import com.notex.app.presentation.screens.editor.NoteEditorScreen
import com.notex.app.presentation.screens.notes.NoteListScreen
import com.notex.app.presentation.screens.profile.ProfileScreen
import com.notex.app.presentation.screens.settings.SettingsScreen
import com.notex.app.presentation.screens.splash.SplashScreen

@Composable
fun NoteXNavHost() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Splash,
        enterTransition = {
            slideInHorizontally(
                initialOffsetX = { it },
                animationSpec = tween(300)
            ) + fadeIn(animationSpec = tween(300))
        },
        exitTransition = {
            slideOutHorizontally(
                targetOffsetX = { -it / 3 },
                animationSpec = tween(300)
            ) + fadeOut(animationSpec = tween(300))
        },
        popEnterTransition = {
            slideInHorizontally(
                initialOffsetX = { -it / 3 },
                animationSpec = tween(300)
            ) + fadeIn(animationSpec = tween(300))
        },
        popExitTransition = {
            slideOutHorizontally(
                targetOffsetX = { it },
                animationSpec = tween(300)
            ) + fadeOut(animationSpec = tween(300))
        }
    ) {
        composable<Screen.Splash> {
            SplashScreen(
                onNavigateToLogin = {
                    navController.navigate(Screen.Login) {
                        popUpTo(Screen.Splash) { inclusive = true }
                    }
                },
                onNavigateToNoteList = {
                    navController.navigate(Screen.NoteList) {
                        popUpTo(Screen.Splash) { inclusive = true }
                    }
                }
            )
        }

        composable<Screen.Login> {
            LoginScreen(
                onNavigateToRegister = {
                    navController.navigate(Screen.Register)
                },
                onNavigateToNoteList = {
                    navController.navigate(Screen.NoteList) {
                        popUpTo(Screen.Login) { inclusive = true }
                    }
                }
            )
        }

        composable<Screen.Register> {
            RegisterScreen(
                onNavigateBack = { navController.popBackStack() },
                onNavigateToNoteList = {
                    navController.navigate(Screen.NoteList) {
                        popUpTo(Screen.Login) { inclusive = true }
                    }
                }
            )
        }

        composable<Screen.NoteList> {
            NoteListScreen(
                onNavigateToEditor = { noteId ->
                    navController.navigate(Screen.NoteEditor(noteId))
                },
                onNavigateToCategories = {
                    navController.navigate(Screen.Categories)
                },
                onNavigateToSettings = {
                    navController.navigate(Screen.Settings)
                },
                onNavigateToProfile = {
                    navController.navigate(Screen.Profile)
                }
            )
        }

        composable<Screen.NoteEditor> { backStackEntry ->
            val args = backStackEntry.toRoute<Screen.NoteEditor>()
            NoteEditorScreen(
                noteId = args.noteId,
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable<Screen.Categories> {
            CategoriesScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable<Screen.Settings> {
            SettingsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }

        composable<Screen.Profile> {
            ProfileScreen(
                onNavigateBack = { navController.popBackStack() },
                onLogout = {
                    navController.navigate(Screen.Login) {
                        popUpTo(0) { inclusive = true }
                    }
                }
            )
        }
    }
}
