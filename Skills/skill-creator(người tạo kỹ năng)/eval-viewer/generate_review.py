#!/usr/bin/env python3
"""
generate_review.py
------------------
Tạo trang HTML review kết quả eval và serve qua HTTP server nhỏ gọn.

Đọc workspace, tìm các run (thư mục chứa outputs/), nhúng toàn bộ dữ liệu
vào trang HTML tự chứa (self-contained), rồi serve qua HTTP server stdlib.
Feedback được tự động lưu vào feedback.json trong workspace.

Cách dùng:
    python generate_review.py <workspace-path>
    python generate_review.py <workspace-path> --port 8080 --skill-name "MySkill"
    python generate_review.py <workspace-path> --static output.html
    python generate_review.py <workspace-path> --previous-workspace /path/to/prev/

Không cần cài thêm thư viện ngoài (chỉ dùng stdlib).
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import signal
import subprocess
import sys
import time
import webbrowser
from dataclasses import dataclass, field
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


# ---------------------------------------------------------------------------
# Hằng số
# ---------------------------------------------------------------------------

# Các file metadata — không hiển thị trong danh sách output
METADATA_FILES: frozenset[str] = frozenset({"transcript.md", "user_notes.md", "metrics.json"})

# Đuôi file hiển thị dạng text inline
TEXT_EXTENSIONS: frozenset[str] = frozenset({
    ".txt", ".md", ".json", ".csv", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".yaml", ".yml", ".xml", ".html", ".css", ".sh", ".rb", ".go", ".rs",
    ".java", ".c", ".cpp", ".h", ".hpp", ".sql", ".r", ".toml",
})

# Đuôi file hiển thị dạng ảnh inline
IMAGE_EXTENSIONS: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"})

# Ghi đè MIME type cho một số định dạng phổ biến
MIME_OVERRIDES: dict[str, str] = {
    ".svg":  "image/svg+xml",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

# Thư mục bỏ qua khi duyệt đệ quy
SKIP_DIRS: frozenset[str] = frozenset({"node_modules", ".git", "__pycache__", "skill", "inputs"})


# ---------------------------------------------------------------------------
# Kiểu dữ liệu
# ---------------------------------------------------------------------------

RunDict      = dict   # Kết quả một lần chạy eval
FileDict     = dict   # File đã nhúng (text/image/pdf/binary)
PreviousData = dict[str, dict]  # run_id → {"feedback": str, "outputs": list}


# ---------------------------------------------------------------------------
# Tiện ích: MIME type
# ---------------------------------------------------------------------------

def get_mime_type(path: Path) -> str:
    """Trả về MIME type của file, ưu tiên MIME_OVERRIDES."""
    ext = path.suffix.lower()
    if ext in MIME_OVERRIDES:
        return MIME_OVERRIDES[ext]
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


# ---------------------------------------------------------------------------
# Nhúng file vào dict (embed)
# ---------------------------------------------------------------------------

def _read_as_base64(path: Path) -> str | None:
    """Đọc file binary và trả về chuỗi base64. None nếu lỗi."""
    try:
        return base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return None


def embed_file(path: Path) -> FileDict:
    """
    Đọc file và trả về dict mô tả nội dung để nhúng vào HTML.

    Phân loại theo đuôi file:
    - Text      → {"type": "text",   "content": str}
    - Ảnh       → {"type": "image",  "data_uri": str}
    - PDF       → {"type": "pdf",    "data_uri": str}
    - Excel     → {"type": "xlsx",   "data_b64": str}
    - Còn lại   → {"type": "binary", "data_uri": str}
    """
    ext  = path.suffix.lower()
    mime = get_mime_type(path)
    base = {"name": path.name}

    # --- Text ---
    if ext in TEXT_EXTENSIONS:
        try:
            return {**base, "type": "text", "content": path.read_text(encoding="utf-8", errors="replace")}
        except OSError:
            return {**base, "type": "error", "content": "(Error reading file)"}

    # --- Ảnh inline ---
    if ext in IMAGE_EXTENSIONS:
        b64 = _read_as_base64(path)
        if b64 is None:
            return {**base, "type": "error", "content": "(Error reading file)"}
        return {**base, "type": "image", "mime": mime, "data_uri": f"data:{mime};base64,{b64}"}

    # --- PDF ---
    if ext == ".pdf":
        b64 = _read_as_base64(path)
        if b64 is None:
            return {**base, "type": "error", "content": "(Error reading file)"}
        return {**base, "type": "pdf", "data_uri": f"data:{mime};base64,{b64}"}

    # --- Excel ---
    if ext == ".xlsx":
        b64 = _read_as_base64(path)
        if b64 is None:
            return {**base, "type": "error", "content": "(Error reading file)"}
        return {**base, "type": "xlsx", "data_b64": b64}

    # --- Binary / unknown → link download ---
    b64 = _read_as_base64(path)
    if b64 is None:
        return {**base, "type": "error", "content": "(Error reading file)"}
    return {**base, "type": "binary", "mime": mime, "data_uri": f"data:{mime};base64,{b64}"}


# ---------------------------------------------------------------------------
# Đọc metadata và transcript
# ---------------------------------------------------------------------------

def _try_read_json(path: Path) -> dict | None:
    """Đọc và parse JSON. Trả về None nếu file không tồn tại hoặc lỗi."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _extract_prompt_from_transcript(path: Path) -> str:
    """Trích xuất phần 'Eval Prompt' từ file transcript.md."""
    try:
        text  = path.read_text(encoding="utf-8")
        match = re.search(r"## Eval Prompt\n\n([\s\S]*?)(?=\n##|$)", text)
        return match.group(1).strip() if match else ""
    except OSError:
        return ""


