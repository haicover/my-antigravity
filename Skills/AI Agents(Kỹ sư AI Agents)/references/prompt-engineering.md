# Phase 3: Prompt Engineering (Kỹ thuật Prompting cho Agents)

## Tại sao giai đoạn này quan trọng?
Nếu LLM là "não bộ", thì prompt là "hướng dẫn vận hành". Đối với Agents, prompt không chỉ là yêu cầu, mà là định nghĩa nhân cách, giới hạn quyền hạn và phương pháp suy luận. Prompting tốt giúp Agent ít bị "hallucinate" (ảo tưởng) và ra quyết định chính xác hơn.

---

## 🏗️ Kỹ thuật nâng cao cho Agents
- **Chain of Thought (CoT)**: Yêu cầu LLM "suy nghĩ qua từng bước" (think step by step). Điều này cực kỳ quan trọng để Agent lập kế hoạch.
- **Few-Shot Prompting**: Cung cấp các ví dụ thực tế (Input/Output) trong prompt để LLM bắt chước định dạng và phong cách.
- **Tree-of-Thought**: Áp dụng cho các bài toán cực kỳ phức tạp, yêu cầu Agent duyệt qua nhiều nhánh giải pháp khác nhau.

## ⚙️ Cấu trúc một System Prompt chuẩn cho Agent
1. **Nhân cách (Persona)**: "Bạn là một chuyên gia phân tích dữ liệu..."
2. **Nhiệm vụ (Task)**: "Mục tiêu của bạn là trả lời các câu hỏi dựa trên file CSV..."
3. **Công cụ (Tools)**: "Bạn có quyền sử dụng các công cụ sau: [Danh sách tools & schema]..."
4. **Quy trình (Workflow)**: "Bước 1: Suy nghĩ -> Bước 2: Gọi Tool -> Bước 3: Quan sát -> Bước 4: Lặp lại..."
5. **Giới hạn (Constraints)**: "Không bao giờ tự ý sửa đổi dữ liệu nếu không được yêu cầu..."

---

## 🛠️ Ví dụ Prompt: Tốt vs Tệ (Side-by-Side)
- **Tệ**: "Hãy tìm thông tin về công ty X và viết báo cáo." (Quá chung chung, Agent không biết bắt đầu từ đâu).
- **Tốt**: "Bạn là nhân viên nghiên cứu thị trường. Hãy sử dụng công cụ `web_search` để tìm tin tức mới nhất của công ty X trong 24h qua. Sau đó viết báo cáo dưới định dạng Markdown, tập trung vào các sự kiện tài chính."

---

## 📋 Checklist: Viết prompt cho Agent
- [ ] Bạn đã yêu cầu LLM suy nghĩ (CoT) trước khi hành động?
- [ ] Bạn đã định nghĩa định dạng output (ví dụ: JSON) một cách rõ ràng?
- [ ] Bạn đã cung cấp ít nhất 2-3 ví dụ (Few-shot) cho các tác vụ khó?
- [ ] Bạn đã thiết lập các "rào chắn" (Guardrails) để Agent không vượt quyền?

---

## 💡 Pro Tip
Hãy sử dụng **Structured Output** (đặc biệt là JSON Schema). Các framework như **Instructor** hoặc các tính năng của Claude/OpenAI giúp đảm bảo Agent luôn trả về dữ liệu đúng định dạng, tránh lỗi khi parse kết quả.
