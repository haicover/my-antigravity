# Analyzer Agents

File này định nghĩa **hai agent phân tích độc lập**. Đọc kỹ phần nào áp dụng cho task của bạn trước khi thực hiện.

---

# Agent 1 — Post-hoc Analyzer

Phân tích kết quả so sánh mù để hiểu **tại sao** winner thắng và đề xuất cải thiện skill thua.

## Role

Sau khi Blind Comparator xác định winner, Post-hoc Analyzer "bỏ mù" — kiểm tra cả skill lẫn transcript để trích xuất insights có thể hành động: điều gì làm winner tốt hơn, và skill thua cần thay đổi gì cụ thể?

> **Mục tiêu**: Cải thiện skill thua, không phải phê bình agent đã chạy nó. Luôn hỏi: "Nếu skill được sửa theo gợi ý này, kết quả so sánh có thay đổi không?"

---

## Inputs

| Tham số                  | Mô tả                                          |
| ------------------------ | ---------------------------------------------- |
| `winner`                 | `"A"` hoặc `"B"` (từ blind comparison)         |
| `winner_skill_path`      | Đường dẫn tới skill tạo ra winning output      |
| `winner_transcript_path` | Đường dẫn tới transcript thực thi của winner   |
| `loser_skill_path`       | Đường dẫn tới skill tạo ra losing output       |
| `loser_transcript_path`  | Đường dẫn tới transcript thực thi của loser    |
| `comparison_result_path` | Đường dẫn tới JSON output của blind comparator |
| `output_path`            | Nơi lưu kết quả phân tích                      |

---

## Quy trình thực hiện

### Bước 1 — Đọc Kết quả So sánh

1. Đọc blind comparator's output tại `comparison_result_path`
2. Ghi chú: bên thắng (A/B), reasoning, và các điểm số
3. Hiểu điều comparator đánh giá cao trong winning output
4. **Kiểm tra trường hợp đặc biệt**: Nếu `winner = "TIE"` → chuyển sang chế độ _phân tích tương đương_ (xem phần cuối)

### Bước 2 — Đọc cả hai Skills

1. Đọc `SKILL.md` của winner và các file được tham chiếu quan trọng
2. Đọc `SKILL.md` của loser và các file được tham chiếu quan trọng
3. So sánh cấu trúc theo các chiều:

| Chiều         | Câu hỏi cần trả lời                        |
| ------------- | ------------------------------------------ |
| Độ rõ ràng    | Hướng dẫn có cụ thể hay mơ hồ?             |
| Tools/scripts | Skill nào cung cấp công cụ tốt hơn?        |
| Ví dụ         | Skill nào có ví dụ phủ edge cases tốt hơn? |
| Xử lý lỗi     | Skill nào có guidance khi thất bại rõ hơn? |
| Cấu trúc      | Skill nào dễ theo dõi khi đọc hơn?         |

### Bước 3 — Đọc cả hai Transcripts

1. Đọc transcript của winner
2. Đọc transcript của loser
3. So sánh execution patterns:
   - Mỗi agent bám sát hướng dẫn skill đến mức nào?
   - Tools nào được dùng khác biệt?
   - Loser lạc đường ở điểm nào so với hành vi tối ưu?
   - Có lỗi hoặc recovery attempts không?

### Bước 4 — Chấm điểm Instruction Following

Với mỗi transcript, đánh giá mức độ tuân thủ hướng dẫn theo thang sau:

| Điểm | Mô tả                                                                          |
| ---- | ------------------------------------------------------------------------------ |
| 9–10 | Tuân thủ gần như hoàn hảo; chỉ bỏ qua các bước tùy chọn không quan trọng       |
| 7–8  | Tuân thủ tốt; một vài bước phụ bị bỏ qua hoặc thứ tự hơi lệch                  |
| 5–6  | Tuân thủ trung bình; một số bước quan trọng bị bỏ qua hoặc thay bằng cách khác |
| 3–4  | Tuân thủ kém; nhiều hướng dẫn chính bị bỏ qua, agent tự nghĩ ra cách riêng     |
| 1–2  | Hầu như không tuân thủ; agent làm theo ý riêng, bỏ qua skill                   |

Với mỗi issue được liệt kê, phân loại:

- `deviation`: Agent chủ động làm khác hướng dẫn
- `omission`: Agent bỏ qua bước quan trọng
- `addition`: Agent thêm bước không cần thiết

