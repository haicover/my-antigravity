#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

This script tests whether Claude decides to use/read a temporary skill command
for each query in an evaluation set. It supports repeated runs per query and
summarizes pass/fail rates as JSON.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import select
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from scripts.utils import parse_skill_md

SKILL_FILENAME = "SKILL.md"
CLAUDE_DIRNAME = ".claude"
COMMANDS_DIRNAME = "commands"
STREAM_CHUNK_SIZE = 8192
STREAM_POLL_SECONDS = 0.5
RELEVANT_TOOL_NAMES = {"Skill", "Read"}


def find_project_root() -> Path:
    """Find the project root by walking upward until a .claude/ directory is found."""
    current = Path.cwd()
    for candidate in (current, *current.parents):
        if (candidate / CLAUDE_DIRNAME).is_dir():
            return candidate
    return current


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run one query and return True if the temporary skill command was triggered."""
    if timeout <= 0:
        raise ValueError("timeout must be greater than 0")

    root_path = Path(project_root)
    command_name = _build_command_name(skill_name)
    command_file = _write_command_file(root_path, command_name, skill_name, skill_description)

    process: subprocess.Popen[bytes] | None = None
    try:
        process = _start_claude_process(query=query, model=model, project_root=root_path)
        if process.stdout is None:
            raise RuntimeError("Claude process did not provide a readable stdout pipe")

        deadline = time.monotonic() + timeout
        buffer = ""
        stream_state: dict[str, str | None] = {
            "active_tool_name": None,
            "active_input_json": "",
        }

        while time.monotonic() < deadline:
            if process.poll() is not None:
                remaining = process.stdout.read()
                if remaining:
                    buffer += remaining.decode("utf-8", errors="replace")
                break

            wait_time = min(STREAM_POLL_SECONDS, max(0.0, deadline - time.monotonic()))
            ready, _, _ = select.select([process.stdout], [], [], wait_time)
            if not ready:
                continue

            chunk = os.read(process.stdout.fileno(), STREAM_CHUNK_SIZE)
            if not chunk:
                break

            buffer += chunk.decode("utf-8", errors="replace")
            triggered, finished, buffer = _consume_stream_buffer(
                buffer=buffer,
                command_name=command_name,
                stream_state=stream_state,
            )
            if triggered:
                return True
            if finished:
                return False

        triggered, finished, _ = _consume_stream_buffer(
            buffer=f"{buffer}\n" if buffer else "",
            command_name=command_name,
            stream_state=stream_state,
        )
        if triggered:
            return True
        return False

    except FileNotFoundError as exc:
        raise RuntimeError(
            "Could not run the 'claude' command. Make sure Claude Code is installed "
            "and available on your PATH."
        ) from exc
    finally:
        _stop_process(process)
        command_file.unlink(missing_ok=True)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the evaluation set and return a JSON-friendly summary."""
    _validate_run_arguments(
        num_workers=num_workers,
        timeout=timeout,
        runs_per_query=runs_per_query,
        trigger_threshold=trigger_threshold,
    )
    _validate_eval_set(eval_set)

    if not eval_set:
        return {
            "skill_name": skill_name,
            "description": description,
            "results": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
            },
        }

    total_tasks = len(eval_set) * runs_per_query
    max_workers = min(num_workers, total_tasks)

    trigger_map: dict[int, list[bool]] = {index: [] for index in range(len(eval_set))}

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_info = {}

        for eval_index, item in enumerate(eval_set):
            query = item["query"]
            for run_index in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    query,
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (eval_index, run_index)

        for future in as_completed(future_to_info):
            eval_index, run_index = future_to_info[future]
            try:
                was_triggered = future.result()
            except Exception as exc:
                query = eval_set[eval_index]["query"]
                print(
                    f"Warning: query #{eval_index} run #{run_index} failed "
                    f"for {query!r}: {exc}",
                    file=sys.stderr,
                )
                was_triggered = False

            trigger_map[eval_index].append(was_triggered)

    results: list[dict[str, Any]] = []
    for eval_index, item in enumerate(eval_set):
        triggers = trigger_map[eval_index]
        query = item["query"]
        should_trigger = item["should_trigger"]
        trigger_count = sum(triggers)
        trigger_rate = trigger_count / len(triggers)

        did_pass = (
            trigger_rate >= trigger_threshold
            if should_trigger
            else trigger_rate < trigger_threshold
        )

        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": trigger_count,
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for result in results if result["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation for a skill description"
    )
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--description",
        default=None,
        help="Override description to test",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=10,
        help="Number of parallel workers",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout per query in seconds",
    )
    parser.add_argument(
        "--runs-per-query",
        type=int,
        default=3,
        help="Number of runs per query",
    )
    parser.add_argument(
        "--trigger-threshold",
        type=float,
        default=0.5,
        help="Trigger rate threshold",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model to use for claude -p (default: user's configured model)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress to stderr",
    )
    args = parser.parse_args()

    try:
        _validate_run_arguments(
            num_workers=args.num_workers,
            timeout=args.timeout,
            runs_per_query=args.runs_per_query,
            trigger_threshold=args.trigger_threshold,
        )
        eval_set = _load_eval_set(Path(args.eval_set))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    skill_path = Path(args.skill_path)
    if not (skill_path / SKILL_FILENAME).exists():
        parser.error(f"No {SKILL_FILENAME} found at {skill_path}")

    name, original_description, _ = parse_skill_md(skill_path)
    description = (
        args.description
        if args.description is not None
        else original_description
    )
    project_root = find_project_root()

    if args.verbose:
        print(f"Project root: {project_root}", file=sys.stderr)
        print(f"Evaluating description: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        _print_verbose_summary(output)

    print(json.dumps(output, indent=2))


def _build_command_name(skill_name: str) -> str:
    """Create a filesystem-safe unique command name."""
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", skill_name).strip("-._")
    if not safe_name:
        safe_name = "skill"
    unique_suffix = uuid.uuid4().hex[:8]
    return f"{safe_name}-skill-{unique_suffix}"


def _write_command_file(
    project_root: Path,
    command_name: str,
    skill_name: str,
    skill_description: str,
) -> Path:
    """Write a temporary command file so Claude can discover the skill."""
    commands_dir = project_root / CLAUDE_DIRNAME / COMMANDS_DIRNAME
    commands_dir.mkdir(parents=True, exist_ok=True)

    command_file = commands_dir / f"{command_name}.md"
    command_content = _build_command_content(
        skill_name=skill_name,
        skill_description=skill_description,
    )
    command_file.write_text(command_content, encoding="utf-8")
    return command_file


def _build_command_content(skill_name: str, skill_description: str) -> str:
    """Build the temporary command file content."""
    indented_description = _indent_block_text(skill_description)
    return (
        "---\n"
        "description: |\n"
        f"{indented_description}\n"
        "---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {skill_description}\n"
    )


def _indent_block_text(text: str, prefix: str = "  ") -> str:
    """Indent text so it can be safely embedded under a YAML block scalar."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if not lines:
        lines = [""]
    return "\n".join(f"{prefix}{line}" for line in lines)


def _start_claude_process(
    query: str,
    model: str | None,
    project_root: Path,
) -> subprocess.Popen[bytes]:
    """Launch `claude -p` and stream JSON events from stdout."""
    command = [
        "claude",
        "-p",
        query,
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
    ]
    if model:
        command.extend(["--model", model])

    env = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}

    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        cwd=project_root,
        env=env,
    )


def _consume_stream_buffer(
    buffer: str,
    command_name: str,
    stream_state: dict[str, str | None],
) -> tuple[bool, bool, str]:
    """Parse complete JSON lines from the current buffer.

    Returns:
        (triggered, finished, remaining_buffer)

    - triggered=True  -> our skill was definitely used/read
    - finished=True   -> Claude finished without triggering our skill
    """
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        line = line.strip()
        if not line:
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if _stream_event_triggered(event, command_name, stream_state):
            return True, False, buffer

        if _assistant_message_triggered(event, command_name):
            return True, False, buffer

        if event.get("type") == "result":
            return False, True, buffer

    return False, False, buffer


def _stream_event_triggered(
    event: dict[str, Any],
    command_name: str,
    stream_state: dict[str, str | None],
) -> bool:
    """Inspect partial stream events to detect the target skill early."""
    if event.get("type") != "stream_event":
        return False

    stream_event = event.get("event", {})
    stream_type = stream_event.get("type", "")

    if stream_type == "content_block_start":
        content_block = stream_event.get("content_block", {})
        if content_block.get("type") != "tool_use":
            stream_state["active_tool_name"] = None
            stream_state["active_input_json"] = ""
            return False

        tool_name = content_block.get("name", "")
        stream_state["active_tool_name"] = tool_name
        stream_state["active_input_json"] = ""

        existing_input = content_block.get("input", {})
        return _tool_input_mentions_command(tool_name, existing_input, command_name)

    if stream_type == "content_block_delta":
        active_tool_name = stream_state.get("active_tool_name")
        if active_tool_name not in RELEVANT_TOOL_NAMES:
            return False

        delta = stream_event.get("delta", {})
        if delta.get("type") != "input_json_delta":
            return False

        current_json = stream_state.get("active_input_json", "") or ""
        current_json += delta.get("partial_json", "")
        stream_state["active_input_json"] = current_json
        return command_name in current_json

    if stream_type == "content_block_stop":
        stream_state["active_tool_name"] = None
        stream_state["active_input_json"] = ""
        return False

    if stream_type == "message_stop":
        stream_state["active_tool_name"] = None
        stream_state["active_input_json"] = ""
        return False

    return False


def _assistant_message_triggered(event: dict[str, Any], command_name: str) -> bool:
    """Fallback detection using full assistant messages."""
    if event.get("type") != "assistant":
        return False

    message = event.get("message", {})
    for content_item in message.get("content", []):
        if content_item.get("type") != "tool_use":
            continue

        tool_name = content_item.get("name", "")
        tool_input = content_item.get("input", {})
        if _tool_input_mentions_command(tool_name, tool_input, command_name):
            return True

    return False


def _tool_input_mentions_command(
    tool_name: str,
    tool_input: Any,
    command_name: str,
) -> bool:
    """Check whether a tool input references our temporary command."""
    if not isinstance(tool_input, dict):
        return False

    if tool_name == "Skill":
        value = str(tool_input.get("skill", ""))
        return command_name in value

    if tool_name == "Read":
        value = str(tool_input.get("file_path", ""))
        return command_name in value

    return False


def _stop_process(process: subprocess.Popen[bytes] | None) -> None:
    """Terminate a subprocess safely if it is still running."""
    if process is None or process.poll() is not None:
        return

    process.kill()
    process.wait()


def _load_eval_set(path: Path) -> list[dict]:
    """Load and validate the eval-set JSON file."""
    content = path.read_text(encoding="utf-8")
    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError("Eval set JSON must be a list of objects")
    _validate_eval_set(data)
    return data


def _validate_eval_set(eval_set: list[dict]) -> None:
    """Validate the basic structure of the eval set."""
    for index, item in enumerate(eval_set):
        if not isinstance(item, dict):
            raise ValueError(f"Eval item #{index} must be an object")
        if "query" not in item:
            raise ValueError(f"Eval item #{index} is missing 'query'")
        if "should_trigger" not in item:
            raise ValueError(f"Eval item #{index} is missing 'should_trigger'")
        if not isinstance(item["query"], str):
            raise ValueError(f"Eval item #{index} field 'query' must be a string")
        if not isinstance(item["should_trigger"], bool):
            raise ValueError(
                f"Eval item #{index} field 'should_trigger' must be true/false"
            )


def _validate_run_arguments(
    *,
    num_workers: int,
    timeout: int,
    runs_per_query: int,
    trigger_threshold: float,
) -> None:
    """Validate numeric runtime arguments."""
    if num_workers <= 0:
        raise ValueError("num_workers must be greater than 0")
    if timeout <= 0:
        raise ValueError("timeout must be greater than 0")
    if runs_per_query <= 0:
        raise ValueError("runs_per_query must be greater than 0")
    if not 0.0 <= trigger_threshold <= 1.0:
        raise ValueError("trigger_threshold must be between 0.0 and 1.0")


def _print_verbose_summary(output: dict[str, Any]) -> None:
    """Print a compact human-readable summary to stderr."""
    summary = output["summary"]
    print(
        f"Results: {summary['passed']}/{summary['total']} passed",
        file=sys.stderr,
    )
    for result in output["results"]:
        status = "PASS" if result["pass"] else "FAIL"
        rate_str = f"{result['triggers']}/{result['runs']}"
        print(
            f"  [{status}] rate={rate_str} expected={result['should_trigger']}: "
            f"{result['query'][:70]}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
