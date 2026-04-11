## Phân tích đoạn code gốc (instruction cho AI)

Đoạn code thứ năm này là một **instruction dành cho AI** – hướng dẫn viết các **loại truyền thông nội bộ không theo khuôn mẫu chuẩn** (tức là không phải 3P update, newsletter hay FAQ). Nội dung chính:

- **Bối cảnh**: Khi một yêu cầu truyền thông nội bộ không khớp với 3 định dạng có sẵn.
- **Quy trình trước khi viết**: Hỏi người dùng 4 điều:
  1. Đối tượng mục tiêu (target audience)
  2. Mục đích của thông báo
  3. Giọng văn mong muốn (formal, casual, urgent, informational)
  4. Yêu cầu định dạng cụ thể
- **Nguyên tắc chung**:
  - Rõ ràng, súc tích
  - Dùng câu chủ động (active voice)
  - Đặt thông tin quan trọng nhất lên đầu
  - Bao gồm link và tài liệu tham khảo
  - Phù hợp với phong cách truyền thông của công ty

**Điểm mạnh**: Rất thực tế, có bước làm rõ yêu cầu trước khi viết – tránh hiểu lầm.  
**Điểm yếu**: Trình bày dạng plain text, thiếu cấu trúc README, không có ví dụ minh họa, không có mẫu hoặc checklist cụ thể, thiếu hướng dẫn cho người dùng cuối.

---

## Đoạn code README viết lại xuất sắc (dạng README.md)

Dưới đây là file `README.md` hoàn chỉnh. **Bạn copy toàn bộ khối markdown này** và dán vào file README.md của bạn.

```markdown
# General Internal Communications – Hướng dẫn viết thông báo nội bộ không theo khuôn mẫu

Khi bạn cần viết một **thông báo nội bộ** nhưng nó không phải là 3P update, không phải bản tin toàn công ty (newsletter), cũng không phải FAQ – thì tài liệu này dành cho bạn. Nó giúp bạn (hoặc AI) xác định rõ yêu cầu trước khi viết và tạo ra bản tin rõ ràng, đúng đối tượng.

## 🎯 Khi nào dùng tài liệu này?

Dùng khi:

- ✅ Thông báo thay đổi quy trình làm việc nhưng không phải 3P.
- ✅ Thông báo một cuộc họp đột xuất (không phải newsletter định kỳ).
- ✅ Chia sẻ kết quả khảo sát nội bộ.
- ✅ Gửi lời cảm ơn hoặc ghi nhận thành tích.
- ✅ Thông báo thay đổi nhân sự (nghỉ việc, bổ nhiệm mới).
- ✅ Bất kỳ nội dung giao tiếp nội bộ nào khác **không thuộc 3 format chuẩn**.

Không dùng khi:

- ❌ Đã có khuôn mẫu riêng (3P, newsletter, FAQ) – hãy dùng đúng khuôn mẫu đó để tiết kiệm thời gian.

## 📁 Cấu trúc thư mục đề xuất
```

general-comms/
├── README.md
├── templates/
│ ├── short-announcement.md
│ ├── policy-change.md
│ └── recognition.md
└── examples/
├── example-sick-leave-policy.md
├── example-new-hire.md
└── example-office-closure.md

````

## ⚙️ Quy trình bắt buộc trước khi viết (cho cả AI và con người)

**Không viết bất kỳ nội dung nào cho đến khi bạn trả lời được 4 câu hỏi sau:**

### 1. Xác định đối tượng mục tiêu (Target Audience)
- Toàn công ty? Một phòng ban? Một nhóm nhỏ?
- Ví dụ: “Tất cả nhân viên văn phòng Hà Nội” – khác với “Tất cả nhân viên kỹ thuật toàn công ty”.

### 2. Hiểu mục đích của thông báo (Purpose)
- Thông báo, cảnh báo, khen thưởng, yêu cầu hành động, chia sẻ thông tin, hay giải thích lý do?
- Ví dụ: “Mục đích: Thông báo lịch nghỉ lễ và yêu cầu mọi người cập nhật timesheet trước ngày 30/04.”

### 3. Xác định giọng văn (Tone)
| Loại giọng | Khi nào dùng | Ví dụ câu mở đầu |
|------------|--------------|------------------|
| **Formal** | Thông báo chính sách mới, vấn đề pháp lý, thay đổi cấu trúc công ty | “The management team has approved the following changes to our remote work policy.” |
| **Casual** | Ghi nhận nỗ lực, thông báo nội bộ thân mật, sự kiện văn hóa | “Hey team, just wanted to give a huge shoutout to the customer support crew for handling the last week like champs!” |
| **Urgent** | Sự cố bảo mật, thiên tai, vấn đề vận hành nghiêm trọng | “Immediate action required: Please disconnect all devices from the office network until further notice.” |
| **Informational** | Chia sẻ dữ liệu, báo cáo, kết quả khảo sát | “Here’s a summary of the Q1 engagement survey results. Overall satisfaction increased by 12%.” |

