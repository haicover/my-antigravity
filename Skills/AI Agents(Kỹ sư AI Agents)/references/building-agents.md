# Phase 8: Building Agents (Xây dựng Agent)

## Tại sao giai đoạn này quan trọng?
Đây là lúc bạn biến lý thuyết thành sản phẩm thực tế. Bạn có hai lựa chọn chính: Xây dựng từ đầu (From Scratch) để kiểm soát tối đa hoặc sử dụng các Khung (Frameworks) để tăng tốc độ phát triển. Hiểu rõ sự khác biệt giữa hai phương pháp này giúp bạn đưa ra quyết định đúng đắn cho dự án của mình.

---

## 🏗️ Lựa chọn A: Xây dựng từ đầu (From Scratch)
Phù hợp cho các dự án cần tối ưu hóa hiệu suất hoặc có yêu cầu cực kỳ đặc thù. Bạn sẽ trực tiếp gọi API của Anthropic (Claude), OpenAI hoặc Gemini.

## 🛠️ Code Example: Agent loop đơn giản (Python with Claude API)
```python
import anthropic

client = anthropic.Anthropic()

def run_agent_loop(task, tools):
    messages = [{"role": "user", "content": task}]
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Nếu LLM muốn dùng tool
        if response.stop_reason == "tool_use":
            tool_use = response.content[-1]
            # Thực thi tool logic ở đây
            observation = execute_tool(tool_use.name, tool_use.input)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": observation}]
            })
        else:
            return response.content[0].text
```

## 🏗️ Lựa chọn B: Sử dụng Frameworks
- **LangChain / LangGraph**: Hệ sinh thái lớn nhất, hỗ trợ nhiều mô hình và công cụ.
- **CrewAI / AutoGen**: Chuyên dụng cho hệ thống Đa nhân (Multi-agent).
- **LlamaIndex**: Tối ưu cho các bài toán RAG và truy xuất dữ liệu.
- **Agno / Smol Depot**: Các framework tinh gọn, dễ tiếp cận cho người mới.

---

## 📋 Checklist: Bắt đầu xây dựng
- [ ] Bạn đã quyết định xây dựng từ đầu (API) hay dùng Framework?
- [ ] Bạn đã thiết lập cơ chế xử lý lỗi (Rate limit, Retry) cho API calls?
- [ ] Bạn có kiểm soát được số lượng vòng lặp tối đa (Max iterations) để tránh tốn kém?
- [ ] Bạn đã chuẩn bị các tài liệu hướng dẫn (System Prompt) cho từng Agent?

---

## 💡 Pro Tip
Đừng "vắt kiệt" Agent bằng cách nạp quá nhiều công cụ. Hãy sử dụng kiến trúc **Planner-Executor** nếu Agent của bạn cần xử lý hơn 10 công cụ khác nhau. Một Agent chuyên trách lập kế hoạch sẽ giúp các nhân thực thi làm việc chính xác hơn.
