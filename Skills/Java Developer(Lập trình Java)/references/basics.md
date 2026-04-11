# Phase 1 & 4: Java Basics & Key Features (Cơ bản về Java & Tính năng cốt lõi)

## Tại sao giai đoạn này quan trọng?
Nền tảng vững chắc là chìa khóa để trở thành một lập trình viên Java giỏi. Hiểu được cú pháp, kiểu dữ liệu, vòng đời của một chương trình Java và các tính năng hiện đại như **Lambda**, **Optional** giúp bạn viết code sạch ngay từ đầu.

---

## 🏗️ Cấu trúc chương trình Java (Anatomy)
- **Compilation**: Code (`.java`) → Bytecode (`.class`) qua `javac`.
- **Execution**: JVM (Java Virtual Machine) thực thi Bytecode trên mọi nền tảng (WORA - Write Once, Run Anywhere).

## ⚙️ Các kiểu dữ liệu (Data Types)
| Kiểu dữ liệu | Đặc điểm | Memory |
|--------------|----------|--------|
| **Primitive** | int, long, double, boolean, char | Stack memory (Nhanh) |
| **Reference** | String, Array, Objects | Heap memory (Linh hoạt) |
- **Autoboxing/Unboxing**: Tự động chuyển đổi giữa primitive và wrapper class (ví dụ: `int` ↔ `Integer`).

## 🧬 Các tính năng Java hiện đại (Java 17-21)
1. **Var (Local Variable Type Inference)**: Rút gọn khai báo biến (Java 10+).
   - `var list = new ArrayList<String>();`
2. **Text Blocks**: Viết chuỗi nhiều dòng dễ dàng (Java 15+).
3. **Switch Expressions**: Trả về kết quả trực tiếp từ switch (Java 14+).
4. **Lambda Expressions**: `(a, b) -> a + b` — nền tảng của lập trình hàm.
5. **Optional**: Ngăn chặn `NullPointerException` (Sử dụng `.ifPresentOrElse`, `.map`, `.orElse`).

---

## 🛠️ Code Example: Modern Java Syntax
```java
public record User(String name, int age) {} // Một dòng để tạo data class

public class Greeting {
    public static void main(String[] args) {
        var user = new User("Antigravity", 1);
        
        // Text blocks
        String welcomeMessage = """
                    Chào mừng %s đến với Java 2026.
                    Hệ thống đã sẵn sàng cho bạn.
                """.formatted(user.name());
        
        System.out.println(welcomeMessage);
    }
}
```

---

## 📋 Checklist: Lỗi thường gặp
- [ ] So sánh chuỗi bằng `==` thay vì `.equals()`.
- [ ] Quên kiểm tra `null` (Dùng `Optional` thay thế).
- [ ] Tràn số nguyên (Integer overflow) khi tính toán số lớn.

---

## 💡 Pro Tip
Hãy sử dụng **Text Blocks** (`"""..."""`) cho các câu lệnh SQL hoặc JSON nằm trong code Java. Nó giúp code cực kỳ dễ đọc và không cần phải nối chuỗi (`+`) phức tạp.
