# 🌌 Midnight Galaxy Theme

> Một theme vũ trụ đầy kịch tính, với tông màu tím đậm và xanh huyền bí – **mạnh mẽ, bí ẩn và sang trọng**, phù hợp để tạo ấn tượng sâu sắc.

## 🎨 Bảng màu

| Tên màu     | Mã HEX    | Cảm hứng từ            | Ứng dụng gợi ý                              |
| ----------- | --------- | ---------------------- | ------------------------------------------- |
| Deep Purple | `#2b1e3e` | Bầu trời đêm sâu thẳm  | Nền chính, tạo chiều sâu và sự sang trọng   |
| Cosmic Blue | `#4a4e8f` | Tinh vân xanh huyền ảo | Màu nhấn cho nút bấm, đường kẻ, biểu đồ     |
| Lavender    | `#a490c2` | Ánh sáng tím dịu       | Vùng highlight, khung thông tin phụ         |
| Silver      | `#e6e6fa` | Ánh bạc lấp lánh       | Chữ chính, icon, vùng sáng – tương phản cao |

> 💡 Mẹo phối hợp: Dùng `Deep Purple` làm nền toàn bộ, `Silver` cho hầu hết văn bản, `Cosmic Blue` cho các yếu tố tương tác, `Lavender` cho những điểm nhấn nhẹ nhàng.

## 🔤 Kiểu chữ (Typography)

| Loại                  | Phông chữ     | Đặc điểm                                 |
| --------------------- | ------------- | ---------------------------------------- |
| **Tiêu đề (Headers)** | FreeSans Bold | Đậm, rõ, hiện đại – nổi bật trên nền tối |
| **Nội dung (Body)**   | FreeSans      | Sáng, gọn, dễ đọc – giữ được sự tối giản |

> Dùng chung họ FreeSans giúp giao diện nhất quán. Trên nền tối, font sans-serif với độ dày vừa phải đảm bảo khả năng đọc tốt nhất.

## ✅ Khi nào nên dùng theme này

Midnight Galaxy tạo hiệu ứng mạnh trong các bối cảnh:

- 🎬 **Ngành giải trí, rạp chiếu phim** – gợi cảm giác màn ảnh rộng, kịch tính.
- 🎮 **Giới thiệu game, esports** – đồng bộ với không gian ảo, bí ẩn.
- 🌃 **Địa điểm về đêm, câu lạc bộ, bar** – tạo không khí sang trọng, huyền ảo.
- 💎 **Thương hiệu xa xỉ (luxury)** – màu tím đen luôn gắn liền với quyền lực và đẳng cấp.
- 🎨 **Công ty sáng tạo, agency** – thể hiện sự khác biệt, đột phá, không sợ nổi loạn.

## 📂 Cách sử dụng trong Theme Factory Skill

1. Đặt file này vào thư mục `themes/` với tên `midnight-galaxy.md`.
2. Khi người dùng chọn "Midnight Galaxy" từ theme showcase:
   - Màu nền chính: `#2b1e3e` (Deep Purple)
   - Màu chữ chính: `#e6e6fa` (Silver) – để đảm bảo tương phản
   - Màu nút, liên kết, icon: `#4a4e8f` (Cosmic Blue)
   - Màu highlight, khung nhẹ: `#a490c2` (Lavender)
   - Font: FreeSans cho mọi thứ, header dùng Bold
3. Kiểm tra độ tương phản: chữ `#e6e6fa` trên nền `#2b1e3e` rất tốt; chữ trắng trên nền `#4a4e8f` cũng đạt chuẩn.

## 🖼️ Ví dụ nhanh (CSS)

```css
body {
  background-color: #2b1e3e; /* Deep Purple */
  color: #e6e6fa; /* Silver */
  font-family: "FreeSans", sans-serif;
}
h1,
h2,
h3 {
  font-family: "FreeSans", sans-serif;
  font-weight: bold;
  color: #e6e6fa;
  border-bottom: 2px solid #4a4e8f; /* Cosmic Blue */
}
.button {
  background-color: #4a4e8f; /* Cosmic Blue */
  color: #e6e6fa;
  border: none;
  border-radius: 40px;
  padding: 10px 24px;
}
.highlight {
  background-color: #a490c2; /* Lavender */
  color: #2b1e3e;
  padding: 4px 12px;
  border-radius: 20px;
}
```
