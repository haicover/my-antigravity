# Phase 9: Evaluation & Testing (Đánh giá & Kiểm thử)

## Tại sao giai đoạn này quan trọng?
Một Agent có thể hoạt động tốt hôm nay nhưng lại thất bại vào ngày mai do sự thay đổi của dữ liệu hoặc sự không ổn định (non-determinism) của LLM. Đánh giá và kiểm thử giúp bạn đảm bảo Agent luôn hoạt động đúng như mong đợi, tối ưu hóa chi phí và sẵn sàng cho môi trường sản xuất (Production).

---

## 🏗️ Các chỉ số quan trọng (Metrics)
1. **Accuracy (Độ chính xác)**: Tỷ lệ Agent trả lời đúng so với kết quả mong đợi.
2. **Latency (Độ trễ)**: Thời gian từ lúc nhận input đến khi trả về kết quả cuối cùng.
3. **Tool Precision (Độ chính xác của Tool)**: Tỷ lệ Agent gọi đúng tool và truyền đúng tham số.
4. **Cost-per-task (Chi phí cho mỗi tác vụ)**: Số lượng token tiêu thụ trung bình cho một yêu cầu.

## 🛠️ Code Example: Unit Test cho Tool (Python with Pytest)
```python
import pytest

def test_google_search_tool():
    """Kiểm tra xem tool search có trả về kết quả hợp lệ không."""
    query = "AI Agents 2026"
    results = google_search(query)
    
    assert len(results) > 0
    assert "Agent" in results[0]["title"]
    assert "https://" in results[0]["link"]

# Chạy test bằng lệnh: pytest references/test_tools.py
```

## 🧬 Các phương pháp kiểm thử
- **Unit Testing**: Kiểm tra từng công cụ (Tool) và từng hàm logic nhỏ.
- **Integration Testing**: Kiểm tra toàn bộ luồng (Loop) của Agent từ đầu đến cuối.
- **Human-in-the-loop (HITL)**: Người dùng thực tế đánh giá kết quả của Agent và cung cấp feedback.
- **Automated Evaluation (LLM-as-a-judge)**: Dùng một LLM mạnh hơn (ví dụ: Claude 3.5 Opus) để đánh giá câu trả lời của Agent yếu hơn.

---

## 📋 Checklist: Đảm bảo chất lượng
- [ ] Bạn đã thiết lập các chỉ số KPI để theo dõi hiệu suất của Agent?
- [ ] Bạn có bộ dữ liệu mẫu (Test cases) bao gồm cả trường hợp lỗi (Edge cases)?
- [ ] Bạn đã tích hợp các công cụ theo dõi như **LangSmith** hay **DeepEval**?
- [ ] Bạn có quy trình xử lý khi Agent trả về kết quả sai hoặc không hợp lệ?

---

## 💡 Pro Tip
Hãy sử dụng **Golden Datasets** - một tập hợp các yêu cầu mẫu và câu trả lời hoàn hảo mà bạn đã duyệt qua. Luôn chạy bộ dữ liệu này sau mỗi lần thay đổi System Prompt để đảm bảo không có sự sụt giảm chất lượng (Regressions).
