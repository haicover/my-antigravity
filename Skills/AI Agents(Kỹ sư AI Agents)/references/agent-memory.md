# Phase 6: Agent Memory (Bộ nhớ của Agent)

## Tại sao giai đoạn này quan trọng?
Bộ nhớ giúp Agent vượt qua giới hạn của "Context Window". Nếu không có Memory, Agent sẽ quên những gì bạn đã nói ở 5 phút trước hoặc trong các phiên làm việc trước đó. Bộ nhớ cho phép Agent hiểu rõ cá nhân bạn (User Profile) và học hỏi từ các tương tác trong quá khứ.

---

## 🏗️ Các loại Memory
1. **Short-Term Memory (Bộ nhớ ngắn hạn)**: Nằm trực tiếp trong prompt hoặc hội thoại hiện tại.
2. **Long-Term Memory (Bộ nhớ dài hạn)**: Dùng Vector DB (Pinecone, pgvector) hoặc SQL để lưu trữ vĩnh viễn.
3. **Episodic Memory (Bộ nhớ sự kiện)**: Ghi lại các tương tác cụ thể trong quá khứ ("Bạn đã từng hỏi về X").
4. **Semantic Memory (Bộ nhớ ngữ nghĩa)**: Kiến thức chung và các sự kiện ("Thủ đô của Pháp là Paris").

## 🛠️ Code Example: RAG với Vector DB (Pinecone)
```python
import pinecone

# Khởi tạo vector index
index = pinecone.Index("agent-memory")

def save_to_memory(text, vector):
    """Lưu văn bản vào bộ nhớ dài hạn."""
    index.upsert([(id, vector, {"text": text})])

def search_memory(query_vector):
    """Tìm kiếm các ký ức liên quan."""
    results = index.query(query_vector, top_k=5)
    return results
```

## 🧬 Chiến lược duy trì Memory
- **RAG (Retrieval-Augmented Generation)**: Tìm kiếm các đoạn tài liệu/ký ức liên quan nhất để nạp vào prompt.
- **Summarization (Tóm tắt)**: Tóm tắt lại lịch sử hội thoại khi nó quá dài để tiết kiệm context.
- **Aging Strategies**: Xóa hoặc giảm ưu tiên các thông tin cũ, không còn phù hợp.

---

## 📋 Checklist: Thiết lập Memory
- [ ] Bạn đã phân loại rõ thông tin nào cần lưu vĩnh viễn (SQL/Vector) và thông tin nào tạm thời?
- [ ] Bạn có sử dụng Embedding model chất lượng cao (ví dụ: `text-embedding-3-small`)?
- [ ] Bạn đã thiết lập cơ chế nén/tóm tắt (Compression/Summarization) cho hội thoại dài?
- [ ] Bạn có tuân thủ quyền riêng tư dữ liệu khi lưu trữ thông tin của User?

---

## 💡 Pro Tip
Hãy sử dụng **User Profile Storage**. Agent ghi nhớ sở thích, phong cách làm việc của User (ví dụ: "User thích báo cáo ngắn gọn bằng Markdown") sẽ tạo ra trải nghiệm cực kỳ ấn tượng.
