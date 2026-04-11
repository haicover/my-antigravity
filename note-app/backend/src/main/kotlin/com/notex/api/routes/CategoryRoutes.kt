package com.notex.api.routes

import com.notex.api.models.*
import com.notex.api.models.db.Categories
import com.notex.api.plugins.getUserId
import io.ktor.http.*
import io.ktor.server.auth.*
import io.ktor.server.auth.jwt.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.transactions.transaction
import java.time.Instant
import java.util.*

fun Route.categoryRoutes() {
    authenticate("auth-jwt") {
        route("/api/v1/categories") {

            get {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()

                val categories = transaction {
                    Categories.selectAll().where { Categories.userId eq userId }
                        .orderBy(Categories.name to SortOrder.ASC)
                        .map { it.toCategoryDto() }
                }

                call.respond(ApiResponse(success = true, data = categories))
            }

            post {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val request = call.receive<CreateCategoryRequest>()
                val categoryId = UUID.randomUUID().toString()

                transaction {
                    Categories.insert {
                        it[id] = categoryId
                        it[Categories.userId] = userId
                        it[name] = request.name
                        it[color] = request.color
                        it[createdAt] = Instant.now()
                    }
                }

                val category = transaction {
                    Categories.selectAll().where { Categories.id eq categoryId }
                        .first().toCategoryDto()
                }

                call.respond(HttpStatusCode.Created, ApiResponse(success = true, data = category))
            }

            delete("/{id}") {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val categoryId = call.parameters["id"]!!

                val deleted = transaction {
                    Categories.deleteWhere {
                        (Categories.id eq categoryId) and (Categories.userId eq userId)
                    }
                }

                if (deleted == 0) {
                    call.respond(HttpStatusCode.NotFound, ApiResponse<Unit>(false, message = "Category not found"))
                } else {
                    call.respond(ApiResponse<Unit>(success = true, message = "Category deleted"))
                }
            }
        }
    }
}

private fun ResultRow.toCategoryDto() = CategoryDto(
    id = this[Categories.id],
    userId = this[Categories.userId],
    name = this[Categories.name],
    color = this[Categories.color],
    createdAt = this[Categories.createdAt].toEpochMilli()
)
