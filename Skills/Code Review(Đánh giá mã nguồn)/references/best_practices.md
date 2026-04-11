# 💡 Elite Code Review Best Practices (2026 Edition)

Bản đặc tả các quy trình và kỹ thuật đánh giá mã nguồn cấp độ Elite, tối ưu cho môi trường **AI-Native** và **High-Speed Engineering**.

---

## 🚀 1. PR Hygiene (Vệ sinh Pull Request)
- **The 400-Line Rule**: Mọi PR phải có quy mô nhỏ hơn 400 dòng code. Nếu quá lớn, bộ não con người không thể review hiệu quả.
- **Contract-First PR**: PR phải bao gồm tài liệu (API Spec/Docs) trước hoặc đi kèm với code thực thi.
- **Context Clarity**: Tác giả phải cung cấp "What, Why, and How to test" trong phần mô tả PR.

## 🤖 2. Agentic Review Protocol (Giao diện AI Review)
- **First Pass (AI)**: Luôn để AI Reviewer ( Sentinel) quét qua trước để dọn sạch các lỗi Nitpick (Format, linting).
- **Consensus Voting**: Sử dụng ít nhất 2 mô hình AI khác nhau để review các PR quan trọng. Nếu chúng không đồng thuận, cần sự can thiệp của Human Senior.
- **Intent Verification**: AI kiểm tra xem code thực tế có khớp với yêu cầu (Prompts/Tickets) hay không.

## 🛡️ 3. Security-First Audit (Thẩm định bảo mật)
- **Secrets Detection**: Tự động chặn các PR chứa thông tin nhạy cảm (API Keys, Tokens).
- **Authorization Depth**: Kiểm tra kỹ các logic phân quyền (Broken Object Level Authorization - BOLA).
- **Data Sanitization**: Soi kỹ các điểm nhập liệu từ người dùng (User Input) để tránh SQL Injection và XSS.

## ⚡ 4. Performance & Scale Audit
- **N+1 Identification**: Phát hiện các truy vấn lặp lại trong vòng lặp hoặc thiếu eager loading.
- **Concurrency Risks**: Kiểm tra Race conditions, Deadlocks trong code đa luồng hoặc async.
- **Resource Usage**: Soi kỹ việc đóng các connection (DB, Stream) để tránh Memory Leak.

## 👨‍💻 5. Professional Communication (Nghệ thuật Góp ý)
- **Conventional Comments**: Sử dụng `(Nitpick)`, `(Suggestion)`, `(Blocker)` để phân loại mức độ nghiêm trọng.
- **Objective Feedback**: Góp ý dựa trên dữ liệu và bài học (references), tránh dùng cảm xúc cá nhân.
- **Knowledge Transfer**: Mỗi comment nên là một cơ hội để dạy và học.

---
> [!IMPORTANT]
> **Elite Creed:** "Code review is not about finding mistakes; it's about raising the collective intelligence of the team."
> 
> *Duy trì bởi Antigravity Quality Assurance Council (2026)*