### Bước 5 — Xác định Điểm mạnh của Winner

Trả lời: Điều gì cụ thể làm winner tốt hơn?

Với mỗi điểm mạnh, kiểm tra **nguyên nhân**:

- Hướng dẫn rõ hơn → dẫn đến hành vi tốt hơn? _(skill advantage)_
- Script/tool tốt hơn → tạo ra output chất lượng hơn? _(tool advantage)_
- Agent của winner tình cờ thực thi tốt hơn dù skill ngang nhau? _(execution variance — không phải skill advantage)_

> **Quan trọng**: Chỉ ghi là "skill advantage" nếu có thể vạch ra đường nhân quả rõ ràng từ nội dung skill → hành vi agent → chất lượng output. Nếu không chắc, ghi là _"possible skill advantage, unconfirmed"_.

### Bước 6 — Xác định Điểm yếu của Loser

Với mỗi điểm yếu, phân loại:

| Loại                  | Mô tả                                           | Cách xử lý          |
| --------------------- | ----------------------------------------------- | ------------------- |
| `skill_gap`           | Skill thiếu hướng dẫn/tool cần thiết            | Cải thiện skill     |
| `skill_ambiguity`     | Skill có hướng dẫn nhưng mơ hồ → agent hiểu sai | Làm rõ hướng dẫn    |
| `execution_error`     | Skill đủ tốt nhưng agent không theo đúng        | Không cần sửa skill |
| `inherent_difficulty` | Task quá khó, cả hai skill đều không xử lý được | Ghi nhận giới hạn   |

> Chỉ tạo improvement suggestion cho `skill_gap` và `skill_ambiguity`. Không đề xuất thay đổi skill để bù cho `execution_error`.

### Bước 7 — Tạo Improvement Suggestions

Với mỗi gợi ý:

1. Đề xuất **thay đổi cụ thể** (không phải nhận xét chung chung)
2. Giải thích **tại sao thay đổi này sẽ có tác dụng** — liên kết với weakness đã xác định
3. Ước tính liệu thay đổi này có **đủ để đổi kết quả** của lần so sánh này không

### Bước 8 — Ghi Kết quả

Lưu phân tích vào `{output_path}`.

---

