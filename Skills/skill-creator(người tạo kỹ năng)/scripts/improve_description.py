#!/usr/bin/env python3
"""
improve_description.py
======================
Tự động cải thiện mô tả (description) của một skill dựa trên kết quả eval.

Cách dùng:
    python improve_description.py \
        --eval-results path/to/eval_results.json \
        --skill-path  path/to/skill_dir \
        --model       claude-3-5-sonnet-20241022 \
        [--history    path/to/history.json] \
        [--log-dir    path/to/logs] \
        [--verbose]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ─── Hằng số ────────────────────────────────────────────────────────────────

MAX_DESCRIPTION_CHARS = 1024   # Giới hạn cứng cho độ dài description
CLAUDE_TIMEOUT_SECONDS = 300   # Timeout khi gọi claude -p
RECOMMENDED_MAX_WORDS   = 200  # Gợi ý giới hạn số từ (không bắt buộc)


# ─── Dataclass để tổ chức dữ liệu ───────────────────────────────────────────

@dataclass
class EvalCase:
    """Kết quả của một trường hợp kiểm tra."""
    query: str
    should_trigger: bool
    passed: bool
    triggers: int
    runs: int

    @classmethod
    def from_dict(cls, data: dict) -> "EvalCase":
        return cls(
            query        = data["query"],
            should_trigger = data["should_trigger"],
            passed       = data["pass"],
            triggers     = data["triggers"],
            runs         = data["runs"],
        )


@dataclass
class EvalSummary:
    """Tổng hợp kết quả eval."""
    passed: int
    failed: int
    total: int

    @classmethod
    def from_dict(cls, data: dict) -> "EvalSummary":
        return cls(
            passed = data["passed"],
            failed = data["failed"],
            total  = data["total"],
        )


@dataclass
class EvalResults:
    """Toàn bộ kết quả eval từ file JSON."""
    description: str
    summary: EvalSummary
    cases: list[EvalCase]

    @property
    def failed_triggers(self) -> list[EvalCase]:
        """Các trường hợp nên trigger nhưng không trigger."""
        return [c for c in self.cases if c.should_trigger and not c.passed]

    @property
    def false_triggers(self) -> list[EvalCase]:
        """Các trường hợp không nên trigger nhưng lại trigger."""
        return [c for c in self.cases if not c.should_trigger and not c.passed]

    @classmethod
    def from_dict(cls, data: dict) -> "EvalResults":
        return cls(
            description = data["description"],
            summary     = EvalSummary.from_dict(data["summary"]),
            cases       = [EvalCase.from_dict(r) for r in data["results"]],
        )


@dataclass
class HistoryEntry:
    """Một lần thử cải thiện description trong quá khứ."""
    description: str
    train_passed: int
    train_total: int
    test_passed: Optional[int] = None
    test_total: Optional[int] = None
    results: list[dict] = field(default_factory=list)
    note: str = ""

    @property
    def score_string(self) -> str:
        train = f"{self.train_passed}/{self.train_total}"
        if self.test_passed is not None:
            return f"train={train}, test={self.test_passed}/{self.test_total}"
        return f"train={train}"


# ─── Gọi Claude ──────────────────────────────────────────────────────────────

def call_claude(prompt: str, model: Optional[str], timeout: int = CLAUDE_TIMEOUT_SECONDS) -> str:
    """
    Gọi `claude -p` qua subprocess và trả về phản hồi dạng text.

    Prompt được truyền qua stdin thay vì argv để tránh giới hạn độ dài.
    Biến môi trường CLAUDECODE bị xóa để tránh xung đột khi chạy lồng nhau.

    Args:
        prompt:  Nội dung prompt gửi cho Claude.
        model:   Tên model (None = dùng default của claude -p).
        timeout: Thời gian chờ tối đa (giây).

    Returns:
        Phản hồi text từ Claude.

    Raises:
        RuntimeError: Nếu claude -p trả về exit code khác 0.
    """
    cmd = ["claude", "-p", "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])

    # Loại bỏ CLAUDECODE để cho phép gọi lồng nhau an toàn
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p thất bại (exit code {result.returncode})\n"
            f"stderr: {result.stderr.strip()}"
        )

    return result.stdout


def extract_description_from_response(response: str) -> str:
    """
    Trích xuất description từ thẻ <new_description>...</new_description>.
    Nếu không tìm thấy thẻ, dùng toàn bộ response đã được làm sạch.
    """
    match = re.search(r"<new_description>(.*?)</new_description>", response, re.DOTALL)
    raw = match.group(1) if match else response
    return raw.strip().strip('"')


# ─── Xây dựng Prompt ─────────────────────────────────────────────────────────

def _format_score_summary(train: EvalSummary, test: Optional[EvalSummary] = None) -> str:
    train_str = f"{train.passed}/{train.total}"
    if test:
        return f"Train: {train_str}, Test: {test.passed}/{test.total}"
    return f"Train: {train_str}"


def _format_failed_cases(cases: list[EvalCase], label: str) -> str:
    if not cases:
        return ""
    lines = [f"{label}:\n"]
    for case in cases:
        lines.append(f'  - "{case.query}" (triggered {case.triggers}/{case.runs} lan)\n')
    return "".join(lines) + "\n"


def _format_history(entries: list[HistoryEntry]) -> str:
    if not entries:
        return ""
    lines = ["PREVIOUS ATTEMPTS (khong lap lai - hay thu cach khac):\n\n"]
    for entry in entries:
        lines.append(f"<attempt {entry.score_string}>\n")
        lines.append(f'Description: "{entry.description}"\n')
        if entry.results:
            lines.append("Train results:\n")
            for r in entry.results:
                status = "PASS" if r["pass"] else "FAIL"
                lines.append(f'  [{status}] "{r["query"][:80]}" (triggered {r["triggers"]}/{r["runs"]})\n')
        if entry.note:
            lines.append(f"Note: {entry.note}\n")
        lines.append("</attempt>\n\n")
    return "".join(lines)


def build_improvement_prompt(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: EvalResults,
    history: list[HistoryEntry],
    test_results: Optional[EvalSummary] = None,
) -> str:
    """Xây dựng prompt đầy đủ để gửi cho Claude."""

    score_summary = _format_score_summary(eval_results.summary, test_results)
    failed_section = _format_failed_cases(
        eval_results.failed_triggers,
        "FAILED TO TRIGGER (nen trigger nhung khong trigger)"
    )
    false_section = _format_failed_cases(
        eval_results.false_triggers,
        "FALSE TRIGGERS (trigger nhung khong nen)"
    )
    history_section = _format_history(history)

    return f"""You are optimizing a skill description for a Claude Code skill called "{skill_name}".

