# 🧠 Mastery Chapter 2: Context Governance & Agentic Prompting

> "Context is the currency of Vibe Coding."
> Làm thế nào để điều khiển AI không bị 'lạc lối' giữa hàng nghìn dòng code?

## 📂 1. Context Governance (Quản trị ngữ cảnh)

AI không có trí nhớ vô hạn. Quản lý những gì AI nhìn thấy là chìa khóa của sự ổn định.

### 1.1 Context Isolation
- Chỉ mở những file thực sự liên quan đến Task.
- Sử dụng `@file`, `@folder` trong Cursor/Cline để chỉ định rõ ngữ cảnh.
- Tránh đưa toàn bộ codebase vào prompt nếu không cần thiết.

### 1.2 The Role of `.cursorrules` & `.clinerules`
Đây là "bản sắc" của dự án. File này giúp AI hiểu:
- Quy tắc đặt tên (Naming conventions).
- Coding styles (e.g., "Luôn dùng Lucide-react cho icon", "Không dùng thư viện X").
- Hành vi mong muốn (e.g., "Mỗi lần sửa file, hãy tự động cập nhật Docs").

---

## 🎭 2. Agentic Prompting Techniques

Kỹ thuật Prompting dành cho các Agent tự chủ cao cấp hơn so với Chat truyền thống.

### 2.1 Role-Playing with Purpose
Thay vì "You are a senior coder", hãy cụ thể hóa:
- "Bạn là một Performance Specialist tập trung vào việc giảm thiểu LCP và CLS của Next.js."
- "Bạn là một QA Automation Agent, nhiệm vụ của bạn là bẻ gãy (break) code của tôi."

### 2.2 Chain-of-Thought (CoT) prompting
Luôn yêu cầu AI: "Hãy suy nghĩ từng bước một (Think step by step)" và liệt kê các giả định của nó trước khi thực hiện hành vi `replace_file`.

### 2.3 Feedback Loops
Khi AI làm sai:
1. Đừng chỉ bảo "Fix it".
2. Hãy cung cấp **Logs/Error messages** đầy đủ.
3. Giải thích **tại sao** nó sai theo logic nghiệp vụ của bạn.

---

## 🛠️ 3. Prompting Patterns for Elite Engineers

- **The Sandbox Pattern:** Yêu cầu AI tạo một file test riêng biệt để thử nghiệm logic phức tạp trước khi áp dụng vào main branch.
- **The Refactor-Then-Implement Pattern:** Bảo AI tối ưu code hiện tại trước khi thêm tính năng mới để tránh tăng thêm `Technical Debt`.

---
🔗 **Resources:**
- [Mastery Chapter 3: Automated Workflows](file:///e:/Google%20Antigravity/Skills/Vibe%20Coding%28L%E1%BA%ADp%20tr%C3%ACnh%20phong%20c%C3%A1ch%20Vibe%29/references/automated_workflow_agents.md)
