# Phân tích JSON Schemas — Hệ thống skill-creator

## Tổng quan

File `schemas.md` định nghĩa **cấu trúc dữ liệu JSON** cho toàn bộ hệ thống **skill-creator** — một hệ thống tự động tạo, đánh giá và cải thiện "skill" cho Claude Code.

Hệ thống chạy theo vòng lặp:

```
Eval → Chạy → Chấm → Phân tích → Cải thiện → (lặp lại)
```

---

## Sơ đồ luồng dữ liệu

```
ĐẦU VÀO          XỬ LÝ              ĐẦU RA THÔ
──────────        ──────────         ──────────────
evals.json  ──→                ──→  timing.json
                Skill executor
history.json ──→               ──→  metrics.json
                     │
                     ↓
                grading.json
               ↙      ↓      ↘
benchmark.json  comparison.json  analysis.json

              KẾT QUẢ CUỐI
```

---

## Chi tiết từng file JSON

### 1. `evals.json` — Bộ đề kiểm tra

**Vị trí:** `evals/evals.json` trong thư mục skill

**Mục đích:** Đây là điểm xuất phát. Định nghĩa các bài kiểm tra cho skill — giống như "đề thi".

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": ["The output includes X", "The skill used script Y"]
    }
  ]
}
```

**Các trường quan trọng:**

| Trường                    | Kiểu    | Mô tả                                          |
| ------------------------- | ------- | ---------------------------------------------- |
| `skill_name`              | string  | Tên skill, khớp với frontmatter                |
| `evals[].id`              | integer | ID duy nhất của từng bài test                  |
| `evals[].prompt`          | string  | Câu lệnh/nhiệm vụ cần thực thi                 |
| `evals[].expected_output` | string  | Mô tả kết quả mong đợi (dạng text)             |
| `evals[].files`           | array   | Danh sách file đính kèm (tuỳ chọn)             |
| `evals[].expectations`    | array   | Danh sách tiêu chí cần đạt (có thể kiểm chứng) |

---

### 2. `history.json` — Lịch sử cải tiến

**Vị trí:** Thư mục gốc của workspace

**Mục đích:** Theo dõi các phiên bản `v0, v1, v2...` qua từng lần cải thiện. Đây là "bộ nhớ" của vòng lặp cải tiến.

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**Các trường quan trọng:**

| Trường                               | Kiểu        | Mô tả                                         |
| ------------------------------------ | ----------- | --------------------------------------------- |
| `current_best`                       | string      | Version tốt nhất hiện tại (vd: "v2")          |
| `iterations[].version`               | string      | Tên version: v0, v1, v2...                    |
| `iterations[].parent`                | string/null | Version cha (sinh ra từ đâu)                  |
| `iterations[].expectation_pass_rate` | float       | Tỉ lệ đạt (0.0 → 1.0)                         |
| `iterations[].grading_result`        | string      | `"baseline"`, `"won"`, `"lost"`, hoặc `"tie"` |

---

### 3. `metrics.json` — Số liệu kỹ thuật

**Vị trí:** `<run-dir>/outputs/metrics.json`

**Mục đích:** Executor ghi lại trong quá trình chạy — bao nhiêu tool call, bao nhiêu bước, file nào được tạo ra, có lỗi không.

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

**Các trường quan trọng:**

| Trường               | Mô tả                                            |
| -------------------- | ------------------------------------------------ |
| `tool_calls`         | Số lần gọi từng loại tool (Read, Write, Bash...) |
| `total_tool_calls`   | Tổng tất cả tool calls                           |
| `files_created`      | Danh sách file output được tạo                   |
| `errors_encountered` | Số lỗi xảy ra trong quá trình chạy               |

---

### 4. `timing.json` — Thời gian thực thi

**Vị trí:** `<run-dir>/timing.json`

**Mục đích:** Lưu thời điểm bắt đầu/kết thúc và tổng token tiêu thụ.

> ⚠️ **Quan trọng:** Phải lưu ngay khi task hoàn thành. Dữ liệu `total_tokens` và `duration_ms` chỉ có trong thông báo kết thúc task — **không thể lấy lại sau đó**.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z",
  "executor_duration_seconds": 165.0,
  "grader_start": "2026-01-15T10:32:46Z",
  "grader_end": "2026-01-15T10:33:12Z",
  "grader_duration_seconds": 26.0
}
```

---

### 5. `grading.json` — Kết quả chấm điểm ⭐

**Vị trí:** `<run-dir>/grading.json`

