#!/usr/bin/env python3
"""
aggregate_benchmark.py
----------------------
Tổng hợp kết quả chạy benchmark thành thống kê tóm tắt.

Đọc các file grading.json từ thư mục benchmark và tạo ra:
- benchmark.json : dữ liệu thống kê đầy đủ (mean, stddev, min, max)
- benchmark.md   : bảng tóm tắt dạng Markdown dễ đọc

Cách dùng:
    python aggregate_benchmark.py <benchmark_dir>
    python aggregate_benchmark.py benchmarks/2026-01-15/ --skill-name "MySkill"

Hỗ trợ 2 kiểu cấu trúc thư mục:

    Kiểu 1 — Workspace (từ skill-creator):
    <benchmark_dir>/
    └── eval-N/
        ├── with_skill/
        │   ├── run-1/grading.json
        │   └── run-2/grading.json
        └── without_skill/
            └── run-1/grading.json

    Kiểu 2 — Legacy (có thư mục runs/):
    <benchmark_dir>/
    └── runs/
        └── eval-N/
            ├── with_skill/run-1/grading.json
            └── without_skill/run-1/grading.json
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Hằng số
# ---------------------------------------------------------------------------

DELTA_KEY = "delta"   # Key đặc biệt trong run_summary, không phải config thật


# ---------------------------------------------------------------------------
# Kiểu dữ liệu
# ---------------------------------------------------------------------------

Stats      = dict[str, float]      # {"mean": ..., "stddev": ..., "min": ..., "max": ...}
RunResult  = dict                  # Kết quả một lần chạy
ConfigData = dict[str, list[RunResult]]  # {"with_skill": [...], "without_skill": [...]}


# ---------------------------------------------------------------------------
# Tính thống kê
# ---------------------------------------------------------------------------

def calculate_stats(values: list[float]) -> Stats:
    """
    Tính mean, stddev (mẫu), min, max từ danh sách giá trị.

    Trả về dict với 4 khoá: mean, stddev, min, max.
    Nếu danh sách rỗng, trả về tất cả bằng 0.
    """
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    n    = len(values)
    mean = sum(values) / n
    # Dùng độ lệch chuẩn mẫu (chia n-1) khi có >1 phần tử
    stddev = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1)) if n > 1 else 0.0

    return {
        "mean":   round(mean,        4),
        "stddev": round(stddev,       4),
        "min":    round(min(values),  4),
        "max":    round(max(values),  4),
    }


# ---------------------------------------------------------------------------
# Tìm thư mục gốc chứa các eval-N
# ---------------------------------------------------------------------------

def find_search_dir(benchmark_dir: Path) -> Path | None:
    """
    Tìm thư mục chứa các thư mục eval-N.

    Ưu tiên: <benchmark_dir>/runs/ → <benchmark_dir>/ → None
    """
    runs_subdir = benchmark_dir / "runs"
    if runs_subdir.exists() and any(runs_subdir.glob("eval-*")):
        return runs_subdir
    if any(benchmark_dir.glob("eval-*")):
        return benchmark_dir
    return None


# ---------------------------------------------------------------------------
# Đọc eval_id từ metadata hoặc tên thư mục
# ---------------------------------------------------------------------------

def read_eval_id(eval_dir: Path, fallback: int) -> int | str:
    """
    Lấy eval_id từ eval_metadata.json nếu có,
    ngược lại parse từ tên thư mục (eval-N), cuối cùng dùng fallback.
    """
    metadata_path = eval_dir / "eval_metadata.json"
    if metadata_path.exists():
        try:
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
            return data.get("eval_id", fallback)
        except (json.JSONDecodeError, OSError):
            pass

    try:
        return int(eval_dir.name.split("-")[1])
    except (IndexError, ValueError):
        return fallback


# ---------------------------------------------------------------------------
# Đọc kết quả một lần chạy (run_dir)
# ---------------------------------------------------------------------------

def load_grading(grading_file: Path) -> dict | None:
    """Đọc và parse grading.json. Trả về None nếu lỗi."""
    try:
        return json.loads(grading_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON không hợp lệ trong {grading_file}: {e}")
        return None


def extract_timing(grading: dict, run_dir: Path) -> tuple[float, int]:
    """
    Lấy thông tin thời gian và token.

    Kiểm tra grading.json trước, nếu thiếu thì đọc timing.json bên cạnh.
    Trả về: (time_seconds, tokens)
    """
    timing      = grading.get("timing", {})
    time_secs   = timing.get("total_duration_seconds", 0.0)
    tokens      = 0

    if time_secs == 0.0:
        timing_file = run_dir / "timing.json"
        if timing_file.exists():
            try:
                td        = json.loads(timing_file.read_text(encoding="utf-8"))
                time_secs = td.get("total_duration_seconds", 0.0)
                tokens    = td.get("total_tokens", 0)
            except json.JSONDecodeError:
                pass

    return time_secs, tokens


def extract_metrics(grading: dict, tokens_fallback: int) -> dict:
    """Lấy các chỉ số thực thi (tool calls, tokens, errors) từ grading.json."""
    metrics = grading.get("execution_metrics", {})
    return {
        "tool_calls": metrics.get("total_tool_calls", 0),
        "tokens":     tokens_fallback or metrics.get("output_chars", 0),
        "errors":     metrics.get("errors_encountered", 0),
    }


def validate_expectations(expectations: list[dict], source: Path) -> None:
    """Cảnh báo nếu expectation thiếu các trường bắt buộc."""
    required = {"text", "passed"}
    for exp in expectations:
        missing = required - exp.keys()
        if missing:
            print(f"⚠️  Expectation trong {source} thiếu trường: {missing} — {exp}")


def parse_run(run_dir: Path, eval_id: int | str) -> RunResult | None:
    """
    Đọc và chuyển đổi kết quả một lần chạy thành dict chuẩn hoá.

    Trả về None nếu không tìm thấy hoặc lỗi grading.json.
    """
    grading_file = run_dir / "grading.json"
    if not grading_file.exists():
        print(f"⚠️  Không tìm thấy grading.json trong {run_dir}")
        return None

    grading = load_grading(grading_file)
    if grading is None:
        return None

    summary = grading.get("summary", {})
    time_secs, tokens = extract_timing(grading, run_dir)
    metrics = extract_metrics(grading, tokens)

    expectations = grading.get("expectations", [])
    validate_expectations(expectations, grading_file)

    notes_summary = grading.get("user_notes_summary", {})
    notes = (
        notes_summary.get("uncertainties", [])
        + notes_summary.get("needs_review",  [])
        + notes_summary.get("workarounds",   [])
    )

    try:
        run_number = int(run_dir.name.split("-")[1])
    except (IndexError, ValueError):
        run_number = 0

    return {
        "eval_id":    eval_id,
        "run_number": run_number,
        "pass_rate":  summary.get("pass_rate",  0.0),
        "passed":     summary.get("passed",      0),
        "failed":     summary.get("failed",      0),
        "total":      summary.get("total",       0),
        "time_seconds": time_secs,
        **metrics,
        "expectations": expectations,
        "notes":        notes,
    }


# ---------------------------------------------------------------------------
# Tải toàn bộ kết quả từ thư mục benchmark
# ---------------------------------------------------------------------------

def load_run_results(benchmark_dir: Path) -> ConfigData:
    """
    Tải tất cả kết quả chạy từ thư mục benchmark.

    Trả về dict: { "with_skill": [RunResult, ...], "without_skill": [...], ... }
    """
    search_dir = find_search_dir(benchmark_dir)
    if search_dir is None:
        print(f"❌ Không tìm thấy thư mục eval-* trong: {benchmark_dir}")
        return {}

    results: ConfigData = {}

    for idx, eval_dir in enumerate(sorted(search_dir.glob("eval-*"))):
        eval_id = read_eval_id(eval_dir, fallback=idx)

        # Duyệt qua từng thư mục config (with_skill, without_skill, ...)
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            # Bỏ qua thư mục không chứa run-*
            if not any(config_dir.glob("run-*")):
                continue

            config = config_dir.name
            results.setdefault(config, [])

            for run_dir in sorted(config_dir.glob("run-*")):
                run = parse_run(run_dir, eval_id)
                if run is not None:
                    results[config].append(run)

    return results


# ---------------------------------------------------------------------------
# Tổng hợp thống kê
# ---------------------------------------------------------------------------

def aggregate_results(results: ConfigData) -> dict:
    """
    Tính thống kê tổng hợp cho từng config và delta giữa 2 config đầu tiên.

    Trả về run_summary dict gồm stats mỗi config + khoá "delta".
    """
    run_summary: dict = {}
    configs = list(results.keys())

    for config in configs:
        runs = results[config]
        if not runs:
            run_summary[config] = {
                "pass_rate":    {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                "time_seconds": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                "tokens":       {"mean": 0,   "stddev": 0,   "min": 0,   "max": 0},
            }
            continue

        run_summary[config] = {
            "pass_rate":    calculate_stats([r["pass_rate"]        for r in runs]),
            "time_seconds": calculate_stats([r["time_seconds"]     for r in runs]),
            "tokens":       calculate_stats([r.get("tokens", 0)    for r in runs]),
        }

    # Tính delta giữa config đầu tiên (primary) và config thứ hai (baseline)
    primary  = run_summary.get(configs[0], {}) if len(configs) >= 1 else {}
    baseline = run_summary.get(configs[1], {}) if len(configs) >= 2 else {}

    def mean_of(cfg: dict, key: str) -> float:
        return cfg.get(key, {}).get("mean", 0.0)

    run_summary[DELTA_KEY] = {
        "pass_rate":    f"{mean_of(primary, 'pass_rate')    - mean_of(baseline, 'pass_rate'):+.2f}",
        "time_seconds": f"{mean_of(primary, 'time_seconds') - mean_of(baseline, 'time_seconds'):+.1f}",
        "tokens":       f"{mean_of(primary, 'tokens')       - mean_of(baseline, 'tokens'):+.0f}",
    }

    return run_summary


# ---------------------------------------------------------------------------
# Tạo benchmark.json
# ---------------------------------------------------------------------------

def generate_benchmark(
    benchmark_dir: Path,
    skill_name: str = "",
    skill_path: str = "",
) -> dict:
    """
    Tạo dict benchmark hoàn chỉnh từ thư mục kết quả.

    Bao gồm metadata, toàn bộ runs, và thống kê tổng hợp.
    """
    results     = load_run_results(benchmark_dir)
    run_summary = aggregate_results(results)

    # Danh sách tất cả runs phẳng (flat list)
    runs = [
        {
            "eval_id":       r["eval_id"],
            "configuration": config,
            "run_number":    r["run_number"],
            "result": {
                "pass_rate":    r["pass_rate"],
                "passed":       r["passed"],
                "failed":       r["failed"],
                "total":        r["total"],
                "time_seconds": r["time_seconds"],
                "tokens":       r.get("tokens",     0),
                "tool_calls":   r.get("tool_calls",  0),
                "errors":       r.get("errors",      0),
            },
            "expectations": r["expectations"],
            "notes":         r["notes"],
        }
        for config in results
        for r in results[config]
    ]

    eval_ids = sorted({r["eval_id"] for config in results.values() for r in config})

    return {
        "metadata": {
            "skill_name":             skill_name or "<skill-name>",
            "skill_path":             skill_path or "<path/to/skill>",
            "executor_model":         "<model-name>",
            "analyzer_model":         "<model-name>",
            "timestamp":              datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run":              eval_ids,
            "runs_per_configuration": 3,
        },
        "runs":        runs,
        "run_summary": run_summary,
        "notes":       [],   # Được điền thêm bởi analyzer
    }


# ---------------------------------------------------------------------------
# Tạo benchmark.md
# ---------------------------------------------------------------------------

def _format_pass_rate(summary: dict, delta_val: str) -> str:
    pr = summary.get("pass_rate", {})
    return f"| Pass Rate | {pr.get('mean',0)*100:.0f}% ± {pr.get('stddev',0)*100:.0f}% | {delta_val} |"


def _format_time(a: dict, b: dict, delta_val: str) -> str:
    at = a.get("time_seconds", {})
    bt = b.get("time_seconds", {})
    return (
        f"| Time | {at.get('mean',0):.1f}s ± {at.get('stddev',0):.1f}s | "
        f"{bt.get('mean',0):.1f}s ± {bt.get('stddev',0):.1f}s | {delta_val}s |"
    )


def _format_tokens(a: dict, b: dict, delta_val: str) -> str:
    at = a.get("tokens", {})
    bt = b.get("tokens", {})
    return (
        f"| Tokens | {at.get('mean',0):.0f} ± {at.get('stddev',0):.0f} | "
        f"{bt.get('mean',0):.0f} ± {bt.get('stddev',0):.0f} | {delta_val} |"
    )


def generate_markdown(benchmark: dict) -> str:
    """
    Tạo báo cáo Markdown dễ đọc từ dữ liệu benchmark.

    Trả về chuỗi Markdown hoàn chỉnh.
    """
    metadata    = benchmark["metadata"]
    run_summary = benchmark["run_summary"]

    configs  = [k for k in run_summary if k != DELTA_KEY]
    config_a = configs[0] if len(configs) >= 1 else "config_a"
    config_b = configs[1] if len(configs) >= 2 else "config_b"
    label_a  = config_a.replace("_", " ").title()
    label_b  = config_b.replace("_", " ").title()

    a_summary = run_summary.get(config_a, {})
    b_summary = run_summary.get(config_b, {})
    delta     = run_summary.get(DELTA_KEY, {})

    evals_str = ", ".join(map(str, metadata["evals_run"]))

    lines = [
        f"# Skill Benchmark: {metadata['skill_name']}",
        "",
        f"**Model**: {metadata['executor_model']}",
        f"**Date**: {metadata['timestamp']}",
        f"**Evals**: {evals_str} ({metadata['runs_per_configuration']} runs mỗi config)",
        "",
        "## Summary",
        "",
        f"| Metric | {label_a} | {label_b} | Delta |",
        "|--------|-----------|-----------|-------|",
    ]

    # Pass Rate — chỉ hiển thị cột A vs Delta (B chưa đủ thông tin trong hàm gốc)
    a_pr = a_summary.get("pass_rate", {})
    b_pr = b_summary.get("pass_rate", {})
    lines.append(
        f"| Pass Rate | {a_pr.get('mean',0)*100:.0f}% ± {a_pr.get('stddev',0)*100:.0f}% "
        f"| {b_pr.get('mean',0)*100:.0f}% ± {b_pr.get('stddev',0)*100:.0f}% "
        f"| {delta.get('pass_rate', '—')} |"
    )
    lines.append(_format_time(a_summary, b_summary, delta.get("time_seconds", "—")))
    lines.append(_format_tokens(a_summary, b_summary, delta.get("tokens", "—")))

    if benchmark.get("notes"):
        lines += ["", "## Notes", ""]
        lines += [f"- {note}" for note in benchmark["notes"]]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tổng hợp kết quả benchmark thành thống kê tóm tắt"
    )
    parser.add_argument(
        "benchmark_dir",
        type=Path,
        help="Đường dẫn tới thư mục benchmark",
    )
    parser.add_argument(
        "--skill-name", default="",
        help="Tên kỹ năng đang benchmark",
    )
    parser.add_argument(
        "--skill-path", default="",
        help="Đường dẫn tới file kỹ năng",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="File JSON đầu ra (mặc định: <benchmark_dir>/benchmark.json)",
    )
    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"❌ Thư mục không tồn tại: {args.benchmark_dir}")
        sys.exit(1)

    # Tạo dữ liệu benchmark
    benchmark = generate_benchmark(args.benchmark_dir, args.skill_name, args.skill_path)

    # Đường dẫn đầu ra
    output_json = args.output or (args.benchmark_dir / "benchmark.json")
    output_md   = output_json.with_suffix(".md")

    # Ghi benchmark.json
    output_json.write_text(json.dumps(benchmark, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Đã tạo: {output_json}")

    # Ghi benchmark.md
    output_md.write_text(generate_markdown(benchmark), encoding="utf-8")
    print(f"✅ Đã tạo: {output_md}")

    # In tóm tắt ra terminal
    run_summary = benchmark["run_summary"]
    configs     = [k for k in run_summary if k != DELTA_KEY]
    delta       = run_summary.get(DELTA_KEY, {})

    print("\n📊 Tóm tắt kết quả:")
    for config in configs:
        pr    = run_summary[config]["pass_rate"]["mean"]
        label = config.replace("_", " ").title()
        print(f"   {label:<20}: {pr * 100:.1f}% pass rate")
    print(f"   {'Delta':<20}: {delta.get('pass_rate', '—')}")


if __name__ == "__main__":
    main()