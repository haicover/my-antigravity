# Company FAQ Generator – Tổng hợp câu hỏi & câu trả lời toàn công ty

Hướng dẫn và khuôn mẫu để **phát hiện các câu hỏi gây nhầm lẫn phổ biến** trong công ty và **trả lời chúng một cách ngắn gọn, nhất quán** – dựa trên các kênh giao tiếp nội bộ (Slack, Email, tài liệu).

## 🎯 Mục đích

Giúp đội ngũ Internal Comms, HR, hoặc AI assistant:

- **Thu thập** những câu hỏi thực sự được nhiều nhân viên quan tâm (ảnh hưởng đến >30% công ty).
- **Soạn câu trả lời** chính xác, dễ hiểu, có kèm nguồn tham khảo.
- **Giảm confusion** và đảm bảo mọi người cùng một thông tin.

## 📁 Cấu trúc thư mục đề xuất

company-faq/
├── README.md
├── templates/
│ └── faq-template.md
├── examples/
│ ├── sample-faqs.md
│ └── weekly-faq-roundup.md
└── tools/
└── slack-crawler-config.md (optional)

## ⚙️ Cách sử dụng

### Đối với AI (Claude/GPT)

Khi được yêu cầu "tổng hợp FAQ toàn công ty", AI sẽ:

1. **Quét các nguồn** (Slack, Email, Google Drive) để tìm câu hỏi có nhiều reaction/reply hoặc tài liệu gây tranh luận.
2. **Chọn lọc** các câu hỏi ảnh hưởng đến nhiều bộ phận (không chỉ một team nhỏ).
3. **Viết câu trả lời** dựa trên thông báo chính thức, link nguồn, nếu không chắc thì nêu rõ “hiện tại chưa có thông tin chính thức”.
4. **Xuất ra** danh sách theo định dạng bên dưới.

### Đối với con người (bạn tự làm)

Hãy sử dụng mẫu dưới đây, mỗi cặp Question/Answer chiếm 2-3 dòng.

## 📝 Định dạng bắt buộc

