# 🚀 Project Blueprint: Elite Task Manager (KMP + AI)

## 📌 Tổng Quan (Overview)
**Elite Task Manager** là một dự án mẫu trình diễn toàn bộ sức mạnh của Android Development năm 2026. Đây là một ứng dụng quản lý công việc đa nền tảng (Android/iOS) sử dụng **Kotlin Multiplatform (KMP)** và tích hợp AI cục bộ (**Gemini Nano**) để tự động tóm tắt và phân loại công việc.

## 🛠️ Stack Công Nghệ (Tech Stack)
- **Core Logic:** Kotlin Multiplatform (KMP).
- **UI:** Jetpack Compose (Android) & Compose Multiplatform (iOS).
- **Architecture:** Clean Architecture (Domain - Data - UI).
- **Dependency Injection:** Hilt (Android) & Koin (Shared module).
- **Database:** SQLDelight (Multi-platform persistence).
- **Networking:** Ktor Client.
- **AI Integration:** Google AI Edge SDK (Gemini Nano) for on-device summarization.
- **Concurrency:** Kotlin Coroutines & Flow.

## 🏗️ Cấu Trúc Thư Mục (Directory Structure)
```text
.
├── androidApp/             # Android code (Hilt setup, MainActivity)
├── iosApp/                 # iOS code (SwiftUI wrapper)
├── shared/                 # Common code (KMP module)
│   ├── commonMain/         # Shared logic, Domain, Repositories, Ktor
│   ├── androidMain/        # Android-specific implementations (e.g., File system)
│   └── iosMain/            # iOS-specific implementations
├── ai-core/                # Module xử lý AI (Wrapper cho Gemini Nano)
└── gradle/                 # Version catalogs (libs.versions.toml)
```

## 🌟 Tính Năng Elite (Elite Features)
1. **AI Smart Summary:** Tự động tóm tắt danh sách công việc trong ngày bằng Gemini Nano (không tốn data, bảo mật tuyệt đối).
2. **Offline-first with SQLDelight:** Dữ liệu được đồng bộ và lưu trữ cục bộ mượt mà.
3. **Type-safe Navigation:** Sử dụng thư viện Navigation mới nhất của Compose (Serialization base).
4. **Dark Mode & Material 3:** Giao diện premium, animation 60fps.

## 📅 Roadmap Triển Khai (Implementation Roadmap)
- [ ] **Giai đoạn 1:** Setup cấu trúc KMP Multi-module & SQLDelight.
- [ ] **Giai đoạn 2:** Xây dựng UI bằng Compose Multiplatform.
- [ ] **Giai đoạn 3:** Tích hợp Hilt và Koin cho DI.
- [ ] **Giai đoạn 4:** Cấu hình Google AI Edge SDK và viết module tóm tắt công việc.
- [ ] **Giai đoạn 5:** Tối ưu hiệu năng (Baseline Profiles) & Build Release.

---
_Dự án được thiết kế để huấn luyện kỹ năng Mobile Architect — Hệ sinh thái Elite 2026._
