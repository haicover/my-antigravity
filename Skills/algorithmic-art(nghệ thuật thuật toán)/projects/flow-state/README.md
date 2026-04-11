# 🌊 Lab: The Flow State (Elite Art 2026)

## 🎯 Overview
Xây dựng một hệ thống tranh vẽ thuật toán dựa trên **Flow Fields** (Dòng chảy nhiễu) và **Autonomous Agents** (Thực thể tự trị). Mục tiêu là tạo ra các tác phẩm có cảm giác hữu cơ, mềm mại nhưng được điều phối bởi toán học chặt chẽ.

---

## 🏗️ Architecture (Cấu trúc lab)
1.  **Field Layer**: Một grid các vectors được tạo ra bởi đa tầng Perlin Noise (`noise()`).
2.  **Agent Layer**: Hệ hàng ngàn "hạt" (particles) di chuyển theo hướng của vector tại vị trí của chúng.
3.  **Visual Layer**: Cách các hạt để lại dấu vết (trails) — sử dụng độ alpha thấp để tích lũy mật độ hình ảnh theo thời gian.

---

## 🛠️ Phase-by-Phase Implementation

### Phase 1: Grid & Vector Initial
- Thiết lập grid 2D.
- Tính toán góc xoay dựa trên `noise(x * scale, y * scale, z)`. Lưu ý: `z` có thể dùng làm tham số thời gian để dòng chảy "biến thiên".

### Phase 2: Autonomous Particles
- Tạo class `Particle` với các thuộc tính: `pos`, `vel`, `acc`, `maxSpeed`.
- Phương thức `follow(vectors)`: tìm vector gần nhất trong grid và áp dụng lực đẩy.

### Phase 3: Aesthetic Tuning (Master Layer)
- **Multi-layered Noise**: Kết hợp các mức scale noise khác nhau (một cái cho cấu trúc lớn, một cái cho chi tiết nhỏ).
- **Color Mapping**: Màu sắc thay đổi dựa trên vận tốc (velocity) hoặc vị trí.
- **Parametric UI**: Thêm slider để chỉnh `Noise Influence`, `Particle Life`, và `Flow Strength`.

---

## 🚦 How to run
1.  Copy `templates/viewer.html` làm khung.
2.  Nhúng code p5.js vào phần `VARIABLE`.
3.  Mở bằng browser và nhấn **Random Seed** để khám phá các biến thể vô tận.

---

## 🏆 Success Criteria
- Tác phẩm không bị " visual noise" — các dòng chảy phải rành mạch và có nhịp điệu.
- Hệ thống chạy mượt mà ở 60fps trên trình duyệt.
- Các tham số thay đổi làm thay đổi rõ rệt " personality" của bức tranh (từ êm đềm đến bão tố).

---
> [!TIP]
> **Pro Tip:** Hãy thử thêm một chút **"Jitter"** (rung động ngẫu nhiên) vào vận tốc của hạt để phá vỡ sự hoàn hảo của toán học, giúp tác phẩm trông "người" hơn.
