# Claude Code Roadmap 2026: Elite Mastery Path

Tài liệu này là lộ trình chi tiết để trở thành một **Claude Code Expert** — từ người mới bắt đầu đến kiến trúc sư hệ thống agentic hoàn chỉnh.

> **Nguồn gốc:** Dựa trên [roadmap.sh — Claude Code Roadmap](https://roadmap.sh/claude-code) phiên bản 2026.

---

## ⚡ Phase 1 — Introduction (Month 1)
**Mục tiêu**: Hiểu paradigm Vibe Coding và thiết lập môi trường Claude Code.

### 🎯 What is Vibe Coding?
- Phương pháp phát triển nơi bạn mô tả ý đồ bằng ngôn ngữ tự nhiên, AI agent viết, debug và refactor code tự chủ
- Do Andrej Karpathy đặt tên — "you fully give in to the vibes, embrace exponentials, and forget that the code even exists"
- Chuyển vai trò developer từ viết code sang **điều phối kết quả (directing outcomes)**
- Yêu cầu kỹ năng: communication, architecture thinking, prompt engineering

### 🤖 What is a Coding Agent?
- Hệ thống AI đọc file, viết code, chạy terminal commands, browse web, và lặp lại cho đến khi giải quyết vấn đề
- Vượt xa autocomplete — suy luận, lập kế hoạch, thực thi multi-step tasks
- Claude Code là flagship coding agent của Anthropic, chạy trực tiếp trong terminal
- Có mặt trên: **CLI**, **Desktop App**, **VS Code**, **JetBrains**, **Mobile**

### 🔄 What is the Agentic Loop?
```
Observe → Think → Act → Iterate
   ↑                        |
   └────────────────────────┘
```
1. **Observe**: Đọc codebase, files, errors, context
2. **Think**: Suy luận về hành động cần thực hiện (chain-of-thought)
3. **Act**: Thực thi tools — edit files, run commands, search web
4. **Iterate**: Kiểm tra kết quả, sửa lỗi, tinh chỉnh đến khi hoàn thành

### ⚙️ Setting up Claude
| Phương thức | Chi tiết | Phù hợp |
|-------------|----------|---------|
| **Subscription (Pro)** | $20/tháng | Cá nhân, sử dụng vừa |
| **Subscription (Max)** | $100/tháng, 5× usage | Cá nhân power user |
| **API Usage** | Pay-per-token, `ANTHROPIC_API_KEY` | Teams, CI/CD, automation |

```bash
# Cài đặt
npm install -g @anthropic-ai/claude-code

# Xác thực
claude  # Theo dõi flow đăng nhập
```

---

## 🧠 Phase 2 — Understand the Basics (Months 1-2)
**Mục tiêu**: Nắm vững các khái niệm cốt lõi phân biệt Claude Code với các công cụ khác.

### 📋 CLAUDE.md
- File markdown Claude **tự động đọc** khi bắt đầu session
- Chứa project conventions, architecture decisions, coding standards, commands
- Hoạt động như **persistent system prompt** cho codebase
- Đặt ở: repo root, subdirectories, hoặc `~/.claude/CLAUDE.md` (global)

### 🧩 Skills
- Bộ hướng dẫn tập trung (SKILL.md files) dạy Claude khả năng cụ thể
- Khác CLAUDE.md: skills được gọi **on-demand** thay vì luôn load
- Ví dụ: "Deploy to AWS", "Write Jest tests", "Migrate database schema"
- **Composable** — skills tham chiếu lẫn nhau cho workflows phức tạp

### 🧠 Context
- Claude có **context window** — mọi thứ trong conversation tiêu tốn tokens
- Files đọc, terminal output, search results đều tiêu thụ context
- **Quản lý context là kỹ năng #1** cho việc sử dụng Claude Code hiệu quả
- Dùng `/compact` để tóm tắt, `/clear` để reset

### 🔀 Modes
- **Normal mode** — Claude đọc, viết, và thực thi tự do
- **Plan mode** (`/plan`) — Claude chỉ lập kế hoạch, không thay đổi code cho đến khi approve
- Plan mode thiết yếu cho tasks phức tạp — review trước, thực thi sau

### 🏗️ Models, Tools & MCP

| Model | Đặc điểm | Use Case |
|-------|----------|----------|
| **Opus** | Deep reasoning, chậm nhất | Planning, bugs phức tạp, architecture |
| **Sonnet** | Balanced, nhanh & capable | Default cho hầu hết coding tasks |
| **Haiku** | Ultra-fast, lightweight | Quick questions, simple edits |

- **Tools**: Khả năng built-in — file editing, terminal, search, browser
- **MCP (Model Context Protocol)**: Standard kết nối external tools — databases, APIs, services
- **Plugins**: Extensions cộng đồng & chính thức (vd: Code Intelligence)

### 🪝 Hooks & Subagents
- **Hooks**: Event-driven scripts chạy trước/sau Claude actions
- **Subagents**: Spawn Claude instances cô lập cho parallel tasks
- Hooks: enforce guardrails (auto-lint sau mỗi file save)
- Subagents: scale (agent review code, agent khác viết tests)

---

## ⌨️ Phase 3 — Using Claude Code (Months 2-3)
**Mục tiêu**: Thành thạo keyboard shortcuts, commands, và workflows để maximize năng suất.

### ⌨️ Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel generation / interrupt Claude |
| `Ctrl+R` | Search command history (reverse search) |
| `Esc` | Cancel current input / dismiss |
| `Esc + Esc` | Force stop agentic loop immediately |
| `Shift+Tab` | Toggle multi-line / single-line input |

### 🚀 CLI Invocation Patterns
| Command | Description |
|---------|-------------|
| `claude` | Start interactive REPL session |
| `claude -r` | Resume most recent conversation |
| `claude "query"` | One-shot command (run & exit) |
| `claude -p "query"` | Print mode — output only |
| `claude -c <id>` | Resume specific conversation by ID |
| `claude --add-dir <path>` | Add additional directory context |

### 📎 Slash Commands

**Session Commands:**
```
/help      — Show help
/usage     — Display token/cost usage
/cost      — Detailed cost breakdown
/status    — Session status (model, tokens, permissions)
/exit      — End session
/export    — Export conversation (Markdown/JSON)
```

**Context & Memory:**
```
/clear     — Clear conversation history
/compact   — Summarize to reduce tokens
/context   — Show context sources & token counts
/init      — Create/update CLAUDE.md
/memory    — View/manage persistent memory
```

**Workflow:**
```
/plan      — Enter plan mode (plan only, no execution)
/rewind    — Revert to previous conversation point
```

**Configuration:**
```
/config      — View/modify configuration
/permissions — Manage tool permissions
/model       — Switch active AI model
/agents      — Configure subagents
/hooks       — Manage event hooks
/mcp         — Configure MCP server connections
/doctor      — Run diagnostics
```

### 🔤 Special Prefixes
| Prefix | Description |
|--------|-------------|
| `!` | Run shell command (vd: `!npm test`) |
| `\` | Escape — send literal text |
| `@` | Reference file/symbol (vd: `@src/utils.ts`) |

> **💡 Pro Tip:** Kết hợp `claude -r` với `/compact` cho dự án dài hạn. Resume session, rồi compact để giải phóng context mà vẫn giữ decisions và progress.

---

## 🔄 Phase 4 — Claude Workflow (Months 3-4)
**Mục tiêu**: Phát triển workflow hệ thống cho các loại task khác nhau.

### 🔐 Permission Modes
| Mode | Mô tả | Khi nào dùng |
|------|--------|-------------|
| **Ask** | Claude hỏi trước mỗi tool use | Codebase chưa quen, cần cẩn thận |
| **Auto-allow** | Tự động approve safe operations | Project tin cậy |
| **YOLO** | Chạy mọi thứ không hỏi | ⚠️ Dùng cực kỳ cẩn thận! |

Configure qua `/permissions` hoặc `.claude/settings.json`

### 📝 Plan Mode
1. Activate: `/plan` → Claude research và tạo implementation plan
2. Review plan, hỏi thêm, iterate approach
3. Approve → Claude thực thi plan
4. **Dùng cho:** Major refactors, new features, architectural changes
5. **Bỏ qua cho:** Quick bug fixes, formatting, one-liner tasks

### 📂 Session Management
- **Resume:** `claude -r` — tiếp tục từ chỗ dừng, full context
- **Rewind:** `/rewind` — rollback về điểm trước — undo mistakes
- **Specific:** `claude -c <id>` — resume session cũ theo ID
- Sessions được lưu local — resume sau nhiều ngày
- **Tip:** Bắt đầu session mới cho task khác biệt để giữ context sạch

### ✅ Usage Best Practices
1. **Be specific:** "Add error handling to login function in auth.ts" > "fix the login"
2. **Provide context:** Dùng `@` file references để chỉ Claude đến code liên quan
3. **Iterate small:** Chia task lớn thành subtask nhỏ tập trung
4. **Review diffs:** Luôn review changes trước khi accept
5. **Use git:** Commit trước khi yêu cầu thay đổi lớn — easy rollback
6. **TDD workflow:** Yêu cầu Claude viết tests trước, rồi implement

---

## 🧬 Phase 5 — Advanced Claude Code (Months 4-6)
**Mục tiêu**: Level up với CLAUDE.md mastery, hooks, subagents, MCP, và context optimization.

### 📄 Mastering CLAUDE.md
**Structure tối ưu:**
```markdown
# Project Overview
Brief description, tech stack, architecture.

# Architecture
Key patterns, folder structure, data flow.

# Conventions
Coding standards, naming, error handling.

# Commands  
Build, test, deploy commands.

# Gotchas
Known issues, edge cases, traps to avoid.
```

**Locations (theo priority):**
1. `~/.claude/CLAUDE.md` — Global (tất cả projects)
2. Repo root `CLAUDE.md` — Project-specific
3. Subdirectory `CLAUDE.md` — Module-specific

> **Elite Tip:** Giữ CLAUDE.md ngắn gọn — mỗi token đều tốn context window. Include examples output để train Claude responses.

### 🎓 Creating Skills
- Tạo `SKILL.md` trong bất kỳ directory nào
- Skills load **on-demand** — Claude tự phát hiện khi relevant
- **Best practices:** One skill per domain, include examples, define boundaries
- Compose skills bằng cách tham chiếu: "Use the deployment skill"
- Store shared skills trong `~/.claude/skills/` để reuse cross-project

### 🧬 Subagents
- Claude instances cô lập cho subtasks cụ thể
- Chạy trong context riêng — không pollute parent context
- **Use for:** Parallel code reviews, test generation, documentation, research
- Configure via `/agents` hoặc `.claude/agents.json`
- Mỗi subagent có model, tools, và permissions riêng

### 🪝 Hooks Deep Dive

**Hook Events:**
| Event | Khi nào chạy |
|-------|-------------|
| `SessionStart` | Khi bắt đầu session mới |
| `SessionEnd` | Khi kết thúc session |
| `PreToolUse` | Trước khi Claude sử dụng tool |
| `PostToolUse` | Sau khi Claude sử dụng tool |
| `UserPromptSubmit` | Khi user gửi prompt |
| `Stop` | Khi Claude dừng lại |

- **Matchers:** Filter hooks cho tools cụ thể (vd: chỉ chạy trên `write_file`)
- **Inputs:** Hooks nhận tool name, parameters, session context
- **Outputs:** Hooks có thể modify, block, hoặc augment tool behavior
- **Example:** Auto-run `eslint --fix` sau mỗi file write

### 📊 Managing Context (Kỹ năng quan trọng nhất!)
1. **Understand pricing:** Mỗi token in/out tốn tiền. Opus ~15× đắt hơn Haiku
2. **`/compact` trước, `/clear` nếu cần:** Compact tóm tắt; Clear reset hoàn toàn
3. **Mindful extensions:** MCP servers, plugins, large file reads tiêu tốn context nhanh
4. **Subagents & hooks:** Offload subtasks cho subagents để bảo toàn parent context
5. **Thinking modes & effort:** Điều chỉnh reasoning depth — không phải lúc nào cũng cần full chain-of-thought
6. **Prompt caching:** Anthropic cache repeated prompt prefixes — giữ CLAUDE.md ổn định để tiết kiệm

### 🔌 Connecting Tools with MCP
- **MCP (Model Context Protocol):** Open standard kết nối AI với external tools
- Kết nối databases, APIs, cloud services, Postman, GitHub, Slack...
- Configure qua `/mcp` hoặc `.claude/mcp.json`
- **Skills for MCP:** Tạo SKILL.md để dạy Claude cách sử dụng MCP servers cụ thể
- **Channels:** Bidirectional communication pathways cho real-time data flow

---

## 🚀 Phase 6 — Scaling & Production (Months 6-8+)
**Mục tiêu**: Mở rộng Claude Code ra ngoài cá nhân — CI/CD, agent teams, security at scale.

### 🎛️ Model Configuration (Opusplan)
- **Opusplan:** Dùng Opus cho planning, Sonnet cho execution — best of both worlds
- Route tasks theo complexity: Haiku → quick lookups, Sonnet → coding, Opus → architecture
- Configure per-project model preferences trong `.claude/settings.json`
- Adjust thinking effort levels để tối ưu cost vs quality

### 📡 Headless Mode
- Chạy Claude Code không cần interactive input — hoàn hảo cho CI/CD pipelines
- `claude -p "task" --output json` cho machine-parseable output
- Tích hợp vào GitHub Actions, GitLab CI, hoặc bất kỳ automation workflow
- Auto-review PRs, generate changelogs, run security audits — hoàn toàn unattended

### 🌿 Git Worktrees
- Dùng git worktrees để chạy nhiều Claude instances trên branches khác nhau đồng thời
- Mỗi worktree có working directory riêng — không conflicts
- Pattern: Main branch cho features, worktree cho bug fixes, worktree cho experiments
- Tăng tốc multi-task workflows đáng kể

### 👥 Agent Teams
- Điều phối nhiều Claude instances làm việc trên cùng project
- **Architect agent** → assigns tasks. **Worker agents** → implement. **Reviewer agent** → validates
- Kết hợp với git worktrees cho truly parallel development
- Define team configurations trong `.claude/agents.json`

### 🎨 Output Styles & Plugins
- **Output Styles:** Control verbosity, formatting, response structure
- **Customize status line:** Show token count, cost, model trong terminal
- **Scheduling Jobs:** Cron-like scheduling cho recurring Claude tasks
- **Code Intelligence plugin:** Enhanced code navigation và understanding

### 🛡️ Security Best Practices
- ❌ Không expose API keys, secrets, credentials trong prompts hay CLAUDE.md
- ✅ Dùng environment variables và `.env` files (add vào `.gitignore`)
- ✅ Review tất cả Claude-generated code cho security vulnerabilities trước khi merge
- ✅ Dùng permission modes để restrict dangerous operations
- ✅ Implement hooks cho security scanning — auto-run `gitleaks` hoặc `trivy`
- ✅ Chỉ kết nối trusted MCP servers

---

## 🏁 Kết luận: Elite Mindset

Claude Code không phải là tool để bạn lười biếng hơn — nó là **force multiplier** biến bạn thành một developer 10×. Bí mật nằm ở 3 chữ:

1. **Context** — CLAUDE.md tốt = output tốt
2. **Control** — Plan mode + Permission modes = an toàn
3. **Scale** — Hooks + Subagents + Headless = vô hạn

> "An expert Claude Code user doesn't write more code — they write better prompts."

---

## 🔗 Roadmaps liên quan
- 🎨 [Vibe Coding](file:///e:/Google%20Antigravity/Skills/Vibe%20Coding%28L%E1%BA%ADp%20tr%C3%ACnh%20phong%20c%C3%A1ch%20Vibe%29/SKILL.md) — Natural-language-driven development
- 🤖 [AI Agents](file:///e:/Google%20Antigravity/Skills/AI%20Agents%28K%E1%BB%B9%20s%C6%B0%20AI%20Agents%29/SKILL.md) — Autonomous agent systems
- ⚡ [AI Engineer](file:///e:/Google%20Antigravity/Skills/AI%20Engineer%28K%E1%BB%B9%20s%C6%B0%20AI%29/SKILL.md) — Full-stack AI engineering
- 💬 [Prompt Engineering](file:///e:/Google%20Antigravity/Skills/Prompt%20Engineering%28K%E1%BB%B9%20s%C6%B0%20Prompt%29/SKILL.md) — Craft powerful prompts

---
_Cập nhật lần cuối: Tháng 4, 2026 — Bởi Đội ngũ Antigravity (Elite Engineering Division)_
