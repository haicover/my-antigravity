# Phase 5: Java Collections Framework (Hệ thống tập hợp)

## Tại sao giai đoạn này quan trọng?
Để quản lý dữ liệu hiệu quả, bạn cần biết cách lưu trữ và truy vấn chúng. **Collections Framework** cung cấp các cấu trúc dữ liệu tối ưu cho từng mục đích (Sắp xếp, Tìm kiếm, Lọc). Hiểu rõ sự khác biệt giữa `ArrayList`, `HashSet` và `HashMap` giúp bạn tối ưu hóa hiệu năng ứng dụng một cách đáng kể.

---

## 🏗️ Cấu trúc hệ thống Collections (Hierarchy)
- **List Interface**: Các phần tử có thứ tự, cho phép trùng lặp.
  - `ArrayList`: Truy cập nhanh (`O(1)`), thêm/xóa chậm (`O(n)`).
  - `LinkedList`: Thêm/xóa nhanh (`O(1)`), truy cập chậm (`O(n)`).
- **Set Interface**: Các phần tử duy nhất, không trùng lặp.
  - `HashSet`: Không theo thứ tự, tìm kiếm cực nhanh (`O(1)`).
  - `TreeSet`: Các phần tử được sắp xếp độ ưu tiên (Tự nhiên hoặc Custom).
- **Map Interface**: Lưu trữ cặp Key-Value.
  - `HashMap`: Không thứ tự, truy cập Key nhanh (`O(1)`).
  - `LinkedHashMap`: Giữ nguyên thứ tự thêm vào.
  - `TreeMap`: Sắp xếp theo Key.

## ⚙️ Generics: An toàn kiểu dữ liệu (Type Safety)
Generics giúp bạn xác định kiểu dữ liệu mà Collection sẽ chứa, ngăn chặn lỗi `ClassCastException` khi chạy chương trình.
- `List<String> names = new ArrayList<>();`

## 🧬 Các kỹ thuật quan trọng
- **Iterator Pattern**: Duyệt tập hợp an toàn (Tránh lỗi `ConcurrentModificationException`).
- **Collections utility**: `sort()`, `shuffle()`, `reverse()`, `unmodifiableList()`.
- **Performance Cheat Sheet**: `HashSet` cho tra cứu nhanh, `ArrayList` cho quản lý danh sách có thứ tự.

---

## 🛠️ Code Example: Collections in Action
```java
public class CollectionDemo {
    public static void main(String[] args) {
        // Map: Key là ID, Value là tên
        Map<Integer, String> users = new HashMap<>();
        users.put(1, "Antigravity");
        users.put(2, "Developer");

        // List & Streams
        List<String> names = users.values().stream()
                .filter(name -> name.startsWith("A"))
                .sorted()
                .toList();

        System.out.println("Users filtered: " + names);
    }
}
```

---

## 📋 Checklist: Khi nào dùng cái nào?
- [ ] Cần truy cập phần tử nhanh qua index? Dùng **ArrayList**.
- [ ] Cần danh sách ko trùng lặp? Dùng **HashSet**.
- [ ] Cần lưu trữ các cặp dữ liệu liên kết? Dùng **HashMap**.
- [ ] Cần danh sách luôn được sắp xếp? Dùng **TreeSet** hoặc **TreeMap**.

---

## 💡 Pro Tip
Hãy luôn sử dụng **Immutable Collections** (`List.of(...)`, `Set.of(...)`, `Map.of(...)`) cho các giá trị hằng số hoặc dữ liệu không thay đổi. Chúng an toàn hơn và giúp ngăn chặn các lỗi logic không đáng có trong hệ thống.
