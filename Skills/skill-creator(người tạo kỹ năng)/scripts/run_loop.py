#!/usr/bin/env python3
"""Run the eval + improve loop for a skill description.

This refactored version keeps the original behavior, but is easier to read,
safer with input validation, and avoids mixing train/test results by query
string when duplicate queries exist.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import tempfile
import time
import webbrowser
from pathlib import Path
from typing import Any

from scripts.generate_report import generate_html
from scripts.improve_description import improve_description
from scripts.run_eval import find_project_root, run_eval
from scripts.utils import parse_skill_md

EvalItem = dict[str, Any]
EvalResult = dict[str, Any]
EvalSummary = dict[str, int]
EvalPayload = dict[str, Any]

DEFAULT_SPLIT_SEED = 42


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def load_eval_set(eval_set_path: Path) -> list[EvalItem]:
    """Load and validate the eval-set JSON file."""
    try:
        raw_text = eval_set_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Eval set file not found: {eval_set_path}") from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in eval set: {eval_set_path}") from exc

    if not isinstance(data, list):
        raise ValueError("Eval set JSON must be a list of objects")

    if not data:
        raise ValueError("Eval set is empty")

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Eval item #{index} is not a JSON object")
        if "query" not in item:
            raise ValueError(f"Eval item #{index} is missing 'query'")
        if "should_trigger" not in item:
            raise ValueError(f"Eval item #{index} is missing 'should_trigger'")
        if not isinstance(item["query"], str):
            raise ValueError(f"Eval item #{index} has a non-string 'query'")
        if not isinstance(item["should_trigger"], bool):
            raise ValueError(f"Eval item #{index} has a non-boolean 'should_trigger'")

    return data


def validate_cli_args(args: argparse.Namespace) -> None:
    """Validate CLI arguments before running the loop."""
    if args.num_workers < 1:
        raise ValueError("--num-workers must be at least 1")
    if args.timeout < 1:
        raise ValueError("--timeout must be at least 1")
    if args.max_iterations < 1:
        raise ValueError("--max-iterations must be at least 1")
    if args.runs_per_query < 1:
        raise ValueError("--runs-per-query must be at least 1")
    if not 0 <= args.trigger_threshold <= 1:
        raise ValueError("--trigger-threshold must be between 0 and 1")
    if not 0 <= args.holdout < 1:
        raise ValueError("--holdout must be in the range [0, 1)")


# ---------------------------------------------------------------------------
# Split helpers
# ---------------------------------------------------------------------------

def split_eval_set(
    eval_set: list[EvalItem],
    holdout: float,
    seed: int = DEFAULT_SPLIT_SEED,
) -> tuple[list[EvalItem], list[EvalItem]]:
    """Split eval items into train/test while keeping class balance.

    The split is stratified by the boolean field ``should_trigger``.
    A local random generator is used so this function does not change global
    random state for the rest of the program.
    """
    if not 0 <= holdout < 1:
        raise ValueError("holdout must be in the range [0, 1)")

    rng = random.Random(seed)

    should_trigger_items = [item for item in eval_set if item["should_trigger"]]
    should_not_trigger_items = [item for item in eval_set if not item["should_trigger"]]

    rng.shuffle(should_trigger_items)
    rng.shuffle(should_not_trigger_items)

    train_pos, test_pos = _split_group(should_trigger_items, holdout)
    train_neg, test_neg = _split_group(should_not_trigger_items, holdout)

    train_set = train_pos + train_neg
    test_set = test_pos + test_neg

    rng.shuffle(train_set)
    rng.shuffle(test_set)
    return train_set, test_set



def _split_group(group: list[EvalItem], holdout: float) -> tuple[list[EvalItem], list[EvalItem]]:
    """Split one class-specific group into train/test.

    Rules:
    - empty group -> both empty
    - holdout == 0 -> everything stays in train
    - single example -> keep it in train so optimization still has data
    - otherwise, reserve at least one example for test but keep at least one
      example in train
    """
    if not group or holdout == 0:
        return group[:], []

    if len(group) == 1:
        return group[:], []

    test_size = max(1, int(len(group) * holdout))
    test_size = min(test_size, len(group) - 1)

    test_set = group[:test_size]
    train_set = group[test_size:]
    return train_set, test_set


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def evaluate_subset(
    subset: list[EvalItem],
    *,
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int,
    trigger_threshold: float,
    model: str,
) -> tuple[EvalPayload, float]:
    """Run evaluation for one subset and return (payload, elapsed_seconds)."""
    if not subset:
        empty_summary = {"passed": 0, "failed": 0, "total": 0}
        return {"results": [], "summary": empty_summary}, 0.0

    started_at = time.perf_counter()
    raw_results = run_eval(
        eval_set=subset,
        skill_name=skill_name,
        description=description,
        num_workers=num_workers,
        timeout=timeout,
        project_root=project_root,
        runs_per_query=runs_per_query,
        trigger_threshold=trigger_threshold,
        model=model,
    )
    elapsed = time.perf_counter() - started_at

    results = raw_results.get("results")
    if not isinstance(results, list):
        raise ValueError("run_eval() returned an invalid payload: missing 'results' list")

    summary = summarize_results(results)
    return {"results": results, "summary": summary}, elapsed



def summarize_results(results: list[EvalResult]) -> EvalSummary:
    """Build a simple passed/failed/total summary from eval results."""
    passed = sum(1 for item in results if item.get("pass"))
    total = len(results)
    return {
        "passed": passed,
        "failed": total - passed,
        "total": total,
    }



def print_eval_stats(label: str, results: list[EvalResult], elapsed: float) -> None:
    """Pretty-print evaluation statistics to stderr."""
    if not results:
        print(f"{label}: no examples ({elapsed:.1f}s)", file=sys.stderr)
        return

    positive_results = [item for item in results if item["should_trigger"]]
    negative_results = [item for item in results if not item["should_trigger"]]

    true_positive = sum(item["triggers"] for item in positive_results)
    positive_runs = sum(item["runs"] for item in positive_results)
    false_negative = positive_runs - true_positive

    false_positive = sum(item["triggers"] for item in negative_results)
    negative_runs = sum(item["runs"] for item in negative_results)
    true_negative = negative_runs - false_positive

    total_runs = true_positive + true_negative + false_positive + false_negative
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 1.0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 1.0
    accuracy = (true_positive + true_negative) / total_runs if total_runs > 0 else 0.0

    print(
        f"{label}: {true_positive + true_negative}/{total_runs} correct, "
        f"precision={precision:.0%} recall={recall:.0%} accuracy={accuracy:.0%} "
        f"({elapsed:.1f}s)",
        file=sys.stderr,
    )

    for item in results:
        status = "PASS" if item["pass"] else "FAIL"
        trigger_rate = f"{item['triggers']}/{item['runs']}"
        print(
            f"  [{status}] rate={trigger_rate} expected={item['should_trigger']}: {item['query'][:60]}",
            file=sys.stderr,
        )


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------

def build_history_entry(
    iteration: int,
    description: str,
    train_payload: EvalPayload,
    test_payload: EvalPayload | None,
) -> dict[str, Any]:
    """Create one history record for the HTML report and JSON output."""
    train_summary = train_payload["summary"]
    test_summary = test_payload["summary"] if test_payload else None

    return {
        "iteration": iteration,
        "description": description,
        "train_passed": train_summary["passed"],
        "train_failed": train_summary["failed"],
        "train_total": train_summary["total"],
        "train_results": train_payload["results"],
        "test_passed": test_summary["passed"] if test_summary else None,
        "test_failed": test_summary["failed"] if test_summary else None,
        "test_total": test_summary["total"] if test_summary else None,
        "test_results": test_payload["results"] if test_payload else None,
        # Backward compatibility for the existing report generator.
        "passed": train_summary["passed"],
        "failed": train_summary["failed"],
        "total": train_summary["total"],
        "results": train_payload["results"],
    }



def write_live_report(
    report_path: Path,
    *,
    skill_name: str,
    original_description: str,
    current_description: str,
    holdout: float,
    train_size: int,
    test_size: int,
    history: list[dict[str, Any]],
) -> None:
    """Write a temporary auto-refreshing HTML report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    partial_output = {
        "original_description": original_description,
        "best_description": current_description,
        "best_score": "in progress",
        "iterations_run": len(history),
        "holdout": holdout,
        "train_size": train_size,
        "test_size": test_size,
        "history": history,
    }
    html = generate_html(partial_output, auto_refresh=True, skill_name=skill_name)
    report_path.write_text(html, encoding="utf-8")



