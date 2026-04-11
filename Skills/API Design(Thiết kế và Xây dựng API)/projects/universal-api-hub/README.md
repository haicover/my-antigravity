# Lab: The Universal API Hub (Elite 2026)

Dự án thực chiến nhằm xây dựng một hệ thống API tối thượng, kết hợp sức mạnh của đa giao thức và khả năng tích hợp AI Agent.

## 🎯 Mục tiêu
- Xây dựng một API Gateway hợp nhất REST, gRPC và GraphQL.
- Triển khai **MCP Server** để cung cấp công cụ cho AI Agents.
- Tự động hóa hoàn toàn quy trình bàn giao API (Documentation, SDK, và Mocks).

## 🛠️ Stack kỹ thuật khuyến nghị
- **Language:** Go hoặc TypeScript (Node.js).
- **Specs:** OpenAPI 3.1, AsyncAPI, GraphQL SDL.
- **Gateway/Proxy:** Envoy hoặc Apollo Router (cho GraphQL).
- **Tooling:** Speakeasy (SDK Gen), Spectral (Linting), Prism (Mocking).
- **Protocol:** REST, gRPC, GraphQL, MCP.

## 🏗️ Cấu trúc dự án
```text
universal-api-hub/
├── specs/             # Nơi chứa các bản "hợp đồng" (Source of Truth)
│   ├── openapi.yaml   # REST Specs
│   ├── schema.proto   # gRPC Specs
│   └── schema.graphql # GraphQL Specs
├── mcp-server/        # Implementation của MCP Protocol cho AI
├── gateway/           # Cấu hình Gateway hợp nhất
├── sdk/               # Thư mục chứa SDK được gen tự động
└── docs/              # Tài liệu tương tác (Swagger/Redoc)
```

## 🚀 Các bước triển khai (Milestones)

### Giai đoạn 1: Schema First
1. Viết file `openapi.yaml` cho một hệ thống quản lý tài nguyên (ví dụ: Task Manager).
2. Sử dụng **Spectral** để đảm bảo file Spec đạt điểm 10/10 về thiết kế.

### Giai đoạn 2: Multi-Protocol Bridge
1. Viết logic backend bằng gRPC để đạt hiệu năng cao nhất.
2. Sử dụng một gateway (như Envoy) để chuyển đổi từ REST client sang gRPC backend (Transcoding).
3. Thêm một lớp GraphQL Layer để cho phép client query dữ liệu tùy biến.

### Giai đoạn 3: AI-Native (MCP Integration)
1. Xây dựng một **MCP Server** kết nối trực tiếp với backend.
2. Cấu hình để AI (như Claude Desktop hoặc Gemini) có thể gọi các "tools" từ API Hub này để thực thi tác vụ.

### Giai đoạn 4: Automation Factory
1. Cấu hình Github Actions để mỗi khi cập nhật Spec:
    - Tự động kiểm tra lỗi thiết kế.
    - Tự động cập nhật tài liệu API.
    - **Tự động generate SDK** mới cho Python, JS, và Go.

---

> [!TIP]
> **Elite Challenge:** Hãy thử tích hợp một cơ chế "Self-Healing Documentation" - nơi AI tự động cập nhật phần mô tả trong file OpenAPI mỗi khi logic code thay đổi.
