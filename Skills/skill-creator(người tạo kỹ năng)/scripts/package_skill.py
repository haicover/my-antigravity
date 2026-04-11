#!/usr/bin/env python3
"""Package a skill folder into a distributable .skill archive.

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-path-or-directory]

Examples:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
    python utils/package_skill.py skills/public/my-skill ./dist/my-skill.skill
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

from scripts.quick_validate import validate_skill

SKILL_FILENAME = "SKILL.md"
ARCHIVE_SUFFIX = ".skill"

# Exclude these directories anywhere inside the skill.
EXCLUDE_DIRS = {"__pycache__", "node_modules"}
# Exclude these directories only when they are directly under the skill root.
ROOT_EXCLUDE_DIRS = {"evals"}
# Exclude individual files by exact name.
EXCLUDE_FILES = {".DS_Store"}
# Exclude files by glob pattern.
EXCLUDE_GLOBS = {"*.pyc"}


@dataclass(frozen=True)
class PackageSummary:
    """Summary of a completed packaging operation."""

    archive_path: Path
    validation_message: str
    added_files: tuple[Path, ...]
    skipped_files: tuple[Path, ...]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Package a skill folder into a .skill archive",
        epilog=(
            "Examples:\n"
            "  python utils/package_skill.py skills/public/my-skill\n"
            "  python utils/package_skill.py skills/public/my-skill ./dist\n"
            "  python utils/package_skill.py skills/public/my-skill ./dist/my-skill.skill"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help=(
            "Optional output directory or full output file path. "
            "If omitted, the archive is written to the current directory."
        ),
    )
    return parser.parse_args()


def ensure_skill_directory(skill_path: Path) -> None:
    """Validate that the given path is a skill directory containing SKILL.md."""
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill folder not found: {skill_path}")

    if not skill_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {skill_path}")

    skill_md = skill_path / SKILL_FILENAME
    if not skill_md.exists():
        raise FileNotFoundError(f"{SKILL_FILENAME} not found in {skill_path}")


def validate_skill_or_raise(skill_path: Path) -> str:
    """Run the existing validator and raise a clear error if validation fails."""
    valid, message = validate_skill(skill_path)
    if not valid:
        raise ValueError(
            f"Skill validation failed: {message}. "
            "Please fix the validation errors before packaging."
        )
    return message


def resolve_output_path(skill_path: Path, output: str | Path | None) -> Path:
    """Resolve the final .skill archive path.

    Rules:
    - If output is None, write <skill-name>.skill to the current directory.
    - If output ends with .skill, treat it as the exact archive file path.
    - Otherwise, treat output as a directory and create <skill-name>.skill inside it.
    """
    if output is None:
        return (Path.cwd() / f"{skill_path.name}{ARCHIVE_SUFFIX}").resolve()

    output_path = Path(output).expanduser()
    if output_path.suffix.lower() == ARCHIVE_SUFFIX:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path.resolve()

    if output_path.exists() and not output_path.is_dir():
        raise NotADirectoryError(
            f"Output path exists but is not a directory: {output_path}"
        )

    output_path.mkdir(parents=True, exist_ok=True)
    return (output_path / f"{skill_path.name}{ARCHIVE_SUFFIX}").resolve()


def should_exclude(relative_to_skill: Path) -> bool:
    """Return True if a file should be excluded from the archive."""
    parts = relative_to_skill.parts
    if not parts:
        return False

    if parts[0] in ROOT_EXCLUDE_DIRS:
        return True

    if any(part in EXCLUDE_DIRS for part in parts):
        return True

    name = relative_to_skill.name
    if name in EXCLUDE_FILES:
        return True

    return any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDE_GLOBS)


def iter_skill_files(skill_path: Path) -> list[Path]:
    """Return all regular files under the skill directory in stable order."""
    return sorted(
        (path for path in skill_path.rglob("*") if path.is_file()),
        key=lambda path: str(path),
    )


def package_skill(
    skill_path: str | Path,
    output: str | Path | None = None,
) -> PackageSummary:
    """Package a skill directory into a .skill archive.

    Returns a PackageSummary with the archive path and file lists.
    Raises a descriptive exception if packaging fails.
    """
    skill_dir = Path(skill_path).expanduser().resolve()
    ensure_skill_directory(skill_dir)
    validation_message = validate_skill_or_raise(skill_dir)

    archive_path = resolve_output_path(skill_dir, output)
    added_files: list[Path] = []
    skipped_files: list[Path] = []

    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for file_path in iter_skill_files(skill_dir):
            relative_to_skill = file_path.relative_to(skill_dir)

            # Symlinks can make archives surprising and non-portable.
            if file_path.is_symlink():
                skipped_files.append(relative_to_skill)
                continue

            # Avoid packaging the output archive itself if the user writes it
            # somewhere inside the skill folder.
            if file_path.resolve() == archive_path:
                skipped_files.append(relative_to_skill)
                continue

            if should_exclude(relative_to_skill):
                skipped_files.append(relative_to_skill)
                continue

            archive_name = Path(skill_dir.name) / relative_to_skill
            archive.write(file_path, arcname=str(archive_name))
            added_files.append(relative_to_skill)

    return PackageSummary(
        archive_path=archive_path,
        validation_message=validation_message,
        added_files=tuple(added_files),
        skipped_files=tuple(skipped_files),
    )


def main() -> int:
    """CLI entry point."""
    args = parse_args()

    print(f"Packaging skill: {args.skill_path}")
    if args.output:
        print(f"Output target: {args.output}")
    print()

    try:
        summary = package_skill(args.skill_path, args.output)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Validation passed: {summary.validation_message}")
    print()

    for relative_path in summary.added_files:
        print(f"  Added:   {relative_path}")

    for relative_path in summary.skipped_files:
        print(f"  Skipped: {relative_path}")

    print(f"\nSuccessfully packaged skill to: {summary.archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