def initialize_report(report_arg: str, skill_path: Path) -> Path | None:
    """Create the first report file and try to open it in the browser."""
    if report_arg == "none":
        return None

    if report_arg == "auto":
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_path = Path(tempfile.gettempdir()) / f"skill_description_report_{skill_path.name}_{timestamp}.html"
    else:
        report_path = Path(report_arg)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    startup_html = (
        "<html><body><h1>Starting optimization loop...</h1>"
        "<meta http-equiv='refresh' content='5'></body></html>"
    )
    report_path.write_text(startup_html, encoding="utf-8")

    try:
        webbrowser.open(report_path.resolve().as_uri())
    except Exception:
        # Opening the browser is just a convenience. The script can continue.
        pass

    return report_path



def choose_best_iteration(history: list[dict[str, Any]], use_test_set: bool) -> tuple[dict[str, Any], str]:
    """Select the best history entry and return (entry, score_string)."""
    if not history:
        raise ValueError("Cannot choose best iteration from empty history")

    if use_test_set:
        best = max(history, key=lambda item: ((item["test_passed"] or 0), item["train_passed"]))
        best_score = f"{best['test_passed']}/{best['test_total']}"
    else:
        best = max(history, key=lambda item: item["train_passed"])
        best_score = f"{best['train_passed']}/{best['train_total']}"

    return best, best_score