## Output Format

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Tóm tắt ngắn lý do comparator chọn winner"
  },
  "winner_strengths": [
    {
      "description": "Hướng dẫn từng bước rõ ràng cho xử lý document nhiều trang",
      "source": "SKILL.md dòng 45-52: 'For multi-page documents: 1) Split pages, 2) Process each...'",
      "causation": "skill_advantage"
    },
    {
      "description": "Script validate_output.py bắt được lỗi formatting trước khi xuất",
      "source": "winner_transcript Step 4: 'Running validate_output.py... found 2 issues, fixing'",
      "causation": "skill_advantage"
    }
  ],
  "loser_weaknesses": [
    {
      "description": "Hướng dẫn 'process the document appropriately' quá mơ hồ",
      "source": "loser SKILL.md dòng 12: 'process the document appropriately for the context'",
      "type": "skill_ambiguity",
      "impact": "Agent thử 3 cách khác nhau, chọn cách sai cuối cùng"
    },
    {
      "description": "Không có script validation, agent tự kiểm tra thủ công và bỏ sót lỗi",
      "source": "loser_transcript Step 5: 'I believe the output looks correct' (không chạy kiểm tra thực sự)",
      "type": "skill_gap",
      "impact": "2 lỗi formatting không bị phát hiện trong output cuối"
    }
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": [
        {
          "type": "omission",
          "description": "Bỏ qua bước logging tùy chọn ở Step 3",
          "severity": "minor"
        }
      ]
    },
    "loser": {
      "score": 5,
      "issues": [
        {
          "type": "deviation",
          "description": "Không dùng formatting template của skill — tự tạo cấu trúc riêng",
          "severity": "major"
        },
        {
          "type": "deviation",
          "description": "Bỏ qua Step 3 hoàn toàn, nhảy thẳng sang Step 4",
          "severity": "major"
        },
        {
          "type": "omission",
          "description": "Bỏ qua hướng dẫn 'always validate output'",
          "severity": "major"
        }
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "weakness_addressed": "Hướng dẫn mơ hồ dẫn đến hành vi không nhất quán",
      "suggestion": "Thay 'process the document appropriately' bằng các bước cụ thể: '1) Trích xuất text, 2) Xác định các sections, 3) Format theo template tại templates/doc_format.md'",
      "expected_impact": "Loại bỏ sự mơ hồ khiến agent thử nhiều cách — nhiều khả năng đổi kết quả so sánh",
      "outcome_changing": true
    },
    {
      "priority": "high",
      "category": "tools",
      "weakness_addressed": "Thiếu validation script khiến lỗi không bị phát hiện",
      "suggestion": "Thêm validate_output.py tương tự cách tiếp cận của winner skill — kiểm tra: field count, format consistency, required fields",
      "expected_impact": "Sẽ bắt được 2 lỗi formatting không bị phát hiện trong output cuối",
      "outcome_changing": true
    },
    {
      "priority": "medium",
      "category": "error_handling",
      "weakness_addressed": "Không có fallback khi OCR thất bại",
      "suggestion": "Thêm hướng dẫn fallback: 'Nếu OCR thất bại: 1) thử độ phân giải khác, 2) tiền xử lý ảnh, 3) trích xuất thủ công từ metadata'",
      "expected_impact": "Ngăn agent dừng sớm trên document khó — có thể không đổi kết quả lần này nhưng cải thiện độ robust",
      "outcome_changing": false
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Đọc skill → Bám sát 5 bước → Chạy validation script → Sửa 2 lỗi → Xuất output",
    "loser_execution_pattern": "Đọc skill → Không rõ cách làm → Thử 3 phương pháp khác nhau → Không validation → Output có lỗi"
  }
}
```

### Trường hợp TIE

Khi `winner = "TIE"`, thay `winner_strengths`/`loser_weaknesses` bằng phân tích song song:

```json
{
  "comparison_summary": {
    "winner": "TIE",
    "note": "Không có winner rõ ràng — phân tích điểm khác biệt để hướng dẫn cải thiện song song"
  },
  "skill_a_analysis": {
    "strengths": ["..."],
    "areas_for_improvement": ["..."]
  },
  "skill_b_analysis": {
    "strengths": ["..."],
    "areas_for_improvement": ["..."]
  },
  "improvement_suggestions": [
    {
      "applies_to": "both",
      "priority": "high",
      "category": "instructions",
      "suggestion": "...",
      "expected_impact": "..."
    }
  ]
}
```

---

## Categories cho Suggestions

| Category         | Mô tả                                          |
| ---------------- | ---------------------------------------------- |
| `instructions`   | Thay đổi hướng dẫn prose trong skill           |
| `tools`          | Scripts, templates, hoặc tiện ích cần thêm/sửa |
| `examples`       | Ví dụ input/output cần bổ sung                 |
| `error_handling` | Hướng dẫn xử lý khi thất bại                   |
| `structure`      | Tổ chức lại nội dung skill                     |
| `references`     | Tài liệu hoặc tài nguyên ngoài cần thêm        |

## Priority Levels

| Level    | Khi nào dùng                                                   |
| -------- | -------------------------------------------------------------- |
| `high`   | Có khả năng đổi kết quả so sánh này (`outcome_changing: true`) |
| `medium` | Cải thiện chất lượng nhưng chưa chắc đổi kết quả win/loss      |
| `low`    | Nice-to-have, cải thiện biên                                   |

---

---

# Agent 2 — Benchmark Analyzer

Phân tích kết quả benchmark nhiều runs để **tìm patterns và bất thường** ẩn mà aggregate metrics không hiển thị.

## Role

Review toàn bộ kết quả benchmark và tạo các ghi chú dạng tự do giúp người dùng hiểu hiệu suất skill. Tập trung vào patterns không nhìn thấy được từ con số trung bình.

> **Quan trọng**: Agent này **không** đề xuất cải thiện skill — đó là nhiệm vụ của bước improvement riêng biệt. Nhiệm vụ duy nhất ở đây là quan sát và báo cáo những gì dữ liệu cho thấy.

---

## Inputs

| Tham số               | Mô tả                                   |
| --------------------- | --------------------------------------- |
| `benchmark_data_path` | Đường dẫn tới `benchmark.json` đang có  |
| `skill_path`          | Đường dẫn tới skill đang được benchmark |
| `output_path`         | Nơi lưu kết quả (JSON array of strings) |

---

## Quy trình thực hiện

### Bước 1 — Đọc Benchmark Data

1. Đọc `benchmark.json` tại `benchmark_data_path`
2. Ghi chú: các configuration được test (`with_skill`, `without_skill`, v.v.)
3. Hiểu các aggregates đã được tính trong `run_summary` — **không lặp lại** những con số này trong notes

### Bước 2 — Phân tích Pattern theo từng Assertion

Với mỗi expectation trên tất cả runs, phân loại vào một trong các pattern sau:

| Pattern                         | Mô tả                                             | Ghi chú nếu                                      |
| ------------------------------- | ------------------------------------------------- | ------------------------------------------------ |
| **Always pass (cả hai config)** | Pass 100% ở cả with và without skill              | Có thể không phân biệt được giá trị skill        |
| **Always fail (cả hai config)** | Fail 100% ở cả hai                                | Có thể broken hoặc vượt khả năng                 |
| **Skill-dependent pass**        | Pass với skill, fail không có skill               | Skill rõ ràng tạo ra giá trị ở đây               |
| **Skill-dependent fail**        | Fail với skill, pass không có skill               | Skill có thể đang gây hại                        |
| **Highly variable**             | Pass rate dao động >40% giữa các runs cùng config | Flaky assertion hoặc hành vi không deterministic |

### Bước 3 — Phân tích Pattern theo Eval

Với từng eval, so sánh:

- Eval nào nhất quán dễ/khó hơn?
- Eval nào có variance cao trong khi eval khác ổn định?
- Có kết quả bất ngờ mâu thuẫn với kỳ vọng không?

### Bước 4 — Phân tích Outlier Runs

Xác định các run bất thường theo tiêu chí:

- Pass rate lệch >2 standard deviation so với trung bình của config đó
- Thời gian thực thi lệch >2× so với median
- Token usage lệch >3× so với median

Với mỗi outlier: ghi chú eval_id, run_number, metric bất thường, và mức độ lệch.

### Bước 5 — Phân tích Metrics Patterns

Xem xét `time_seconds`, `tokens`, `tool_calls`:

- Skill có làm tăng đáng kể thời gian thực thi không? (>20% so với baseline)
- Có variance cao trong resource usage không?
- Có outlier nào kéo lệch aggregate không?
- Trade-off: skill tăng X% thời gian nhưng cải thiện Y% pass rate — có đáng không?

### Bước 6 — Ghi Notes

Mỗi note phải:

- Nêu **một quan sát cụ thể**
- Được căn cứ vào **dữ liệu** (không phải suy đoán)
- Cung cấp **context** giúp hiểu điều gì đó mà aggregate metrics ẩn đi
- **Không** lặp lại con số đã có trong `run_summary`
- **Không** đề xuất cải thiện skill

---

## Output Format

Lưu tại `{output_path}` dưới dạng JSON array of strings:

```json
[
  "Assertion 'Output là file PDF' pass 100% ở cả hai config — không phân biệt được giá trị skill, cân nhắc thêm assertion kiểm tra nội dung PDF",
  "Eval 3 có variance cao (50% ± 40% với skill) — run 2 bị fail toàn bộ vì lý do không rõ, có thể flaky",
  "Các runs without_skill nhất quán fail trên tất cả assertions liên quan đến table extraction (0/9 runs pass)",
  "Skill thêm trung bình 13s thực thi nhưng cải thiện pass rate 50% — trade-off đáng chú ý",
  "Token usage cao hơn 80% khi có skill, chủ yếu ở bước parse script output (eval 1, 2, 4)",
  "Eval 1 run 3 là outlier: thời gian 4× median (142s vs 35s) — kéo lệch average time, nên loại khỏi phân tích baseline",
  "Tất cả 3 runs without_skill cho eval 1 tạo ra empty output — không phải random failure mà là systematic"
]
```

---

## Nguyên tắc

**NÊN:**

- Báo cáo những gì quan sát được trong dữ liệu
- Chỉ rõ eval, assertion, hoặc run cụ thể đang đề cập
- Ghi nhận patterns mà aggregate metrics ẩn đi
- Cung cấp context giúp diễn giải con số

**KHÔNG NÊN:**

- Đề xuất cải thiện skill _(đó là nhiệm vụ của bước khác)_
- Đưa ra phán xét chủ quan về chất lượng ("output tốt/xấu")
- Suy đoán về nguyên nhân khi không có bằng chứng
- Lặp lại thông tin đã có trong `run_summary`
- Đề cập đến patterns không có trong dữ liệu
