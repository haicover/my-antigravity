package com.notex.api.plugins

import com.notex.api.routes.authRoutes
import com.notex.api.routes.categoryRoutes
import com.notex.api.routes.noteRoutes
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Application.configureRouting() {
    routing {
        // Health check
        get("/health") {
            call.respond(HttpStatusCode.OK, mapOf(
                "status" to "healthy",
                "service" to "notex-api",
                "version" to "1.0.0"
            ))
        }

        authRoutes()
        noteRoutes()
        categoryRoutes()
    }
}