A "skill" has a title + description (Claude reads to decide whether to use it),
and if used, reads the .md file for full details.

Current description:
<current_description>
"{current_description}"
</current_description>

Current scores ({score_summary}):
<scores_summary>
{failed_section}{false_section}{history_section}</scores_summary>

Skill content (for context on what the skill does):
<skill_content>
{skill_content}
</skill_content>

Based on the failures above, write an improved description. Guidelines:
- Do NOT list specific queries — generalize to broader user intent categories.
- Max 100-200 words. Hard limit: {MAX_DESCRIPTION_CHARS} characters.
- Use imperative: "Use this skill when..." not "This skill does..."
- Focus on user intent, not implementation details.
- Be creative and try different sentence structures across iterations.

Respond with ONLY the new description inside <new_description> tags, nothing else."""


# ─── Logic cải thiện chính ────────────────────────────────────────────────────

def shorten_if_needed(description: str, original_prompt: str, model: Optional[str]) -> str:
    """
    Nếu description vượt quá MAX_DESCRIPTION_CHARS, gọi Claude để rút gọn.
    Trả về description đã được rút gọn (hoặc nguyên bản nếu không cần).
    """
    if len(description) <= MAX_DESCRIPTION_CHARS:
        return description

    shorten_prompt = (
        f"{original_prompt}\n\n---\n\n"
        f"A previous attempt produced this description ({len(description)} chars), "
        f"which exceeds the {MAX_DESCRIPTION_CHARS}-character hard limit:\n\n"
        f'"{description}"\n\n'
        f"Rewrite it under {MAX_DESCRIPTION_CHARS} characters, keeping key trigger words. "
        f"Respond with ONLY the new description in <new_description> tags."
    )

    response = call_claude(shorten_prompt, model)
    return extract_description_from_response(response)


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: EvalResults,
    history: list[HistoryEntry],
    model: Optional[str],
    test_results: Optional[EvalSummary] = None,
    log_dir: Optional[Path] = None,
    iteration: Optional[int] = None,
) -> str:
    """
    Cải thiện description dựa trên kết quả eval.

    Args:
        skill_name:          Tên của skill.
        skill_content:       Nội dung file SKILL.md.
        current_description: Description hiện tại cần cải thiện.
        eval_results:        Kết quả eval đã parse.
        history:             Lịch sử các lần thử trước.
        model:               Model Claude sử dụng.
        test_results:        Kết quả test set (nếu có).
        log_dir:             Thư mục lưu log (None = không lưu).
        iteration:           Số lần lặp hiện tại (dùng để đặt tên file log).

    Returns:
        Description mới đã được cải thiện.
    """
    prompt = build_improvement_prompt(
        skill_name=skill_name,
        skill_content=skill_content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        test_results=test_results,
    )

    response = call_claude(prompt, model)
    description = extract_description_from_response(response)

    # Rút gọn nếu vượt giới hạn
    description = shorten_if_needed(description, prompt, model)

    # Lưu log nếu có log_dir
    if log_dir:
        _save_log(
            log_dir=log_dir,
            iteration=iteration,
            prompt=prompt,
            response=response,
            description=description,
        )

    return description


def _save_log(
    log_dir: Path,
    iteration: Optional[int],
    prompt: str,
    response: str,
    description: str,
) -> None:
    """Lưu log của một lần cải thiện vào file JSON."""
    log_dir.mkdir(parents=True, exist_ok=True)
    label = iteration if iteration is not None else "unknown"
    log_file = log_dir / f"improve_iter_{label}.json"
    log_file.write_text(json.dumps({
        "iteration":   iteration,
        "prompt":      prompt,
        "response":    response,
        "description": description,
        "char_count":  len(description),
        "over_limit":  len(description) > MAX_DESCRIPTION_CHARS,
    }, indent=2, ensure_ascii=False))


# ─── Đọc SKILL.md ────────────────────────────────────────────────────────────

def read_skill_md(skill_path: Path) -> tuple[str, str]:
    """
    Đọc file SKILL.md và trả về (tên skill, nội dung).
    Tên skill lấy từ tiêu đề H1 đầu tiên; nếu không có thì dùng tên thư mục.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"Khong tim thay SKILL.md tai: {skill_path}")

    content = skill_md.read_text(encoding="utf-8")

    # Tìm tiêu đề H1
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    name = match.group(1).strip() if match else skill_path.name

    return name, content


