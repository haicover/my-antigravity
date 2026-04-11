# Phase 2: AI Agents 101 (Nhập môn AI Agents)

## Tại sao giai đoạn này quan trọng?
Để xây dựng một Agent thực thụ, bạn phải chuyển tư duy từ "Chatbot phản hồi" sang "Hệ thống tự chủ". Giai đoạn này giúp bạn hiểu cấu trúc lõi của một Agent và cách nó đưa ra quyết định thông qua vòng lặp suy luận.

---

## 🏗️ Agent Loop (Vòng lặp Agent)
Một Agent hoạt động theo 4 bước lặp lại cho đến khi đạt được mục tiêu:
1. **Perception (Tiếp nhận)**: Nhận yêu cầu từ người dùng và phân tích ngữ cảnh.
2. **Reasoning & Planning (Suy luận & Lập kế hoạch)**: Chia nhỏ yêu cầu thành các bước nhỏ, quyết định hành động tiếp theo.
3. **Acting (Hành động)**: Gọi các công cụ (Tools) hoặc thực thi code với tham số cụ thể.
4. **Observation (Quan sát)**: Nhận kết quả từ Tool, phân tích xem đã đạt mục tiêu chưa. Nếu chưa -> Lặp lại bước 2.

## 🛠️ Pseudocode cho Agent Loop
```python
while not task_completed:
    # 1. Suy luận
    thought, action = llm.think(task, history, tools)
    
    # 2. Kiểm tra nếu đã kết thúc
    if action == "FINAL_ANSWER":
        return thought
    
    # 3. Hành động
    observation = tools.execute(action.name, action.args)
    
    # 4. Ghi nhớ và lặp lại
    history.append(thought, action, observation)
```

## 🧬 Phân biệt sự khác nhau
- **Chatbot**: Phản hồi dựa trên prompt. Không thể hành động bên ngoài cửa sổ chat.
- **Workflow/Pipeline**: Một chuỗi các bước được lập trình sẵn. Cứng nhắc, không linh hoạt.
- **AI Agent**: Có khả năng tự chọn công cụ, tự sửa lỗi và điều chỉnh kế hoạch dựa trên kết quả thực tế.

---

## 📊 Các Use Cases thực tế
- **Cá nhân hóa**: Lên lịch hẹn, quản lý email, tóm tắt tin tức hằng ngày.
- **Kỹ thuật**: Coding Agent tự động viết tests, sửa bug, giải quyết issues.
- **Dữ liệu**: Tự động truy vấn SQL, vẽ biểu đồ và phân tích xu hướng kinh doanh.
- **Marketing**: Nghiên cứu đối thủ, viết content và đăng bài lên mạng xã hội.

---

## 📋 Checklist: Hiểu về Agent
- [ ] Sự khác biệt giữa mô hình ReAct (Reason + Act) và mô hình chỉ có suy luận.
- [ ] Khái niệm "Tool Use" (hoặc Function Calling) là gì?
- [ ] Tại sao vòng lặp Agent lại cần có "điểm dừng" (Stop criteria) để tránh lặp vô hạn.

---

## 💡 Pro Tip
Hãy bắt đầu với một Agent đơn giản có 1-2 công cụ (ví dụ: Google Search và Máy tính) trước khi xây dựng các hệ thống đa nhân (Multi-agent) phức tạp. Càng ít công cụ, Agent càng dễ kiểm soát và ít gặp lỗi logic.
