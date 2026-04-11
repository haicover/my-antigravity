# Bonus Phase: Documentation & Logging (Tài liệu và Ghi nhật ký)

## Tại sao giai đoạn này quan trọng?
Một ứng dụng chuyên nghiệp cần có tài liệu hướng dẫn và hệ thống ghi nhật ký (Logging) tốt để bảo trì và gỡ lỗi (Debugging). **Javadoc** giúp đồng nghiệp hiểu code của bạn, còn **SLF4J/Logback** giúp bạn theo dõi những gì đang xảy ra trong ứng dụng khi nó đang chạy thực tế trên server (Production).

---

## 🏗️ Javadoc: Tài liệu hóa mã nguồn
- **Tags**: 
  - `@param`: Giải thích tham số đầu vào.
  - `@return`: Giải thích kết quả trả về.
  - `@throws`: Giải thích các ngoại lệ có thể xảy ra.
  - `@see`: Liên kết tới các class/hàm liên quan khác.

## ⚙️ Logging Framework (SLF4J & Logback)
- **SLF4J**: Một lớp trừu tượng (Facade) giúp bạn thay đổi thư viện logging (Logback, Log4j2) mà không cần đổi code.
- **Log Levels**: 
  - `TRACE`: Rất chi tiết (Nhấn debug).
  - `DEBUG`: Thông tin hỗ trợ fix lỗi.
  - `INFO`: Thông tin quan trọng về tiến trình (Mặc định).
  - `WARN`: Sự kiện bất thường nhưng chưa lỗi.
  - `ERROR`: Lỗi nghiêm trọng cần xử lý ngay.

## 🧬 Logging Best Practices
- **Structured Logging**: Ghi log dưới dạng JSON để các hệ thống như ELK (Elasticsearch, Logstash, Kibana) dễ dàng phân tích.
- **MDC (Mapped Diagnostic Context)**: Thêm thông tin vào log (như Request ID, User ID) để dễ dàng truy vết một luồng xử lý qua nhiều dịch vụ.

---

## 🛠️ Code Example: Logging với SLF4J (Java)
```java
public class ServiceDemo {
    private static final Logger logger = LoggerFactory.getLogger(ServiceDemo.class);

    public void processOrder(Long orderId) {
        logger.info("Bắt đầu xử lý đơn hàng: {}", orderId);

        try {
            // Processing logic...
            if (orderId < 0) {
                logger.warn("ID đơn hàng lạ được phát hiện: {}", orderId);
            }
        } catch (Exception e) {
            logger.error("Lỗi khi xử lý đơn hàng: {}", orderId, e);
        }
    }
}
```

---

## 📋 Checklist: Ghi nhật ký thông minh
- [ ] Không ghi log các thông tin nhạy cảm (Mật khẩu, Số thẻ tín dụng, PII).
- [ ] Không lạm dụng log (Tránh làm đầy ổ cứng server).
- [ ] Chọn đúng mức độ (Level) cho từng loại thông báo.

---

## 💡 Pro Tip
Hãy sử dụng **Structured Logging** (JSON layout). Điều này làm cho việc tìm kiếm và lọc log trên các hệ thống giám sát hiện đại như Grafana Loki hoặc ELK trở nên nhanh hơn gấp 10 lần so với việc đọc các file log văn bản thuần túy.
