# Phase 8: I/O, Networking & Date/Time (Nhập xuất và Thời gian)

## Tại sao giai đoạn này quan trọng?
Để xây dựng các ứng dụng thực tế, bạn cần làm việc với tệp tin (Files), mạng (Networking) và thời gian (Date/Time). Java cung cấp hệ thống **NIO.2** hiện đại để thao tác file nhanh hơn và **Time API** (Java 8+) để xử lý các vấn đề về múi giờ, định dạng ngày tháng một cách an toàn và chính xác.

---

## 🏗️ File I/O (NIO.2)
- **Path & Files API**: Cách tiếp cận hiện đại thay thế cho `File` cũ.
- **Dễ dàng thao tác**: `Files.readString(path)`, `Files.writeString(path, content)`, `Files.delete(path)`.
- **Duyệt thư mục**: `Files.walk(path)` (Sử dụng Stream) để đệ quy qua các thư mục con.

## ⚙️ Networking & HttpClient (Java 11+)
Java cung cấp một HttpClient hiện đại, hỗ trợ cả HTTP/2 và các phương thức đồng bộ/bất đồng bộ.
- **GET / POST Request**: Định nghĩa dễ dàng qua Builder pattern.
- **Async calls**: Phối hợp với `CompletableFuture` để gọi API không chặn (Non-blocking).

## 🧬 Modern Date/Time API (java.time)
- **LocalDate / LocalTime**: Ngày tháng và thời gian không chứa thông tin múi giờ.
- **LocalDateTime**: Kết hợp cả ngày và giờ.
- **ZonedDateTime**: Chứa thông tin múi giờ (Ví dụ: `Asia/Ho_Chi_Minh`).
- **Duration / Period**: Tính toán khoảng cách thời gian.
- **DateTimeFormatter**: Định dạng và phân tích chuỗi ngày tháng dễ dàng.

---

## 🛠️ Code Example: HttpClient & Date/Time
```java
public class IoDemo {
    public static void main(String[] args) throws Exception {
        // 1. HttpClient gọi API bất đồng bộ
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.github.com/"))
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenAccept(System.out::println);

        // 2. Date/Time API hất dẫn
        LocalDateTime now = LocalDateTime.now();
        String formatted = now.format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss"));
        System.out.println("Thời điểm hiện tại: " + formatted);
    }
}
```

---

## 📋 Checklist: Tránh lỗi thời gian
- [ ] Luôn sử dụng `java.time` (Java 8+), tuyệt đối KHÔNG dùng `java.util.Date` hoặc `java.util.Calendar`.
- [ ] Luôn lưu trữ thời gian dưới dạng **UTC** (Unix timestamp hoặc Instant) trong database và chỉ chuyển đổi sang múi giờ địa phương (ZonedDateTime) khi hiển thị cho người dùng.

---

## 💡 Pro Tip
Hãy sử dụng **Files.lines(path)** để đọc các tệp tin văn bản cực lớn. Nó sử dụng Stream để đọc từng dòng thay vì nạp toàn bộ tệp vào bộ nhớ, giúp ứng dụng không bị lỗi `OutOfMemoryError`.
