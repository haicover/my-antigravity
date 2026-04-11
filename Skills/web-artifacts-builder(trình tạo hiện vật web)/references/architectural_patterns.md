# 🏛️ Mastery Chapter 1: Architectural Patterns for Artifacts

> "Kiến trúc tốt là nền móng cho những trải nghiệm tương tác liền mạch trong một file HTML duy nhất."

## 🏗️ 1. Single-File Constraints & Opportunities

Trong môi trường Artifact (như Claude), chúng ta bị giới hạn trong một file HTML duy nhất. Tuy nhiên, với React và Bundling hiện đại, chúng ta có thể xây dựng các ứng dụng cực kỳ phức tạp.

### 1.1 App Structure
Mô hình lý tưởng là cấu trúc thư mục Component-based:
- `src/components/`: Nguyên tử UI (Atomic UI).
- `src/features/`: Các module chức năng (e.g., Dashboard, Editor).
- `src/hooks/`: Logic tái sử dụng.
- `src/store/`: Quản lý trạng thái tập trung.

## 🧠 2. State Management Strategy

### 2.1 Zustand (Recommended)
Với Artifacts, Zustand cực kỳ mạnh mẽ vì nhẹ và dễ tích hợp.
- **Why:** Tránh "Prop drilling" khi UI trở nên sâu và phức tạp.
- **Usage:** Tạo một global store để quản lý Auth state, Preferences, hoặc Data fetched.

### 2.2 React Context
Dùng cho các thành phần ở cấp thấp hơn hoặc khi muốn tránh dependency bên ngoài nếu Artifact cần cực nhẹ.

---

## 🚦 3. Mock Routing (Giả lập điều hướng)

Vì chúng ta chỉ có một trang, việc điều hướng thực sự bằng URL là không khả thi.
- **Pattern:** Sử dụng một `viewState` (e.g., 'home', 'settings', 'details') để render component theo điều kiện.
- **Elite Tip:** Sử dụng Framer Motion `AnimatePresence` để các bước chuyển trang trông như một App thực thụ.

---

## 📦 4. Data Persistence (Giả lập)

Artifacts thường mất trạng thái khi re-render hoặc reload.
- **Local Storage:** Lưu dữ liệu tạm thời vào trình duyệt của người dùng.
- **JSON Export/Import:** Cho phép người dùng lưu "Progress" của họ ra file JSON và tải lại sau đó.

---
🔗 **Resources:**
- [Mastery Chapter 2: UI/UX Fidelity](file:///e:/Google%20Antigravity/Skills/web-artifacts-builder%28tr%C3%ACnh%20t%E1%BA%A1o%20hi%E1%BB%87n%20v%E1%BA%ADt%20web%29/references/ui_ux_fidelity.md)