# ─── CLI ─────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cai thien mo ta skill dua tren ket qua eval",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--eval-results", required=True,
        help="Duong dan den file JSON ket qua eval (tu run_eval.py)",
    )
    parser.add_argument(
        "--skill-path", required=True,
        help="Duong dan den thu muc chua SKILL.md",
    )
    parser.add_argument(
        "--model", required=True,
        help="Model Claude dung de cai thien",
    )
    parser.add_argument(
        "--history", default=None,
        help="Duong dan den file JSON lich su (cac lan thu truoc)",
    )
    parser.add_argument(
        "--log-dir", default=None,
        help="Thu muc luu log (moi lan thu tao mot file rieng)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="In them thong tin ra stderr",
    )
    return parser.parse_args()


def load_history(history_path: Optional[str]) -> list[HistoryEntry]:
    """Tải lịch sử từ file JSON. Trả về list rỗng nếu không có."""
    if not history_path:
        return []

    raw = json.loads(Path(history_path).read_text(encoding="utf-8"))
    entries = []
    for h in raw:
        entries.append(HistoryEntry(
            description  = h["description"],
            train_passed = h.get("train_passed", h.get("passed", 0)),
            train_total  = h.get("train_total", h.get("total", 0)),
            test_passed  = h.get("test_passed"),
            test_total   = h.get("test_total"),
            results      = h.get("results", []),
            note         = h.get("note", ""),
        ))
    return entries


def main() -> None:
    args = parse_args()

    skill_path = Path(args.skill_path)
    log_dir    = Path(args.log_dir) if args.log_dir else None

    # Đọc dữ liệu đầu vào
    try:
        skill_name, skill_content = read_skill_md(skill_path)
    except FileNotFoundError as e:
        print(f"Loi: {e}", file=sys.stderr)
        sys.exit(1)

    eval_data    = json.loads(Path(args.eval_results).read_text(encoding="utf-8"))
    eval_results = EvalResults.from_dict(eval_data)
    history      = load_history(args.history)

    if args.verbose:
        print(f"Skill: {skill_name}", file=sys.stderr)
        print(f"Description hien tai: {eval_results.description}", file=sys.stderr)
        print(
            f"Diem: {eval_results.summary.passed}/{eval_results.summary.total}",
            file=sys.stderr,
        )

    # Cải thiện description
    new_description = improve_description(
        skill_name          = skill_name,
        skill_content       = skill_content,
        current_description = eval_results.description,
        eval_results        = eval_results,
        history             = history,
        model               = args.model,
        log_dir             = log_dir,
    )

    if args.verbose:
        print(f"Description moi ({len(new_description)} ky tu): {new_description}", file=sys.stderr)

    # Xuất kết quả JSON
    output = {
        "description": new_description,
        "history": [
            # Giữ nguyên các entry cũ dưới dạng dict để tương thích ngược
            *(
                {
                    "description":   h.description,
                    "train_passed":  h.train_passed,
                    "train_total":   h.train_total,
                    "test_passed":   h.test_passed,
                    "test_total":    h.test_total,
                    "results":       h.results,
                    "note":          h.note,
                }
                for h in history
            ),
            # Thêm lần thử hiện tại vào lịch sử
            {
                "description":  eval_results.description,
                "train_passed": eval_results.summary.passed,
                "train_total":  eval_results.summary.total,
                "results":      eval_data["results"],
            },
        ],
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()