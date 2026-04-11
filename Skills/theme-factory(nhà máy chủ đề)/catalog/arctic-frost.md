# ❄️ Arctic Frost Theme

> Một theme lấy cảm hứng từ mùa đông mát lạnh, sắc nét – mang lại sự **rõ ràng**, **chính xác** và **chuyên nghiệp** cho mọi artifact.

## 🎨 Bảng màu

| Tên màu     | Mã HEX    | Ứng dụng gợi ý                              |
| ----------- | --------- | ------------------------------------------- |
| Ice Blue    | `#d4e4f7` | Nền nhạt, vùng tô sáng (highlight)          |
| Steel Blue  | `#4a6fa5` | Màu nhấn chính (nút, đường kẻ, tiêu đề phụ) |
| Silver      | `#c0c0c0` | Yếu tố kim loại, đường viền, khung          |
| Crisp White | `#fafafa` | Nền sạch, vùng đọc chính, chữ tối           |

> 💡 Mẹo: Sử dụng `Ice Blue` làm nền chính, `Steel Blue` để làm nổi bật, `Crisp White` cho vùng nội dung cần độ tương phản cao.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ        |
| --------------------- | ---------------- |
| **Tiêu đề (Headers)** | DejaVu Sans Bold |
| **Nội dung (Body)**   | DejaVu Sans      |

> DejaVu Sans là họ font sans-serif dễ đọc, hỗ trợ nhiều ký tự đặc biệt – rất phù hợp với môi trường kỹ thuật và y tế.

## ✅ Khi nào nên dùng theme này

Arctic Frost đặc biệt hiệu quả trong các bối cảnh:

- 🏥 **Y tế & Dược phẩm** – tạo cảm giác sạch sẽ, vô trùng, chính xác.
- 💻 **Công nghệ & giải pháp sạch** – truyền tải sự hiện đại, mát mẻ, thân thiện với môi trường.
- ⛷️ **Thể thao mùa đông** – gợi nhắc băng tuyết, không khí trong lành.
- 📊 **Báo cáo & slide dữ liệu** – màu sắc trung tính, ít gây mỏi mắt.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đảm bảo file này nằm trong thư mục `themes/` với tên `arctic-frost.md` (hoặc tương thích).
2. Khi người dùng chọn "Arctic Frost" từ theme showcase, hệ thống sẽ đọc file này và áp dụng:
   - Màu nền: `#fafafa` hoặc `#d4e4f7`
   - Màu nhấn: `#4a6fa5`
   - Màu viền/phụ: `#c0c0c0`
   - Font: DejaVu Sans (Bold cho header, Regular cho body)
3. Đảm bảo độ tương phản (ví dụ: chữ đen trên nền `#fafafa` hoặc chữ trắng trên nền `#4a6fa5`).

---

## 🖼️ Ví dụ nhanh (mô phỏng)

```html
<style>
  body {
    background-color: #fafafa; /* Crisp White */
    color: #1e2a3a; /* tối tự chọn để đọc tốt */
    font-family: "DejaVu Sans", sans-serif;
  }
  h1,
  h2,
  h3 {
    font-family: "DejaVu Sans Bold", sans-serif;
    color: #4a6fa5; /* Steel Blue */
  }
  .highlight {
    background-color: #d4e4f7; /* Ice Blue */
  }
  .accent {
    border-bottom: 2px solid #c0c0c0; /* Silver */
  }
</style>
```
