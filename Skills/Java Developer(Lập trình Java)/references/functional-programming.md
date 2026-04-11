# Phase 7: Functional Programming & Stream API (Lập trình hàm)

## Tại sao giai đoạn này quan trọng?
Lập trình hàm thay đổi cách bạn viết và tư duy về xử lý dữ liệu. Thay vì sử dụng các vòng lặp `for/while` truyền thống, bạn sử dụng các phép toán khai báo (Declarative) như `filter`, `map`, `reduce`. Điều này giúp code ngắn gọn, dễ đọc, dễ bảo trì và quan trọng nhất là dễ dàng thực thi song song (Parallel Processing).

---

## 🏗️ Lambda Expressions & Functional Interfaces
Lambda là cách viết hàm nặc danh (Anonymous functions) cực kỳ súc tích.
- **Cú pháp**: `(parameters) -> { body }`.
- **4 Interfaces cốt lõi**:
  1. **Predicate<T>**: Kiểm tra điều kiện (`T -> boolean`).
  2. **Function<T, R>**: Biến đổi dữ liệu (`T -> R`).
  3. **Consumer<T>**: Tiêu thụ dữ liệu (`T -> void`).
  4. **Supplier<T>**: Cung cấp dữ liệu (`void -> T`).

## ⚙️ Stream API Pipeline (Luồng xử lý)
Một luồng Stream bao gồm 3 bước:
1. **Source (Nguồn)**: `List.stream()`, `Arrays.stream()`.
2. **Intermediate Operations (Xử lý trung gian)**: `filter`, `map`, `sorted`, `distinct`, `limit`. (Không thay đổi dữ liệu gốc).
3. **Terminal Operations (Kết thúc)**: `collect`, `forEach`, `reduce`, `count`, `anyMatch`. (Kết thúc Stream và trả về kết quả).

## 🧬 Các kỹ thuật nâng cao
- **Method References**: `String::toUpperCase`, `System.out::println` — Rút gọn Lambda.
- **Optional**: Giúp xử lý các giá trị rỗng một cách an toàn (`ifPresent`, `orElseThrow`).
- **Parallel Streams**: Tự động tận dụng đa lõi CPU (`.parallelStream()`).

---

## 🛠️ Code Example: Stream API in Action
```java
public class StreamDemo {
    public static void main(String[] args) {
        List<String> fruits = List.of("Apple", "Banana", "Cherry", "Avocado", "Durian");

        List<String> result = fruits.stream()
                .filter(f -> f.startsWith("A")) // Lọc quả bắt đầu bằng A
                .map(String::toUpperCase)      // Viết hoa
                .sorted()                      // Sắp xếp
                .collect(Collectors.toList()); // Lưu vào List mới

        result.forEach(System.out.println); // Output: APPLE, AVOCADO
    }
}
```

---

## 📋 Checklist: Khi nào dùng Parallel Stream?
- [ ] Dữ liệu đủ lớn (Hàng ngàn phần tử trở lên).
- [ ] Phép toán xử lý trong `map` hoặc `filter` tốn nhiều CPU thời gian.
- [ ] Thứ tự xuất hiện không quan trọng.
- [ ] Cẩn thận: Không dùng cho các task I/O (Database, API) — thay vào đó hãy dùng **Virtual Threads**.

---

## 💡 Pro Tip
Hãy sử dụng **Collectors.groupingBy** để thực hiện các phép gom nhóm dữ liệu phức tạp (tương tự như `GROUP BY` trong SQL). Nó là công cụ cực kỳ mạnh mẽ để tạo ra các báo cáo nhanh từ tập hợp dữ liệu.
