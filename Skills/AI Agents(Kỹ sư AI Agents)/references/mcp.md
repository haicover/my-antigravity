# Phase 5: MCP (Model Context Protocol)

## Tại sao giai đoạn này quan trọng?
MCP là một "cách mạng" trong việc kết nối AI với dữ liệu và công cụ, được giới thiệu bởi Anthropic vào cuối năm 2024. Thay vì xây dựng API riêng lẻ cho mỗi Agent, MCP cung cấp một tiêu chuẩn chung để Host (ví dụ: Claude Desktop) có thể sử dụng bất kỳ công cụ (Server) nào một cách an toàn và mạnh mẽ.

---

## 🏗️ Kiến trúc MCP (3 thành phần)
1. **MCP Host**: Phần mềm trực tiếp giao tiếp với LLM (ví dụ: Claude Desktop, IDE).
2. **MCP Client**: Nằm bên trong Host, quản lý các kết nối đến Server.
3. **MCP Server**: Nơi chứa các công cụ (Tools) và dữ liệu (Resources). Server có thể viết bằng Python hoặc TypeScript.

## 🛠️ Code Example: MCP Server đơn giản (Python)
```python
from mcp.server.fastmcp import FastMCP

# Tạo server MCP
mcp = FastMCP("MyBusinessTools")

@mcp.tool()
def query_database(sql_query: str) -> str:
    """Truy vấn cơ sở dữ liệu doanh nghiệp bằng SQL."""
    # Logic truy vấn DB ở đây
    return f"Kết quả cho: {sql_query}"

# Chạy server
if __name__ == "__main__":
    mcp.run()
```

## 🧬 Các loại MCP Server phổ biến
- **Local Desktop**: Chạy trực tiếp trên máy tính cá nhân để AI truy cập file, danh bạ hoặc terminal.
- **Remote/Cloud**: Chạy trên server để AI truy cập vào database, API nội bộ hoặc các công cụ doanh nghiệp tập trung.

---

## 📋 Checklist: Triển khai MCP
- [ ] Bạn đã cài đặt thư viện `mcp` của Anthropic?
- [ ] Server của bạn có cung cấp đủ description cho các Tools/Resources không?
- [ ] Bạn đã cấu hình file `claude_desktop_config.json` để Claude nhận được server chưa?
- [ ] Bạn đã thiết lập bảo mật (API Keys, Permissions) cho MCP Server?

---

## 💡 Pro Tip
Tận dụng cộng đồng **MCP Hub** trên GitHub. Có hàng trăm MCP Servers sẵn có cho Google Drive, Slack, GitHub, Supabase... mà bạn có thể dùng ngay thay vì tự viết.
