# 🏭 Project: The Prompt Factory (Elite Lab)

## 🎯 Goal
Xây dựng một hệ thống quản lý Prompt chuyên nghiệp, nơi các Prompt được quản lý như **Code**, có phiên bản (Versioning), có kiểm thử (Testing), và được tối ưu hóa cho **AI Agents**.

---

## 🏗️ Architecture
1. **Prompt Library**: Lưu trữ dưới dạng file `.yaml` hoặc `.json` để tách biệt cấu trúc và dữ liệu.
2. **Variable Injection Engine**: Engine nhỏ để đổ dữ liệu động vào template.
3. **Tester Hub**: Bộ script (Python/JS) để tự động gọi API (Gemini/Claude) và kiểm tra output.
4. **Agentic Reflection Wrapper**: Một layer bọc quanh Prompt để bắt AI tự kiểm tra kết quả.

---

## 🛠️ Tech Stack (Suggested)
- **Engine**: Python / Node.js
- **Format**: YAML (để dễ đọc và viết Multi-line)
- **Validation**: Pydantic / Zod (để ép kiểu JSON output)
- **Storage**: Git (Versioning)

---

## 🚀 Execution Roadmap (Lab Phase)

### Step 1: Template Standardization
Thiết kế cấu trúc file YAML chuẩn cho mọi Prompt trong hệ thống:
```yaml
name: "Customer_Support_Agent"
version: "1.2.0"
config:
  model: "claude-3-5-sonnet"
  temperature: 0.2
system_block: |
  <instructions>
    You are an elite support agent...
  </instructions>
variables:
  - "customer_name"
  - "issue_description"
```

### Step 2: The "Thinking" Wrapper
Triển khai kỹ thuật bắt AI viết suy luận vào `<thought>` tag trước khi trả lời.

### Step 3: Evaluator Prompt
Viết một Prompt "Giám khảo" để tự động chấm điểm output của Step 2 dựa trên các tiêu chí (Độ chính xác, Giọng điệu, Cấu trúc JSON).

---

## 📁 Directory Structure
```text
prompt-arch-lab/
├── templates/       # Thư mục chứa file .yaml
├── test_cases/      # Dữ liệu đầu vào để test prompt
├── scripts/         # Engine chạy và đánh giá
└── README.md        # File hướng dẫn này
```

---
> [!IMPORTANT]
> Dự án này giúp bạn chuyển từ tư duy "Viết tay từng cái" sang tư duy "Sản xuất hàng loạt có kiểm soát". Đây là kỹ năng nền tảng để xây dựng các AI App lớn.
