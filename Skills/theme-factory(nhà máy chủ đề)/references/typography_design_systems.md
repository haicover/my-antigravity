# 🔠 Mastery Chapter 2: Typography & Design Systems

> Khám phá nghệ thuật sắp chữ, hệ thống lưới (grid) và cách xây dựng các Design Tokens bền vững.

## 📐 1. The Power of Typography

Typography không chỉ là chọn font chữ, đó là việc thiết lập **Hierarchy (Thứ bậc)** và **Readability (Khả năng đọc)**.

### 1.1 Font Pairing Rules
- **Contrast is Key:** Kết hợp một font Serif (có chân) cho tiêu đề và Sans-serif (không chân) cho nội dung, hoặc ngược lại.
- **Limit Your Faces:** Không nên dùng quá 2-3 font family trong một dự án.
- **X-Height Matters:** Chọn font có x-height lớn cho nội dung để dễ đọc trên màn hình nhỏ.

### 1.2 Vertical Rhythm & Spacing
- **The 8pt Grid:** Sử dụng bội số của 8 (8, 16, 24, 32...) cho margin, padding và line-height để tạo sự cân bằng toán học.
- **Line Height (Leading):** Thường nằm trong khoảng `1.4` đến `1.6` lần font-size cho body text.

---

## 💎 2. Design Tokens: The Language of Systems

Design Tokens là các "nguyên tử" của CSS, giúp đồng bộ hóa giữa thiết kế và code.

| Token Type | Unit Examples | Purpose |
| :--- | :--- | :--- |
| **Spacing** | `4px`, `8px`, `16px` | Định nghĩa khoảng cách nhất quán. |
| **Sizing** | `1rem`, `1.25rem` | Quy mô font chữ (Text Scales). |
| **Radius** | `4px`, `8px`, `full` | Bo góc của các thành phần UI. |
| **Shadows** | `sm`, `md`, `lg` | Độ nổi (Elevation) của component. |

---

## 📏 3. Responsive Typography

Đừng dùng giá trị cố định (`px`). Hãy dùng:
- **REM:** Dựa trên root font size (mặc định 16px).
- **EM:** Dựa trên font size của cha.
- **Clamp():** `font-size: clamp(1rem, 5vw, 2rem);` giúp font tự co giãn mượt mà giữa các thiết bị.

---

## 🛠️ 4. Recommended Font Stacks (2026)
- **Modern Tech:** Inter + JetBrains Mono.
- **Elegant Business:** Playfair Display + Lato.
- **Clean SaaS:** Outfit + Plus Jakarta Sans.

---
🔗 **Resources:**
- [Google Fonts](https://fonts.google.com/) - Kho font miễn phí chất lượng cao.
- [Typescale](https://type-scale.com/) - Công cụ tính toán tỉ lệ font chữ.
- [Next Chapter: Visual Storytelling](file:///e:/Google%20Antigravity/Skills/theme-factory%28nh%C3%A0%20m%C3%A1y%20ch%E1%BB%A7%20%C4%91%E1%BB%81%29/references/visual_storytelling_branding.md)
