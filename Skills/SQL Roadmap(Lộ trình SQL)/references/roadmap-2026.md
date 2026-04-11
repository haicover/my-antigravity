# Elite SQL Roadmap 2026

Bắt đầu từ số 0, trở thành một Data Engineering Specialist với lộ trình tinh gọn và tập trung nhất.

## Phase 1: Relational & Procedural Foundations (Tuần 1-2)
*Mục tiêu: Viết được bất kỳ câu truy vấn CRUD nào mà không cần suy nghĩ.*

- **Data Types**: Phân biệt `INT`, `UUID`, `VARCHAR`, `TEXT`, `TIMEZONES`.
- **Primary vs Foreign Keys**: Hiểu về tính định danh và mối quan hệ.
- **Filtering & Aggregate**: `WHERE`, `GROUP BY`, `HAVING`.
- **Exercise**: Thiết kế và triển khai Database cho một Blog đơn giản.

## Phase 2: Structural Integrity & Normalization (Tuần 3-4)
*Mục tiêu: Thiết kế được Database cho hệ thống Enterprise mà không bị dư thừa dữ liệu.*

- **Normal Forms**: 1NF, 2NF, 3NF.
- **Constraints Architecture**: `UNIQUE`, `CHECK`, `DEFAULT`, `CASCADE`.
- **Views & Stored Procedures**: Đóng gói logic nghiệp vụ vào Database.
- **Exercise**: Refactor một Flat Excel file thành Database 3NF.

## Phase 3: Advanced Analytics & Modern SQL (Tuần 5-6)
*Mục tiêu: Trở thành "phù thủy" dữ liệu, xử lý được các report cực khó.*

- **Window Functions**: `RANK`, `LEAD`, `LAG`, `PARTITION BY`.
- **CTEs (Recursive)**: Xử lý dữ liệu dạng cây (Tree Data).
- **Semi-structured Data**: Làm chủ JSON / JSONB trong PostgreSQL.
- **Exercise**: Viết Report tính toán tỉ lệ tăng trưởng doanh thu theo tháng (MoM Growth).

## Phase 4: Extreme Performance Tuning (Tuần 7-8)
*Mục tiêu: Query hàng triệu bản ghi trong tích tắc.*

- **Indexing Mastery**: Tối ưu Index cho từng loại Query (Read-heavy vs Write-heavy).
- **Execution Plans**: Đọc và hiểu `EXPLAIN ANALYZE`.
- **Partitioning**: Chia nhỏ bảng dữ liệu lớn (Declarative Partitioning).
- **Exercise**: Tối ưu hóa một câu query chậm (Slow Query) thông qua Indexing.

## Phase 5: Reliability & Distributed Data (Tuần 9+)
*Mục tiêu: Đảm bảo dữ liệu an toàn và nhất quán ở quy mô lớn.*

- **ACID & Transactions**: Lock mechanisms (Pessimistic vs Optimistic).
- **Replication & High Availability**: Master-Slave, WAL Shipping.
- **Database Security**: Row-Level Security (RLS) & Encryption.
- **Exercise**: Triển khai Postgres RLS cho hệ thống Multi-tenant.

---
*Return to [SKILL.md](file:///e:/Google%20Antigravity/Skills/SQL%20Roadmap%28L%E1%BB%99%20tr%C3%ACnh%20SQL%29/SKILL.md)*
