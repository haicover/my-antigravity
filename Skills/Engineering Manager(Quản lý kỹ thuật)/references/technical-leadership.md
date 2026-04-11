# Domain 2: Technical Leadership (Dẫn dắt kỹ thuật cho EM)

## Tại sao giai đoạn này quan trọng?
Dù không còn code trực tiếp, EM vẫn phải chịu trách nhiệm về chất lượng và định hướng kỹ thuật của team. Bạn cần duy trì hiểu biết về hệ thống để có thể đưa ra các quyết định chiến lược, quản lý nợ kỹ thuật (Technical Debt) và đánh giá các rủi ro dài hạn. EM giỏi là người biết cách đặt ra các tiêu chuẩn cao mà không cần trực tiếp thực hiện chúng.

---

## 🏗️ Cách duy trì năng lực kỹ thuật mà không cần code
- **Code Reviews**: Tham gia review các phần quan trọng để hiểu cách hệ thống đang vận hành.
- **Architecture Reviews**: Tổ chức và dẫn dắt các buổi thảo luận về kiến trúc hệ thống.
- **ADRs (Architecture Decision Records)**: Ghi lại các quyết định kiến trúc quan trọng để dễ dàng truy vết và học hỏi.
- **Prototypes & Spikes**: Thỉnh thoảng dành thời gian tự xây dựng các mẫu thử nhỏ cho các công nghệ mới.

## ⚙️ Quản lý nợ kỹ thuật (Technical Debt)
Nợ kỹ thuật không phải là điều xấu, nó là một công cụ kinh doanh nếu được quản lý đúng cách:
- **4 Loại nợ kỹ thuật**:
  - **Chủ động/Có suy nghĩ**: "Chúng ta sẽ làm nhanh để đưa ra thị trường trước và fix sau".
  - **Bị động/Thiếu suy nghĩ**: Code cẩu thả, không có kiến trúc.
  - **Phát sinh**: Công nghệ cũ đi, yêu cầu thay đổi.
- **Cách xử lý**: Dành 20% thời gian mỗi Sprint để trả nợ kỹ thuật và thuyết phục Business về những lợi ích dài hạn (Tốc độ phát triển nhanh hơn, Ít lỗi hơn).

## 🧬 Các chỉ số DORA (Đo lường hiệu suất kỹ thuật)
1. **Deployment Frequency**: Tần suất triển khai code lên Production.
2. **Lead Time for Changes**: Thời gian từ khi code xong đến khi User dùng được.
3. **Change Failure Rate**: Tỷ lệ deploy gây ra lỗi nghiêm trọng.
4. **Time to Restore Service (MTTR)**: Thời gian trung bình để phục hồi khi có sự cố.

---

## 🛠️ Build vs Buy Framework (Xây dựng hay Mua)
| Tiêu chí | Điểm (1-5) | Lý do |
|----------|------------|-------|
| Core Competency? (Giá trị lõi?) | | Nếu không phải lõi, hãy cân nhắc "Buy". |
| Chi phí vận hành (Total Cost)? | | Server, Bảo trì, Nhân lực. |
| Thời gian đưa ra thị trường? | | "Buy" thường nhanh hơn "Build". |
| Khả năng tùy biến? | | "Build" mang lại sự linh hoạt tuyệt đối. |

---

## 💡 Pro Tip
Hãy sử dụng **ADRs (Architecture Decision Records)** ngay từ bây giờ. Nó giúp team hiểu rõ "Tại sao chúng ta lại chọn giải pháp X vào thời điểm Y?". Điều này cực kỳ quan trọng để các thành viên mới hòa nhập nhanh chóng và tránh lặp lại các sai lầm cũ.
