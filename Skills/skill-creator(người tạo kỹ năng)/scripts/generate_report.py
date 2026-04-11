#!/usr/bin/env python3
"""
report_generator.py
-------------------
Tạo báo cáo HTML từ kết quả tối ưu hóa mô tả kỹ năng AI (skill description).

Cách dùng:
    python report_generator.py input.json -o output.html --skill-name "MySkill"
    python report_generator.py - -o output.html   # đọc từ stdin
"""

import argparse
import html
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Kiểu dữ liệu (type aliases) — giúp code dễ đọc hơn
# ---------------------------------------------------------------------------
QueryInfo = dict       # {"query": str, "should_trigger": bool}
ResultMap = dict       # {query_str: result_dict}
HistoryEntry = dict    # một iteration trong lịch sử tối ưu hóa


# ---------------------------------------------------------------------------
# CSS — tách riêng để dễ chỉnh sửa giao diện
# ---------------------------------------------------------------------------
STYLES = """
    body {
        font-family: 'Lora', Georgia, serif;
        max-width: 100%;
        margin: 0 auto;
        padding: 20px;
        background: #faf9f5;
        color: #141413;
    }
    h1 { font-family: 'Poppins', sans-serif; color: #141413; }

    /* --- Hộp giải thích --- */
    .explainer {
        background: white;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        border: 1px solid #e8e6dc;
        color: #b0aea5;
        font-size: 0.875rem;
        line-height: 1.6;
    }

    /* --- Hộp tóm tắt --- */
    .summary {
        background: white;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        border: 1px solid #e8e6dc;
    }
    .summary p { margin: 5px 0; }
    .best { color: #788c5d; font-weight: bold; }

    /* --- Bảng kết quả --- */
    .table-container { overflow-x: auto; width: 100%; }
    table {
        border-collapse: collapse;
        background: white;
        border: 1px solid #e8e6dc;
        border-radius: 6px;
        font-size: 12px;
        min-width: 100%;
    }
    th, td {
        padding: 8px;
        text-align: left;
        border: 1px solid #e8e6dc;
        white-space: normal;
        word-wrap: break-word;
    }
    th {
        font-family: 'Poppins', sans-serif;
        background: #141413;
        color: #faf9f5;
        font-weight: 500;
    }
    th.test-col { background: #6a9bcc; }
    th.query-col { min-width: 200px; }

    td.description {
        font-family: monospace;
        font-size: 11px;
        word-wrap: break-word;
        max-width: 400px;
    }
    td.result { text-align: center; font-size: 16px; min-width: 40px; }
    td.test-result { background: #f0f6fc; }

    .pass { color: #788c5d; }
    .fail { color: #c44; }
    .rate { font-size: 9px; color: #b0aea5; display: block; }

    tr:hover { background: #faf9f5; }
    .best-row { background: #f5f8f2; }

    /* --- Nhãn điểm số --- */
    .score {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 11px;
    }
    .score-good { background: #eef2e8; color: #788c5d; }
    .score-ok   { background: #fef3c7; color: #d97706; }
    .score-bad  { background: #fceaea; color: #c44; }

    /* --- Đường viền dưới cột (phân biệt positive/negative) --- */
    th.positive-col { border-bottom: 3px solid #788c5d; }
    th.negative-col { border-bottom: 3px solid #c44; }
    th.test-col.positive-col { border-bottom: 3px solid #788c5d; }
    th.test-col.negative-col { border-bottom: 3px solid #c44; }

    /* --- Chú thích bảng màu --- */
    .legend {
        font-family: 'Poppins', sans-serif;
        display: flex;
        gap: 20px;
        margin-bottom: 10px;
        font-size: 13px;
        align-items: center;
    }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-swatch { width: 16px; height: 16px; border-radius: 3px; display: inline-block; }
    .swatch-positive { background: #141413; border-bottom: 3px solid #788c5d; }
    .swatch-negative { background: #141413; border-bottom: 3px solid #c44; }
    .swatch-test  { background: #6a9bcc; }
    .swatch-train { background: #141413; }
"""


# ---------------------------------------------------------------------------
# Các hàm tiện ích nhỏ
# ---------------------------------------------------------------------------

def score_class(correct: int, total: int) -> str:
    """Trả về class CSS dựa trên tỉ lệ đúng/tổng."""
    if total > 0 and (correct / total) >= 0.8:
        return "score-good"
    if total > 0 and (correct / total) >= 0.5:
        return "score-ok"
    return "score-bad"


