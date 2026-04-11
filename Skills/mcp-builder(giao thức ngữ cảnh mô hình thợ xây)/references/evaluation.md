# MCP Evaluation Guide 2.0 (Elite 2026)

Tài liệu này hướng dẫn xây dựng bộ đánh giá (Evaluation) chuẩn Elite 2026 để kiểm tra khả năng suy luận và sử dụng công cụ của MCP Server.

## 📖 Mục lục

1. [Tổng quan về Evaluation 2.0](#1-tổng-quan-về-evaluation-20)
2. [Chiến lược Agentic Multi-Tool Reasoning](#2-chiến-lược-agentic-multi-tool-reasoning)
3. [Tiêu chuẩn câu hỏi & đáp án](#3-tiêu-chuẩn-câu-hỏi--đáp-án)
4. [Định dạng XML 2026](#4-định-dạng-xml-2026)
5. [Quy trình xây dựng (5 bước)](#5-quy-trình-xây-dựng-5-bước)
6. [Chạy Evaluation & Tracing](#6-chạy-evaluation--tracing)

---

## 1. Tổng quan về Evaluation 2.0

Trong năm 2026, Evaluation không chỉ kiểm tra "đúng/sai" mà còn kiểm tra **quỹ đạo suy luận (trajectory)**. 
- **Mục tiêu**: Đảm bảo Agent có thể vượt qua các "context traps" và sử dụng tối ưu context window khi gọi nhiều tools liên tục.
- **Phạm vi**: 10 câu hỏi phức tạp, hoàn toàn Read-only và Idempotent.

---

## 2. Chiến lược Agentic Multi-Tool Reasoning

Một bộ Evaluation chất lượng phải ép Agent thực hiện ít nhất 3-5 tool calls để tìm ra đáp án.

### Các loại bẫy suy luận (Reasoning Traps) nên đưa vào:
- **Pagination Depth**: Đáp án nằm ở trang thứ 3 hoặc 4 của kết quả trả về.
- **Cross-Service Join**: Cần lấy ID từ server Slack để tra cứu dữ liệu trong server GitHub.
- **Ambiguity Resolution**: Câu hỏi có chút mơ hồ, yêu cầu Agent phải dùng tool `search` trước khi `get_details`.

---

## 3. Tiêu chuẩn câu hỏi & đáp án

| Tiêu chuẩn | Yêu cầu Elite 2026 |
| :--- | :--- |
| **Tính ổn định** | Dùng dữ liệu lịch sử (Frozen data). Không dùng "hôm nay", "bây giờ". |
| **Độ phủ Tool** | Cần ít nhất 60% số tools của server được gọi trong toàn bộ 10 câu hỏi. |
| **Định dạng đáp án** | Phải là chuỗi ký tự đơn giản (String/Number/Boolean) để so sánh tự động chính xác. |
| **Tính bảo mật** | Tuyệt đối không có câu hỏi yêu cầu sửa đổi dữ liệu (Write operations). |

---

## 4. Định dạng XML 2026

Sử dụng schema chuẩn để tích hợp với hệ thống auto-evaluator.

```xml
<evaluation_suite version="2026-04">
  <metadata>
    <server_name>github-mcp-server</server_name>
    <difficulty>Advanced</difficulty>
  </metadata>

  <test_case id="1">
    <question>
      Identify the contributor who closed the most 'high-priority' issues 
      in the 'core-engine' repository between January and March 2024. 
      Provide only their GitHub username.
    </question>
    <expected_trajectory>
      1. github_list_repos()
      2. github_list_issues(state='closed', labels=['high-priority'])
      3. Logic check on closed_at timestamps
      4. Aggregation by assignee
    </expected_trajectory>
    <answer>octocat_dev</answer>
  </test_case>

  <!-- Repeat for 10 test cases -->
</evaluation_suite>
```

---

## 5. Quy trình xây dựng (5 bước)

1. **Discovery**: Dùng Inspector để liệt kê tất cả khả năng của tools.
2. **Data Mining**: Gọi thử các tool read-only để tìm các điểm dữ liệu "thú vị" và ổn định.
3. **Drafting**: Viết câu hỏi thô theo dạng "multi-hop".
4. **Validation**: Tự giải câu hỏi bằng Agent (Claude/Gemini) để xem nó có bị "lạc đường" không.
5. **XML Encoding**: Đóng gói vào định dạng XML 2026.

---

## 6. Chạy Evaluation & Tracing

Sử dụng công cụ `mcp-eval` (version 2026+) để báo cáo chi tiết.

```bash
mcp-eval run \
  --server-config ./config.json \
  --suite ./evaluation.xml \
  --model claude-3-7-sonnet \
  --detail-report ./report-2026.md
```

### Phân tích Report:
- **Pass Rate**: Mục tiêu > 90%.
- **Token Efficiency**: Đo lường lượng context lãng phí khi Agent gọi sai tool.
- **Trajectory Accuracy**: Agent có đi đúng các bước "expected_trajectory" không?

---

> [!TIP]
> Luôn cập nhật bộ Evaluation khi bạn thêm tool mới hoặc thay đổi cấu trúc dữ liệu trả về để tránh "Evaluation Decay".
