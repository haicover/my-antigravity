package com.notex.api.routes

import com.notex.api.models.*
import com.notex.api.models.db.Notes
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

fun Route.noteRoutes() {
    authenticate("auth-jwt") {
        route("/api/v1/notes") {

            // GET all notes
            get {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val categoryId = call.request.queryParameters["category_id"]
                val search = call.request.queryParameters["search"]

                val notes = transaction {
                    val query = Notes.selectAll().where {
                        (Notes.userId eq userId) and (Notes.isDeleted eq false)
                    }

                    if (categoryId != null) {
                        query.andWhere { Notes.categoryId eq categoryId }
                    }
                    if (!search.isNullOrBlank()) {
                        query.andWhere {
                            (Notes.title like "%$search%") or (Notes.content like "%$search%")
                        }
                    }

                    query.orderBy(Notes.isPinned to SortOrder.DESC, Notes.updatedAt to SortOrder.DESC)
                        .map { it.toNoteDto() }
                }

                call.respond(ApiResponse(success = true, data = notes))
            }

            // GET note by id
            get("/{id}") {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val noteId = call.parameters["id"]!!

                val note = transaction {
                    Notes.selectAll().where {
                        (Notes.id eq noteId) and (Notes.userId eq userId)
                    }.firstOrNull()?.toNoteDto()
                }

                if (note == null) {
                    call.respond(HttpStatusCode.NotFound, ApiResponse<Unit>(false, message = "Note not found"))
                } else {
                    call.respond(ApiResponse(success = true, data = note))
                }
            }

            // POST create note
            post {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val request = call.receive<CreateNoteRequest>()
                val noteId = UUID.randomUUID().toString()
                val now = Instant.now()

                transaction {
                    Notes.insert {
                        it[id] = noteId
                        it[Notes.userId] = userId
                        it[categoryId] = request.categoryId
                        it[title] = request.title
                        it[content] = request.content
                        it[contentFormat] = request.contentFormat
                        it[color] = request.color
                        it[createdAt] = now
                        it[updatedAt] = now
                    }
                }

                val note = transaction {
                    Notes.selectAll().where { Notes.id eq noteId }.first().toNoteDto()
                }

                call.respond(HttpStatusCode.Created, ApiResponse(success = true, data = note))
            }

            // PUT update note
            put("/{id}") {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val noteId = call.parameters["id"]!!
                val request = call.receive<UpdateNoteRequest>()

                val exists = transaction {
                    Notes.selectAll().where {
                        (Notes.id eq noteId) and (Notes.userId eq userId)
                    }.firstOrNull()
                }

                if (exists == null) {
                    call.respond(HttpStatusCode.NotFound, ApiResponse<Unit>(false, message = "Note not found"))
                    return@put
                }

                transaction {
                    Notes.update({ (Notes.id eq noteId) and (Notes.userId eq userId) }) {
                        request.title?.let { v -> it[title] = v }
                        request.content?.let { v -> it[content] = v }
                        request.contentFormat?.let { v -> it[contentFormat] = v }
                        request.color?.let { v -> it[color] = v }
                        request.categoryId?.let { v -> it[categoryId] = v }
                        request.isPinned?.let { v -> it[isPinned] = v }
                        request.isArchived?.let { v -> it[isArchived] = v }
                        it[updatedAt] = Instant.now()
                    }
                }

                val note = transaction {
                    Notes.selectAll().where { Notes.id eq noteId }.first().toNoteDto()
                }

                call.respond(ApiResponse(success = true, data = note))
            }

            // DELETE note (soft delete)
            delete("/{id}") {
                val principal = call.principal<JWTPrincipal>()!!
                val userId = principal.getUserId()
                val noteId = call.parameters["id"]!!

                val deleted = transaction {
                    Notes.update({ (Notes.id eq noteId) and (Notes.userId eq userId) }) {
                        it[isDeleted] = true
                        it[deletedAt] = Instant.now()
                        it[updatedAt] = Instant.now()
                    }
                }

                if (deleted == 0) {
                    call.respond(HttpStatusCode.NotFound, ApiResponse<Unit>(false, message = "Note not found"))
                } else {
                    call.respond(ApiResponse<Unit>(success = true, message = "Note deleted"))
                }
            }
        }

        // Sync endpoint
        post("/api/v1/sync") {
            val principal = call.principal<JWTPrincipal>()!!
            val userId = principal.getUserId()
            val clientNotes = call.receive<List<NoteDto>>()

            transaction {
                clientNotes.forEach { noteDto ->
                    val existing = Notes.selectAll().where { Notes.id eq noteDto.id }.firstOrNull()
                    if (existing == null) {
                        Notes.insert {
                            it[id] = noteDto.id
                            it[Notes.userId] = userId
                            it[categoryId] = noteDto.categoryId
                            it[title] = noteDto.title
                            it[content] = noteDto.content
                            it[contentFormat] = noteDto.contentFormat
                            it[color] = noteDto.color
                            it[isPinned] = noteDto.isPinned
                            it[isArchived] = noteDto.isArchived
                            it[isDeleted] = noteDto.isDeleted
                            it[createdAt] = Instant.ofEpochMilli(noteDto.createdAt)
                            it[updatedAt] = Instant.ofEpochMilli(noteDto.updatedAt)
                            noteDto.deletedAt?.let { d -> it[deletedAt] = Instant.ofEpochMilli(d) }
                        }
                    } else {
                        val serverUpdated = existing[Notes.updatedAt].toEpochMilli()
                        if (noteDto.updatedAt > serverUpdated) {
                            Notes.update({ Notes.id eq noteDto.id }) {
                                it[title] = noteDto.title
                                it[content] = noteDto.content
                                it[color] = noteDto.color
                                it[isPinned] = noteDto.isPinned
                                it[isArchived] = noteDto.isArchived
                                it[isDeleted] = noteDto.isDeleted
                                it[updatedAt] = Instant.ofEpochMilli(noteDto.updatedAt)
                            }
                        }
                    }
                }
            }

            val serverNotes = transaction {
                Notes.selectAll().where {
                    (Notes.userId eq userId)
                }.map { it.toNoteDto() }
            }

            call.respond(ApiResponse(success = true, data = serverNotes))
        }
    }
}

private fun ResultRow.toNoteDto() = NoteDto(
    id = this[Notes.id],
    userId = this[Notes.userId],
    categoryId = this[Notes.categoryId],
    title = this[Notes.title],
    content = this[Notes.content],
    contentFormat = this[Notes.contentFormat],
    color = this[Notes.color],
    isPinned = this[Notes.isPinned],
    isArchived = this[Notes.isArchived],
    isDeleted = this[Notes.isDeleted],
    createdAt = this[Notes.createdAt].toEpochMilli(),
    updatedAt = this[Notes.updatedAt].toEpochMilli(),
    deletedAt = this[Notes.deletedAt]?.toEpochMilli()
)
