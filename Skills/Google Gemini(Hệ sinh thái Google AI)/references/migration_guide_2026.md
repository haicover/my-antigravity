# 🔄 Migration Guide: Legacy to Unified SDK (June 2026 Cutoff)

Google đã hợp nhất luồng API của AI Studio và Vertex AI vào một bộ SDK duy nhất: `google-genai`. Toàn bộ mã nguồn cũ sử dụng `google-generativeai` PHẢI được nâng cấp trước tháng 06/2026 để tránh gián đoạn dịch vụ.

---

## 1. Cài đặt (Installation)

Gỡ bỏ (nếu cần) và cài đặt bộ SDK chuẩn mới:

```powershell
pip uninstall google-generativeai
pip install google-genai
```

---

## 2. So sánh Mã Nguồn (Code Comparison)

### ❌ Legacy (Trước 2026) -> `google-generativeai`
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
```

### ✅ Unified (Chuẩn 2026) -> `google-genai`
```python
from google import genai
import os

client = genai.Client(api_key=os.environ["API_KEY"])
response = client.models.generate_content(
    model='gemini-2.0-flash', # Or gemini-3.1-flash
    contents='Hello'
)
print(response.text)
```

---

## 3. Các thay đổi quan trọng (Key Changes)

| Tính năng | Legacy SDK | Unified SDK (2026) |
| :--- | :--- | :--- |
| **Import** | `google.generativeai` | `from google import genai` |
| **Khởi tạo** | `genai.configure()` | `genai.Client(api_key=...)` |
| **Model ID** | `gemini-1.5-pro` | `gemini-2.0-flash`, `gemini-3.1-pro` |
| **System Instruction** | `system_instruction="..."` | Cấu hình trong `config` của Client |
| **Function Calling** | `tools=[...]` | Thống nhất cấu hình `tools` cho Vertex AI & AI Studio |

---

## 4. Troubleshooting (Xử lý lỗi phổ biến)

### Lỗi 404 (Model not found)
Google hiện tại đã chuyển các model cũ sang trạng thái **Deprecated**. Luôn sử dụng script kiểm tra model trước khi chạy production:

```python
from google import genai
client = genai.Client(api_key="YOUR_KEY")

for model in client.models.list():
    print(f"Model khả dụng: {model.name}")
```

### Lỗi 429 (Resource Exhausted)
Nếu gặp lỗi này thường xuyên trên `gemini-2.0-flash`, hãy cân nhắc hạ cấp xuống `gemini-2.0-flash-lite` hoặc bật **Pay-as-you-go** trong AI Studio để có quota cao hơn.

---

## 5. Danh sách Model đề xuất (Q2-2026)

1. **`gemini-3.1-pro`**: Mô hình mạnh nhất cho Reasoning, Thinking (Logic cực khó).
2. **`gemini-2.0-flash`**: Mô hình cân bằng nhất, tốc độ cao, hỗ trợ Multimodal Live.
3. **`gemini-2.0-flash-lite`**: Tiết kiệm nhất cho các tác vụ đơn giản như phân loại text.

---

> [!CAUTION]
> Đảm bảo biến môi trường `GEMINI_API_KEY` của bạn luôn được bảo mật trong file `.env` và không commit lên GitHub công khai.
