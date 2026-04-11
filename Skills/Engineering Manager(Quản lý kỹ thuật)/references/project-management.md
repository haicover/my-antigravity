# Domain 4: Project Management (Quản lý dự án cho EM)

## Tại sao giai đoạn này quan trọng?
EM là người chịu trách nhiệm cuối cùng về việc thực thi và giao hàng (Delivery) của team. Quản lý dự án hiệu quả giúp team không bị quá tải, dự báo được thời gian hoàn thành chính xác và duy trì sự ổn định của hệ thống. Khác với PM chỉ quan tâm đến "What", EM quan tâm sâu sắc đến "How" và "When".

---

## 🏗️ Lập kế hoạch dự án (Project Planning)
- **Resource Allocation (Phân bổ nguồn lực)**: Ai sẽ làm việc gì? Dựa trên kỹ năng và mục tiêu phát triển cá nhân.
- **Sprint Planning**: Ưu tiên các task trong Backlog cho 2 tuần tiếp theo.
- **Timeline Estimation (Ước lượng thời gian)**:
  - **T-shirt sizing**: S, M, L, XL cho các task lớn.
  - **Planning Poker**: Dùng Fibonacci để ước lượng độ khó (Complexity) thay vì thời gian thực tế.
  - **Cone of Uncertainty**: Hiểu rằng ước lượng ban đầu luôn có sai số lớn.

## ⚙️ Quản lý rủi ro & Phụ thuộc (RAID log)
Sử dụng bảng **RAID log** để theo dõi:
- **Risks (Rủi ro)**: Điều gì có thể xảy ra? (Ví dụ: Một kĩ sư xin nghỉ).
- **Assumptions (Giả định)**: Ví dụ: "Giả định API của bên thứ ba hoạt động ổn định".
- **Issues (Vấn đề)**: Những gì đang xảy ra làm chậm tiến độ.
- **Dependencies (Phụ thuộc)**: Những việc team khác phải làm xong thì chúng ta mới bắt đầu được.

## 🧬 Các mô hình Agile cho EM
- **Scrum**: Tập trung vào các buổi họp (Ceremonies) và vai trò (Roles).
- **Kanban**: Tập trung vào luồng (Flow) và giới hạn công việc đang thực hiện (WIP limits) để tránh nghẽn cổ chai.

## 🛠️ Đo lường hiệu quả (Measurement)
- **Velocity (Vận tốc)**: Số lượng Story Points hoàn thành mỗi Sprint. (Lưu ý: Không dùng để so sánh giữa các team khác nhau).
- **Cycle Time**: Thời gian từ khi bắt đầu code đến khi deploy xong.
- **Lead Time**: Thời gian từ khi yêu cầu được ghi lại đến khi người dùng dùng được.
- **Team Health Survey**: Đo lường sự hài lòng và mức độ stress của team định kỳ.

---

## 📋 Checklist: Project Postmortem (Rút kinh nghiệm) - Blameless
Sau mỗi dự án lớn, hãy tổ chức họp để rút kinh nghiệm:
- [ ] Điều gì đã diễn ra tốt đẹp?
- [ ] Những rào cản nào đã xuất hiện?
- [ ] Chúng ta có thể làm gì tốt hơn vào lần sau?
- [ ] Có task nào cần thực hiện ngay sau cuộc họp không? (Action Items).

---

## 💡 Pro Tip
Đừng bao giờ để team của bạn đạt mức **100% công suất**. Hãy luôn dành ra ít nhất 20% cho các công việc không tên như Research, Trả nợ kỹ thuật và Xử lý lỗi phát sinh. Một team "căng cứng" là một team dễ bị tổn thương nhất trước các biến động.