### 4. Xác nhận định dạng cụ thể (Formatting Requirements)
- Chiều dài tối đa? Có cần bullet points? Có cần link đính kèm? Có cần hình ảnh? Gửi qua Slack hay email?
- Ví dụ: “Tối đa 200 từ, gửi trên Slack, có 1 link đến Google Doc chi tiết, không dùng emoji.”

## ✍️ Nguyên tắc viết nội dung (sau khi có 4 câu trả lời)

| Nguyên tắc | Giải thích | Ví dụ (sai → đúng) |
|------------|------------|---------------------|
| **Rõ ràng, súc tích** | Không lan man, mỗi câu chỉ một ý. | *Sai:* “Chúng tôi muốn thông báo rằng sau một quá trình xem xét kỹ lưỡng, công ty đã quyết định thay đổi chính sách nghỉ phép có hiệu lực từ tháng sau.” <br> *Đúng:* “Chính sách nghỉ phép mới có hiệu lực từ 01/05. Chi tiết: [link]” |
| **Dùng câu chủ động (active voice)** | Chủ thể thực hiện hành động đứng đầu câu. | *Bị động:* “Một email sẽ được gửi đến tất cả mọi người vào ngày mai.” <br> *Chủ động:* “Chúng tôi sẽ gửi email đến tất cả mọi người vào ngày mai.” |
| **Thông tin quan trọng nhất lên đầu** | Đọc 2 câu đầu là biết nội dung chính. | *Sai:* “Chào cả nhà, hy vọng ai cũng khỏe. Tuần vừa rồi đội ngũ của chúng ta đã làm việc rất chăm chỉ…” <br> *Đúng:* “[QUAN TRỌNG] Văn phòng sẽ đóng cửa vào thứ Sáu tuần này để bảo trì.” |
| **Có link/tài liệu tham khảo** | Giúp người đọc tìm hiểu sâu nếu cần. | “Chính sách mới được mô tả chi tiết tại [link Google Doc]. Mọi thắc mắc xem tại #hr-faq.” |
| **Phù hợp với phong cách công ty** | Nếu công ty dùng nhiều emoji, hãy dùng. Nếu công ty nghiêm túc, tránh emoji. | Kiểm tra các thông báo trước đây từ cùng một phòng ban để làm mẫu. |

## 📝 Mẫu viết nhanh (template)

Sao chép và điền nội dung vào khung sau:

```markdown
**Tiêu đề:** [Tóm gọn nội dung chính, in đậm]

**Đối tượng:** [ai sẽ nhận?]

**Mục đích:** [thông báo / yêu cầu hành động / khen thưởng / ...]

**Giọng văn:** [formal / casual / urgent / informational]

**Nội dung:**
[Đoạn 1: Thông tin quan trọng nhất]
[Đoạn 2: Chi tiết hỗ trợ, link, hành động cần làm]
[Đoạn 3: (nếu cần) Lời kêu gọi hành động hoặc liên hệ]

**Liên hệ:** [Kênh Slack, email, người phụ trách]
````

## 📋 Ví dụ thực tế

### Ví dụ 1: Thông báo thay đổi giờ làm việc (casual, informational)

```markdown
**Tiêu đề:** 🕒 Thay đổi giờ làm việc từ tháng 5 (áp dụng cho team HCM)

**Đối tượng:** Nhân viên văn phòng TP.HCM

**Mục đích:** Thông báo & yêu cầu cập nhật lịch làm việc mới

**Giọng văn:** Casual, informational

**Nội dung:**
Từ ngày 05/05, văn phòng HCM sẽ chuyển sang khung giờ 9:00 - 17:30 (thay vì 8:30 - 17:00). Lý do: thí nghiệm giờ làm việc linh hoạt dựa trên khảo sát tháng 3. Các bạn dùng phần mềm chấm công cần cập nhật ca làm việc mới trước ngày 30/04. Hướng dẫn chi tiết: [link Google Doc]. Mọi thắc mắc hỏi #hr-hcm.
```

### Ví dụ 2: Thông báo sự cố khẩn cấp (urgent, formal)

```markdown
**Tiêu đề:** [URGENT] Gián đoạn hệ thống email – Đang khắc phục

**Đối tượng:** Toàn công ty

**Mục đích:** Cảnh báo và hướng dẫn hành động tạm thời

**Giọng văn:** Urgent, formal

**Nội dung:**
Hệ thống email công ty đang gặp sự cố từ 8:45 sáng nay. Đội ngũ IT đang khắc phục và dự kiến có lại sau 2 giờ. Trong thời gian này, vui lòng liên hệ nội bộ qua Slack và sử dụng Google Drive để chia sẻ tài liệu. Cập nhật mới nhất sẽ được gửi tại kênh #it-alerts mỗi 30 phút. Xin lỗi về sự bất tiện.
```

### Ví dụ 3: Ghi nhận thành tích (casual, ngắn)

```markdown
**Tiêu đề:** 🎉 Cảm ơn team Sales vì đợt chốt deal kỷ lục

**Đối tượng:** Toàn công ty

**Mục đích:** Khen thưởng, động viên