def aggregate_runs(results: list[dict]) -> tuple[int, int]:
    """
    Tính tổng số lần đúng và tổng số lần chạy qua tất cả kết quả.

    Trả về: (số lần đúng, tổng số lần chạy)
    """
    correct = 0
    total = 0
    for r in results:
        runs     = r.get("runs", 0)
        triggers = r.get("triggers", 0)
        total   += runs
        # Nếu nên trigger → đúng khi trigger; nếu không nên → đúng khi KHÔNG trigger
        correct += triggers if r.get("should_trigger", True) else (runs - triggers)
    return correct, total


def extract_queries(results: list[dict]) -> list[QueryInfo]:
    """Lấy danh sách query và cờ should_trigger từ danh sách kết quả."""
    return [
        {"query": r["query"], "should_trigger": r.get("should_trigger", True)}
        for r in results
    ]


def find_best_iteration(history: list[HistoryEntry], has_test: bool) -> int | str:
    """Tìm iteration có điểm cao nhất (ưu tiên test nếu có)."""
    if has_test:
        return max(history, key=lambda h: h.get("test_passed") or 0).get("iteration")
    return max(history, key=lambda h: h.get("train_passed", h.get("passed", 0))).get("iteration")


# ---------------------------------------------------------------------------
# Các hàm tạo từng phần HTML
# ---------------------------------------------------------------------------

def build_html_head(title_prefix: str, auto_refresh: bool) -> str:
    """Tạo phần <head> của HTML."""
    refresh_tag = '    <meta http-equiv="refresh" content="5">\n' if auto_refresh else ""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
{refresh_tag}    <title>{title_prefix}Skill Description Optimization</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Lora:wght@400;500&display=swap" rel="stylesheet">
    <style>
{STYLES}
    </style>
</head>
<body>
    <h1>{title_prefix}Skill Description Optimization</h1>
