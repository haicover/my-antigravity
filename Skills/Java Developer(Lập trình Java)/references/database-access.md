# Phase 11: Database Access (Tương tác cơ sở dữ liệu)

## Tại sao giai đoạn này quan trọng?
Phần lớn các ứng dụng Backend đều cần lưu trữ dữ liệu vào database. Java cung cấp nhiều cách để tương tác, từ mức thấp nhất như **JDBC** (Raw SQL) đến các công cụ trừu tượng mạnh mẽ như **Hibernate** (ORM). Hiểu rõ các phương pháp này giúp bạn chọn đúng kỹ thuật cho từng bài toán về hiệu năng và bảo trì.

---

## 🏗️ JDBC: Nền tảng cốt lõi
- **Đặc trưng**: Gửi SQL thô trực tiếp đến database. Kết nối qua `Connection`, thực thi qua `PreparedStatement`.
- **Ưu điểm**: Kiểm soát tuyệt đối hiệu năng, không tốn tài nguyên cho ORM.
- **Nhược điểm**: Code dài dòng (Boilerplate), dễ gây lỗi SQL Injection nếu không cẩn thận.

## ⚙️ Hibernate: Object-Relational Mapping (ORM)
- **Đặc trưng**: Tự động ánh xạ (Mapping) giữa các Class Java và các Table SQL.
- **Tính năng**: Lazy Loading, Caching, HQL (Hibernate Query Language).
- **Phù hợp**: Ứng dụng nghiệp vụ phức tạp, cần phát triển nhanh.

## 🧬 Spring Data JPA (Phổ biến nhất)
- **Đặc trưng**: Tận dụng Hibernate nhưng rút gọn mã nguồn qua interface.
- **Lợi ích**: Tự động sinh query dựa trên tên hàm (ví dụ: `findByEmail`).
- **Phù hợp**: Đại đa số dự án Spring Boot hiện nay.

---

## 🛠️ Code Example: Entity Mapping (Hibernate)
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    private String email;
    
    // Getters / Setters / Constructors
}
```

---

## 📋 Checklist: Chống SQL Injection
- [ ] Luôn sử dụng **PreparedStatement** (JDBC) hoặc tham số hóa trong query (`:name` trong JPA).
- [ ] Tuyệt đối KHÔNG BAO GIỜ nối chuỗi trực tiếp từ Input người dùng vào câu lệnh SQL.

---

## 💡 Pro Tip
Hãy sử dụng **HikariCP** cho Database Connection Pooling. Nó là thư viện quản lý kết nối nhanh nhất hiện nay và đã được tích hợp mặc định trong Spring Boot 2.x/3.x, giúp giảm thiểu tối đa độ trễ khi kết nối đến database.
