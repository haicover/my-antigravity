# Phase 7: Agent Architectures (Kiến trúc Agent)

## Tại sao giai đoạn này quan trọng?
Một Agent tốt không chỉ là một cái prompt đơn lẻ. Tùy thuộc vào độ phức tạp của bài toán, bạn cần chọn một kiến trúc phù hợp để Agent có thể suy luận chính xác và hiệu quả nhất. Các kiến trúc này giúp phân chia trách nhiệm và kiểm soát luồng hoạt động của Agent.

---

## 🏗️ Các kiến trúc phổ biến
1. **ReAct (Reason + Act)**: Đan xen giữa suy luận và hành động. Phổ biến nhất cho các task đơn giản, linh hoạt.
2. **RAG Agent**: Kết hợp tìm kiếm tài liệu (Retrieval) và sinh văn bản (Generation). Dùng để trả lời câu hỏi dựa trên kiến thức.
3. **Planner-Executor**: Một LLM chuyên lập kế hoạch (Plan) và một LLM khác thực thi các bước (Execute). Dùng cho các task cực kỳ phức tạp.
4. **Multi-Agent Systems**: Nhiều nhân chuyên biệt (ví dụ: Researcher Agent + Writer Agent) phối hợp với nhau. Dùng cho hệ thống lớn.
5. **Self-Critique (Tự phản biện)**: Agent tự kiểm tra kết quả của mình trước khi gửi cho người dùng. Dùng để nâng cao chất lượng đầu ra.

## 🛠️ Code Skeleton: ReAct Architecture (Python)
```python
def react_agent_loop(task):
    history = []
    while True:
        # LLM nhận task và history -> ra quyết định (Thought + Action)
        thought, action = llm.generate(task, history)
        
        if action == "FINAL_ANSWER":
            return thought
            
        # Thực thi tool
        observation = execute_tool(action.name, action.args)
        
        # Ghi nhận kết quả
        history.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })
```

## 🧬 So sánh kiến trúc
- **ReAct**: Linh hoạt nhưng có thể bị lặp vô hạn nếu không kiểm soát.
- **RAG**: Chính xác về thông tin nhưng thiếu khả năng giải quyết vấn đề đa bước.
- **Multi-Agent**: Mạnh mẽ nhưng tốn kém (nhiều token) và khó debug hơn (độ trễ cao).

---

## 📋 Checklist: Chọn kiến trúc
- [ ] Task của bạn có yêu cầu nhiều bước thực thi độc lập không? (Planner-Executor).
- [ ] Task của bạn yêu cầu kiến thức chuyên sâu trong tài liệu lớn (RAG).
- [ ] Bạn có cần đảm bảo chất lượng cực cao thông qua nhiều bước kiểm duyệt (Self-critique)?
- [ ] Bạn đã thiết lập các luồng dữ liệu (DAG) giữa các Agent để tối ưu hóa hiệu suất?

---

## 💡 Pro Tip
Hãy sử dụng **Directed Acyclic Graphs (DAGs)** để thiết kế luồng cho Agent. Các framework như **LangGraph** giúp bạn xây dựng các workflow Agentic có cấu trúc, dễ kiểm soát và có khả năng phục hồi (Stateful).
