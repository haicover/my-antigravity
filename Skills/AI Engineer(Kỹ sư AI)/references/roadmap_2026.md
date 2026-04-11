# 🛣️ Step-by-Step Guide to Becoming an Elite AI Engineer (2026)

## MODULE 0 — THE AI ENGINEER MINDSET (Week 1)
- **AI Engineer vs ML Engineer**: Focusing on building and shipping AI features with pre-trained models.
- **2026 Stack**: Context Engineering Layer -> Foundation Models -> Output Processing -> Application Layer -> Observability.
- **🇻🇳 Tóm tắt:** Tập trung vào việc triển khai (Shipping) thay vì đào tạo model. AI Engineer 2026 là người làm chủ "Context Engineering" và kết hợp linh hoạt các API.

---

## MODULE 1 — HOW LLMs WORK (Weeks 2–3)
- **Core Concepts**: Tokens, Context Window, Embeddings, Inference vs Training.
- **Context Caching**: Utilizing pre-filled context to reduce latency and cost (Gemini/Claude).
- **Sampling**: Temperature, Top-P, Top-K, and Min-P.
- **🇻🇳 Tóm tắt:** Nắm vững cơ chế Token và Caching. Hiểu rõ sự khác biệt giữa RAG và Fine-tuning để chọn giải pháp tối ưu.

---

## MODULE 2 — PROMPT & CONTEXT ENGINEERING (Weeks 4–6)
- **Techniques**: Chain-of-Thought (CoT), ReAct pattern, Skeleton-of-Thought.
- **Structured Outputs**: Pydantic models for JSON Schema enforcement.
- **Advanced**: Multi-modal prompting (Vision context), Prefill controls.
- **🇻🇳 Tóm tắt:** Không chỉ là viết text, mà là thiết kế cấu trúc dữ liệu trả về (JSON) và điều hướng luồng suy nghĩ của model thông qua CoT.

---

## MODULE 3 — AI MODELS & ECOSYSTEM (Weeks 7–9)
- **Frontier Models**: Claude 3.7+ (Reasoning), GPT-o4/o5 series, Gemini 2.0.
- **Open Weights**: Llama 4, DeepSeek-R2, Mistral Large 3.
- **Inference Stack**: Ollama, vLLM, SGLang (Local & Cloud distribution).
- **🇻🇳 Tóm tắt:** Làm chủ hệ sinh thái model. Biết khi nào dùng đồ nhà trồng (Llama) khi nào dùng API trả phí (Claude/GPT).

---

## MODULE 4 — EMBEDDINGS & VECTOR DATABASES (Weeks 10–13)
- **Semantic Search**: Distance metrics (Cosine, Euclidean) and Indexing (HNSW/IVF).
- **Modern Vector DBs**: Qdrant (Local first), Weaviate (GraphQL), Pinecone (Serverless).
- **Hybrid Search**: Combining BM25 (Keyword) with Vector (Meaning).
- **🇻🇳 Tóm tắt:** Lưu trữ tri thức doanh nghiệp. Kết hợp tìm kiếm keyword truyền thống và tìm kiếm ngữ nghĩa để đạt độ chính xác cao nhất.

---

## MODULE 5 — AGENTIC RAG (Weeks 14–18)
- **Agentic Loops**: Reasoning before retrieval, Self-Correction, and Tool-calling integrated RAG.
- **Advanced Retrieval**: HyDE (Hypothetical Document Embeddings), Re-ranking (Cohere/BGE).
- **GraphRAG**: Implementing Knowledge Graphs to capture complex entity relationships.
- **🇻🇳 Tóm tắt:** RAG "có bộ não". AI không chỉ lấy dữ liệu mà còn tự đánh giá dữ liệu lấy ra có đúng hay không và tự tìm lại nếu sai.

---

## MODULE 6 — MCP & AI TOOLS (Weeks 19–25)
- **MCP (Model Context Protocol)**: The universal standard for AI tool connection.
- **Building MCP Servers**: Exposing local databases, APIs, and file systems to LLMs securely.
- **Agent Orchestration**: Multi-agent delegation (LangGraph, CrewAI).
- **🇻🇳 Tóm tắt:** Xây dựng "cánh tay" cho AI qua MCP. Giúp AI có thể thao tác trực tiếp trên dữ liệu và hệ thống thực tế của công ty.

---

## MODULE 7 — AI SAFETY & SECURITY (Weeks 26–30)
- **Threats**: Prompt Injection (Jailbreaking), Data Poisoning, PII leakage.
- **Guardrails**: Implementing NeMo Guardrails or Llama Guard for input/output filtering.
- **Adversarial Testing**: Red-teaming AI agent logic.
- **🇻🇳 Tóm tắt:** Bảo mật cho AI. Ngăn chặn việc người dùng "lừa" AI cung cấp thông tin nhạy cảm hoặc truy cập trái phép.

---

## MODULE 8 — MULTIMODAL AI & PRODUCTION TOOLS (Weeks 31–36)
- **Vision/Audio/Video**: Seamless context switching between modalities.
- **AI Toolchain**: Cursor, Claude Code, Windsurf integration into the dev workflow.
- **🇻🇳 Tóm tắt:** AI đa phương thức. Xử lý hình ảnh, âm thanh và video trong cùng một luồng logic với văn bản.

---

## MODULE 9 — PRODUCTION OPS & OPTIMIZATION (Weeks 37–40)
- **Observability**: Langfuse/LangSmith for tracing agent reasoning steps.
- **Optimization**: Speculative Decoding (using a small model to speed up a large one).
- **Evaluations**: RAGAS (Faithfulness, Answer Relevance), LLM-as-a-Judge.
- **🇻🇳 Tóm tắt:** Đưa AI vào thực tế. Đảm bảo hệ thống chạy nhanh, rẻ và quan trọng nhất là đo lường được "chất lượng" của AI.

---

## THE ELITE AI ENGINEER TECH STACK (2026)
- **Runtime**: vLLM / SGLang
- **Orchestration**: LangGraph / LlamaIndex
- **Tools**: MCP SDK (fastmcp)
- **Eval**: RAGAS + Langfuse
- **IDE**: Cursor + Claude Code
