# Phase 2 & 3: Object-Oriented Programming (Hướng đối tượng nâng cao)

## Tại sao giai đoạn này quan trọng?
OOP là "linh hồn" của Java. Để làm việc trong các dự án lớn, bạn cần hiểu cách tổ chức code thành các đối tượng, cách chúng kế thừa và giao tiếp với nhau. Java hiện đại (17-21) cung cấp các công cụ mạnh mẽ như **Records** và **Sealed Classes** để làm cho OOP trở nên an toàn và ngắn gọn hơn.

---

## 🏗️ 4 Trụ cột của OOP
1. **Encapsulation (Đóng gói)**: Giấu dữ liệu qua `private` và cung cấp truy cập qua `getters/setters`.
2. **Inheritance (Kế thừa)**: Tái sử dụng code qua `extends` và `super`.
3. **Abstraction (Trừu tượng)**: Định nghĩa "cái gì" thay vì "như thế nào" qua `Interface` và `Abstract Class`.
4. **Polymorphism (Đa hình)**: Một đối tượng có nhiều hình thái qua `Overriding` (Ghi đè) và `Overloading` (Nạp chồng).

## ⚙️ Các tính năng OOP hiện đại
- **Records (Java 16+)**: Immutable data class cực gọn.
  - `public record User(String name, int age) {}`
- **Sealed Classes (Java 17+)**: Kiểm soát chính xác những class nào được phép kế thừa.
  - `public sealed class SpaceCraft permits Rocket, Station {}`
- **Interfaces**: Hỗ trợ `default` methods (Java 8+) và `private` methods (Java 9+).

## 🧬 Vòng đời đối tượng (Object Lifecycle)
- **Creation (Khởi tạo)**: `new` → Constructor → Allocating memory in Heap.
- **Usage (Sử dụng)**: Tương tác qua reference.
- **GC (Garbage Collection)**: JVM tự động thu hồi bộ nhớ khi đối tượng không còn được sử dụng.

---

## 🛠️ Code Example: Modern OOP Pattern
```java
// Abstract & Sealed
public sealed interface Shape permits Circle, Square {
    double area();
    
    // Default method
    default void print() {
        System.out.println("Shape area: " + area());
    }
}

// Records as implementers
public record Circle(double radius) implements Shape {
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public record Square(double side) implements Shape {
    @Override
    public double area() {
        return side * side;
    }
}
```

---

## 📋 Checklist: Khi nào dùng Interface vs Abstract Class?
- [ ] **Interface**: Khi muốn định nghĩa một "khả năng" (Capability) chung (ví dụ: `Flyable`, `Deletable`).
- [ ] **Abstract Class**: Khi muốn cung cấp một bộ khung chung cho các class có quan hệ họ hàng mật thiết (is-a).

---

## 💡 Pro Tip
Hãy sử dụng **Records** cho mọi DTO (Data Transfer Object) hoặc các class chỉ dùng để chứa dữ liệu. Records tự động tạo `equals()`, `hashCode()`, và `toString()`, giúp bạn tiết kiệm hàng chục dòng code Boilerplate (Lombok-style).
