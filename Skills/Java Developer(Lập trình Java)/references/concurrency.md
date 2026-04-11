# Phase 6: Concurrency & Virtual Threads (Lập trình đa luồng)

## Tại sao giai đoạn này quan trọng?
Lập trình đồng thời giúp ứng dụng của bạn thực thi nhiều công việc cùng một lúc, từ đó tối ưu hóa tài nguyên hệ thống và cải thiện tốc độ phản hồi. Java 21 mang đến cuộc cách mạng với **Virtual Threads**, giúp việc quản lý hàng triệu luồng xử lý trở nên đơn giản và hiệu quả hơn rất nhiều so với Platform Threads truyền thống.

---

## 🏗️ Luồng xử lý (Threads)
- **Thread class & Runnable Interface**: Cơ bản về đa luồng.
- **Platform Threads**: Được CPU quản lý trực tiếp qua OS, chi phí khởi tạo cao và tốn tài nguyên.
- **Virtual Threads (Java 21)**: Luồng "ảo" siêu nhẹ, do JVM quản lý. Phù hợp cho các ứng dụng I/O intensive (Gọi API, Database).

## ⚙️ Các cơ chế đồng bộ (Synchronization)
- **synchronized**: Khóa một phương thức hoặc khối code, đảm bảo chỉ có 1 thread truy cập tại 1 thời điểm.
- **volatile**: Đảm bảo tính hiển thị (Visibility) của biến trên tất cả các luồng.
- **Locks & ReentrantLock**: Linh hoạt hơn `synchronized`.
- **Atomic Variables**: `AtomicInteger`, `AtomicLong` cho các phép tính toán an toàn không cần khóa.

## 🧬 Framework hỗ trợ
- **ExecutorService**: Quản lý Thread Pool hiệu quả.
- **CompletableFuture**: Lập trình hướng sự kiện (Async pipeline).
- **Concurrent Collections**: `ConcurrentHashMap`, `CopyOnWriteArrayList` — an toàn trong đa luồng.

---

## 🛠️ Code Example: Virtual Threads (Java 21)
```java
public class ConcurrencyDemo {
    public static void main(String[] args) {
        // Khởi tạo hàng triệu Virtual Threads siêu nhẹ
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, 10_000).forEach(i -> {
                executor.submit(() -> {
                    Thread.sleep(Duration.ofSeconds(1));
                    System.out.println("Thực thi task " + i + " trên " + Thread.currentThread());
                });
            });
        } // Executor tự động đóng và đợi tất cả các thread hoàn tất
    }
}
```

---

## 📋 Checklist: Tránh các lỗi đa luồng
- [ ] **Race Condition**: Khi nhiều luồng cùng thay đổi 1 giá trị (Dùng `Atomic` hoặc `Lock`).
- [ ] **Deadlock**: Khi 2 luồng đợi nhau giải phóng tài nguyên.
- [ ] **Visibility Problem**: Dùng `volatile` hoặc `synchronized` để cập nhật trạng thái mới nhất cho các luồng.

---

## 💡 Pro Tip
Hãy sử dụng **Virtual Threads** cho thay thế cho Platform Threads truyền thống nếu ứng dụng của bạn thực hiện nhiều thao tác I/O (như gọi REST API hoặc truy vấn Database). Điều này giúp ứng dụng chịu tải cao hơn mà không cần tăng thêm tài nguyên phần cứng.
