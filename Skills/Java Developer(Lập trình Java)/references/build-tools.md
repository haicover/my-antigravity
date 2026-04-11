# Phase 9: Build Tools & Dependency Management (Công cụ xây dựng)

## Tại sao giai đoạn này quan trọng?
Để xây dựng các dự án thực tế, bạn cần một công cụ tự động hóa việc biên dịch, chạy test và quản lý các thư viện bên thứ ba (Dependencies). **Maven** và **Gradle** là hai tiêu chuẩn vàng giúp bạn không phải tải file `.jar` thủ công, đồng thời đảm bảo mọi thành viên trong team đều sử dụng cùng một phiên bản thư viện.

---

## 🏗️ Maven (Tiêu chuẩn công nghiệp)
- **pom.xml**: Tệp cấu hình trung tâm (Project Object Model).
- **Phases (Vòng đời)**:
  1. `clean`: Xóa các file build cũ.
  2. `compile`: Biên dịch code.
  3. `test`: Chạy unit tests.
  4. `package`: Đóng gói thành `.jar` hoặc `.war`.
  5. `install`: Cài đặt vào local repository.

## ⚙️ Gradle (Hiện đại & Linh hoạt)
- **build.gradle / build.gradle.kts**: Tệp cấu hình sử dụng Groovy hoặc Kotlin DSL.
- **Ưu điểm**: Tốc độ build cực nhanh (nhờ Incremental Build), cấu hình linh hoạt cho các dự án phức tạp hoặc Android.

## 🧬 Dependency Management (Quản lý thư viện)
- **GroupId / ArtifactId / Version**: Cách định danh độc nhất một thư viện trên Maven Central.
- **Transitive Dependencies**: Khi một thư viện bạn dùng lại phụ thuộc vào những thư viện khác.
- **Exclusion**: Loại bỏ các thư viện không mong muốn bị kéo vào tự động.

---

## 🛠️ Code Example: Một file pom.xml cơ bản (Maven)
```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.antigravity</groupId>
    <artifactId>java-app</artifactId>
    <version>1.0.0</version>

    <dependencies>
        <!-- Thư viện hỗ trợ tiện ích -->
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
            <version>3.12.0</version>
        </dependency>
        
        <!-- Thư viện Testing -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

---

## 📋 Checklist: Khi nào chọn Maven vs Gradle?
- [ ] **Maven**: Dự án chuẩn công nghiệp, cấu hình rõ ràng bằng XML, dễ làm quen.
- [ ] **Gradle**: Dự án cực lớn (Monorepo), cần build nhanh, hoặc phát triển Android.

---

## 💡 Pro Tip
Hãy sử dụng **BOM (Bill of Materials)** khi làm việc với hệ sinh thái Spring hoặc Quarkus. Nó giúp bạn quản lý hàng chục thư viện liên quan mà không cần phải khai báo phiên bản cho từng cái, tránh tối đa các lỗi xung đột phiên bản (Version conflicts).
