# Phase 1: LLM Fundamentals (Cơ bản về LLM)

## Tại sao giai đoạn này quan trọng?
Để xây dựng AI Agents hiệu quả, bạn cần phải hiểu cách mà "não bộ" (LLM) của chúng hoạt động. Những kiến thức này giúp bạn tối ưu hóa chi phí (costs), tốc độ (latency) và chất lượng phản hồi (quality) cho Agent của mình.

---

## 🏗️ Transformer & LLMs
Mô hình Transformer là bước đột phá giúp các LLM như Claude, GPT-4, Gemini ra đời. Bạn cần hiểu:
- **Tokenization**: LLM không đọc từ, chúng đọc "token" (số/mã). Quy tắc ngón tay: 1000 tokens ≈ 750 từ.
- **Context Window**: Giới hạn bộ nhớ ngắn hạn của LLM. Vượt quá giới hạn này, LLM sẽ bắt đầu quên các phần đầu của hội thoại.
- **Token-based Pricing**: Chi phí dựa trên số lượng token nạp vào (input) và xuất ra (output). Input tokens thường rẻ hơn output tokens.

## ⚙️ Generation Controls
Đây là các tham số bạn cần tinh chỉnh khi gọi API:
- **Temperature**: Độ ngẫu nhiên/sáng tạo (0.0 = logic/cực kỳ nhất quán, 1.0+ = sáng tạo/đa dạng). Agents thường dùng 0.0 - 0.3 để tránh lỗi dự đoán.
- **Top-p (Nucleus Sampling)**: Giới hạn tập hợp các từ tiếp theo dựa trên xác suất tích lũy.
- **Frequency/Presence Penalty**: Giảm thiểu sự lặp lại từ ngữ.

## 🧬 Các loại mô hình (Model Families)
- **Closed weight**: Claude-3.5 (Anthropic), GPT-4o (OpenAI), Gemini 1.5 (Google) - Truy cập qua API.
- **Open weight**: Llama-3 (Meta), Mistral, Qwen - Có thể tự host (Ollama, vLLM).

---

## 🛠️ Code Example: Kiểm soát tham số (Python with Anthropic)
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    temperature=0,  # Nhất quán tuyệt đối cho Agent
    messages=[{"role": "user", "content": "Phân tích log lỗi này: [Lỗi X]"}]
)
print(response.content[0].text)
```

---

## 📋 Checklist: Những điều cần nắm
- [ ] Sự khác biệt giữa mô hình suy luận (Reasoning models - o1) và mô hình tiêu chuẩn (Standard models - Sonnet/GPT-4o).
- [ ] Cách tính toán chi phí sơ bộ dựa trên số lượng tokens dự kiến.
- [ ] Khi nào dùng Fine-tuning (Huấn luyện lại) và khi nào dùng Prompt Engineering (Cung cấp hướng dẫn).
- [ ] Khái niệm cơ bản về Embeddings (Vector đại diện cho văn bản) và Vector Search.

---

## 💡 Pro Tip
Sử dụng **RAG (Retrieval-Augmented Generation)** thay vì Fine-tuning cho hầu hết các bài toán cung cấp kiến thức mới cho Agent. RAG nhanh hơn, rẻ hơn và dễ cập nhật hơn.
