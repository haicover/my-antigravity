# 🚀 Google AI Studio: Best Practices & Vibe Coding Templates

Đây là tài liệu tham khảo nhanh giúp ní tối ưu hóa quy trình làm việc trong Google AI Studio (Gais) năm 2026.

---

## 1. 🌈 Vibe Coding Templates (Mẫu Prompt)

Khi ní muốn AI Studio tạo nhanh một chức năng nào đó, hãy dùng cấu trúc "3 lớp":

### Mẫu: Tạo Dashboard Doanh Thu (Revenue Dashboard)
*   **Role**: Một chuyên gia Frontend và Data Visualization.
*   **Context**: Dự án SaaS-Production đang chạy Next.js và TailwindCSS.
*   **Goal**: Tạo một trang Dashboard hiển thị doanh thu theo tuần/tháng/năm bằng Chart.js.
*   **Vibe**: Thiết kế phải "premium", hiện đại, hỗ trợ Dark Mode.

> [!TIP]
> **Prompt thực tế**: *"Hãy làm việc như một chuyên gia UI/UX. Tôi đang xây dựng Dashboard doanh thu cho dự án SaaS của mình. Hãy tạo code React dùng Tailwind và Chart.js. Tôi muốn biểu đồ có hiệu ứng mờ (glassmorphism) và màu sắc hài hòa (Deep Purple & Neon Blue). Hãy xuất code tích hợp sẵn API Fetch mẫu."*

---

## 2. 🧠 System Instructions (Premium Rules)

Đừng để trống ô **System Instruction**. Hãy dán các quy tắc này vào để Gemini thông minh hơn:

```text
- Bạn là chuyên gia AI Engineer (2026).
- Luôn ưu tiên sử dụng các thư viện ổn định nhất.
- Khi viết mã nguồn Python, luôn sử dụng SDK 'google-genai' thay vì các SDK cũ.
- Trả lời bằng tiếng Việt chuyên nghiệp nhưng gần gũi.
- Nếu người dùng hỏi về giao diện, hãy thiết kế theo phong cách hiện đại (Premium Aesthetics).
- Luôn giải trình logic trước khi đưa ra code.
```

---

## 3. 💾 Prompt Caching Strategy

Sử dụng Caching khi:
1.  **Context lớn**: Khi ní tải lên hơn 32k tokens (tài liệu dày, mã nguồn toàn bộ project).
2.  **Lặp lại nhiều lần**: Khi ní đang test nhiều loại Prompt trên cùng một tập dữ liệu.

**Cách bật**: Trong menu cài đặt bên phải của AI Studio (phần Config), chọn "Enable Caching" và thiết lập "TTL" (Time To Live) phù hợp (ví dụ: 1h để tiết kiệm tối đa).

---

## 4. 🎯 Model Tuning (Fine-tuning)

Khi nào nên dùng **Tuned Models**?
- Khi ní muốn model có giọng văn đặc thù (Brand Voice).
- Khi ní muốn model trả về format JSON cực kỳ chuẩn xác mà Prompt thông thường không làm được.
- Khi ní muốn model học kiến thức chuyên biệt của công ty (Domain Knowledge).

**Quy trình**:
1.  Chuẩn bị file CSV với cột `input` và `output`.
2.  Chọn "Create Tuned Model" trong Studio.
3.  Chọn base model là `gemini-1.5-flash` để vừa rẻ vừa nhanh.
4.  Đợi training xong rồi dùng trực tiếp ID của model đó trong code.

---

## 5. 🛠️ Export Code (Cầu nối sang Production)

Sau khi "vibe" xong trong Studio, hãy nhấn nút **"Get Code"**. 
*   Chọn ngôn ngữ: **Python**.
*   Đảm bảo code xuất ra sử dụng `genai.Client` (Unified SDK).
*   Copy API Key vào file `.env` của ní.

---

> [!IMPORTANT]
> Google AI Studio năm 2026 đã hỗ trợ **Multi-turn Chat** cực tốt. Đừng ngại "cãi nhau" với nó nếu code lần đầu chưa ưng ý. Sức mạnh của AI Studio nằm ở việc ní có thể tinh chỉnh từng dòng code trực tiếp.
