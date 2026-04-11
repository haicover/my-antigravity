# 🏗️ Project Nexus: The Universal Orchestrator (Elite Lab)

## 🎯 Goal
Thiết kế bản vẽ (Blueprint) cho một hệ thống điều phối đa Agent (Multi-Agent Orchestrator) có khả năng xử lý hàng triệu yêu cầu thời gian thực, tích hợp bộ nhớ dài hạn và khả năng tự phục hồi.

---

## 🏗️ Architecture Design (High-Level)
1. **Ingress Layer**: Tiếp nhận yêu cầu từ Human (Web/Mobile) và Machine (API/IoT).
2. **Cognitive Router**: Phân tích Intent của User bằng LLM để chọn Agent phù hợp.
3. **Agent Swarm**: Nhóm các Agent chuyên biệt (Coder, Researcher, Designer) làm việc song song.
4. **Shared Reality (Memory)**: Vector DB lưu trữ ngữ cảnh dùng chung cho các Agent.
5. **Quality Guard**: Hệ thống kiểm tra kết quả cuối cùng trước khi trả về User.

---

## 📐 System Analysis Artifacts (Required)

### 1. Requirements Matrix
- **Functional**: Dynamic agent recruitment, Stateful conversations, Tool-use execution.
- **Non-Functional**: Latency < 2s for routing, 99.99% availability, SOC2 compliance.

### 2. BPMN 2.0 (The Global Flow)
- Sơ đồ quy trình từ lúc nhận Input -> Phân tích -> Điều phối Agent -> Tổng hợp kết quả -> Trả về Client.

### 3. Entity-Relationship Diagram (ERD)
- `Tenants`, `Agents`, `Conversations`, `Messages`, `Tools`, `Logs`, `VectorIndexes`.

### 4. Sequence Diagram (The Interaction)
- Luồng tương tác giữa `Orchestrator` ↔ `Agent A` ↔ `Tool B` ↔ `Memory DB`.

---

## 📁 Lab Structure
```text
universal-orchestrator/
├── docs/
│   ├── srs.md              # Software Requirements Specification
│   ├── architecture.md     # ADRs and Component Diagrams
│   └── diagrams/           # Mermaid source files
├── schemas/                # SQL DDL and JSON Schemas
└── README.md               # File hướng dẫn này
```

---
> [!IMPORTANT]
> Lab này tập trung vào **TƯ DUY THIẾT KẾ**. Bạn không cần code ngay lập tức, mà cần tạo ra một bộ tài liệu kỹ thuật hoàn chỉnh để bất kỳ team dev nào cũng có thể triển khai được. Đây chính là sức mạnh của một System Analyst Elite.
