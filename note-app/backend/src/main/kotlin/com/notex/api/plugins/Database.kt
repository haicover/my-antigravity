package com.notex.api.plugins

import com.notex.api.models.db.Categories
import com.notex.api.models.db.Notes
import com.notex.api.models.db.Users
import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import io.ktor.server.application.*
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction

fun Application.configureDatabase() {
    val dbUrl = System.getenv("DATABASE_URL") ?: "jdbc:h2:mem:notex;DB_CLOSE_DELAY=-1"
    val dbDriver = System.getenv("DATABASE_DRIVER") ?: "org.h2.Driver"
    val dbUser = System.getenv("DATABASE_USER") ?: "sa"
    val dbPassword = System.getenv("DATABASE_PASSWORD") ?: ""

    val config = HikariConfig().apply {
        jdbcUrl = dbUrl
        driverClassName = dbDriver
        username = dbUser
        password = dbPassword
        maximumPoolSize = 10
        isAutoCommit = false
        transactionIsolation = "TRANSACTION_REPEATABLE_READ"
        validate()
    }

    val dataSource = HikariDataSource(config)
    Database.connect(dataSource)

    // Create tables
    transaction {
        SchemaUtils.create(Users, Notes, Categories)
    }

    log.info("Database connected: $dbUrl")
}
