# Phase 4: Tools / Actions (Công cụ & Hành động)

## Tại sao giai đoạn này quan trọng?
Công cụ là "đôi tay" của AI Agent. Nếu không có Tools, Agent chỉ có thể nói mà không thể làm. Định nghĩa Tool chuẩn xác (JSON Schema) giúp LLM biết khi nào cần gọi công cụ nào và truyền tham số gì, đây là xương sống của mọi hệ thống Agentic.

---

## 🏗️ Cấu trúc một Tool (4 thành phần)
Một Tool tốt cần có:
1. **Name**: Tên ngắn gọn (ví dụ: `google_search`).
2. **Description**: QUAN TRỌNG NHẤT. Mô tả rõ mục đích của Tool để LLM hiểu khi nào nên dùng (ví dụ: "Dùng để tìm tin tức trực tuyến...").
3. **Input Schema (JSON)**: Định nghĩa các tham số cần thiết (ví dụ: `query`, `limit`).
4. **Error Handling**: Cách xử lý khi Tool không trả về kết quả hoặc bị lỗi API.

## 🛠️ Code Example: Định nghĩa Tool (Anthropic Claude API)
```python
tools = [
     {
        "name": "get_weather",
        "description": "Lấy thông tin thời tiết hiện tại cho một địa điểm cụ thể.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Thành phố và bang, ví dụ: San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]
```

## 🧬 Các loại Tool phổ biến
- **Web Search**: Tìm kiếm thông tin mới nhất trên Internet (Tavily, Perplexity).
- **Code Execution**: Thực thi code (Python/JS) trong môi trường sandbox.
- **Database Query**: Truy vấn SQL hoặc NoSQL để lấy dữ liệu kinh doanh.
- **API Requests**: Gửi email qua SendGrid, nhắn tin qua Slack, đặt lịch qua Google Calendar.

---

## 📋 Checklist: Định nghĩa Tool chuẩn
- [ ] Description của bạn có đủ rõ ràng để LLM không bị nhầm lẫn?
- [ ] Bạn đã thiết lập các tham số "Required" (Bắt buộc) một cách hợp lý?
- [ ] Bạn đã có phương án xử lý lỗi (Retry, Error message) khi Tool thất bại?
- [ ] Bạn có sử dụng Parallel Tool Calling (gọi nhiều tool cùng lúc) để tối ưu?

---

## 💡 Pro Tip
Cung cấp **ví dụ về input/output** ngay trong description của Tool. Điều này giúp LLM hiểu định dạng dữ liệu mà Tool mong đợi, đặc biệt là với các tham số phức tạp như JSON string hay regex.
