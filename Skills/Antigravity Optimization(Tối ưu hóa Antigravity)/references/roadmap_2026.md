# 🗺️ Roadmap: Antigravity & Agentic Mastery — Elite 2026

Lộ trình này giúp bạn tinh chỉnh môi trường làm việc và kỹ năng điều khiển Agent để đạt được trạng thái "Cộng sinh AI" hoàn hảo.

---

## LAYER 1: SYSTEM PERFORMANCE (Hiệu suất Hệ thống)

### PHASE 1 — OS & TERMINAL STABILITY (Giai đoạn Ổn định)
> **🇻🇳 Tóm tắt:** Khắc phục triệt để các lỗi treo, lag terminal và xung đột hệ thống trên Windows.

- **Disable ConPTY**: Tắt lõi terminal gây treo agent trên Electron apps.
- **Windows Defender Exclusions**: Bỏ qua các process `antigravity.exe` và thư mục workspace để tránh bị scan gây lag.
- **FS Optimization**: Sử dụng SSD NVMe và cấu hình case-sensitive (nếu cần) trên Windows 11.

### PHASE 2 — SHELL & ENVIRONMENT (Môi trường Dòng lệnh)
> **🇻🇳 Tóm tắt:** Tối ưu hóa tốc độ thực thi lệnh terminal.

- **PowerShell -NoProfile**: Giảm thời gian khởi động terminal từ 5s xuống <1s.
- **Path Management**: Giữ biến PATH tinh gọn để Agent tìm tool nhanh nhất.
- **Node.js & Tool Caching**: Cấu hình local cache cho npm/yarn để tăng tốc cài đặt package.

---

## LAYER 2: AGENTIC WORKFLOW (Quy trình Agent)

### PHASE 3 — TOOL MASTERY (Làm chủ Bộ Công Cụ)
> **🇻🇳 Tóm tắt:** Hiểu sâu về cách Agent "nhìn" và "viết" vào hệ thống của bạn.

- **Read vs Write Efficiency**: Khi nào nên dùng `view_file` (đọc 800 dòng) và khi nào dùng `grep_search`.
- **Atomic Edits**: Sử dụng `multi_replace_file_content` để thay đổi nhiều vị trí mà không gây quá tải Token.
- **Execution Guardrails**: Biết cách giám sát lệnh `run_command` để tránh xóa nhầm dữ liệu.

### PHASE 4 — PLANNING & TASK MANAGEMENT (Lên Kế Hoạch)
> **🇻🇳 Tóm tắt:** Chuyển từ "Ra lệnh rời rạc" sang "Lập kế hoạch chiến lược".

- **The Implementation Plan**: Luôn yêu cầu Agent lên plan trước khi code.
- **Task Tracking**: Sử dụng `task.md` làm bảng TODO sống (living document).
- **Approval Cycles**: Xây dựng quy trình Duyệt -> Chạy -> Kiểm tra.

---

## LAYER 3: CONTEXT & RULES (Ngữ cảnh & Quy tắc)

### PHASE 5 — PERSISTENT CONTEXT (Ngữ cảnh Vĩnh viễn)
> **🇻🇳 Tóm tắt:** Giúp Agent luôn nhớ những gì quan trọng nhất về dự án.

- **Metadata Management**: Hiểu cách Agent lưu thông tin trong `persistent_context`.
- **Context Pruning**: Kỹ thuật xóa bớt các ngữ cảnh rác để Agent tập trung vào task hiện tại.

### PHASE 6 — PROMPT ARCHITECTURE (`.gemini` Rules)
> **🇻🇳 Tóm tắt:** "Lập trình" hành vi của Agent thông qua các tệp quy tắc.

- **Project Heuristics**: Tạo file `GEMINI.md` để Agent tuân thủ chuẩn code của riêng bạn.
- **Role Definition**: Định nghĩa Agent là Senior Architect, Security Expert, hay UI Designer tùy theo folder.

---

## LAYER 4: ADVANCED AUTONOMY (Tự động hóa Cấp cao)

### PHASE 7 — TURBO WORKFLOWS (Tự động hóa Toàn diện)
> **🇻🇳 Tóm tắt:** Để Agent tự chạy, tự fix và tự báo cáo.

- **SafeToAutoRun Optimization**: Nhập môn kỹ thuật tin tưởng Agent chạy các lệnh an toàn.
- **Automated QA Loops**: Setup flow: Agent viết code -> Agent chạy test -> Agent tự sửa nếu lỗi.

### PHASE 8 — CUSTOM MCP SERVERS (Mở rộng Sức mạnh)
> **🇻🇳 Tóm tắt:** Cấp thêm "siêu năng lực" cho Agent.

- **Building Tools**: Viết custom tools để Agent có thể tương tác với API nội bộ, Calendar, hay các database đặc thù.
- **Multi-Agent Orchestration**: Cách để nhiều Agent (Antigravity & các công cụ khác) làm việc cùng nhau.

---
_Tài liệu nâng cấp chuẩn Elite 2026 bởi Antigravity._
