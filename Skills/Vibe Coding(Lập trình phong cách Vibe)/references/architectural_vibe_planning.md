# 🏛️ Mastery Chapter 1: Architectural Intent & Vibe Planning

> "Vibe Coding is 90% thinking and 10% orchestration."
> Lập trình phong cách Vibe không có nghĩa là lập trình không tư duy. Ngược lại, nó yêu cầu một khả năng kiến trúc hệ thống cực kỳ sắc bén.

## 🏗️ 1. Spec-Driven Development (SDD)

Trong thế giới Vibe, file **Specification (Spec)** là "source of truth" cho AI. Thay vì bắt AI tự đoán, hãy cung cấp một bản thiết kế chi tiết.

### 1.1 Cấu trúc một file Spec chuẩn:
- **Project Goal:** Mục tiêu cốt lõi của tính năng.
- **Tech Stack:** Chỉ định rõ thư viện và phiên bản (e.g., Next.js 15, Tailwind v4).
- **Architecture:** Sơ đồ module, cấu trúc folder.
- **Data Model:** Định nghĩa các bảng Database, quan hệ giữa chúng.
- **API Endpoints:** Danh sách các hàm/route cần triển khai.

## 🎯 2. The MVP Mindset

Đừng bao giờ yêu cầu AI xây dựng một hệ thống khổng lồ cùng lúc.
- **Atomic Tasks:** Chia nhỏ dự án thành các nhiệm vụ nguyên tử (có thể làm xong trong 1-2 lần generate).
- **Incremental Growth:** Build -> Test -> Verify -> Repeat.

---

## 🛠️ 3. Tech Stack Selection for AI

Không phải stack nào cũng thân thiện với AI. Hãy chọn những công nghệ có:
1. **Documentation tốt:** AI được huấn luyện trên những dữ liệu này. (e.g., React, Prisma, Node.js).
2. **Type Safety (TypeScript):** Giúp AI phát hiện lỗi ngay khi sinh code.
3. **Modular Patterns:** Giúp giới hạn Context tốt hơn.

---

## 📋 4. The "Vibe Plan" Artifact

Trước khi cho AI code, hãy bắt nó viết một file `PLAN.md`:
1. Liệt kê các file sẽ tạo mới.
2. Liệt kê các file sẽ chỉnh sửa.
3. Các lệnh terminal sẽ chạy.
4. Điều kiện để coi là Task hoàn thành.

> [!TIP]
> Luôn hỏi AI: "Dựa trên Spec này, hãy phác thảo kế hoạch triển khai của bạn trước khi gõ phím."

---
🔗 **Resources:**
- [Mastery Chapter 2: Context & Agents](file:///e:/Google%20Antigravity/Skills/Vibe%20Coding%28L%E1%BA%ADp%20tr%C3%ACnh%20phong%20c%C3%A1ch%20Vibe%29/references/context_agentic_prompting.md)
