# Phase 10: Debugging & Monitoring (Sửa lỗi & Giám sát)

## Tại sao giai đoạn này quan trọng?
Trong thế giới AI Agents, việc sửa lỗi (Debugging) không chỉ là về cú pháp code, mà là về logic suy luận ("Tại sao Agent lại gọi Tool này?") và quản lý trạng thái ("Tại sao Agent bị lặp vô hạn?"). Giám sát (Monitoring) giúp bạn nắm bắt được các hành vi bất thường, tối ưu hóa chi phí token và tốc độ phản hồi.

---

## 🏗️ Quy trình Sửa lỗi (Debugging)
1. **Structured Logging**: Ghi lại mọi LLM call, Tool call, Thought, Action và Observation.
2. **Trace Visualization**: Sử dụng các công cụ để xem dòng chảy của Agent (ví dụ: LangSmith).
3. **Reproducibility**: Thiết lập các "seed" hoặc bộ dữ liệu mẫu để tái hiện lỗi suy luận của Agent.
4. **Infinite Loop Prevention**: Đặt giới hạn tối đa cho số lượng vòng lặp (Max iterations).

## 🛠️ Code Example: Structured Logging (Python)
```python
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI-Agent")

def log_agent_step(step_name, data):
    """Ghi lại các bước của Agent một cách có cấu trúc."""
    logger.info(json.dumps({
        "step": step_name,
        "data": data
    }, indent=2))

# Sử dụng trong Agent Loop:
# log_agent_step("THOUGHT", {"thought": "Cần tìm kiếm giá cổ phiếu Apple."})
# log_agent_step("TOOL_CALL", {"name": "google_search", "query": "AAPL stock price"})
```

## 🧬 Công cụ Giám sát (Observability)
- **LangSmith**: Công cụ mạnh mẽ nhất cho tracing, testing và monitoring các ứng dụng LLM.
- **Helicone / LangFuse**: Theo dõi chi phí token, độ trễ và các chỉ số hiệu suất.
- **OpenLLMetry**: Tiêu chuẩn mở dựa trên OpenTelemetry để thu thập dữ liệu từ LLM.

---

## 📋 Checklist: Giám sát Agent
- [ ] Bạn đã ghi lại (log) tất cả các yêu cầu và phản hồi từ LLM?
- [ ] Bạn đã cài đặt các công cụ theo dõi chi phí (Helicone) để tránh hóa đơn API quá cao?
- [ ] Bạn đã thiết lập cảnh báo (Alerting) khi Agent gặp lỗi liên tục hoặc không thể đạt mục tiêu?
- [ ] Bạn có thể truy vết được lý do tại sao Agent đưa ra một quyết định cụ thể?

---

## 💡 Pro Tip
Sử dụng **LangSmith** ngay khi bắt đầu dự án. Khả năng "playback" một yêu cầu từ người dùng và xem chính xác các bước mà Agent thực hiện sẽ giúp bạn tiết kiệm hàng giờ debug.