**Mục đích:** File trung tâm nhất sau khi chạy xong. Tổng hợp toàn bộ kết quả từ executor, chấm từng `expectation`, và gợi ý cải thiện.

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in transcript Step 3: 'Extracted names: John Smith'"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "execution_metrics": { ... },
  "timing": { ... },
  "eval_feedback": {
    "suggestions": [...],
    "overall": "Assertions check presence but not correctness."
  }
}
```

**Các trường quan trọng:**

| Trường               | Mô tả                                                        |
| -------------------- | ------------------------------------------------------------ |
| `expectations[]`     | Từng tiêu chí: đạt/không đạt + bằng chứng cụ thể             |
| `summary.pass_rate`  | Tỉ lệ đạt tổng thể (0.0 → 1.0)                               |
| `execution_metrics`  | Nhúng dữ liệu từ `metrics.json`                              |
| `timing`             | Nhúng dữ liệu từ `timing.json`                               |
| `eval_feedback`      | Gợi ý cải thiện bộ eval (chỉ có khi grader phát hiện vấn đề) |
| `user_notes_summary` | Các vấn đề executor tự ghi chú (bất định, workaround...)     |

---

### 6. `benchmark.json` — So sánh with/without skill

**Vị trí:** `benchmarks/<timestamp>/benchmark.json`

**Mục đích:** Chạy nhiều lần với và không có skill, rồi tổng hợp thống kê để đánh giá skill thực sự có giúp ích hay không.

```json
{
  "runs": [
    {
      "eval_id": 1,
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "time_seconds": 42.5,
        "tokens": 3800
      }
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 0.85, "stddev": 0.05 }
    },
    "without_skill": {
      "pass_rate": { "mean": 0.35, "stddev": 0.08 }
    },
    "delta": { "pass_rate": "+0.50" }
  }
}
```

> ⚠️ **Lưu ý tên field:** Phải dùng đúng `"configuration"` (không phải `"config"`), và `pass_rate` phải nằm trong `result` (không phải ngoài cùng). Viewer đọc chính xác tên field này.

---

### 7. `comparison.json` — Blind A/B test

**Vị trí:** `<grading-dir>/comparison-N.json`

**Mục đích:** So sánh trực tiếp hai output A và B qua bộ tiêu chí rubric có điểm cụ thể. Blind (không biết cái nào là "with skill") để tránh bias.

```json
{
  "winner": "A",
  "reasoning": "Output A provides a complete solution...",
  "rubric": {
    "A": { "content_score": 4.7, "structure_score": 4.3, "overall_score": 9.0 },
    "B": { "content_score": 2.7, "structure_score": 2.7, "overall_score": 5.4 }
  },
  "expectation_results": {
    "A": { "passed": 4, "total": 5, "pass_rate": 0.8 },
    "B": { "passed": 3, "total": 5, "pass_rate": 0.6 }
  }
}
```

---

### 8. `analysis.json` — Phân tích sâu

**Vị trí:** `<grading-dir>/analysis.json`

**Mục đích:** Sau khi so sánh xong, phân tích tại sao bên thắng tốt hơn, bên thua thiếu gì, và đề xuất cải thiện cụ thể có độ ưu tiên.

```json
{
  "comparison_summary": {
    "winner": "A",
    "comparator_reasoning": "Brief summary of why comparator chose winner"
  },
  "winner_strengths": ["Clear step-by-step instructions..."],
  "loser_weaknesses": ["Vague instruction led to inconsistent behavior..."],
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace vague instructions with explicit steps",
      "expected_impact": "Would eliminate ambiguity"
    }
  ]
}
```

---

## Bảng tổng hợp nhanh

| File              | Ai tạo      | Dùng để làm gì                      |
| ----------------- | ----------- | ----------------------------------- |
| `evals.json`      | Developer   | Định nghĩa bài test đầu vào         |
| `history.json`    | Hệ thống    | Theo dõi lịch sử phiên bản          |
| `metrics.json`    | Executor    | Ghi số liệu kỹ thuật khi chạy       |
| `timing.json`     | Executor    | Ghi thời gian và token              |
| `grading.json`    | Grader      | Chấm điểm và tổng hợp kết quả       |
| `benchmark.json`  | Benchmarker | So sánh thống kê with/without skill |
| `comparison.json` | Comparator  | Blind A/B giữa hai output           |
| `analysis.json`   | Analyzer    | Phân tích nguyên nhân và đề xuất    |

---

## Mối quan hệ giữa các file

```
evals.json ──────────────────────────────────────┐
                                                  ↓
history.json ──────────────────────────→  Skill executor
                                                  │
                                    ┌─────────────┤
                                    ↓             ↓
                              timing.json    metrics.json
                                    │             │
                                    └──────┬──────┘
                                           ↓
                                     grading.json
                                    ↙      ↓      ↘
                          benchmark  comparison  analysis
                            .json      .json      .json
                               │
                               └──────→ history.json (cập nhật)
```

---

_Tài liệu này được phân tích và tổng hợp từ file `schemas.md` của hệ thống skill-creator._
