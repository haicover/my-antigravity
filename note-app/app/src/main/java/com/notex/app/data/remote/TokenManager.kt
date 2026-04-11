package com.notex.app.data.remote

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "notex_prefs")

@Singleton
class TokenManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        private val ACCESS_TOKEN = stringPreferencesKey("access_token")
        private val REFRESH_TOKEN = stringPreferencesKey("refresh_token")
        private val USER_ID = stringPreferencesKey("user_id")
        private val USER_EMAIL = stringPreferencesKey("user_email")
        private val USER_NAME = stringPreferencesKey("user_name")
        private val USER_AVATAR = stringPreferencesKey("user_avatar")
        private val AUTH_PROVIDER = stringPreferencesKey("auth_provider")
    }

    suspend fun saveTokens(accessToken: String, refreshToken: String) {
        context.dataStore.edit { prefs ->
            prefs[ACCESS_TOKEN] = accessToken
            prefs[REFRESH_TOKEN] = refreshToken
        }
    }

    suspend fun saveUser(
        id: String,
        email: String,
        name: String,
        avatar: String?,
        provider: String
    ) {
        context.dataStore.edit { prefs ->
            prefs[USER_ID] = id
            prefs[USER_EMAIL] = email
            prefs[USER_NAME] = name
            avatar?.let { prefs[USER_AVATAR] = it }
            prefs[AUTH_PROVIDER] = provider
        }
    }

    suspend fun getAccessToken(): String? =
        context.dataStore.data.map { it[ACCESS_TOKEN] }.first()

    suspend fun getRefreshToken(): String? =
        context.dataStore.data.map { it[REFRESH_TOKEN] }.first()

    suspend fun getUserId(): String? =
        context.dataStore.data.map { it[USER_ID] }.first()

    suspend fun getUserEmail(): String? =
        context.dataStore.data.map { it[USER_EMAIL] }.first()

    suspend fun getUserName(): String? =
        context.dataStore.data.map { it[USER_NAME] }.first()

    suspend fun getUserAvatar(): String? =
        context.dataStore.data.map { it[USER_AVATAR] }.first()

    suspend fun getAuthProvider(): String? =
        context.dataStore.data.map { it[AUTH_PROVIDER] }.first()

    suspend fun isLoggedIn(): Boolean = getAccessToken() != null

    suspend fun clearAll() {
        context.dataStore.edit { it.clear() }
    }
}