**Giọng văn:** Casual

**Nội dung:**
Team Sales vừa đóng thành công 4 deal mới trong 2 ngày, tổng giá trị 800k USD – cao nhất quý. Đặc biệt cảm ơn Minh, Lan, và Hùng vì đã làm việc xuyên cuối tuần. Mọi người hãy gửi lời chúc vào #sales-thanks. Sẽ có một buổi ăn trưa tri ân vào thứ Sáu này. 🍕
```

## 🔁 Quy trình làm việc đề xuất

| Bước | Hành động                                                     | Người thực hiện    | Thời gian ước tính |
| ---- | ------------------------------------------------------------- | ------------------ | ------------------ |
| 1    | Trả lời 4 câu hỏi (đối tượng, mục đích, giọng văn, định dạng) | Người yêu cầu / AI | 2 phút             |
| 2    | Viết nháp theo template                                       | AI hoặc người viết | 5-10 phút          |
| 3    | Đọc lại, kiểm tra 5 nguyên tắc                                | Người viết         | 2 phút             |
| 4    | (Tuỳ chọn) Gửi cho 1 đồng nghiệp kiểm tra                     | Người viết         | 5 phút             |
| 5    | Gửi lên kênh đã định (Slack, email, nội bộ)                   | Người viết         | 1 phút             |

## ⚠️ Những sai lầm thường gặp và cách tránh

| Sai lầm                          | Hậu quả                                                   | Cách khắc phục                                                    |
| -------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| Bỏ qua bước hỏi đối tượng        | Viết sai ngữ cảnh, người đọc không quan tâm               | Luôn bắt đầu bằng câu: “Thông báo này gửi đến ai?”                |
| Dùng giọng văn không phù hợp     | Thông báo khẩn cấp mà viết kiểu casual → mọi người bỏ qua | Xác định tone trước khi viết câu đầu tiên                         |
| Chôn thông tin quan trọng ở cuối | Người đọc bỏ lỡ                                           | Đặt câu quan trọng nhất trong 10 từ đầu tiên                      |
| Thiếu link/nguồn tham khảo       | Mọi người hỏi đi hỏi lại cùng một câu                     | Luôn kèm “Chi tiết tại: [link]”                                   |
| Viết quá dài                     | Không ai đọc hết                                          | Giới hạn 200 từ cho Slack, 300 từ cho email (trừ khi thực sự cần) |

## 📌 Tóm tắt nhanh (cheatsheet)

```markdown
Trước khi viết: Hỏi 4 điều (đối tượng, mục đích, giọng văn, định dạng)

Khi viết:

- Rõ ràng, súc tích
- Chủ động
- Quan trọng nhất lên đầu
- Có link
- Đúng phong cách công ty

Mẫu nhanh:
[TIÊU ĐỀ NGẮN]
Đối tượng: ...
Nội dung chính (1 câu): ...
Chi tiết + link: ...
Hành động cần làm: ...
Liên hệ: ...
```

---

**Tác giả:** Internal Communications Team  
**Phiên bản:** 1.0  
**Áp dụng cho:** Mọi loại thông báo nội bộ không thuộc 3P, newsletter, FAQ  
**Cập nhật lần cuối:** 2026-03-29

```

## Giải thích những cải tiến so với bản gốc

| Khía cạnh | Bản gốc (instruction thuần) | Bản README mới |
|-----------|-----------------------------|----------------|
| **Hình thức** | Plain text, không cấu trúc | Markdown hoàn chỉnh: headings, bảng, code block, emoji, checklist |
| **Phạm vi áp dụng** | Mơ hồ: “không vào format chuẩn” | Liệt kê rõ 6+ tình huống cụ thể (thay đổi quy trình, họp đột xuất, khảo sát, khen thưởng, nhân sự, v.v.) |
| **Quy trình trước khi viết** | Chỉ 4 câu hỏi đơn thuần | Chi tiết hoá từng câu hỏi + bảng tone (4 loại kèm ví dụ) |
| **Nguyên tắc viết** | 5 nguyên tắc chung | Có bảng so sánh sai/đúng cho từng nguyên tắc |
| **Mẫu (template)** | Không có | Có template dạng markdown có thể copy-paste ngay |
| **Ví dụ** | Không có | 3 ví dụ đầy đủ (thay đổi giờ làm, sự cố khẩn cấp, ghi nhận thành tích) |
| **Quy trình làm việc** | Không có | Bảng 5 bước kèm thời gian ước tính |
| **Sai lầm thường gặp** | Không đề cập | Bảng 5 sai lầm + cách khắc phục |
| **Cheatsheet** | Không có | Tóm tắt nhanh cuối trang, dễ in ấn |
| **Tính khả thi** | Chỉ AI hiểu | Cả AI và con người đều làm theo được |

Bạn chỉ cần **copy toàn bộ khối markdown trên** và lưu thành `README.md` trong thư mục `general-comms/` (hoặc bất kỳ đâu bạn muốn). Tất cả các phần đã được tích hợp trong một file duy nhất, không tách rời.
```
