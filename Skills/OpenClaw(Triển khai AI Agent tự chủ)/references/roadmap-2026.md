# OpenClaw Roadmap 2026: Elite Mastery Path

Tài liệu này là lộ trình chi tiết để triển khai và làm chủ **OpenClaw** — framework AI Agent mã nguồn mở, self-hosted. Từ cài đặt đến production security hardening.

> **Nguồn gốc:** Dựa trên [roadmap.sh — OpenClaw Roadmap](https://roadmap.sh/openclaw) phiên bản 2026.
> **Lịch sử tên gọi:** Clawdbot (Nov 2025) → Moltbot (Jan 2026) → **OpenClaw** (chính thức, Feb 2026+).

---

## 🐾 Phase 1 — Introduction
**Mục tiêu**: Hiểu OpenClaw là gì, so sánh với Claude Code, và kiến trúc tổng quan.

### OpenClaw vs Claude Code

| Tiêu chí | OpenClaw | Claude Code |
|----------|----------|-------------|
| **Hosting** | Self-hosted (local/VPS/dedicated) | Cloud (Anthropic servers) |
| **Availability** | 24/7 always-on | On-demand per session |
| **Channels** | Telegram, WhatsApp, iMessage, Slack, Discord, Signal | Terminal, VS Code, JetBrains |
| **Data** | Hoàn toàn private, lưu local (Markdown/YAML) | Processed qua Anthropic API |
| **Models** | Multi-provider (Anthropic, OpenAI, Gemini, Ollama) | Anthropic only (Opus/Sonnet/Haiku) |
| **Cost** | Free (self-hosted) + API costs | Subscription ($20-$100/mo) hoặc API |
| **Setup** | Phức tạp hơn (Docker, gateway config) | Đơn giản (`npm install -g`) |
| **Use case** | Personal AI assistant 24/7, multi-channel | Developer coding agent, IDE integration |

### Use Cases
- 🤖 **Personal AI Assistant** — Trả lời tin nhắn qua WhatsApp/Telegram 24/7
- 📝 **Task Automation** — Quản lý calendar, email, file qua chat
- 🏢 **Team Agent** — Slack bot thông minh cho team
- 🔒 **Data Privacy** — AI agent không gửi data đến cloud bên thứ 3
- 🏠 **Smart Home** — Kết nối IoT qua messaging channels
- 📊 **Monitoring** — Heartbeats kiểm tra hệ thống định kỳ

### How OpenClaw Works
```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ Channels │────▶│   Gateway    │────▶│    Agent     │
│(Telegram,│◀────│(Router/Auth) │◀────│(LLM + Tools) │
│ WhatsApp,│     └──────────────┘     └──────┬───────┘
│  Slack)  │                                 │
└──────────┘                          ┌──────┴───────┐
                                      │   Memory     │
                                      │(MEMORY.md,   │
                                      │ daily logs)  │
                                      └──────────────┘
```

### Understand the Differences

| Component | Vai trò | Tương đương Claude Code |
|-----------|---------|------------------------|
| **Gateway** | Router điều hướng messages, authentication | Terminal session |
| **Agents** | LLM brain xử lý logic, ReAct loop | Claude model |
| **Agent Loop** | Reason → Act → Observe → Iterate | Agentic Loop |
| **Context Window** | Token limit của model đang dùng | Context window |
| **Channels** | Telegram, WhatsApp, Slack, Discord, iMessage, Signal | CLI, VS Code |
| **Skills** | Reusable capabilities (giống Skills) | Skills/SKILL.md |
| **Memory System** | MEMORY.md, daily logs, semantic search | `/memory`, `/compact` |
| **Proactive Core** | Heartbeats, cron jobs — agent tự khởi tạo | Không có (reactive only) |

---

## 🏗️ Phase 2 — Choose Your Installation Method
**Mục tiêu**: Chọn hạ tầng phù hợp cho deployment.

### 💻 Local Machine

| ✅ Why | ❌ Why Not |
|--------|-----------|
| Dễ setup, debug nhanh | Không online 24/7 |
| Free (không cần VPS) | Tốn tài nguyên máy cá nhân |
| Tốt cho learning/testing | Rủi ro bảo mật cao (trên PC chính) |

**Security:** Bind gateway về `localhost` only. Dùng firewall. Không expose ports.

### ☁️ VPS/Cloud

| ✅ Why | ❌ Why Not |
|--------|-----------|
| Online 24/7 | Tốn phí hàng tháng ($5-20/mo) |
| Cô lập khỏi PC chính | Cần kiến thức Linux/SSH |
| Dễ scale | Latency phụ thuộc vị trí server |

**Providers gợi ý:** DigitalOcean, Hetzner, Linode, Vultr, AWS Lightsail.
**Security:** SSH key only (no password). UFW firewall. Fail2ban. Non-root user.

### 🖥️ Dedicated Hardware

| ✅ Why | ❌ Why Not |
|--------|-----------|
| One-time cost, no monthly fees | Cần duy trì phần cứng |
| Full control, cực kỳ private | Phụ thuộc internet nhà |
| Fun DIY project | Không dễ scale |

**Hardware phổ biến:**
- **Raspberry Pi 5** — Compact, tiết kiệm điện (~$80-100). Đủ cho Haiku/small models qua API.
- **Mac Mini M4** — Mạnh mẽ, chạy được local models qua Ollama. Ideal cho power users (~$599+).

---

## ⚙️ Phase 3 — Installation & Onboarding
**Mục tiêu**: Cài đặt OpenClaw, kết nối model provider, thêm channel đầu tiên.

### 🐳 Docker Install (Recommended)
```bash
# Clone repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Docker Compose
docker compose up -d

# Hoặc dùng script cài nhanh
curl -fsSL https://get.openclaw.dev | bash
```

### 🔑 Auth & Model Providers
Kết nối ít nhất 1 LLM provider:

| Provider | Command | Ghi chú |
|----------|---------|---------|
| **Anthropic** | `openclaw models auth add --anthropic` | Claude Sonnet/Opus/Haiku |
| **OpenAI** | `openclaw models auth add --openai` | GPT-4o, o1, o3 |
| **Gemini** | `openclaw models auth add --gemini` | Gemini Pro/Ultra |
| **Ollama** | `openclaw models auth add --ollama` | Local models (Llama, Mistral) |

```bash
# Thêm API key
openclaw models auth setup-token --provider anthropic --key sk-ant-xxx

# Kiểm tra
openclaw models list
openclaw models status
```

### 📱 Adding First Channel

| Channel | Command | Ghi chú |
|---------|---------|---------|
| **Telegram** | `openclaw channels add --telegram` | Cần BotFather token |
| **WhatsApp** | `openclaw channels add --whatsapp` | QR code pairing |
| **iMessage** | `openclaw channels add --imessage` | macOS only |
| **Slack** | `openclaw channels add --slack` | Workspace OAuth |
| **Discord** | `openclaw channels add --discord` | Bot token |
| **Signal** | `openclaw channels add --signal` | Phone number registration |

```bash
# Ví dụ: Thêm Telegram
openclaw channels add --telegram
# → Nhập BotFather token
# → Verify kết nối

# Kiểm tra trạng thái
openclaw channels status --probe
```

---

## 🧠 Phase 4 — Workspace & Gateway Configuration
**Mục tiêu**: Cấu hình brain, personality, và routing cho agent.

### 📄 Workspace Files

| File | Vai trò | Tương đương |
|------|---------|-------------|
| **AGENTS.md** | Định nghĩa các agent và capabilities | Phần nào giống CLAUDE.md |
| **SOUL.md** | Personality, tone, giới hạn hành vi | System prompt |
| **USER.md** | Thông tin về user (preferences, context) | User profile |
| **MEMORY.md** | Long-term memory cho agent | `/memory` |
| **memory/YYYY-MM-DD.md** | Daily conversation logs | Session history |
| **Other workspace files** | Custom data, references | Project files |

**Ví dụ SOUL.md:**
```markdown
# Soul
You are my personal AI assistant named Claw.
- Be concise and professional
- Always respond in Vietnamese unless asked otherwise
- Never share personal information with third parties
- When unsure, ask for clarification
```

**Ví dụ AGENTS.md:**
```markdown
# Agents
## Default Agent
- Model: claude-sonnet
- Tools: filesystem, shell, web-search
- Permissions: read-write (workspace only)

## Research Agent
- Model: claude-opus
- Tools: web-search, web-browse
- Permissions: read-only
```

### ⚙️ Gateway Settings
```bash
# Cấu hình gateway
openclaw gateway         # Xem status
openclaw gateway start   # Khởi động
openclaw gateway stop    # Dừng
openclaw gateway restart # Khởi động lại
```

- **Port mặc định:** 18789 (API) và 18793 (WebSocket)
- **Bind address:** Luôn dùng `localhost` (127.0.0.1), KHÔNG PHẢI `0.0.0.0`
- **Auth token:** Đặt strong token trước khi expose bất kỳ service nào

### 🔧 Adding Daemon
- Daemon giữ OpenClaw chạy nền liên tục
- Auto-restart nếu crash
- Configure qua systemd (Linux) hoặc launchd (macOS)

---

## 🎬 Phase 5 — OpenClaw in Action
**Mục tiêu**: Sử dụng hiệu quả và tự động hóa tasks.

### ✅ Usage Best Practices
1. **Start read-only** → mở rộng permissions dần dần
2. **Audit mọi skill trước khi cài** — community skills có thể chứa mã độc
3. **Giữ SOUL.md focused** — personality rõ ràng giúp agent nhất quán
4. **Monitor memory** — dùng `openclaw memory index --all` để cập nhật semantic index
5. **Backup thường xuyên** — `openclaw backup create`

### 🪝 Hooks

**Hook Structure:**
```yaml
hooks:
  - event: "message.received"
    match: "channel:telegram"
    action: "scripts/log-message.sh"
```

**Event Types:**
| Event | Khi nào |
|-------|---------|
| `message.received` | Khi nhận tin nhắn mới |
| `message.sent` | Khi agent gửi reply |
| `session.start` | Khi bắt đầu session mới |
| `session.end` | Khi kết thúc session |
| `tool.before` | Trước khi agent dùng tool |
| `tool.after` | Sau khi agent dùng tool |
| `error` | Khi xảy ra lỗi |

### 🌐 Webhooks
- HTTP endpoints nhận events từ external services
- Trigger agent actions từ GitHub, CI/CD, monitoring systems
- **Securing Webhooks:**
  - Validate signature/HMAC trên mỗi request
  - Whitelist IP sources
  - Rate limiting
  - HTTPS only

### 💓 Heartbeats
Tính năng **Proactive Core** — agent tự khởi tạo hành động mà KHÔNG cần user trigger.

```markdown
# HEARTBEAT.md
## Morning Briefing
- Interval: daily 7:00 AM
- Action: Summarize unread emails, calendar events, weather

## System Check
- Interval: every 6 hours
- Action: Check server status, disk space, running services
```

| Config | Mô tả |
|--------|--------|
| **Interval** | Tần suất chạy (cron syntax hoặc natural language) |
| **Active Hours** | Giờ hoạt động (vd: 7AM-11PM) — tránh spam lúc ngủ |
| **HEARTBEAT.md** | File định nghĩa tất cả heartbeats |

### ⏰ Cron Jobs
```bash
# Liệt kê cron jobs
openclaw cron list

# Thêm cron job mới
openclaw cron add --name "daily-backup" --schedule "0 2 * * *" --action "backup create"

# Quản lý
openclaw cron disable --name "daily-backup"
openclaw cron enable --name "daily-backup"
```

### 📂 Sessions
- Mỗi conversation tạo một session riêng
- Slash commands trong chat: `/new`, `/status`, `/stop`, `/reset`
- `/compact` — tóm tắt context | `/context` — xem context hiện tại
- `/usage` — xem token usage | `/think` — bật deep reasoning

---

## 🧩 Phase 6 — Skills & Plugins
**Mục tiêu**: Mở rộng khả năng của agent.

### 📝 Creating Skills
- Skills là các capability modules agent có thể gọi
- Tạo file SKILL definition trong workspace
- Include instructions, examples, và tool bindings
- **Security Risks:**
  - ⚠️ Skills có quyền truy cập tools (filesystem, shell)
  - ⚠️ Community skills CHƯA ĐƯỢC audit mặc định
  - ✅ Luôn review source code trước khi cài
  - ✅ Sandbox skills trong environment cô lập

### 🏪 Installing from ClawHub
```bash
# Browse ClawHub marketplace
openclaw skills search "calendar"

# Cài đặt skill
openclaw skills install @clawhub/calendar-manager

# Liệt kê skills đã cài
openclaw skills list
```

### 🔌 Plugins

**Installing Plugins:**
```bash
openclaw plugins install @openclaw/web-browser
openclaw plugins list
openclaw plugins status
```

**Creating Plugins:**
- Plugins là extensions mức hệ thống (sâu hơn Skills)
- Viết bằng TypeScript/Python
- Đăng ký tools, hooks, và middleware
- Publish lên ClawHub để cộng đồng sử dụng

---

## 🔌 Phase 7 — MCP & Multi-Agents
**Mục tiêu**: Kết nối external tools qua MCP và điều phối nhiều agents.

### 🔗 MCP (Model Context Protocol)
- Kết nối OpenClaw với databases, APIs, cloud services
- Configure qua `/mcp` hoặc workspace config

**Security Risks:**
- MCP servers có thể truy cập data nhạy cảm
- Chỉ kết nối trusted servers
- Review permissions trước khi enable
- Monitor MCP traffic logs

### 👥 Multi-Agents

**Routing Rules:**
```markdown
# AGENTS.md — Multi-Agent Setup
## Router
- Rule: messages about "code" → Developer Agent
- Rule: messages about "schedule" → Calendar Agent  
- Rule: messages about "research" → Research Agent
- Default: Default Agent

## Developer Agent
- Model: claude-sonnet
- Skills: code-review, git-ops, testing

## Calendar Agent
- Model: haiku
- Skills: google-calendar, reminder

## Research Agent
- Model: claude-opus
- Skills: web-search, summarizer
```

- Routing dựa trên content, channel, hoặc explicit `/model` command
- Mỗi agent có model, skills, và permissions riêng
- Load balancing giữa các agents

---

## 🛡️ Phase 8 — Security & Production
**Mục tiêu**: Hardening hoàn chỉnh cho production deployment.

### Security Checklist ✅

| # | Action | Priority |
|---|--------|----------|
| 1 | Deploy trên VPS/VM/dedicated cô lập, KHÔNG trên PC cá nhân | 🔴 Critical |
| 2 | Chạy OpenClaw dưới non-root user | 🔴 Critical |
| 3 | Bind gateway về `localhost`, không phải `0.0.0.0`. Secure ports 18789 và 18793 | 🔴 Critical |
| 4 | Set strong gateway auth token trước khi expose service | 🔴 Critical |
| 5 | Enable device pairing và duy trì minimal sender allowlist | 🟡 High |
| 6 | Không hardcode API keys — dùng environment variables | 🟡 High |
| 7 | Start ở read-only mode, mở rộng permissions có chủ đích | 🟡 High |
| 8 | Không trust external content (emails, web pages) — phòng prompt injection | 🟡 High |
| 9 | Chạy `openclaw security audit --deep` sau mọi config change | 🟠 Medium |
| 10 | Update OpenClaw thường xuyên — security fixes trong patch releases | 🟠 Medium |
| 11 | Rotate credentials ngay lập tức nếu nghi ngờ bị breach | 🟠 Medium |

### Production Deploy Checklist
```bash
# 1. Health check
openclaw doctor --deep

# 2. Security audit
openclaw security audit --deep

# 3. Backup
openclaw backup create

# 4. Gateway security
# Đảm bảo gateway chỉ bind localhost
# Dùng SSH tunnel hoặc VPN để remote access

# 5. Monitoring
# Set up heartbeat cho system monitoring
# Enable error notifications qua preferred channel
```

---

## 🏁 Kết luận: Elite Mindset

OpenClaw là sức mạnh thực sự của AI Agent — **tự chủ, luôn hoạt động, và hoàn toàn dưới quyền kiểm soát của bạn**. Nhưng sức mạnh đi kèm trách nhiệm:

1. **Security First** — Mọi thứ phải được audit trước khi deploy
2. **Proactive, Not Reactive** — Heartbeats biến agent từ "chatbot" thành "trợ lý thực sự"
3. **Channel Strategy** — Chọn channels phù hợp, không cần kết nối tất cả
4. **Memory is Power** — MEMORY.md + daily logs = agent ngày càng thông minh hơn

> "The best AI agent is one that works for you even when you're not looking."

---

## 🔗 Roadmaps liên quan
- ⚡ [Claude Code](file:///e:/Google%20Antigravity/Skills/Claude%20Code%28Chuy%C3%AAn%20gia%20Claude%20Code%29/SKILL.md) — Cloud-based coding agent
- 🎨 [Vibe Coding](file:///e:/Google%20Antigravity/Skills/Vibe%20Coding%28L%E1%BA%ADp%20tr%C3%ACnh%20phong%20c%C3%A1ch%20Vibe%29/SKILL.md) — AI-first development
- ⚡ [AI Engineer](file:///e:/Google%20Antigravity/Skills/AI%20Engineer%28K%E1%BB%B9%20s%C6%B0%20AI%29/SKILL.md) — Full-stack AI engineering

---
_Cập nhật lần cuối: Tháng 4, 2026 — Bởi Đội ngũ Antigravity (Elite Engineering Division)_
