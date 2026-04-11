# Domain 7: Crisis Management (Quản lý khủng hoảng cho EM)

## Tại sao giai đoạn này quan trọng?
Khủng hoảng là bài kiểm tra thực sự cho vai trò quản lý. Khi hệ thống bị sập (Outage), dữ liệu bị rò rỉ (Security breach) hoặc kĩ sư mệt mỏi (Burnout), EM phải là điểm tựa bình tĩnh để dẫn dắt team vượt qua. Quản lý khủng hoảng tốt không chỉ là giải quyết sự cố mà còn là bảo vệ sức khỏe cho các thành viên.

---

## 🏗️ Phản ứng sự cố (Incident Response)
- **Incident Commander (IC)**: Người điều phối chính, không trực tiếp fix bug nhưng quản lý thông tin và các bên liên quan.
- **War Room Management**: Thiết lập một không gian (Slack channel hoặc Zoom) duy nhất cho sự cố. Các vai trò cần có:
  - **Communications Lead**: Gửi thông tin cập nhật cho sếp và khách hàng.
  - **Technical Lead**: Tập trung vào việc tìm nguyên nhân và khắc phục.
- **Giao tiếp trong sự cố**:
  - Cập nhật 30 phút một lần (Dù có tiến triển gì mới hay không).
  - Sử dụng các mẫu có sẵn để truyền đạt rõ ràng về tình hình và dự kiến khắc phục.

## ⚙️ Giảm thiểu rủi ro & Hạ tầng hồi phục
- **DR (Disaster Recovery)**: Kế hoạch phục hồi thảm họa.
- **RTO (Recovery Time Objective)** và **RPO (Recovery Point Objective)**: Các chỉ số mục tiêu để phục hồi hệ thống.
- **On-call Health**: Thiết kế lịch trực (On-call rotation) công bằng và hiệu quả để tránh gây áp lực quá lớn cho kĩ sư.

## 🧬 Hỗ trợ team trong khủng hoảng
- **Burnout Prevention**: Nhận diện sớm dấu hiệu quá tải và khuyến khích nghỉ ngơi bù sau các đợt cày cuốc (Crunch).
- **Lãnh đạo trong tình huống khẩn cấp**: Giữ sự bình tĩnh, không đổ lỗi và tập trung vào giải pháp thay vì tìm người gây ra lỗi.
- **Service Recovery (Khôi phục dịch vụ)**: Kế hoạch cắt tỉa tính năng (Feature shedding) để giữ các phần lõi hoạt động ổn định nhất.

---

## 📋 Checklist: 20 mục kiểm tra rủi ro trước khi ra mắt (Production Ready)
- [ ] Bạn đã có log và monitoring đầy đủ chưa?
- [ ] Bạn đã thực hiện Load Test chưa?
- [ ] Quy trình Rollback đã được kiểm tra chưa?
- [ ] Ai là người trực On-call trong 24 giờ đầu?
- [ ] Bạn đã thông báo cho bộ phận Support chưa?

---

## 💡 Pro Tip
Hãy sử dụng **Post-incident Analysis (5 Whys)**. Đừng dừng lại ở "Lỗi do engineer X commit nhầm code". Hãy hỏi "Tại sao engineer X có thể commit code sai?", "Tại sao code sai không được phát hiện bởi CI/CD?", "Tại sao monitoring không báo động ngay lập tức?". Tìm ra gốc rễ vấn đề sẽ ngăn chặn lỗi tương tự lặp lại.
