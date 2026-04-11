# 🐝 Project Swarm: Multi-Agent DevOps Lab (Elite Lab)

## 🎯 Goal
Xây dựng một hệ thống đa tác nhân (Multi-Agent System) có khả năng tự động hóa quy trình phát triển phần mềm từ khâu nhận yêu cầu -> viết code -> kiểm thử -> sửa lỗi.

---

## 🎭 The Swarm Roles
1. **The Product Architect**: Phân tích yêu cầu và thiết kế cấu trúc folder/file.
2. **The Senior Coder**: Thực thi việc viết mã nguồn dựa trên bản thiết kế.
3. **The QA Engineer**: Tự động viết test case và chạy thử nghiệm.
4. **The DevOps Manager**: Kiểm tra sự ổn định và báo cáo kết quả cuối cùng.

---

## 🏗️ Architecture (LangGraph Flow)
- **Node 1: Planner** -> Phân tích yêu cầu.
- **Node 2: Coder** -> Viết code.
- **Node 3: Tester** -> Chạy lệnh `npm test` hoặc `pytest`.
- **Node 4: Evaluator** -> Nếu Test thất bại, gửi feedback ngược lại cho Coder để fix. Nếu thành công, chuyển sang Done.

---

## 🛠️ Tech Stack
- **Framework**: LangGraph / CrewAI.
- **Tools**: Terminal Interaction (MCP), File System Access, Web Search.
- **Memory**: Persistent Checkpointer (để lưu trạng thái nếu hệ thống bị ngắt quãng).

---

## 🚀 Lab Phases

### Step 1: Tooling Setup (MCP)
Cấu hình Agent có quyền truy cập vào Terminal và File System trong môi trường Sandbox (Docker).

### Step 2: Protocol Definition
Định nghĩa cách các Agent giao tiếp với nhau (JSON Schema cho các tin nhắn nội bộ).

### Step 3: Self-Correction Loop
Triển khai logic: Nếu Tester trả về lỗi, Coder phải phân tích log lỗi và gửi bản vá mới.

---

## 📁 Directory Structure
```text
swarm-intelligence-lab/
├── agents/             # Định nghĩa logic từng agent
├── graphs/             # Cấu trúc luồng làm việc (Workflow)
├── tools/              # Các custom MCP tools
└── README.md           # File hướng dẫn này
```

---
> [!IMPORTANT]
> Lab này thách thức khả năng **Quản lý Luồng (State Management)** của bạn. Mục tiêu không phải là viết code nhanh, mà là xây dựng một hệ thống có khả năng **Tự Sửa Lỗi (Self-Healing)** mà không cần sự can thiệp của con người.
