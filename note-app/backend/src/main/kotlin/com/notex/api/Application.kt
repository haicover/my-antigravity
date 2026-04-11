package com.notex.api

import com.notex.api.plugins.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*

fun main() {
    val port = System.getenv("PORT")?.toIntOrNull() ?: 8080
    val host = System.getenv("HOST") ?: "0.0.0.0"

    embeddedServer(Netty, port = port, host = host) {
        module()
    }.start(wait = true)
}

fun Application.module() {
    configureSerialization()
    configureSecurity()
    configureCORS()
    configureStatusPages()
    configureCallLogging()
    configureDatabase()
    configureRouting()
}
