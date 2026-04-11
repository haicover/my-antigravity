# 🧪 Mastery Chapter 4: Quality Assurance & Artifact Delivery

> "Độ tin cậy của một hiện vật tương tác (Artifact) quyết định giá trị chuyên nghiệp của nó."

## 🔬 1. Testing Interactive Artifacts

Việc testing trong môi trường single-file có những đặc thù riêng:

### 1.1 UI Testing
- **Visual Regression:** Kiểm tra giao diện trên các kích thước màn hình khác nhau (Mobile vs Desktop).
- **Interactive States:** Đảm bảo các trạng thái Hover, Active, Disabled hoạt động đúng mong đợi.

### 1.2 Logic Testing
Sử dụng **Vitest** để kiểm tra các hàm xử lý logic (Helper functions) hoặc các Custom Hooks quan trọng tách biệt khỏi UI.

---

## 🚀 2. Delivery & Integration

### 2.1 Claude Artifacts Integration
- Copy nội dung file `bundle.html`.
- Paste vào cửa sổ chat với prompt: "Hãy hiển thị mã HTML này dưới dạng một interactive artifact."
- Kiểm tra tính năng "Publish" của Claude để chia sẻ với người khác.

### 2.2 Self-Hosting & Embedding
- Bạn có thể host file `bundle.html` trên GitHub Pages, Netlify hoặc Vercel đơn giản như một file tĩnh.
- Có thể dùng thẻ `<iframe>` để nhúng Artifact này vào một trang web lớn hơn.

---

## 📊 3. Performance & Size Auditing

- **Audit Tool:** Sử dụng Lighthouse để kiểm tra chỉ số hiệu năng.
- **Size Limit:** Luôn theo dõi kích thước file. Nếu vượt quá 5MB, Claude có thể gặp khó khăn khi render.
- **Font Subsetting:** Chỉ bao gồm những bộ ký tự cần thiết nếu dùng font tùy chỉnh.

---

## 🛡️ 4. Security Considerations

- **XSS (Cross-Site Scripting):** Không bao giờ render nội dung người dùng nhập vào dưới dạng HTML mà không qua xử lý (`dangerouslySetInnerHTML`).
- **Secret Management:** Không bao giờ để API Keys (OpenAI, Stripe, Google Maps) trực tiếp trong mã nguồn Artifact vì bất kỳ ai có file này cũng có thể đọc được. Sử dụng Backend Proxy nếu cần API.

---
🔗 **Resources:**
- [Elite 2026 Roadmap](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/roadmap-2026.md)
