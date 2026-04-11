# 🚀 Lab: The Agentic Search (Elite AI 2026)

## 🎯 Overview
Xây dựng một hệ thống tìm kiếm thông minh cấp độ doanh nghiệp, có khả năng tự suy luận, truy cập nhiều nguồn dữ liệu thông qua **MCP (Model Context Protocol)** và tự sửa lỗi nếu kết quả tìm kiếm không đạt yêu cầu.

---

## 🏗️ Architecture (Cấu trúc hệ thống)
1.  **Orchestrator**: LangGraph / LangChain Agent dùng Claude 3.7.
2.  **MCP Server**: Một custom server kết nối với Local SQLite và Google Search API.
3.  **Vector Store**: Qdrant để lưu trữ và tìm kiếm ngữ nghĩa các tài liệu nội bộ.
4.  **Evaluation Loop**: Tự động chấm điểm kết quả bằng RAGAS trước khi trả về cho người dùng.

---

## 🛠️ Phase-by-Phase Implementation

### Phase 1: Setup Internal Retrieval
- Triển khai Qdrant local.
- Viết script chunking tài liệu bằng `RecursiveCharacterTextSplitter`.
- Ingest dữ liệu vào Qdrant dùng `text-embedding-3-small`.

### Phase 2: Building the MCP Server
- Cấu hình `FastMCP` (Python).
- Expose các tool:
    - `search_internal_docs(query)`: Tìm trong Qdrant.
    - `query_local_db(sql)`: Truy vấn file SQLite nội bộ.
    - `web_search(query)`: Search web nếu dữ liệu nội bộ không có.

### Phase 3: The Agentic Loop
- Thiết kế Agent với logic:
    1.  Nhận yêu cầu.
    2.  Check Qdrant.
    3.  Nếu thông tin cũ hoặc thiếu -> Gọi `web_search`.
    4.  Hợp nhất thông tin và generate câu trả lời.

### Phase 4: Self-Correction (Elite Layer)
- Thêm bước **Critique**: Agent tự đọc câu trả lời và check lại với source.
- Nếu thấy mâu thuẫn -> Thực hiện lại bước Retrieval với query khác.

---

## 🚦 How to run
1.  Cài đặt MCP Inspector: `npx @modelcontextprotocol/inspector`.
2.  Chạy MCP Server: `python mcp_server.py`.
3.  Khởi chạy Agent: `python agent_main.py`.

---

## 🏆 Success Criteria
- Hệ thống trả lời được các câu hỏi kết hợp giữa dữ liệu nội bộ và tin tức thời sự.
- Tốc độ phản hồi < 5s (nhờ Context Caching).
- Điểm **Faithfulness > 0.85** (theo RAGAS).

---
> [!TIP]
> **Pro Tip:** Năm 2026, đừng bao giờ để AI trả lời trực tiếp mà không qua một lớp "Validation". Hãy luôn tin vào "Trust but Verify".
