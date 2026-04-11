# Project Nova: The Autonomous Platform Node

**Trạng thái**: 🟢 Elite Blueprint (Phase 8 Spec)
**Mục tiêu**: Xây dựng một hệ thống "Brain" nằm trên đỉnh của Kubernetes, chuyên theo dõi sức khỏe hệ thống qua OTel và sử dụng AI Agents để tự động hóa việc sửa lỗi (Auto-remediation).

---

## 🏗️ Architecture Design

Project Nova hoạt động theo mô hình **Predictive-Action Loop**:
1. **Perception**: Thu thập logs, metrics, và traces qua OpenTelemetry.
2. **Analysis**: LLM-based Analysis (sử dụng GPT-4o hoặc Claude 3.5) phân tích sự sai khác giữa thực tế và SLOs.
3. **Execution**: AI Agent thực thi các lệnh Terminal/Kubectl để điều chỉnh hạ tầng.

### Core Stack
- **Control Plane**: Kubernetes.
- **Monitoring**: OpenTelemetry + Prometheus.
- **Agent Framework**: LangGraph / AutoGPT (với quyền thực thi CLI).
- **Communication**: Slack/Discord webhook để thông báo quá trình tự sửa lỗi.

---

## 🛠️ Implementation Phases

### Phase 1: OTel & SLO Integration
- Cấu hình OTel Collector để Export dữ liệu về một Central Hub.
- Định nghĩa các "Critical SLOs" (ví dụ: Latency < 200ms, Error Rate < 0.1%).

### Phase 2: Intelligence Layer
- Xây dựng một Service lắng nghe các Alert từ Prometheus.
- Khi nhận Alert, Service này gửi context (logs 5 phút gần nhất + metrics) cho AI Agent.

### Phase 3: Autonomous Action (The "Nova" Agent)
- Cấp quyền `ClusterRole` giới hạn cho Agent.
- Agent phân tích và đưa ra giải pháp:
    - Nếu CPU quá cao -> Scale Up HPA.
    - Nếu dính lỗi OOM -> Tăng Memory limit.
    - Nếu dính lỗi code -> Rollback về phiên bản ổn định nhất qua ArgoCD.

---

## 🛡️ Safety & Guardrails
- **Human-in-the-loop**: Mọi hành động tàn phá (xóa Namespace, xóa Storage) phải qua xác nhận thủ công.
- **Dry-run Mode**: Chế độ thử nghiệm, Agent chỉ đưa ra khuyến nghị mà không thực thi.

---

## 📈 Tầm nhìn 2026
Project Nova không chỉ là một tool, nó là một **Digital SRE** có khả năng học hỏi từ các sự cố cũ để ngăn chặn sự cố tương lai.

---
_Tài liệu thuộc hệ sinh thái Elite Ops 2026._