# ---------------------------------------------------------------------------
# Core loop
# ---------------------------------------------------------------------------

def run_loop(
    eval_set: list[EvalItem],
    skill_path: Path,
    description_override: str | None,
    num_workers: int,
    timeout: int,
    max_iterations: int,
    runs_per_query: int,
    trigger_threshold: float,
    holdout: float,
    model: str,
    verbose: bool,
    live_report_path: Path | None = None,
    log_dir: Path | None = None,
) -> dict[str, Any]:
    """Run the evaluate -> improve loop until success or max iterations."""
    project_root = find_project_root()
    skill_name, original_description, skill_content = parse_skill_md(skill_path)

    current_description = (
        description_override if description_override is not None else original_description
    )

    if holdout > 0:
        train_set, test_set = split_eval_set(eval_set, holdout)
        if verbose:
            print(
                f"Split: {len(train_set)} train, {len(test_set)} test (holdout={holdout})",
                file=sys.stderr,
            )
    else:
        train_set = eval_set
        test_set = []

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)

    history: list[dict[str, Any]] = []
    exit_reason = "unknown"

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n{'=' * 60}", file=sys.stderr)
            print(f"Iteration {iteration}/{max_iterations}", file=sys.stderr)
            print(f"Description: {current_description}", file=sys.stderr)
            print(f"{'=' * 60}", file=sys.stderr)

        train_payload, train_elapsed = evaluate_subset(
            train_set,
            skill_name=skill_name,
            description=current_description,
            num_workers=num_workers,
            timeout=timeout,
            project_root=project_root,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            model=model,
        )

        if test_set:
            test_payload, test_elapsed = evaluate_subset(
                test_set,
                skill_name=skill_name,
                description=current_description,
                num_workers=num_workers,
                timeout=timeout,
                project_root=project_root,
                runs_per_query=runs_per_query,
                trigger_threshold=trigger_threshold,
                model=model,
            )
        else:
            test_payload = None
            test_elapsed = 0.0

        history_entry = build_history_entry(
            iteration=iteration,
            description=current_description,
            train_payload=train_payload,
            test_payload=test_payload,
        )
        history.append(history_entry)

        if live_report_path is not None:
            write_live_report(
                live_report_path,
                skill_name=skill_name,
                original_description=original_description,
                current_description=current_description,
                holdout=holdout,
                train_size=len(train_set),
                test_size=len(test_set),
                history=history,
            )

        if verbose:
            print_eval_stats("Train", train_payload["results"], train_elapsed)
            if test_payload is not None:
                print_eval_stats("Test ", test_payload["results"], test_elapsed)

        if train_payload["summary"]["failed"] == 0:
            exit_reason = f"all_train_passed (iteration {iteration})"
            if verbose:
                print(f"\nAll train queries passed on iteration {iteration}!", file=sys.stderr)
            break

        if iteration == max_iterations:
            exit_reason = f"max_iterations ({max_iterations})"
            if verbose:
                print(f"\nMax iterations reached ({max_iterations}).", file=sys.stderr)
            break

        if verbose:
            print("\nImproving description...", file=sys.stderr)

        blinded_history = [
            {key: value for key, value in entry.items() if not key.startswith("test_")}
            for entry in history
        ]

        started_at = time.perf_counter()
        new_description = improve_description(
            skill_name=skill_name,
            skill_content=skill_content,
            current_description=current_description,
            eval_results=train_payload,
            history=blinded_history,
            model=model,
            log_dir=log_dir,
            iteration=iteration,
        )
        improve_elapsed = time.perf_counter() - started_at

        if verbose:
            print(f"Proposed ({improve_elapsed:.1f}s): {new_description}", file=sys.stderr)

        current_description = new_description

    best_entry, best_score = choose_best_iteration(history, use_test_set=bool(test_set))

    if verbose:
        print(f"\nExit reason: {exit_reason}", file=sys.stderr)
        print(f"Best score: {best_score} (iteration {best_entry['iteration']})", file=sys.stderr)

    return {
        "exit_reason": exit_reason,
        "original_description": original_description,
        "best_description": best_entry["description"],
        "best_score": best_score,
        "best_train_score": f"{best_entry['train_passed']}/{best_entry['train_total']}",
        "best_test_score": (
            f"{best_entry['test_passed']}/{best_entry['test_total']}" if test_set else None
        ),
        "final_description": current_description,
        "iterations_run": len(history),
        "holdout": holdout,
        "train_size": len(train_set),
        "test_size": len(test_set),
        "history": history,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Create and return the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Run the eval + improve loop",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override starting description")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max improvement iterations")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument(
        "--holdout",
        type=float,
        default=0.4,
        help="Fraction of eval set to hold out for testing (0 to disable)",
    )
    parser.add_argument("--model", required=True, help="Model for improvement")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    parser.add_argument(
        "--report",
        default="auto",
        help="Generate HTML report at this path ('auto' for temp file, 'none' to disable)",
    )
    parser.add_argument(
        "--results-dir",
        default=None,
        help="Save all outputs (results.json, report.html, logs/) to a timestamped subdirectory here",
    )
    return parser