```markdown
_Question_: [Viết câu hỏi thành 1 câu, rõ ràng, đúng ngữ pháp]
_Answer_: [Viết câu trả lời 1-2 câu, có thể kèm link, dùng giọng “chúng tôi” hoặc “công ty”]
Ví dụ đúng:
_Question_: Khi nào chúng ta sẽ nhận được laptop mới từ đợt nâng cấp phần cứng?
_Answer_: IT đã bắt đầu giao từ ngày 15/03 và sẽ hoàn thành trước 10/04. Bạn có thể kiểm tra lịch giao tại [link Google Sheet] hoặc liên hệ #it-help.
🛠️ Công cụ & cách khai thác dữ liệu
Công cụ Dấu hiệu nhận biết câu hỏi phổ biến
Slack - Tin nhắn có nhiều reaction (👍, 🙋, ❓)

- Thread có >10 reply
- Câu hỏi lặp lại ở nhiều kênh khác nhau
  Email - Email gửi toàn công ty có nhiều người reply hỏi lại
- Câu hỏi được highlight trong FAQ cũ
  Google Drive - Tài liệu có nhiều comment dạng “Ý này nghĩa là gì?”
- Tài liệu chính sách mới có lượt xem cao
  Calendar - Sự kiện All-Hands có phần Q&A, ghi lại câu hỏi chưa được trả lời
  💡 Mẹo: Nếu bạn dùng AI có tích hợp Slack, hãy cho phép đọc các kênh công khai như #general, #ask-anything, #announcements.

🚦 Nguyên tắc chọn câu hỏi
Nên đưa vào FAQ
✅ Liên quan đến thay đổi chính sách (nghỉ phép, bảo hiểm, làm việc từ xa)

✅ Sự kiện lớn (vòng gọi vốn, mua lại, sa thải, leader mới)

✅ Ra mắt sản phẩm hoặc thay đổi quy trình ảnh hưởng đến nhiều phòng ban

✅ Câu hỏi xuất hiện ≥3 lần trong các kênh khác nhau trong vòng 1 tuần

Không nên đưa vào
❌ Câu hỏi chỉ liên quan đến một cá nhân hoặc một team rất nhỏ (ví dụ: “Sao máy in team Marketing bị lỗi?”)

❌ Câu hỏi đã có câu trả lời rõ ràng trong tài liệu onboarding

❌ Câu hỏi mang tính đùa hoặc không nghiêm túc
✍️ Hướng dẫn viết câu trả lời
Tiêu chí Làm thế nào
Dựa trên nguồn chính thức Trích dẫn link đến Slack announcement, email từ CEO, hoặc Google Doc chính sách
Nếu không chắc chắn Ghi rõ: “Thông tin này chưa được xác nhận chính thức. Chúng tôi sẽ cập nhật trong FAQ tuần sau.”
Giọng văn Chuyên nghiệp, nhưng gần gũi. Dùng “chúng tôi” hoặc “công ty”. Không dùng giọng máy móc.
Độ dài Tối đa 2 câu. Nếu câu trả lời dài hơn, hãy tóm tắt và kèm link “xem chi tiết tại đây”.
Cần ý kiến lãnh đạo? Thêm dòng: “Câu hỏi này đang được đội ngũ điều hành xem xét. Chúng tôi sẽ trả lời trong vòng 5 ngày làm việc.”
📋 Ví dụ hoàn chỉnh (5 cặp FAQ cho một tuần)
_Question_: Chúng ta có kế hoạch tuyển thêm nhân sự cho mảng AI trong quý 2 không?
_Answer_: Có. HR đã phê duyệt 12 headcount mới cho AI division. Chi tiết các vị trí đã được đăng trên #careers và [link Google Sheet].

_Question_: Khi nào kết quả đánh giá hiệu suất quý 1 được công bố?
_Answer_: Kết quả sẽ được gửi qua email cá nhân vào ngày 5/4. Nếu chưa nhận được sau ngày 7/4, hãy liên hệ HR qua #hr-support.

_Question_: Tại sao chúng ta ngừng sử dụng công cụ X và chuyển sang Y?
_Answer_: Do vấn đề bảo mật và chi phí. Thông báo từ IT đã được gửi ngày 15/3 [link Slack]. Mọi người cần hoàn thành migration trước 20/4.

_Question_: Có thay đổi gì về chính sách làm việc từ xa sau đợt dịch mới không?
_Answer_: Hiện tại vẫn giữ nguyên chính sách hybrid (3 ngày ở văn phòng, 2 ngày remote). Nếu có điều chỉnh, CEO sẽ thông báo trong All-Hands ngày 10/4.

_Question_: Ai là người liên hệ khi có ý tưởng sản phẩm mới?
_Answer_: Bạn có thể gửi ý tưởng vào kênh #product-ideas trên Slack hoặc điền [mẫu Google Form này]. Đội ngũ PM sẽ xem xét hàng tuần.
🔁 Quy trình làm việc hàng tuần
Thu thập (Thứ 2-4) – Quét Slack, email, tài liệu tìm câu hỏi tiềm năng.

Lọc & ưu tiên (Thứ 5) – Chọn 5-10 câu hỏi có tác động lớn nhất.

Soạn câu trả lời (Thứ 5) – Dựa trên nguồn chính thức, thêm link.

Phản hồi nhanh (Thứ 6) – Gửi bản nháp cho 1-2 người trong HR hoặc Internal Comms để kiểm duyệt.

Công bố (Thứ 6 cuối ngày) – Đăng lên Slack #faq-weekly và lưu vào Google Drive.

⚠️ Lưu ý quan trọng
Không bao giờ đoán câu trả lời nếu không có nguồn. Hãy nói “chúng tôi đang tìm hiểu”.

Tôn trọng tính bảo mật: Nếu câu hỏi liên quan đến thông tin nhạy cảm (lương, sa thải), hãy trả lời một cách chung chung hoặc chuyển lên cấp quản lý.

Cập nhật FAQ cũ: Nếu câu hỏi tương tự đã được trả lời trước đó, hãy link lại thay vì viết lại.

Luôn có lời kêu gọi hành động: “Xem thêm tại link”, “Liên hệ #channel”, “Gửi câu hỏi tiếp theo tại đây”.
Tác giả: Internal Communications / HR Team
Phiên bản: 1.0
Tần suất khuyến nghị: Xuất bản hàng tuần hoặc hai tuần một lần
Cập nhật lần cuối: 2026-03-29

## Giải thích những cải tiến so với bản gốc

| Khía cạnh                      | Bản gốc (instruction thuần)             | Bản README mới                                                                                                                                         |
| ------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Hình thức**                  | Plain text, không markdown, rất khó đọc | Markdown hoàn chỉnh: heading, bảng, bullet, code block, emoji                                                                                          |
| **Cấu trúc**                   | Dạng danh sách đơn điệu                 | Mục lục + các phần rõ ràng: mục đích, cấu trúc thư mục, cách dùng, định dạng, công cụ, nguyên tắc, hướng dẫn viết câu trả lời, ví dụ, quy trình, lưu ý |
| **Đối tượng hướng dẫn**        | Chỉ AI                                  | Cả AI và con người (có hướng dẫn riêng cho con người tự làm)                                                                                           |
| **Ví dụ**                      | Không có ví dụ cụ thể nào               | Có 5 cặp FAQ thực tế, ví dụ đúng và sai                                                                                                                |
| **Công cụ**                    | Liệt kê Slack, Email, Document          | Có **bảng chi tiết** từng công cụ + dấu hiệu nhận biết câu hỏi phổ biến                                                                                |
| **Nguyên tắc chọn lọc**        | Mô tả chung chung                       | Đóng khung bằng ✅/❌, dễ áp dụng                                                                                                                      |
| **Hướng dẫn viết câu trả lời** | Chỉ 2 dòng                              | Có **bảng hướng dẫn** theo từng tiêu chí (nguồn, độ chắc chắn, giọng văn, độ dài, xử lý khi cần exec)                                                  |
| **Quy trình**                  | Không có                                | Có quy trình 5 bước theo ngày trong tuần                                                                                                               |
| **Tính khả thi**               | Không có mẫu                            | Có **mẫu câu hỏi/trả lời** trong phần định dạng bắt buộc, có thể copy dùng ngay                                                                        |
| **Bảo mật & đạo đức**          | Không đề cập                            | Có lưu ý riêng về bảo mật, không đoán bừa, xử lý câu hỏi nhạy cảm                                                                                      |

Bạn chỉ cần **copy toàn bộ khối markdown trên**, lưu thành `README.md` trong thư mục `company-faq/`. Sau đó, bạn có thể:

- Dùng nó để **hướng dẫn AI** (Claude/GPT) tự động tổng hợp FAQ hàng tuần nếu được cấp quyền truy cập Slack/Drive.
- Hoặc **tự làm thủ công** theo mẫu và quy trình có sẵn.

Mọi thứ đã sẵn sàng để triển khai ngay.
```
