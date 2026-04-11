# Phase 0: Prerequisites (Điều kiện tiên quyết)

## Tại sao giai đoạn này quan trọng?
Để xây dựng AI Agents hiệu quả, bạn không cần phải là một chuyên gia về AI, nhưng bạn cần có nền tảng vững chắc về phát triển phần mềm cơ bản. AI Agents thực chất là các chương trình máy tính điều khiển các mô hình ngôn ngữ lớn (LLMs), vì vậy kỹ năng lập trình và quản lý dự án là bắt buộc.

---

## 🏗️ Nền tảng Python cơ bản
Python là ngôn ngữ phổ biến nhất trong hệ sinh thái AI. Bạn cần nắm vững:
- **Biến và Kiểu dữ liệu**: Strings, Lists, Dictionaries, JSON.
- **Luồng điều khiển**: If/Else, For/While loops (vòng lặp là trái tim của Agent).
- **Hàm và Lớp (Functions & Classes)**: Để đóng gói logic của Agent và Tools.
- **Xử lý bất đồng bộ (Async/Await)**: Quan trọng khi gọi nhiều API cùng lúc.
- **Quản lý môi trường**: `venv`, `pip`, `poetry` hoặc `conda`.

## 📦 Git & Terminal
- **Git workflow**: `init`, `add`, `commit`, `push`, `branch`, `merge`.
- **Terminal**: Di chuyển thư mục, chạy script, quản lý tiến trình.

## 🌐 REST API & JSON
AI Agents giao tiếp với thế giới qua API. Bạn cần hiểu:
- **HTTP Methods**: GET, POST.
- **Auth**: Headers, Bearer Tokens, API Keys.
- **JSON Parsing**: Gửi và nhận dữ liệu cấu trúc.

---

## 🛠️ Code Example: Gọi API đơn giản (Python)
```python
import requests
import json

def get_ai_response(prompt, api_key):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Đừng quên xử lý lỗi và bảo mật API Key!
```

---

## 📋 Checklist: Bạn đã sẵn sàng chưa?
- [ ] Bạn có thể cài đặt thư viện bằng `pip`.
- [ ] Bạn hiểu cách làm việc với kiểu dữ liệu `dictionary` trong Python.
- [ ] Bạn biết cách tạo file `.env` để lưu API Key.
- [ ] Bạn có thể sử dụng `curl` hoặc `Postman` để test một API.

---

## 💡 Pro Tip
Hãy sử dụng **Claude Code** hoặc **Cursor** ngay từ đầu. Những công cụ này không chỉ giúp bạn viết code nhanh hơn mà còn là một ví dụ thực tế tuyệt vời về cách một AI Agent (Coding Agent) hoạt động.
