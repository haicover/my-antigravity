# 🪐 Project Blueprint: The Infinite Workflow

## 📌 Tổng Quan (Overview)
**The Infinite Workflow** không phải là một ứng dụng bình thường, mà là một siêu dự án nhằm thiết lập một môi trường lập trình "Tự sửa lỗi" (Self-healing). Mục tiêu là tạo ra một cấu trúc thư mục và quy tắc giúp Agent Antigravity có thể tự động hóa 90% quy trình từ khi nhận yêu cầu đến khi bàn giao code sạch.

## 🛠️ Stack Công Nghệ (Core Features)
- **Constraint Engine:** Sử dụng `.gemini` và `GEMINI.md` để áp đặt các quy tắc code cứng.
- **Auto-Fix Loops**: Tận dụng `SafeToAutoRun` cho các lệnh lint và test.
- **Standardized State**: Hệ thống `task.md` và `walkthrough.md` được tự động hóa.
- **Context Pruning Scripts**: Các script nhỏ giúp làm sạch persistent context định kỳ.

## 🏗️ Cấu Trúc Dự Án (Project Structure)
```text
.
├── .agents/                # Chứa các workflow markdown cho Agent
├── .gemini/                # Chứa các file cấu hình hành vi của Agent
├── docs/                   # Tài liệu thiết kế hệ thống
├── scripts/                # Các tool hỗ trợ (Clean context, Turbo mode)
└── GEMINI.md               # Bản hiến pháp của dự án
```

## 🌟 Tính Năng Đỉnh Cao (Elite Capabilities)
1. **Context aware planning**: Agent tự động đọc logs từ các phiên làm việc trước để không lặp lại lỗi cũ.
2. **Autonomous Debugging**: Khi `run_command` thất bại, Agent tự động bọc lỗi vào một vòng lặp nghiên cứu để tìm giải pháp thay vì hỏi người dùng.
3. **Multi-layer Documentation**: Hệ thống doc được cập nhật song song với mỗi dòng code được viết.

## 📅 Roadmap Triển Khai (Implementation Roadmap)
- [ ] **Giai đoạn 1:** Thiết lập bộ quy tắc `.gemini` và Core Behavior.
- [ ] **Giai đoạn 2:** Xây dựng hệ thống Template Task cho các loại hình dự án khác nhau (Web, Mobile, AI).
- [ ] **Giai đoạn 3:** Viết scripts hỗ trợ dọn dẹp môi trường terminal (Fix ConPTY tự động).
- [ ] **Giai đoạn 4:** Test thử nghiệm workflow "Zero-touch" (Chỉ ra lệnh 1 lần, Agent làm hết).

---
_Dự án được thiết kế để khai thác 100% sức mạnh của Antigravity Agentic OS._
