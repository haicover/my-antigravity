# 🧪 Mastery Chapter 4: Robust Testing & Agentic Debugging

> "Never trust AI-generated code that hasn't been executed."
> Vibe Coding không phải là "Phó mặc". Nó là "Kiểm định liên tục".

## 🛠️ 1. The Verification Hierarchy

Xây dựng tháp kiểm định chất lượng cho hệ thống được xây dựng bởi AI.

### 1.1 Automated Syntax & Type Checking
- Luôn chạy `tsc` (TypeScript compiler) hoặc Linter ngay sau mỗi lần AI sửa file.
- Đừng để lỗi cú pháp tích tụ.

### 1.2 The "Red-Green-Refactor" Vibe Edition
1. **Red:** Yêu cầu AI viết Test trước. Chạy lệnh test và thấy nó False.
2. **Green:** AI viết code cho đến khi Test pass.
3. **Refactor:** Yêu cầu AI tối ưu lại code khi Test đã ổn định.

---

## 🐞 2. Agentic Debugging (Gỡ lỗi bằng AI)

AI không chỉ "đọc" lỗi, nó phải "điều tra" lỗi.

### 2.1 Error Context Injection
Khi cung cấp lỗi cho AI, hãy bao gồm:
- **Stack Trace:** Đầu ra từ Console/Terminal.
- **Environment info:** Node version, OS, Browser.
- **Recent changes:** Danh sách các file vừa sửa.

### 2.2 The "Self-Reflect" Prompt
Nếu AI không sửa được sau 3 lần:
> "Hãy dừng lại và phân tích tại sao phương án sửa lỗi trước đó của bạn không hiệu quả. Liệt kê tất cả các giả định (assumptions) mà bạn đang có về module này."

---

## 🛡️ 3. Security & Quality Guardrails

Đừng để AI đưa lỗ hổng bảo mật vào code của bạn.

### 3.1 Dependency Auditing
- Luôn yêu cầu AI giải trình tại sao nó muốn cài thêm một thư viện mới.
- Chạy `npm audit` thường xuyên.

### 3.2 Human-in-the-loop (HITL)
Phân tách rõ ràng:
- **AI:** Sinh code, viết tests, gỡ lỗi logic.
- **Human:** Review kiến trúc, kiểm tra Business Logic cấp cao, xác nhận các thay đổi nhạy cảm (Auth, Payment).

---

## 📊 4. Validation Metrics

Làm sao biết "Vibe" của bạn đang tốt?
- **Generation-to-Success Ratio:** Bạn phải sửa lại AI bao nhiêu lần mới xong task?
- **Bug leakage:** Có bao nhiêu lỗi lọt qua lưới AI-testing?
- **Speed-to-Market:** Thời gian từ Spec đến Production là bao lâu?

---
🔗 **Resources:**
- [Elite 2026 Roadmap](file:///e:/Google%20Antigravity/Skills/Vibe%20Coding%28L%E1%BA%ADp%20tr%C3%ACnh%20phong%20c%C3%A1ch%20Vibe%29/references/roadmap-2026.md)
