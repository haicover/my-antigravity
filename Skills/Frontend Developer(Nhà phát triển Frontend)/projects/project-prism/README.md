# Project Prism: Autonomous Frontend Dashboard 2026

**Project Prism** là dự án Lab Flagship dành cho các kỹ sư Frontend muốn chinh phục đẳng cấp Elite. Đây không chỉ là một dashboard thông thường, mà là một hệ thống **Autonomous Frontend** hội tụ những công nghệ tiên tiến nhất của năm 2026.

## 🚀 Vision

Xây dựng một dashboard siêu hiệu năng, có khả năng tự quan sát (Self-observing), tương tác AI-native, và kiến trúc Micro-frontend module hóa hoàn toàn.

## 🛠️ Stack Công Nghệ (Elite Standard)

- **Framework**: Next.js 16 (App Router) + React 19.
- **Rendering**: React Server Components (RSC) + Selective Hydration + Streaming.
- **Styling**: Tailwind CSS v4 + Framer Motion (Layout Transitions).
- **State Management**: Zustand (Client) + TanStack Query (Server).
- **Architecture**: Micro-frontends (Module Federation / Turborepo).
- **Performance**: Edge-side Rendering (ESR) trên Cloudflare/Vercel.
- **AI Integration**: Claude Code SDK cho code analysis & generation dashboard.

## 📈 Các tính năng trọng tâm

1. **Real-time Performance Metrics**: Một "Dashboard trong Dashboard" để theo dõi Core Web Vitals (INP, LCP, CLS) trực tiếp của người dùng.
2. **AI-Driven Data Visualization**: Người dùng có thể yêu cầu AI vẽ biểu đồ từ dữ liệu thô bằng ngôn ngữ tự nhiên.
3. **Dynamic Micro-frontend shell**: Khả năng load và unload các module UI một cách độc lập mà không cần reload trang.
4. **Offline-first with PWA**: Sử dụng Service Workers để đảm bảo dashboard hoạt động mượt mà ngay cả khi mất kết nối.

## 🏗️ Cấu trúc thư mục (Proposed)

```text
project-prism/
├── apps/
│   ├── shell/          # App chính điều phối các micro-frontends
│   ├── analytics/      # Module phân tích dữ liệu
│   └── inventory/      # Module quản lý kho hàng
├── packages/
│   ├── ui/             # Shared Design System (Tailwind + shadcn)
│   ├── config/         # Shared configurations (Linting, build)
│   └── utils/          # Shared helpers
└── README.md
```

## 🎯 Mục tiêu Mastery

- Làm chủ luồng dữ liệu giữa Server và Client trong React 19.
- Tối ưu hóa Interaction to Next Paint (INP) đạt mức "Excellent" (< 200ms).
- Triển khai thành công kiến trúc Monorepo với Turborepo/PNPM.
- Tích hợp AI vào quy trình vận hành Frontend.

---
> [!TIP]
> **Project Prism** là minh chứng cho năng lực thực chiến của bạn. Hãy bắt đầu từ việc setup `shell/` app với Next.js và Tailwind v4.
