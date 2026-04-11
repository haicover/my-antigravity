# Domain 9: Knowledge Management (Quản lý tri thức cho EM)

## Tại sao giai đoạn này quan trọng?
Tri thức là sức mạnh của team kỹ thuật. Nếu một kĩ sư giỏi nghỉ việc và mang theo toàn bộ kiến thức về hệ thống, team sẽ gặp rủi ro cực lớn (Buss Factor). EM là người xây dựng hệ thống lưu trữ, chia sẻ và cập nhật tri thức để đảm bảo mọi thành viên đều có thể tiếp cận thông tin cần thiết một cách nhanh chóng.

---

## 🏗️ Hệ thống tài liệu (Documentation)
- **Tài liệu kiến trúc (Architecture Docs)**: Sử dụng mô hình **C4 model** (Context, Container, Component, Code) để vẽ các sơ đồ hệ thống.
- **Quy trình làm việc (Process Docs)**: Hướng dẫn Onboarding, quy trình release, cách xử lý sự cố.
- **Runbook / Playbook**: Hướng dẫn chi tiết các bước xử lý cho từng vấn đề kỹ thuật cụ thể.
- **Best Practices**: Định nghĩa ra các quy chuẩn code chung cho team.

## ⚙️ ADR (Architecture Decision Records)
Ghi lại các quyết định kiến trúc quan trọng để dễ dàng truy vết và học hỏi.
- **Template ADR**:
  - **Status**: (Draft, Accepted, Rejected, Deprecated).
  - **Context**: Tại sao chúng ta lại cần đưa ra quyết định này?
  - **Decision**: Giải pháp chúng ta chọn là gì?
  - **Consequences**: Những ảnh hưởng (Tốt và Xấu) của quyết định này?

## 🧬 Truyền đạt tri thức (Knowledge Transfer)
- **Mentoring Programs**: Phân công các engineer kỳ cựu hướng dẫn các thành viên mới.
- **Tech Talks**: Tổ chức các buổi chia sẻ kiến thức chuyên sâu hàng tuần hoặc tháng.
- **Brown Bag Sessions**: Các buổi chia sẻ thân mật trong giờ nghỉ trưa.
- **Onboarding Checklist**: Danh sách các việc cần làm cho một kỹ sư mới trong 30 ngày đầu tiên.

## 🛠️ Công cụ quản lý tri thức
- **Confluence / Notion**: Nơi lưu trữ văn bản và tài liệu chính thức.
- **GitHub / GitLab Wiki**: Tài liệu đi kèm với mã nguồn.
- **Stack Overflow for Teams**: Nơi đặt câu hỏi và trả lời nội bộ.

---

## 📋 Checklist: Giảm thiểu "Bus Factor"
- [ ] Mọi hệ thống quan trọng đều có ít nhất 2 người hiểu rõ nó không?
- [ ] Tài liệu có được cập nhật thường xuyên sau mỗi thay đổi lớn không?
- [ ] Có quy trình bàn giao (Handover) rõ ràng khi một thành viên nghỉ việc không?
- [ ] Team có thường xuyên đảo nhiệm vụ (Rotation) để mọi người hiểu các phần khác nhau của hệ thống không?

---

## 💡 Pro Tip
Hãy biến việc viết tài liệu thành một phần của **Definition of Done (DoD)**. Đừng coi tài liệu là việc phụ. Một tính năng chỉ được coi là hoàn thành khi nó đã có tài liệu hướng dẫn đầy đủ. Điều này giúp team của bạn vận hành bền vững trong dài hạn.
