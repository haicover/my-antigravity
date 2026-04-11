# 🌅 Golden Hour Theme

> Một bảng màu mùa thu ấm áp, phong phú, lấy cảm hứng từ khoảnh khắc **“giờ vàng”** khi hoàng hôn buông xuống – tạo bầu không khí **ấm cúng, sang trọng và đầy mời gọi**.

## 🎨 Bảng màu

| Tên màu         | Mã HEX    | Cảm hứng từ           | Ứng dụng gợi ý                                                    |
| --------------- | --------- | --------------------- | ----------------------------------------------------------------- |
| Mustard Yellow  | `#f4a900` | Nắng cuối ngày rực rỡ | Màu nhấn mạnh (nút CTA, icon, tiêu đề phụ) – thu hút mọi ánh nhìn |
| Terracotta      | `#c1666b` | Đất nung ấm áp        | Màu phụ cho đường viền, highlight, khung ảnh                      |
| Warm Beige      | `#d4b896` | Cát vàng lúc chiều tà | Nền chính mềm mại, trung tính, không gây mỏi mắt                  |
| Chocolate Brown | `#4a403a` | Sô cô la đậm đà       | Chữ tiêu đề chính, chân trang, tạo độ tương phản cao              |

> 💡 Mẹo phối hợp: Dùng `Warm Beige` làm nền toàn bộ, `Mustard Yellow` cho các yếu tố cần nổi bật, `Terracotta` làm điểm nhấn dịu, `Chocolate Brown` cho phần lớn văn bản để đảm bảo dễ đọc.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ     | Đặc điểm                                  |
| --------------------- | ------------- | ----------------------------------------- |
| **Tiêu đề (Headers)** | FreeSans Bold | Đậm, rõ ràng, hiện đại – tạo sự chắc chắn |
| **Nội dung (Body)**   | FreeSans      | Nhẹ hơn, thoáng, dễ đọc lướt              |

> Dùng chung một họ FreeSans giúp giao diện nhất quán, không bị rối mắt. Việc chỉ thay đổi độ đậm vẫn đủ phân cấp thông tin.

## ✅ Khi nào nên dùng theme này

Golden Hour tỏa sáng trong các bối cảnh cần sự ấm áp, gần gũi và sang trọng:

- 🍽️ **Nhà hàng, quán cà phê, ẩm thực** – màu vàng và đỏ đất kích thích vị giác, tạo cảm giác ngon miệng.
- 🏨 **Thương hiệu khách sạn, dịch vụ lưu trú** – truyền tải sự chào đón, thoải mái, ấm cúng.
- 🍂 **Chiến dịch mùa thu, lễ hội** – đồng bộ với sắc màu của lá phong, bí ngô, hoàng hôn.
- 🕯️ **Nội dung về lối sống ấm cúng (cozy lifestyle)** – gợi nhắc những tối mùa đông bên lò sưởi.
- 🧵 **Sản phẩm thủ công, artisan** – tạo cảm giác mộc mạc, chân thật, giàu giá trị truyền thống.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đặt file này vào thư mục `themes/` với tên `golden-hour.md`.
2. Khi người dùng chọn "Golden Hour" từ theme showcase:
   - Màu nền chính: `#d4b896` (Warm Beige)
   - Màu tiêu đề chính & chữ: `#4a403a` (Chocolate Brown)
   - Màu nút, liên kết, icon: `#f4a900` (Mustard Yellow)
   - Màu đường viền, khung, highlight: `#c1666b` (Terracotta)
   - Font: FreeSans cho mọi thứ, header dùng phiên bản Bold
3. Kiểm tra độ tương phản: chữ `#4a403a` trên nền `#d4b896` rất rõ; chữ trắng trên nền `#f4a900` hoặc `#c1666b` cũng đảm bảo.

## 🖼️ Ví dụ nhanh (CSS)

```css
body {
  background-color: #d4b896; /* Warm Beige */
  color: #4a403a; /* Chocolate Brown */
  font-family: "FreeSans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "FreeSans", sans-serif;
  font-weight: bold;
  color: #4a403a;
}
.button {
  background-color: #f4a900; /* Mustard Yellow */
  color: #4a403a;
  border: none;
  border-radius: 30px;
  padding: 10px 20px;
  font-weight: bold;
}
.highlight {
  background-color: #c1666b; /* Terracotta */
  color: white;
  padding: 4px 8px;
  border-radius: 8px;
}
```