def load_prompt_and_eval_id(run_dir: Path) -> tuple[str, object]:
    """
    Lấy prompt và eval_id cho một run.

    Thứ tự ưu tiên:
    1. eval_metadata.json trong run_dir
    2. eval_metadata.json trong thư mục cha
    3. transcript.md trong run_dir
    4. transcript.md trong outputs/
    """
    # Thử đọc từ eval_metadata.json
    for candidate in (run_dir / "eval_metadata.json", run_dir.parent / "eval_metadata.json"):
        meta = _try_read_json(candidate)
        if meta and meta.get("prompt"):
            return meta["prompt"], meta.get("eval_id")

    # Thử đọc từ transcript.md
    for candidate in (run_dir / "transcript.md", run_dir / "outputs" / "transcript.md"):
        prompt = _extract_prompt_from_transcript(candidate)
        if prompt:
            return prompt, None

    return "(No prompt found)", None


def load_grading(run_dir: Path) -> dict | None:
    """Đọc grading.json từ run_dir hoặc thư mục cha."""
    for candidate in (run_dir / "grading.json", run_dir.parent / "grading.json"):
        data = _try_read_json(candidate)
        if data:
            return data
    return None


# ---------------------------------------------------------------------------
# Tìm và xây dựng danh sách runs
# ---------------------------------------------------------------------------

def _collect_output_files(run_dir: Path) -> list[FileDict]:
    """Đọc và nhúng tất cả file trong outputs/ (bỏ qua METADATA_FILES)."""
    outputs_dir = run_dir / "outputs"
    if not outputs_dir.is_dir():
        return []
    return [
        embed_file(f)
        for f in sorted(outputs_dir.iterdir())
        if f.is_file() and f.name not in METADATA_FILES
    ]


def build_run(root: Path, run_dir: Path) -> RunDict | None:
    """
    Xây dựng dict đầy đủ cho một run.

    Bao gồm: prompt, eval_id, output files (đã nhúng), và grading.
    """
    prompt, eval_id = load_prompt_and_eval_id(run_dir)
    run_id = str(run_dir.relative_to(root)).replace("/", "-").replace("\\", "-")

    return {
        "id":       run_id,
        "prompt":   prompt,
        "eval_id":  eval_id,
        "outputs":  _collect_output_files(run_dir),
        "grading":  load_grading(run_dir),
    }


def _find_runs_recursive(root: Path, current: Path, runs: list[RunDict]) -> None:
    """Duyệt đệ quy, thu thập run từ các thư mục chứa outputs/."""
    if not current.is_dir():
        return

    if (current / "outputs").is_dir():
        run = build_run(root, current)
        if run:
            runs.append(run)
        return  # Không duyệt sâu hơn vào run đã tìm thấy

    for child in sorted(current.iterdir()):
        if child.is_dir() and child.name not in SKIP_DIRS:
            _find_runs_recursive(root, child, runs)


def find_runs(workspace: Path) -> list[RunDict]:
    """
    Tìm tất cả runs trong workspace (đệ quy).

    Một run là thư mục chứa subdirectory outputs/.
    Kết quả được sắp xếp theo (eval_id, run_id).
    """
    runs: list[RunDict] = []
    _find_runs_recursive(workspace, workspace, runs)
    runs.sort(key=lambda r: (r.get("eval_id") or float("inf"), r["id"]))
    return runs


# ---------------------------------------------------------------------------
# Đọc dữ liệu iteration trước
# ---------------------------------------------------------------------------

