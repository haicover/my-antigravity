# Phase 11: Security & Ethics (Bảo mật & Đạo đức)

## Tại sao giai đoạn này quan trọng?
AI Agents có khả năng thực thi hành động, điều này mang lại rủi ro lớn hơn nhiều so với chatbot thông thường. Nếu không được bảo mật, Agent có thể bị tấn công (Prompt Injection) để đánh cắp dữ liệu hoặc thực thi các lệnh phá hoại. Ngoài ra, việc đảm bảo Agent hoạt động một cách đạo đức và công bằng là trách nhiệm của nhà phát triển.

---

## 🏗️ Bảo mật cho Agent
1. **Prompt Injection**: Kỹ thuật tấn công chèn lệnh để thay đổi mục tiêu của Agent. Giải quyết bằng cách phân tách rõ dữ liệu User và System Prompt.
2. **Tool Sandboxing**: Chỉ cấp quyền tối thiểu (Least Privilege) cho Tools. Không bao giờ để Agent có quyền xóa database hoặc truy cập file hệ thống nhạy cảm.
3. **Data Privacy**: Phát hiện và loại bỏ thông tin định danh cá nhân (PII) trước khi gửi đến các mô hình bên thứ ba.
4. **Sandboxed Environment**: Thực thi mã code của Agent trong các container (Docker) bị cô lập khỏi internet và hệ thống chủ.

## 🛠️ Code Example: Kiểm soát quyền hạn (Python)
```python
def delete_file_tool(filename):
    """Công cụ xóa file với kiểm tra bảo mật."""
    ALLOWED_DIRECTORY = "/tmp/agent_files/"
    
    # Kiểm tra đường dẫn an toàn (tránh Path Traversal)
    full_path = os.path.abspath(os.path.join(ALLOWED_DIRECTORY, filename))
    if not full_path.startswith(ALLOWED_DIRECTORY):
        raise SecurityError("Truy cập thư mục bị cấm!")
    
    os.remove(full_path)
```

## 🧬 Đạo đức trong AI Agents
- **Bias & Fairness**: Đảm bảo Agent không đưa ra các quyết định thiên vị dựa trên chủng tộc, giới tính hoặc tôn giáo.
- **Toxicity Guardrails**: Lọc các phản hồi có nội dung độc hại hoặc không phù hợp trước khi gửi cho người dùng.
- **Red Team Testing**: Tự mình tấn công Agent của mình để tìm kiếm các lỗ hổng tiềm ẩn.

---

## 📋 Checklist: Vận hành an toàn
- [ ] Agent của bạn có quyền truy cập vào các dữ liệu nhạy cảm không cần thiết không?
- [ ] Bạn đã thiết lập các bộ lọc (Guardrails) để ngăn chặn mã độc thực thi?
- [ ] Bạn có cơ chế xác nhận của con người (Human Approval) cho các hành động quan trọng (ví dụ: Chuyển tiền)?
- [ ] Bạn đã thông báo cho người dùng về việc dữ liệu của họ sẽ được xử lý như thế nào?

---

## 💡 Pro Tip
Hãy sử dụng kiến trúc **Human-in-the-loop (HITL)** cho bất kỳ hành động nào có tính chất hủy hoại hoặc tốn kém. Một nút "Chấp nhận" từ con người là rào chắn bảo mật mạnh mẽ nhất mà bạn có thể xây dựng.