"""


def build_explainer() -> str:
    """Tạo hộp giải thích ở đầu trang."""
    return """
    <div class="explainer">
        <strong>Optimizing your skill's description.</strong>
        This page updates automatically as Claude tests different versions of your skill's description.
        Each row is an iteration — a new description attempt. The columns show test queries:
        green checkmarks mean the skill triggered correctly (or correctly didn't trigger),
        red crosses mean it got it wrong. The "Train" score shows performance on queries used
        to improve the description; the "Test" score shows performance on held-out queries
        the optimizer hasn't seen. When it's done, Claude will apply the best-performing
        description to your skill.
    </div>
"""


def build_summary(data: dict) -> str:
    """Tạo hộp tóm tắt thông tin chạy."""
    best_test_score = data.get("best_test_score")
    score_label     = "(test)" if best_test_score else "(train)"
    return f"""
    <div class="summary">
        <p><strong>Original:</strong> {html.escape(data.get('original_description', 'N/A'))}</p>
        <p class="best"><strong>Best:</strong> {html.escape(data.get('best_description', 'N/A'))}</p>
        <p><strong>Best Score:</strong> {data.get('best_score', 'N/A')} {score_label}</p>
        <p>
            <strong>Iterations:</strong> {data.get('iterations_run', 0)} |
            <strong>Train:</strong> {data.get('train_size', '?')} |
            <strong>Test:</strong> {data.get('test_size', '?')}
        </p>
    </div>
"""


def build_legend() -> str:
    """Tạo chú thích màu sắc bên trên bảng."""
    return """
    <div class="legend">
        <span style="font-weight:600">Query columns:</span>
        <span class="legend-item"><span class="legend-swatch swatch-positive"></span> Should trigger</span>
        <span class="legend-item"><span class="legend-swatch swatch-negative"></span> Should NOT trigger</span>
        <span class="legend-item"><span class="legend-swatch swatch-train"></span> Train</span>
        <span class="legend-item"><span class="legend-swatch swatch-test"></span> Test</span>
    </div>
"""


def build_table_header(train_queries: list[QueryInfo], test_queries: list[QueryInfo]) -> str:
    """Tạo hàng tiêu đề (<thead>) của bảng."""
    parts = ["""
    <div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Iter</th>
                <th>Train</th>
                <th>Test</th>
                <th class="query-col">Description</th>
"""]

    # Cột Train queries
    for q in train_queries:
        polarity = "positive-col" if q["should_trigger"] else "negative-col"
        parts.append(f'                <th class="{polarity}">{html.escape(q["query"])}</th>\n')

    # Cột Test queries (màu khác)
    for q in test_queries:
        polarity = "positive-col" if q["should_trigger"] else "negative-col"
        parts.append(f'                <th class="test-col {polarity}">{html.escape(q["query"])}</th>\n')

    parts.append("            </tr>\n        </thead>\n        <tbody>\n")
    return "".join(parts)


def build_result_cell(result: dict, is_test: bool = False) -> str:
    """Tạo một ô <td> kết quả (✓ hoặc ✗) cho một query."""
    did_pass = result.get("pass", False)
    triggers = result.get("triggers", 0)
    runs     = result.get("runs", 0)

    icon     = "✓" if did_pass else "✗"
    css      = "pass" if did_pass else "fail"
    test_cls = " test-result" if is_test else ""

    return f'                <td class="result{test_cls} {css}">{icon}<span class="rate">{triggers}/{runs}</span></td>\n'


def build_table_rows(
    history: list[HistoryEntry],
    train_queries: list[QueryInfo],
    test_queries: list[QueryInfo],
    best_iter: int | str,
) -> str:
    """Tạo tất cả các hàng dữ liệu (<tbody>) của bảng."""
    parts = []

    for entry in history:
        iteration     = entry.get("iteration", "?")
        train_results = entry.get("train_results", entry.get("results", []))
        test_results  = entry.get("test_results", [])

        # Bảng tra cứu nhanh theo query string
        train_by_query: ResultMap = {r["query"]: r for r in train_results}
        test_by_query:  ResultMap = {r["query"]: r for r in test_results}

        # Tính điểm
        train_ok, train_total = aggregate_runs(train_results)
        test_ok,  test_total  = aggregate_runs(test_results)

        train_cls = score_class(train_ok, train_total)
        test_cls  = score_class(test_ok,  test_total)
        row_cls   = "best-row" if iteration == best_iter else ""

        description = html.escape(entry.get("description", ""))

        parts.append(f"""            <tr class="{row_cls}">
                <td>{iteration}</td>
                <td><span class="score {train_cls}">{train_ok}/{train_total}</span></td>
                <td><span class="score {test_cls}">{test_ok}/{test_total}</span></td>
                <td class="description">{description}</td>
""")

        # Ô kết quả cho từng Train query
        for q in train_queries:
            parts.append(build_result_cell(train_by_query.get(q["query"], {}), is_test=False))

        # Ô kết quả cho từng Test query
        for q in test_queries:
            parts.append(build_result_cell(test_by_query.get(q["query"], {}), is_test=True))

        parts.append("            </tr>\n")

    return "".join(parts)


# ---------------------------------------------------------------------------
# Hàm tổng hợp chính
# ---------------------------------------------------------------------------

def generate_html(data: dict, auto_refresh: bool = False, skill_name: str = "") -> str:
    """
    Tạo báo cáo HTML hoàn chỉnh từ dữ liệu JSON của run_loop.

    Args:
        data:         Dữ liệu JSON đã được parse thành dict.
        auto_refresh: Nếu True, trang tự reload mỗi 5 giây.
        skill_name:   Tên kỹ năng hiển thị trong tiêu đề trang.

    Returns:
        Chuỗi HTML hoàn chỉnh.
    """
    history = data.get("history", [])
    title_prefix = html.escape(f"{skill_name} — ") if skill_name else ""

    # Lấy danh sách query từ iteration đầu tiên
    first = history[0] if history else {}
    train_queries = extract_queries(first.get("train_results", first.get("results", [])))
    test_queries  = extract_queries(first.get("test_results", []))

    best_iter = find_best_iteration(history, has_test=bool(test_queries))

    # Ghép từng phần lại
    return "".join([
        build_html_head(title_prefix, auto_refresh),
        build_explainer(),
        build_summary(data),
        build_legend(),
        build_table_header(train_queries, test_queries),
        build_table_rows(history, train_queries, test_queries, best_iter),
        "        </tbody>\n    </table>\n    </div>\n</body>\n</html>\n",
    ])


# ---------------------------------------------------------------------------
# Entry point — xử lý argument dòng lệnh
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tạo báo cáo HTML từ kết quả chạy run_loop.py"
    )
    parser.add_argument(
        "input",
        help="Đường dẫn tới file JSON (hoặc '-' để đọc từ stdin)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="File HTML đầu ra (mặc định: in ra stdout)",
    )
    parser.add_argument(
        "--skill-name",
        default="",
        help="Tên kỹ năng hiển thị trong tiêu đề báo cáo",
    )
    parser.add_argument(
        "--auto-refresh",
        action="store_true",
        help="Thêm meta refresh để trang tự reload mỗi 5 giây",
    )
    args = parser.parse_args()

    # Đọc dữ liệu đầu vào
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    # Tạo HTML
    html_output = generate_html(data, auto_refresh=args.auto_refresh, skill_name=args.skill_name)

    # Xuất kết quả
    if args.output:
        Path(args.output).write_text(html_output, encoding="utf-8")
        print(f"✅ Báo cáo đã được lưu tại: {args.output}", file=sys.stderr)
    else:
        print(html_output)


if __name__ == "__main__":
    main()