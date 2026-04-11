#!/usr/bin/env python3
"""Quick validation script for skills.

This version keeps the original goal of being simple and fast, but it is more
robust and easier to maintain:
- reads files with UTF-8 safely
- extracts YAML frontmatter without fragile regex assumptions
- validates fields with small helper functions
- returns clear error messages
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "This script requires PyYAML. Install it with: pip install pyyaml"
    ) from exc

SKILL_FILENAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
NAME_PATTERN = r"^[a-z0-9-]+$"
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def validate_skill(skill_path: str | Path) -> tuple[bool, str]:
    """Validate a skill directory (or a direct SKILL.md path)."""
    try:
        skill_file = _resolve_skill_file(Path(skill_path))
        content = skill_file.read_text(encoding="utf-8-sig")
        frontmatter_text = extract_frontmatter_text(content)
        frontmatter = load_frontmatter(frontmatter_text)

        validate_allowed_properties(frontmatter)
        validate_required_fields(frontmatter)
        validate_name(frontmatter["name"])
        validate_description(frontmatter["description"])
        validate_optional_fields(frontmatter)
    except ValidationError as exc:
        return False, str(exc)
    except OSError as exc:
        return False, f"Could not read {SKILL_FILENAME}: {exc}"

    return True, "Skill is valid!"


class ValidationError(Exception):
    """Raised when the skill file fails validation."""


def _resolve_skill_file(path: Path) -> Path:
    """Return the SKILL.md file from either a directory path or file path."""
    if path.is_dir():
        skill_file = path / SKILL_FILENAME
    elif path.name == SKILL_FILENAME:
        skill_file = path
    else:
        # Keep the original behavior focused on skill directories.
        skill_file = path / SKILL_FILENAME

    if not skill_file.exists():
        raise ValidationError(f"{SKILL_FILENAME} not found")
    if not skill_file.is_file():
        raise ValidationError(f"{SKILL_FILENAME} is not a regular file")
    return skill_file


def extract_frontmatter_text(content: str) -> str:
    """Extract YAML frontmatter from the beginning of a Markdown file."""
    lines = content.splitlines()

    if not lines:
        raise ValidationError("SKILL.md is empty")
    if lines[0].strip() != FRONTMATTER_DELIMITER:
        raise ValidationError("No YAML frontmatter found")

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == FRONTMATTER_DELIMITER and not line.startswith((" ", "\t")):
            return "\n".join(lines[1:index])

    raise ValidationError("Invalid frontmatter format: missing closing ---")


def load_frontmatter(frontmatter_text: str) -> dict[str, Any]:
    """Parse YAML frontmatter and ensure it is a dictionary."""
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        raise ValidationError(f"Invalid YAML in frontmatter: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise ValidationError("Frontmatter must be a YAML dictionary")
    return frontmatter


# NOTE: re is imported lazily here to keep the top of the file small and readable.
import re


def validate_allowed_properties(frontmatter: dict[str, Any]) -> None:
    """Reject unexpected top-level keys in the frontmatter."""
    unexpected_keys = set(frontmatter) - ALLOWED_PROPERTIES
    if unexpected_keys:
        allowed_text = ", ".join(sorted(ALLOWED_PROPERTIES))
        bad_text = ", ".join(sorted(unexpected_keys))
        raise ValidationError(
            f"Unexpected key(s) in SKILL.md frontmatter: {bad_text}. "
            f"Allowed properties are: {allowed_text}"
        )


def validate_required_fields(frontmatter: dict[str, Any]) -> None:
    """Ensure required fields exist."""
    if "name" not in frontmatter:
        raise ValidationError("Missing 'name' in frontmatter")
    if "description" not in frontmatter:
        raise ValidationError("Missing 'description' in frontmatter")


def validate_name(name: Any) -> None:
    """Validate the skill name."""
    if not isinstance(name, str):
        raise ValidationError(f"Name must be a string, got {type(name).__name__}")

    normalized_name = name.strip()
    if not normalized_name:
        raise ValidationError("Name cannot be empty")
    if len(normalized_name) > MAX_NAME_LENGTH:
        raise ValidationError(
            f"Name is too long ({len(normalized_name)} characters). "
            f"Maximum is {MAX_NAME_LENGTH} characters."
        )
    if not re.fullmatch(NAME_PATTERN, normalized_name):
        raise ValidationError(
            f"Name '{normalized_name}' should be kebab-case "
            "(lowercase letters, digits, and hyphens only)"
        )
    if (
        normalized_name.startswith("-")
        or normalized_name.endswith("-")
        or "--" in normalized_name
    ):
        raise ValidationError(
            f"Name '{normalized_name}' cannot start/end with hyphen "
            "or contain consecutive hyphens"
        )


def validate_description(description: Any) -> None:
    """Validate the skill description."""
    if not isinstance(description, str):
        raise ValidationError(
            f"Description must be a string, got {type(description).__name__}"
        )

    normalized_description = description.strip()
    if not normalized_description:
        raise ValidationError("Description cannot be empty")
    if "<" in normalized_description or ">" in normalized_description:
        raise ValidationError("Description cannot contain angle brackets (< or >)")
    if len(normalized_description) > MAX_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"Description is too long ({len(normalized_description)} characters). "
            f"Maximum is {MAX_DESCRIPTION_LENGTH} characters."
        )


def validate_optional_fields(frontmatter: dict[str, Any]) -> None:
    """Validate optional fields when they are present."""
    if "compatibility" in frontmatter:
        compatibility = frontmatter["compatibility"]
        if not isinstance(compatibility, str):
            raise ValidationError(
                f"Compatibility must be a string, got {type(compatibility).__name__}"
            )
        if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
            raise ValidationError(
                f"Compatibility is too long ({len(compatibility)} characters). "
                f"Maximum is {MAX_COMPATIBILITY_LENGTH} characters."
            )

    if "license" in frontmatter and not isinstance(frontmatter["license"], str):
        raise ValidationError(
            f"License must be a string, got {type(frontmatter['license']).__name__}"
        )

    if "metadata" in frontmatter and not isinstance(frontmatter["metadata"], dict):
        raise ValidationError(
            f"Metadata must be a YAML dictionary, got {type(frontmatter['metadata']).__name__}"
        )

    if "allowed-tools" in frontmatter:
        tools = frontmatter["allowed-tools"]
        if not isinstance(tools, list):
            raise ValidationError(
                f"allowed-tools must be a list, got {type(tools).__name__}"
            )
        if not all(isinstance(tool, str) for tool in tools):
            raise ValidationError("Each item in allowed-tools must be a string")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quick validation script for a skill directory"
    )
    parser.add_argument(
        "skill_path",
        help="Path to the skill directory (or directly to SKILL.md)",
    )
    args = parser.parse_args()

    valid, message = validate_skill(args.skill_path)
    stream = sys.stdout if valid else sys.stderr
    print(message, file=stream)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
