# 🚀 Project Velocity: AI-Driven Distributed Performance Auditor

Hệ thống giám sát và tối ưu hóa hiệu năng tự động dành cho các ứng dụng quy mô lớn, tích hợp AI để dự đoán các điểm nghẽn và đề xuất giải pháp sửa lỗi tức thì.

---

## 🏗️ Kiến trúc Hệ thống
Hệ thống bao gồm 3 thành phần chính:

1.  **Velocity Engine (Go/Rust)**: Công cụ thu thập dữ liệu (Collector) từ RUM (Real User Monitoring) và Lab Data (Lighthouse).
2.  **AI Insights Processor (Python/PyTorch)**: Phân tích các vết (Waterfall traces) để tìm ra nguyên nhân gốc rễ của sự sụt giảm hiệu năng.
3.  **Velocity Dashboard (Next.js - Elite Interface)**: Giao diện hiển thị dashboard theo thời gian thực với các visualization cao cấp.

---

## 🎯 Tính năng Đột phá (2026 Core)
- **Predictive Optimization**: Phân tích log người dùng để dự đoán họ sẽ click vào đâu tiếp theo, từ đó tự động trigger Preloading/Prefetching với độ chính xác cao.
- **Micro-Waterfall Analysis**: Phân tích chi tiết đến từng micro-task trong Main-thread, xác định chính xác function gây ra Long Task (> 50ms).
- **Auto-Fix Recommendations**: Tích hợp AI Agent để tạo ra các pull request tự động tối ưu ảnh, nén JS hoặc cấu hình lại Cache headers.
- **Global Latency Map**: Bản đồ trực quan hóa độ trễ theo từng vùng địa lý và từng thiết bị (Mobile/Desktop/Tablet).

---

## 🛠️ Stack Công nghệ
- **Backend API**: NestJS (Node.js) hoặc Axum (Rust).
- **Monitoring SDK**: Trình SDK nhỏ gọn (< 2KB) để nhúng vào trang web mục tiêu.
- **Storage**: ClickHouse (danh cho dữ liệu chuỗi thời gian lớn) và Redis (Caching).
- **Visuals**: D3.js & Three.js cho các đồ thị performance phức tạp.

---

## 📅 Lộ trình Phát triển Lab
1.  **Giai đoạn 1**: Xây dựng SDK thu thập các chỉ số cơ bản (FCP, LCP, INP).
2.  **Giai đoạn 2**: Thiết lập Dashboard hiển thị dữ liệu thô.
3.  **Giai đoạn 3**: Tích hợp AI Insights để phân tích Waterfall.
4.  **Giai đoạn 4**: Triển khai tính năng Auto-Fix và CI/CD integration.

---

## 📂 Cấu trúc Thư mục Dự kiến
```bash
project-velocity/
├── sdk/          # Lightweight RUM SDK
├── dashboard/    # Next.js Analytics App
├── backend/      # Data Processing API
├── ai-models/    # Performance Heuristics & ML
└── docs/         # Specifications & Architecture
```

---

*“Velocity isn't just about speed; it's about the speed of improvement.”*
