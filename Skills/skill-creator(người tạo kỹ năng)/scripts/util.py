"""Utilities for reading skill metadata from SKILL.md."""

from __future__ import annotations

from pathlib import Path

SKILL_FILENAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
MULTILINE_MARKERS = {">", "|", ">-", "|-"}
TARGET_FIELDS = {"name", "description"}


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """
    Read <skill_path>/SKILL.md and return:
        (name, description, full_content)

    This is intentionally a lightweight parser. It only extracts the fields
    the caller cares about: `name` and `description`.
    """
    skill_file = skill_path / SKILL_FILENAME

    try:
        # utf-8-sig also handles files that start with a UTF-8 BOM.
        content = skill_file.read_text(encoding="utf-8-sig")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Could not find {SKILL_FILENAME!r} in {skill_path}"
        ) from exc

    lines = content.splitlines()

    if not lines:
        raise ValueError("SKILL.md is empty")

    if lines[0].strip() != FRONTMATTER_DELIMITER:
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = _find_frontmatter_end(lines)
    metadata = _parse_frontmatter(lines[1:end_idx])

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    return name, description, content


def _find_frontmatter_end(lines: list[str]) -> int:
    """Return the index of the closing frontmatter delimiter."""
    for index, line in enumerate(lines[1:], start=1):
        if not line.startswith((" ", "\t")) and line.strip() == FRONTMATTER_DELIMITER:
            return index
    raise ValueError("SKILL.md missing frontmatter (no closing ---)")


def _parse_frontmatter(lines: list[str]) -> dict[str, str]:
    """
    Parse only the metadata keys we care about.

    Supported formats:
        name: "My Skill"
        description: "One-line description"
        description: >
          folded line 1
          folded line 2
        description: |
          literal line 1
          literal line 2
    """
    metadata: dict[str, str] = {}
    index = 0

    while index < len(lines):
        raw_line = lines[index]
        stripped_line = raw_line.strip()

        if not stripped_line or stripped_line.startswith("#"):
            index += 1
            continue

        key, separator, value = raw_line.partition(":")
        if not separator:
            index += 1
            continue

        key = key.strip()
        value = value.strip()

        if key not in TARGET_FIELDS:
            index += 1
            continue

        if value in MULTILINE_MARKERS:
            block_lines, next_index = _read_indented_block(lines, start=index + 1)
            metadata[key] = _format_multiline_value(value, block_lines)
            index = next_index
            continue

        metadata[key] = _strip_optional_quotes(value)
        index += 1

    return metadata


def _read_indented_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    Read the indented lines that belong to a multiline YAML value.

    Returns:
        (block_lines, next_index)
    """
    block_lines: list[str] = []
    index = start

    while index < len(lines):
        line = lines[index]

        # Keep blank lines inside the block.
        if not line.strip():
            block_lines.append("")
            index += 1
            continue

        if line.startswith((" ", "\t")):
            block_lines.append(line.lstrip(" \t"))
            index += 1
            continue

        break

    return block_lines, index


def _format_multiline_value(marker: str, lines: list[str]) -> str:
    """
    Convert multiline YAML-style text into a normal Python string.

    - '|' keeps line breaks
    - '>' folds lines into spaces
    """
    if marker.startswith("|"):
        return "\n".join(line.rstrip() for line in lines).strip()

    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return " ".join(cleaned_lines)


def _strip_optional_quotes(value: str) -> str:
    """Remove matching single or double quotes around a value."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value