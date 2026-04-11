# 3P Update Generator – Progress, Plans, Problems

Một khuôn mẫu và hướng dẫn để viết bản cập nhật nội bộ **siêu ngắn gọn** (30–60 giây đọc) dành cho lãnh đạo, quản lý và đồng đội. Phù hợp với bất kỳ quy mô nhóm nào – từ một nhóm nhỏ đến toàn công ty.

## 🎯 3P là gì?

- **Progress (Tiến độ)**: Những gì đã đạt được trong kỳ vừa qua (tuần trước đến hôm nay) – tính năng đã ship, mốc quan trọng, nhiệm vụ hoàn thành.
- **Plans (Kế hoạch)**: Những việc ưu tiên cao nhất trong kỳ tới (hôm nay đến tuần sau).
- **Problems (Vấn đề)**: Bất cứ điều gì làm chậm tiến độ – thiếu nhân lực, bug chặn, deal thất bại, v.v.

## 📁 Cấu trúc thư mục đề xuất

3p-updates/
├── README.md (file này)
├── templates/
│ └── 3p-template.md
└── examples/
├── team-update.md
└── company-update.md

## ⚙️ Cách sử dụng (cho AI hoặc con người)

### Đối với AI (Claude/GPT)

Khi yêu cầu viết 3P update, hãy **cung cấp tên nhóm** và **khoảng thời gian**. AI sẽ tự động:

1. Làm rõ tên nhóm và thời gian nếu thiếu.
2. Thu thập thông tin từ Slack, Google Drive, Email, Calendar (nếu có quyền truy cập) hoặc hỏi bạn.
3. Viết bản nháp theo đúng định dạng bên dưới.
4. Đảm bảo mỗi phần chỉ 1–3 câu, có số liệu nếu có thể.

### Đối với con người (bạn tự viết)

Hãy điền vào mẫu sau:
[🎉🐧🔥] [Tên nhóm] (Tuần từ DD/MM đến DD/MM)
Progress: [Đã làm gì? Đã ship tính năng gì? Đạt metric nào?]
Plans: [Sắp làm gì? Ưu tiên số 1 là gì?]
Problems: [Vướng mắc gì? Cần ai giúp?]

## 📝 Quy tắc định dạng bắt buộc

- **Emoji**: Chọn 1 emoji vui nhộn, phản ánh không khí nhóm (ví dụ: 🚀, 🐞, 🎯, 💡).
- **Tên nhóm**: Viết chính xác (ví dụ: `Mobile Team`, `Sales VN`, `Công ty ABC`).
- **Khoảng thời gian**: Luôn ghi trong ngoặc đơn, thường là 1 tuần.
- **Mỗi phần**: Progress, Plans, Problems – mỗi mục **1–3 câu**. Không viết dài.
- **Giọng văn**: matter-of-fact (thực tế, đi thẳng vào vấn đề), không hoa mỹ.
- **Dữ liệu**: Có thể dùng số liệu: _“giảm 15% thời gian tải trang”_, _“tuyển 3 kỹ sư”_, _“xử lý 12 bug”_.

## 🛠️ Công cụ hỗ trợ thu thập nội dung (nếu AI có quyền truy cập)

| Công cụ          | Loại thông tin nên tìm                                                   |
| ---------------- | ------------------------------------------------------------------------ |
| **Slack**        | Bài đăng của thành viên trong kênh lớn, nhiều phản hồi                   |
| **Google Drive** | Tài liệu của thành viên chủ chốt, nhiều lượt xem                         |
| **Email**        | Chuỗi email có nhiều phản hồi, nội dung liên quan                        |
| **Calendar**     | Các cuộc họp không lặp lại có tầm quan trọng cao (review sản phẩm, v.v.) |

Nếu không có quyền truy cập, AI sẽ hỏi bạn cung cấp các mục bạn muốn đưa vào.

## ✅ Ví dụ cụ thể

### Ví dụ 1: Cập nhật nhóm kỹ thuật (quy mô nhỏ)

🐞 Mobile Team (Tuần 22-28/03)
Progress: Đã fix 5 critical bugs liên quan đến đăng nhập; ship bản cập nhật version 2.3.0 lên store.
Plans: Tối ưu lại màn hình home và chạy test A/B cho tính năng thông báo push.
Problems: Bị chặn bởi team backend vì API chưa hoàn thiện – cần thêm 2 ngày nữa.

### Ví dụ 2: Cập nhật toàn công ty (quy mô lớn)

🚀 Công ty XYZ (Tuần 01-07/04)
Progress: Ký hợp đồng với 3 khách hàng mới (tổng giá trị 1.2 tỷ); tuyển được 5 nhân sự cho mảng sales.
Plans: Ra mắt chiến dịch marketing tháng 4; tổ chức 2 buổi workshop nội bộ về AI.
Problems: Ngân sách quảng cáo bị cắt 20% do thay đổi chiến lược từ hội đồng quản trị.

## 🔁 Quy trình làm việc chuẩn (Workflow)

1. **Xác định phạm vi** – Tên nhóm + khoảng thời gian (Progress/Problems: tuần qua; Plans: tuần tới)
2. **Thu thập thông tin** – Dùng công cụ hoặc hỏi người dùng
3. **Viết nháp** – Tuân thủ định dạng nghiêm ngặt
4. **Rà soát** – Đảm bảo đọc trong 30–60 giây, có dữ liệu, không lan man

## ⚠️ Lưu ý quan trọng

- Không viết quá 3 câu cho mỗi phần – nếu có nhiều điểm, chọn **3 điểm quan trọng nhất**.
- Không sử dụng định dạng khác (in đậm, gạch đầu dòng, bảng) – chỉ giữ đúng cấu trúc emoji + tên + thời gian + 3 dòng Progress/Plans/Problems.
- Nếu không có dữ liệu, hãy ghi _“Không có vấn đề gì nổi bật”_ thay vì bỏ trống.

---

**Tác giả:** Internal Communications Team  
**Phiên bản:** 1.0  
**Cập nhật lần cuối:** 2026-03-29