def load_previous_iteration(workspace: Path) -> PreviousData:
    """
    Đọc feedback và outputs từ workspace của iteration trước.

    Trả về: { run_id → {"feedback": str, "outputs": list} }
    """
    # Đọc feedback đã lưu
    feedback_map: dict[str, str] = {}
    data = _try_read_json(workspace / "feedback.json")
    if data:
        feedback_map = {
            r["run_id"]: r["feedback"]
            for r in data.get("reviews", [])
            if r.get("feedback", "").strip()
        }

    # Gắn feedback vào từng run
    result: PreviousData = {}
    for run in find_runs(workspace):
        result[run["id"]] = {
            "feedback": feedback_map.get(run["id"], ""),
            "outputs":  run.get("outputs", []),
        }

    # Thêm feedback của các run không còn tồn tại
    for run_id, fb in feedback_map.items():
        if run_id not in result:
            result[run_id] = {"feedback": fb, "outputs": []}

    return result


# ---------------------------------------------------------------------------
# Tạo HTML
# ---------------------------------------------------------------------------

def generate_html(
    runs:       list[RunDict],
    skill_name: str,
    previous:   PreviousData | None = None,
    benchmark:  dict | None = None,
) -> str:
    """
    Tạo trang HTML tự chứa (standalone) với toàn bộ dữ liệu nhúng bên trong.

    Đọc template viewer.html từ cùng thư mục và thay thế placeholder
    /*__EMBEDDED_DATA__*/ bằng JSON thực tế.
    """
    template_path = Path(__file__).parent / "viewer.html"
    template = template_path.read_text(encoding="utf-8")

    previous_feedback: dict[str, str]       = {}
    previous_outputs:  dict[str, list[dict]] = {}
    if previous:
        for run_id, data in previous.items():
            if data.get("feedback"):
                previous_feedback[run_id] = data["feedback"]
            if data.get("outputs"):
                previous_outputs[run_id]  = data["outputs"]

    embedded: dict = {
        "skill_name":        skill_name,
        "runs":              runs,
        "previous_feedback": previous_feedback,
        "previous_outputs":  previous_outputs,
    }
    if benchmark:
        embedded["benchmark"] = benchmark

    data_json = json.dumps(embedded, ensure_ascii=False)
    return template.replace("/*__EMBEDDED_DATA__*/", f"const EMBEDDED_DATA = {data_json};")


# ---------------------------------------------------------------------------
# Quản lý cổng (port)
# ---------------------------------------------------------------------------

def _kill_port(port: int) -> None:
    """
    Dừng tiến trình đang dùng cổng `port` (chỉ hỗ trợ Linux/macOS).

    Trên Windows, bước này bị bỏ qua một cách an toàn.
    """
    if sys.platform == "win32":
        return  # lsof không có trên Windows

    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True, text=True, timeout=5,
        )
        for pid_str in result.stdout.strip().splitlines():
            pid = pid_str.strip()
            if pid:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except (ProcessLookupError, ValueError):
                    pass
        if result.stdout.strip():
            time.sleep(0.5)
    except subprocess.TimeoutExpired:
        pass
    except FileNotFoundError:
        print("Lưu ý: lsof không tìm thấy, bỏ qua kiểm tra cổng.", file=sys.stderr)


# ---------------------------------------------------------------------------
# HTTP Server
# ---------------------------------------------------------------------------

@dataclass
class ServerConfig:
    """Cấu hình được chia sẻ giữa các request handler."""
    workspace:     Path
    skill_name:    str
    feedback_path: Path
    previous:      PreviousData = field(default_factory=dict)
    benchmark_path: Path | None = None