def main() -> None:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        validate_cli_args(args)

        eval_set = load_eval_set(Path(args.eval_set))
        skill_path = Path(args.skill_path)

        if not (skill_path / "SKILL.md").exists():
            raise FileNotFoundError(f"No SKILL.md found at {skill_path}")

        skill_name, _, _ = parse_skill_md(skill_path)
        live_report_path = initialize_report(args.report, skill_path)

        if args.results_dir:
            timestamp = time.strftime("%Y-%m-%d_%H%M%S")
            results_dir = Path(args.results_dir) / timestamp
            results_dir.mkdir(parents=True, exist_ok=True)
        else:
            results_dir = None

        log_dir = results_dir / "logs" if results_dir else None

        output = run_loop(
            eval_set=eval_set,
            skill_path=skill_path,
            description_override=args.description,
            num_workers=args.num_workers,
            timeout=args.timeout,
            max_iterations=args.max_iterations,
            runs_per_query=args.runs_per_query,
            trigger_threshold=args.trigger_threshold,
            holdout=args.holdout,
            model=args.model,
            verbose=args.verbose,
            live_report_path=live_report_path,
            log_dir=log_dir,
        )

        json_output = json.dumps(output, indent=2, ensure_ascii=False)
        print(json_output)

        if results_dir is not None:
            (results_dir / "results.json").write_text(json_output, encoding="utf-8")

        if live_report_path is not None:
            final_html = generate_html(output, auto_refresh=False, skill_name=skill_name)
            live_report_path.write_text(final_html, encoding="utf-8")
            print(f"\nReport: {live_report_path}", file=sys.stderr)

            if results_dir is not None:
                (results_dir / "report.html").write_text(final_html, encoding="utf-8")

        if results_dir is not None:
            print(f"Results saved to: {results_dir}", file=sys.stderr)

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
