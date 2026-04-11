# Phase 10: Web Frameworks (Các Framework phát triển Web)

## Tại sao giai đoạn này quan trọng?
Phần lớn các công việc Java hiện nay liên quan đến phát triển Backend hoặc Microservices. **Spring Boot** là framework tiêu chuẩn vàng, nhưng bạn cũng nên biết về các lựa chọn hiện đại khác tùy vào nhu cầu cụ thể (Tốc độ khởi động, Hiệu năng đám mây). Hiểu về các framework giúp bạn chọn đúng công cụ cho giải pháp.

---

## 🏗️ Spring Boot (Lựa chọn số 1)
- **Đặc trưng**: "Opinionated" framework. Cung cấp sẵn cơ chế Tự động cấu hình (Autoconfiguration).
- **Hệ sinh thái**: Spring Security, Spring Data, Spring Cloud.
- **Phù hợp**: 90% dự án Backend, từ Monolith đến Microservices.

## ⚙️ Quarkus (Đám mây hiện đại)
- **Đặc trưng**: Tối ưu hóa cho Kubernetes và Native Images (GraalVM).
- **Tốc độ**: Khởi động siêu nhanh (mili giây), tiêu tốn bộ nhớ cực thấp.
- **Phù hợp**: Cloud-native, Serverless, Microservices cần scale nhanh.

## 🧬 Framework tối giản (Lightweight)
- **Javalin**: Cực kỳ đơn giản, lấy cảm hứng từ Koa.js.
- **Play Framework**: Reactive framework, phù hợp cho các luồng xử lý đồng thời lớn.

---

## 🛠️ Code Example: REST API với Spring Boot 3.x
```java
@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public ResponseEntity<String> sayHello() {
        return ResponseEntity.ok("Chào mừng bạn đến với Web Frameworks 2026!");
    }
}
```

---

## 📋 Checklist: Bảng so sánh Framework
| Framework | Learning Curve | Performance | Ecosystem | Use Case |
|-----------|----------------|-------------|-----------|----------|
| **Spring Boot** | Trung bình | Tốt | Cực lớn | Đại đa số dự án |
| **Quarkus** | Trung bình | Cực tốt (Native) | Lớn | Cloud-native |
| **Javalin** | Thấp (Dễ) | Rất tốt | Nhỏ | Micro-project |

---

## 💡 Pro Tip
Hãy sử dụng **Spring Boot** cho các dự án cần độ ổn định cao và tài liệu dồi dào. Nếu bạn đang xây dựng hệ thống chạy trên AWS Lambda hoặc Google Cloud Run, hãy cân nhắc **Quarkus** để tiết kiệm chi phí tài nguyên và cải thiện thời gian khởi động (Cold start).
