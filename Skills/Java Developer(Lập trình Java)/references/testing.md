# Bonus Phase: Testing (Kiểm thử phần mềm)

## Tại sao giai đoạn này quan trọng?
Kiểm thử (Testing) là cách duy nhất để đảm bảo ứng dụng của bạn không bị lỗi khi bạn thay đổi code (Regression). Trong Java, **JUnit 5** và **Mockito** là hai công cụ tiêu chuẩn giúp bạn viết các bài test tự động từ Unit Test đến Integration Test. Một lập trình viên chuyên nghiệp luôn đi kèm với bộ code test chất lượng cao.

---

## 🏗️ JUnit 5: Nền tảng Testing
- **Annotations**:
  - `@Test`: Đánh dấu hàm là test case.
  - `@BeforeEach / @AfterEach`: Chạy trước/sau mỗi test case.
  - `@ParameterizedTest`: Chạy cùng một test case với nhiều bộ dữ liệu khác nhau.
- **Assertions**: `assertEquals`, `assertTrue`, `assertThrows` (Kiểm tra xem code có ném ngoại lệ đúng không).

## ⚙️ Mockito: Giả lập đối tượng (Mocking)
- **Đặc trưng**: Tạo ra các đối tượng giả (Mocks) để cô lập class cần test khỏi các thành phần phụ thuộc (Dependencies) như Database hoặc API bên ngoài.
- **Tính năng**: `when().thenReturn()` (Định nghĩa hành vi), `verify()` (Kiểm tra hàm có được gọi không).

## 🧬 Integration Testing (Kiểm thử tích hợp)
- **REST Assured**: Thư viện tuyệt vời để test các REST endpoints.
- **Testcontainers**: Khởi chạy database thực trong Docker để test tích hợp, đảm bảo môi trường test giống hệt môi trường thật.

---

## 🛠️ Code Example: Unit Test với Mockito
```java
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void testFindUserById() {
        // Arrange
        User mockUser = new User(1L, "antigravity");
        when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));

        // Act
        User result = userService.getById(1L);

        // Assert
        assertEquals("antigravity", result.username());
        verify(userRepository).findById(1L);
    }
}
```

---

## 📋 Checklist: Quy trình TDD (Test-Driven Development)
1. **Red**: Viết một test case thất bại (Vì chưa có code xử lý).
2. **Green**: Viết code tối thiểu để test case vượt qua.
3. **Refactor**: Tối ưu hóa lại code của bạn mà vẫn đảm bảo test case xanh.

---

## 💡 Pro Tip
Hãy sử dụng **JaCoCo** (Java Code Coverage) để đo lường tỷ lệ code có test bao quanh (Coverage). Một sản phẩm chất lượng tốt thường có tỷ lệ Coverage từ 80% trở lên cho tầng Service và Repository.
