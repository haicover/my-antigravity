# 🤖 Mastery Chapter 3: Automated Workflows & AI Agents

> "Automate the repetitive, orchestrate the creative."
> Nâng cấp từ việc 'Chat với AI' sang 'Điều hành AI' thông qua các Workflow tự động.

## 🛠️ 1. Modern Tooling Stack (2026)

Để đạt hiệu suất Elite, bạn cần những "trình điều khiển" mạnh mẽ nhất:

### 1.1 Cursor / Windsurf / VS Code + Cline
- **Cấu hình mạnh:** Tận dụng khả năng đọc toàn bộ Repo của Indexing.
- **Terminal Integration:** Cho phép bản thân AI tự chạy lệnh `git`, `npm`, `docker` để verify code.

### 1.2 MCP (Model Context Protocol)
- **What it is:** Cầu nối cho phép AI truy cập dữ liệu bên ngoài (PostgreSQL, Documentation, Google Maps, v.v.).
- **Vibe Impact:** AI có thể tự tra cứu tài liệu thư viện mới nhất thay vì dùng dữ liệu cũ trong bộ nhớ.

---

## 🏗️ 2. Autonomous Agent Workflows

Thiết kế quy trình để AI tự hoàn thành Task từ A-Z.

### 2.1 The TDD Cycle (Test Driven Development)
1. **Human:** Viết Test case (ví dụ mô tả hành vi một nút bấm).
2. **AI:** Chạy test -> Thất bại -> Viết code -> Chạy test -> Thành công.
3. **AI:** Tự tối ưu code (Refactor) và lặp lại.

### 2.2 Documentation Automation
AI không chỉ viết code, nó phải duy trì "hệ sinh thái":
- Tự động cập nhật `README.md`.
- Sinh file `walkthrough.md` sau khi hoàn thành Task.
- Vẽ sơ đồ kiến trúc (Mermaid) cho các module mới.

---

## 🚀 3. Orchestration vs. Coding

Sự khác biệt giữa Coder truyền thống và Vibe Architect:
| Coder truyền thống | Vibe Architect |
| :--- | :--- |
| Tập trung cú pháp (Syntax) | Tập trung luồng dữ liệu (Data flow) |
| Fix lỗi thủ công | Cung cấp Logs để AI tự sửa (Self-healing) |
| Viết Unit Tests cuối cùng | Viết Specs và Tests để dẫn dắt AI |

---

## 🧪 4. Self-Healing Systems

Thiết kế hệ thống để khi sụp đổ, AI có thể tự phát hiện và đề xuất phương án sửa chữa:
- Tích hợp Sentry/Log monitoring với Webhook gửi thẳng tới AI Agent.
- AI nhận lỗi -> Phân tích Context -> Đề xuất PR (Pull Request) sửa lỗi.

---
🔗 **Resources:**
- [Mastery Chapter 4: Robust Testing](file:///e:/Google%20Antigravity/Skills/Vibe%20Coding%28L%E1%BA%ADp%20tr%C3%ACnh%20phong%20c%C3%A1ch%20Vibe%29/references/robust_testing_debugging.md)
