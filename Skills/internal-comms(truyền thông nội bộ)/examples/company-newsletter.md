# Company-Wide Newsletter Generator

Khuôn mẫu và hướng dẫn để viết **bản tin nội bộ toàn công ty** (20–25 bullet points) – tóm tắt tuần/tháng vừa qua, gửi qua Slack/email, dễ đọc trong vài phút.

## 🎯 Mục đích

Giúp lãnh đạo và đội ngũ nội bộ truyền thông tạo ra bản tin:

- **Ngắn gọn, súc tích** – mỗi bullet 1–2 câu.
- **Giàu liên kết** – dẫn đến tài liệu Google Drive, tin nhắn Slack quan trọng, email toàn công ty, sự kiện lịch, bài báo.
- **Giọng văn "we"** – thể hiện tinh thần tập thể: _“Chúng ta đã ra mắt tính năng X”_, _“Chúng ta đã ký hợp đồng Y”_.
- **Phân chia theo chủ đề** – dễ theo dõi với công ty 1000+ nhân viên.

## 📁 Cấu trúc thư mục đề xuất

company-newsletter/
├── README.md
├── templates/
│ └── newsletter-template.md
├── examples/
│ └── sample-newsletter.md
└── tools/
└── slack-gdrive-integration.md (tuỳ chọn)

## ⚙️ Cách sử dụng

### Đối với AI (Claude/GPT)

Khi yêu cầu viết bản tin toàn công ty, AI sẽ:

1. **Thu thập thông tin** từ Slack, Email, Calendar, Google Drive, press bên ngoài (nếu được cấp quyền).
2. **Phân loại** thành các section phù hợp.
3. **Viết 20–25 bullet points**, mỗi bullet 1–2 câu, có link kèm.
4. **Kiểm tra** ưu tiên: tác động toàn công ty, thông báo lãnh đạo, cột mốc lớn, press.
5. **Xuất bản** dưới dạng markdown dễ copy vào Slack/email.

Nếu **không có quyền truy cập** công cụ, AI sẽ hỏi bạn cung cấp danh sách các sự kiện/tài liệu quan trọng.

### Đối với con người (bạn tự viết)

Hãy sử dụng mẫu dưới đây, điền nội dung vào từng section. Mỗi section có thể có 3–7 bullet.

## 📝 Định dạng bắt buộc

Sử dụng emoji cho mỗi section. Dưới đây là cấu trúc khuyến nghị:

```markdown
:megaphone: **Company Announcements**

- [Thông báo quan trọng từ CEO/HR] – kèm link Slack/email
- [Thay đổi chính sách hoặc ngày nghỉ lễ] – kèm link tài liệu

:dart: **Progress on Priorities**

- **Mảng A**:
  - Điểm nổi bật 1 (kèm link)
  - Điểm nổi bật 2 (kèm link)
- **Mảng B**:
  - Điểm nổi bật 1

:pillar: **Leadership Updates**

- Bài đăng của [Tên leader] trên Slack: [tóm tắt nội dung] – [link]
- Ghi chú từ cuộc họp All-Hands: [tóm tắt] – [link ghi chú]

:thread: **Social & Culture Updates**

- Sự kiện team building hoặc sinh nhật công ty
- Chương trình thiện nguyện, v.v.

:newspaper: **External News**

- Bài báo viết về công ty trên [Tên báo] – [link]
- Giải thưởng hoặc chứng nhận đạt được
  Quy tắc viết bullet
  Mỗi bullet tối đa 2 câu.

Bắt đầu bằng động từ mạnh: Ra mắt, Ký kết, Tuyển dụng, Hoàn thành, Công bố, Tổ chức.

Dùng "we" (chúng ta) thay vì "the company" hoặc "the team".

Luôn có link nếu có tài liệu/tin nhắn/sự kiện liên quan.

🛠️ Công cụ thu thập thông tin (cho AI)
Công cụ Cách khai thác
Slack Tìm trong kênh #announcements, #general, #leadership. Ưu tiên tin nhắn có nhiều reaction/trả lời.
Email Lọc email từ exec (CEO, CTO, VP) gửi toàn công ty, có nhiều người reply hoặc CC.
Calendar Sự kiện có số lượng người tham dự lớn (>200): All-Hands, Product Review, Strategy Offsite. Lấy tài liệu đính kèm.
Google Drive Tài liệu mới (tuần qua) có nhiều lượt xem hoặc comment – đặc biệt là vision doc, kế hoạch quý, tài liệu từ exec.
External press Dùng Google News với tên công ty + "just published" trong tuần qua.
💡 Gợi ý: Nếu bạn dùng Claude với Slack/GDrive integration, hãy bật quyền truy cập để AI tự động lấy dữ liệu.

🚦 Nguyên tắc ưu tiên nội dung
Nên đưa vào
✅ Thông báo ảnh hưởng đến >80% nhân viên (thay đổi chế độ làm việc, ngày nghỉ, bảo mật)

✅ Cột mốc lớn: đạt doanh thu X, ra mắt sản phẩm Y, tuyển được Z người

✅ Thông tin từ lãnh đạo cấp cao

✅ Press, giải thưởng, sự kiện bên ngoài
✅ Sự kiện văn hoá toàn công ty (All-Hands, team building lớn)

Không nên đưa vào
❌ Chi tiết chỉ một nhóm nhỏ quan tâm (ví dụ: bug fix của team iOS) – để dành cho 3P Updates

❌ Thông tin đã được gửi riêng lẻ và không cần nhắc lại

❌ Nội dung quá dài (>2 câu mỗi bullet)

📋 Ví dụ hoàn chỉnh (20 bullet)
:megaphone: **Company Announcements**

- [CEO Message] We are moving to a 4-day work week starting May 1 – [link to Slack announcement]
- HR launched a new parental leave policy (20 weeks fully paid) – [link to Google Doc]
- Next All-Hands is scheduled for April 10, 3pm PT – [add to calendar link]

:dart: **Progress on Priorities**

- **Product**:
  - We shipped v3.0 of the mobile app with offline mode – [release notes link]
  - We closed 120+ customer-reported bugs in March – [dashboard link]
- **Sales**:
  - We signed 3 enterprise deals worth $2.5M ARR – [press internal link]
  - We expanded to Japan with a new local team of 8 people
- **Engineering**:
  - We migrated 80% of our infrastructure to Kubernetes – [tech blog link]
  - We reduced average API latency by 35%

:pillar: **Leadership Updates**

- CTO shared a technical roadmap for Q3 – [Slack thread with 150+ reactions]
- CPO's post about "AI-first" strategy – [link to document with 200+ views]

:thread: **Social & Culture Updates**

- We held a company-wide hackathon with 45 projects submitted – [photo album link]
- We donated $50k to local STEM education – [charity link]

:newspaper: **External News**

- TechCrunch featured us: "How [Company] is disrupting logistics" – [link]
- We won "Best Workplace for Innovation 2026" – [award link]
  🔁 Quy trình làm việc chuẩn
  Xác định khoảng thời gian – tuần này hay tháng này?

Thu thập – dùng công cụ hoặc hỏi người dùng

Phân loại – chọn 4–6 section phù hợp (không nhất thiết phải dùng hết các section mẫu)

Viết nháp – 20–25 bullet, mỗi bullet 1–2 câu, nhiều link

Rà soát – kiểm tra đã dùng "we", đã tránh chi tiết nhóm nhỏ chưa?

Gửi kiểm duyệt (nếu cần) – cho người đứng đầu bộ phận truyền thông

⚠️ Lưu ý quan trọng
Không dùng quá 3 level bullet (tránh lồng nhau quá sâu). Nên dùng danh sách phẳng hoặc tối đa 2 cấp.

Nếu công ty bạn <100 người, có thể rút xuống 10–15 bullet.

Luôn kiểm tra link – đảm bảo quyền truy cập nội bộ.

Giọng văn: lạc quan, minh bạch, không phô trương.
Tác giả: Internal Comms Team
Phiên bản: 1.0
Dùng cho: Công ty quy mô 100–5000+ nhân viên
Cập nhật lần cuối: 2026-03-29

## Giải thích những cải tiến so với bản gốc

| Khía cạnh              | Bản gốc (instruction thuần)         | Bản README mới                                                                                                  |
| ---------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Trình bày**          | Plain text, không markdown, khó đọc | Markdown hoàn chỉnh, heading, bảng, bullet, emoji, code block                                                   |
| **Đối tượng**          | Chỉ AI                              | Cả AI và con người (phần “đối với con người” riêng)                                                             |
| **Cấu trúc**           | Dạng danh sách đơn                  | Mục lục + các phần rõ ràng (mục đích, thư mục, cách dùng, định dạng, công cụ, ưu tiên, ví dụ, quy trình, lưu ý) |
| **Hướng dẫn cụ thể**   | Mô tả chung chung “chia section”    | Có **ví dụ section cụ thể** (Company Announcements, Progress on Priorities, v.v.) kèm emoji                     |
| **Ví dụ**              | Chỉ format mẫu ngắn                 | Có **ví dụ hoàn chỉnh 20 bullet** với nội dung thực tế                                                          |
| **Tính khả thi**       | Không có mẫu điền                   | Có **template** trong phần “Định dạng bắt buộc” – bạn chỉ cần copy và thay nội dung                             |
| **Hỗ trợ onboarding**  | Không có cây thư mục                | Có cấu trúc thư mục, gợi ý tên file                                                                             |
| **Nguyên tắc ưu tiên** | Liệt kê dạng văn bản                | Đóng khung trong bảng ✅/❌, dễ nhìn                                                                            |
| **Công cụ**            | Kể tên Slack, Email, Calendar       | Có **bảng chi tiết** từng công cụ và cách khai thác cụ thể                                                      |
| **Phạm vi áp dụng**    | Ngầm hiểu cho công ty lớn           | Ghi rõ: “Công ty quy mô 100–5000+ nhân viên” và lưu ý cho công ty nhỏ hơn                                       |

Bạn chỉ cần **copy toàn bộ khối markdown trên**, lưu thành `README.md` trong thư mục dự án newsletter của bạn. Sau đó, bạn có thể:

- **Tự viết** theo mẫu có sẵn.
- **Yêu cầu AI** (Claude/GPT) đọc file này và sinh bản tin dựa trên dữ liệu bạn cung cấp.

Mọi thứ đã sẵn sàng để dùng ngay.
```
