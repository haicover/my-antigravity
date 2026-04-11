package com.notex.app.presentation.screens.editor

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohamedrejeb.richeditor.model.rememberRichTextState
import com.mohamedrejeb.richeditor.ui.material3.RichTextEditor
import com.mohamedrejeb.richeditor.ui.material3.RichTextEditorDefaults
import com.notex.app.presentation.theme.NoteColors

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NoteEditorScreen(
    noteId: String?,
    onNavigateBack: () -> Unit,
    viewModel: NoteEditorViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val richTextState = rememberRichTextState()
    var showColorPicker by remember { mutableStateOf(false) }
    var showDeleteDialog by remember { mutableStateOf(false) }

    LaunchedEffect(noteId) {
        viewModel.loadNote(noteId)
    }

    // Load existing content into rich text editor
    LaunchedEffect(uiState.note) {
        uiState.note?.let { note ->
            if (note.content.isNotBlank() && !uiState.isNew) {
                richTextState.setHtml(note.content)
            }
        }
    }

    LaunchedEffect(uiState.isSaved) {
        if (uiState.isSaved) onNavigateBack()
    }

    // Delete confirmation dialog
    if (showDeleteDialog) {
        AlertDialog(
            onDismissRequest = { showDeleteDialog = false },
            title = { Text("Delete Note") },
            text = { Text("Are you sure you want to delete this note?") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.deleteNote()
                    showDeleteDialog = false
                }) {
                    Text("Delete", color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { showDeleteDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (uiState.isNew) "New Note" else "Edit Note") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                },
                actions = {
                    // Pin toggle
                    IconButton(onClick = viewModel::togglePin) {
                        Icon(
                            Icons.Default.PushPin,
                            contentDescription = "Pin",
                            tint = if (uiState.note?.isPinned == true)
                                MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    // Color picker toggle
                    IconButton(onClick = { showColorPicker = !showColorPicker }) {
                        Icon(Icons.Default.Palette, "Color")
                    }
                    // Delete (only for existing notes)
                    if (!uiState.isNew) {
                        IconButton(onClick = { showDeleteDialog = true }) {
                            Icon(Icons.Default.Delete, "Delete",
                                tint = MaterialTheme.colorScheme.error)
                        }
                    }
                    // Save
                    IconButton(onClick = {
                        viewModel.updateContent(richTextState.toHtml())
                        viewModel.saveNote()
                    }) {
                        Icon(Icons.Default.Check, "Save",
                            tint = MaterialTheme.colorScheme.primary)
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Color picker row
            AnimatedVisibility(visible = showColorPicker) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    NoteColors.forEach { color ->
                        val hexColor = String.format("#%06X", 0xFFFFFF and color.hashCode())
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(color)
                                .border(
                                    width = if (uiState.note?.color == hexColor) 3.dp else 1.dp,
                                    color = if (uiState.note?.color == hexColor)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.outline,
                                    shape = CircleShape
                                )
                                .clickable { viewModel.updateColor(hexColor) }
                        )
                    }
                }
            }

            // Rich Text Formatting Toolbar
            RichTextToolbar(richTextState = richTextState)

            HorizontalDivider()

            // Title field
            OutlinedTextField(
                value = uiState.note?.title ?: "",
                onValueChange = viewModel::updateTitle,
                placeholder = {
                    Text(
                        "Title",
                        style = MaterialTheme.typography.headlineSmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.4f)
                    )
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                textStyle = MaterialTheme.typography.headlineSmall.copy(
                    fontWeight = FontWeight.Bold
                ),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedBorderColor = Color.Transparent,
                    focusedBorderColor = Color.Transparent
                ),
                singleLine = true
            )

            // Rich Text Editor
            RichTextEditor(
                state = richTextState,
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 8.dp),
                colors = RichTextEditorDefaults.richTextEditorColors(
                    containerColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent
                ),
                placeholder = {
                    Text(
                        "Start writing...",
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.4f)
                    )
                }
            )
        }
    }
}

@Composable
fun RichTextToolbar(
    richTextState: com.mohamedrejeb.richeditor.model.RichTextState
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(horizontal = 8.dp, vertical = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        // Bold
        ToolbarButton(
            icon = Icons.Default.FormatBold,
            description = "Bold",
            isActive = richTextState.currentSpanStyle.fontWeight == FontWeight.Bold,
            onClick = { richTextState.toggleSpanStyle(androidx.compose.ui.text.SpanStyle(fontWeight = FontWeight.Bold)) }
        )
        // Italic
        ToolbarButton(
            icon = Icons.Default.FormatItalic,
            description = "Italic",
            isActive = richTextState.currentSpanStyle.fontStyle == androidx.compose.ui.text.font.FontStyle.Italic,
            onClick = { richTextState.toggleSpanStyle(androidx.compose.ui.text.SpanStyle(fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)) }
        )
        // Underline
        ToolbarButton(
            icon = Icons.Default.FormatUnderlined,
            description = "Underline",
            isActive = richTextState.currentSpanStyle.textDecoration == androidx.compose.ui.text.style.TextDecoration.Underline,
            onClick = { richTextState.toggleSpanStyle(androidx.compose.ui.text.SpanStyle(textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline)) }
        )
        // Strikethrough
        ToolbarButton(
            icon = Icons.Default.FormatStrikethrough,
            description = "Strikethrough",
            isActive = richTextState.currentSpanStyle.textDecoration == androidx.compose.ui.text.style.TextDecoration.LineThrough,
            onClick = { richTextState.toggleSpanStyle(androidx.compose.ui.text.SpanStyle(textDecoration = androidx.compose.ui.text.style.TextDecoration.LineThrough)) }
        )

        VerticalDivider(modifier = Modifier.height(24.dp).padding(horizontal = 4.dp))

        // Bullet list
        ToolbarButton(
            icon = Icons.Default.FormatListBulleted,
            description = "Bullet List",
            isActive = richTextState.isUnorderedList,
            onClick = { richTextState.toggleUnorderedList() }
        )
        // Number list
        ToolbarButton(
            icon = Icons.Default.FormatListNumbered,
            description = "Numbered List",
            isActive = richTextState.isOrderedList,
            onClick = { richTextState.toggleOrderedList() }
        )

        VerticalDivider(modifier = Modifier.height(24.dp).padding(horizontal = 4.dp))

        // Code block
        ToolbarButton(
            icon = Icons.Default.Code,
            description = "Code",
            isActive = richTextState.isCodeSpan,
            onClick = { richTextState.toggleCodeSpan() }
        )

        // H1
        ToolbarButton(
            icon = Icons.Default.Title,
            description = "Heading",
            isActive = false,
            onClick = {
                richTextState.toggleSpanStyle(
                    androidx.compose.ui.text.SpanStyle(
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold
                    )
                )
            }
        )
    }
}

@Composable
fun ToolbarButton(
    icon: ImageVector,
    description: String,
    isActive: Boolean,
    onClick: () -> Unit
) {
    IconButton(
        onClick = onClick,
        modifier = Modifier
            .size(36.dp)
            .then(
                if (isActive) Modifier
                    .clip(RoundedCornerShape(8.dp))
                    .background(MaterialTheme.colorScheme.primaryContainer)
                else Modifier
            )
    ) {
        Icon(
            imageVector = icon,
            contentDescription = description,
            modifier = Modifier.size(20.dp),
            tint = if (isActive) MaterialTheme.colorScheme.primary
            else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