class ReviewHandler(BaseHTTPRequestHandler):
    """
    HTTP handler phục vụ trang review và lưu feedback.

    - GET  /              → Tạo lại HTML từ workspace (tự động cập nhật khi refresh)
    - GET  /api/feedback  → Đọc feedback.json hiện tại
    - POST /api/feedback  → Lưu feedback mới vào feedback.json
    """

    config: ServerConfig  # Được gán bởi partial() trong main()

    def __init__(self, config: ServerConfig, *args, **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)

    # --- Helpers ---

    def _send_json(self, status: int, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, content: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    # --- Routing ---

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self._handle_page()
        elif self.path == "/api/feedback":
            self._handle_get_feedback()
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if self.path == "/api/feedback":
            self._handle_post_feedback()
        else:
            self.send_error(404)

    # --- Handlers ---

    def _handle_page(self) -> None:
        """Tạo lại HTML từ workspace mỗi lần request (tự cập nhật khi có run mới)."""
        cfg = self.config
        runs = find_runs(cfg.workspace)

        benchmark = None
        if cfg.benchmark_path and cfg.benchmark_path.exists():
            benchmark = _try_read_json(cfg.benchmark_path)

        html = generate_html(runs, cfg.skill_name, cfg.previous, benchmark)
        self._send_html(html.encode("utf-8"))

    def _handle_get_feedback(self) -> None:
        """Trả về nội dung feedback.json."""
        cfg = self.config
        data = cfg.feedback_path.read_bytes() if cfg.feedback_path.exists() else b"{}"
        self._send_json(200, data)

    def _handle_post_feedback(self) -> None:
        """Nhận và lưu feedback JSON vào feedback.json."""
        cfg    = self.config
        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length)

        try:
            data = json.loads(body)
            if not isinstance(data, dict) or "reviews" not in data:
                raise ValueError("Expected JSON object with 'reviews' key")
            cfg.feedback_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            self._send_json(200, b'{"ok":true}')
        except (json.JSONDecodeError, OSError, ValueError) as e:
            self._send_json(500, json.dumps({"error": str(e)}).encode("utf-8"))

    def log_message(self, format: str, *args: object) -> None:
        pass  # Tắt log request để terminal gọn hơn


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _start_server(config: ServerConfig, port: int) -> tuple[HTTPServer, int]:
    """Khởi động HTTP server. Tự động chọn cổng trống nếu cổng yêu cầu bận."""
    _kill_port(port)
    handler = partial(ReviewHandler, config)
    try:
        server = HTTPServer(("127.0.0.1", port), handler)
    except OSError:
        # Cổng vẫn bận → để OS tự chọn cổng trống
        server = HTTPServer(("127.0.0.1", 0), handler)
        port   = server.server_address[1]
    return server, port


def main() -> None:
    parser = argparse.ArgumentParser(description="Tạo và serve trang review kết quả eval")
    parser.add_argument("workspace", type=Path, help="Đường dẫn tới thư mục workspace")
    parser.add_argument("--port", "-p", type=int, default=3117, help="Cổng server (mặc định: 3117)")
    parser.add_argument("--skill-name", "-n", type=str, default=None, help="Tên kỹ năng hiển thị")
    parser.add_argument(
        "--previous-workspace", type=Path, default=None,
        help="Workspace của iteration trước (hiển thị output và feedback cũ làm context)",
    )
    parser.add_argument(
        "--benchmark", type=Path, default=None,
        help="Đường dẫn tới benchmark.json để hiển thị tab Benchmark",
    )
    parser.add_argument(
        "--static", "-s", type=Path, default=None,
        help="Xuất HTML tĩnh ra file này thay vì khởi động server",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"❌ Không phải thư mục: {workspace}", file=sys.stderr)
        sys.exit(1)

    runs = find_runs(workspace)
    if not runs:
        print(f"❌ Không tìm thấy run nào trong: {workspace}", file=sys.stderr)
        sys.exit(1)

    skill_name    = args.skill_name or workspace.name.replace("-workspace", "")
    feedback_path = workspace / "feedback.json"
    previous: PreviousData = {}

    if args.previous_workspace:
        previous = load_previous_iteration(args.previous_workspace.resolve())

    benchmark_path = args.benchmark.resolve() if args.benchmark else None
    benchmark = _try_read_json(benchmark_path) if benchmark_path else None

    # --- Chế độ xuất file tĩnh ---
    if args.static:
        html = generate_html(runs, skill_name, previous, benchmark)
        args.static.parent.mkdir(parents=True, exist_ok=True)
        args.static.write_text(html, encoding="utf-8")
        print(f"\n✅ HTML tĩnh đã được lưu tại: {args.static}\n")
        sys.exit(0)

    # --- Chế độ HTTP server ---
    config = ServerConfig(
        workspace=workspace,
        skill_name=skill_name,
        feedback_path=feedback_path,
        previous=previous,
        benchmark_path=benchmark_path,
    )

    server, port = _start_server(config, args.port)
    url = f"http://localhost:{port}"

    print(f"\n  🌿 Eval Viewer")
    print(f"  {'─' * 40}")
    print(f"  URL       : {url}")
    print(f"  Workspace : {workspace}")
    print(f"  Feedback  : {feedback_path}")
    if previous:
        print(f"  Previous  : {args.previous_workspace} ({len(previous)} runs)")
    if benchmark_path:
        print(f"  Benchmark : {benchmark_path}")
    print(f"\n  Nhấn Ctrl+C để dừng.\n")

    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⛔ Đã dừng server.")
        server.server_close()


if __name__ == "__main__":
    main()