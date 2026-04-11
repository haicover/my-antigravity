// ═══════════════════════════════════════════════════════════════
//  Antigravity Skills Portal — Data Layer
//  Version: Elite 2026 — 100% CERTIFIED
// ═══════════════════════════════════════════════════════════════

const SKILL_CATEGORIES = [
  { id: 'ai-tools', name: 'AI Tools & Agents', icon: '🤖', color: '#a855f7' },
  { id: 'ai-data', name: 'AI & Data Science', icon: '🧠', color: '#6366f1' },
  { id: 'frontend', name: 'Frontend', icon: '🎨', color: '#06b6d4' },
  { id: 'backend', name: 'Backend', icon: '⚙️', color: '#10b981' },
  { id: 'fullstack', name: 'Full Stack & Mobile', icon: '📱', color: '#f59e0b' },
  { id: 'devops', name: 'DevOps & Security', icon: '🛡️', color: '#ef4444' },
  { id: 'architecture', name: 'Architecture & Systems', icon: '🏗️', color: '#8b5cf6' },
  { id: 'management', name: 'Management & Comms', icon: '📢', color: '#ec4899' },
  { id: 'creative', name: 'Creative & Automation', icon: '✨', color: '#f97316' },
  { id: 'web3', name: 'Web3 & Blockchain', icon: '🔗', color: '#14b8a6' },
];

const SKILLS_DATA = [
  // ─── AI Tools & Agents ─────────────────────
  {
    name: 'Claude Code',
    nameVi: 'Chuyên gia Claude Code',
    folder: 'Claude Code(Chuyên gia Claude Code)',
    category: 'ai-tools',
    status: 'elite',
    version: '1.0',
    date: '2026-04-11',
    pillars: 'Agentic Workflows, CLAUDE.md, Hooks, Subagents, MCP',
    description: 'Anthropic\'s flagship AI coding agent. Master agentic workflows, context management, and scaling strategies.'
  },
  {
    name: 'OpenClaw',
    nameVi: 'Triển khai AI Agent tự chủ',
    folder: 'OpenClaw(Triển khai AI Agent tự chủ)',
    category: 'ai-tools',
    status: 'elite',
    version: '1.0',
    date: '2026-04-11',
    pillars: 'Self-hosted, Gateway, Channels, Skills, Heartbeats, Security',
    description: 'Open-source self-hosted autonomous AI agent framework. Deploy on your own infrastructure.'
  },
  {
    name: 'Vibe Coding',
    nameVi: 'Lập trình phong cách Vibe',
    folder: 'Vibe Coding(Lập trình phong cách Vibe)',
    category: 'ai-tools',
    status: 'elite',
    version: '2.0',
    date: '2026-04-09',
    pillars: 'Natural Language Dev, AI-First, Prompt-Driven',
    description: 'The paradigm of describing intent in natural language and letting AI agents write the code.'
  },
  {
    name: 'MCP Builder',
    nameVi: 'Giao thức ngữ cảnh mô hình thợ xây',
    folder: 'mcp-builder(giao thức ngữ cảnh mô hình thợ xây)',
    category: 'ai-tools',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Protocol V1.0+, Tool Design, Security, Evals, Nexus',
    description: 'Build Model Context Protocol servers connecting AI systems to external tools and data sources.'
  },
  {
    name: 'Prompt Engineering',
    nameVi: 'Kỹ sư Prompt',
    folder: 'Prompt Engineering(Kỹ sư Prompt)',
    category: 'ai-tools',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Chain-of-Thought, Few-Shot, System Prompts, Meta-Prompting',
    description: 'Craft high-quality prompts for LLMs to maximize output accuracy and creativity.'
  },

  // ─── AI & Data Science ─────────────────────
  {
    name: 'AI Agents',
    nameVi: 'Kỹ sư AI Agents',
    folder: 'AI Agents(Kỹ sư AI Agents)',
    category: 'ai-data',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'ReAct, Tool Use, Multi-Agent, Orchestration',
    description: 'Design and build autonomous AI agent systems with agentic loops and tool integration.'
  },
  {
    name: 'AI Engineer',
    nameVi: 'Kỹ sư AI',
    folder: 'AI Engineer(Kỹ sư AI)',
    category: 'ai-data',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'Full-stack AI, RAG, Fine-tuning, Deployment',
    description: 'End-to-end AI engineering from model selection to production deployment.'
  },
  {
    name: 'AI & Data Scientist',
    nameVi: 'Nhà khoa học dữ liệu & AI',
    folder: 'AI and Data Scientist(Nhà khoa học dữ liệu & AI)',
    category: 'ai-data',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Statistics, ML Models, Feature Engineering, NLP',
    description: 'Data science fundamentals, statistical modeling, and AI research methodology.'
  },
  {
    name: 'Machine Learning',
    nameVi: 'Kỹ sư học máy',
    folder: 'Machine Learning(Kỹ sư học máy)',
    category: 'ai-data',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Agentic ML, LLMs, PEFT, MLOps, Multi-modal',
    description: 'Advanced ML engineering from classical algorithms to LLMs and multi-modal systems.'
  },
  {
    name: 'MLOps',
    nameVi: 'Kỹ sư MLOps',
    folder: 'MLOps(Kỹ sư MLOps)',
    category: 'ai-data',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Model Serving, Pipelines, Monitoring, A/B Testing',
    description: 'Operationalize machine learning models at scale with robust CI/CD pipelines.'
  },
  {
    name: 'Data Engineering',
    nameVi: 'Kỹ sư Dữ liệu',
    folder: 'Data Engineering(Kỹ sư Dữ liệu)',
    category: 'ai-data',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'ETL, Data Lakes, Streaming, Orchestration',
    description: 'Build scalable data pipelines, warehouses, and real-time streaming architectures.'
  },
  {
    name: 'Google AI Studio',
    nameVi: 'Trung tâm sáng tạo AI',
    folder: 'Google AI Studio(Trung tâm sáng tạo AI)',
    category: 'ai-data',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Vibe Coding, Multi-modal, Agents, Caching',
    description: 'Google\'s AI development platform for building with Gemini models.'
  },
  {
    name: 'Google Gemini',
    nameVi: 'Hệ sinh thái Google AI',
    folder: 'Google Gemini(Hệ sinh thái Google AI)',
    category: 'ai-data',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Unified SDK, Multimodal Live, Agentic, Vertex AI',
    description: 'The complete Google Gemini AI ecosystem, SDKs, and Vertex AI integration.'
  },

  // ─── Frontend ──────────────────────────────
  {
    name: 'Frontend Developer',
    nameVi: 'Nhà phát triển Frontend',
    folder: 'Frontend Developer(Nhà phát triển Frontend)',
    category: 'frontend',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'RSC, AI-Native DX, Performance Observability',
    description: 'Modern frontend development with React Server Components, AI-native tooling, and performance.'
  },
  {
    name: 'Frontend Performance',
    nameVi: 'Tối ưu hiệu năng Frontend',
    folder: 'Frontend Performance(Tối ưu hiệu năng Frontend)',
    category: 'frontend',
    status: 'elite',
    version: '4.5',
    date: '2026-04-10',
    pillars: 'INP Mastery, RUM Observability, AI-Predictive',
    description: 'Cutting-edge frontend performance optimization with Core Web Vitals and predictive loading.'
  },
  {
    name: 'UX Design',
    nameVi: 'Thiết kế UX',
    folder: 'UX Design(Thiết kế UX)',
    category: 'frontend',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'User Research, Wireframing, Prototyping, Accessibility',
    description: 'User experience design principles, research methods, and interaction design.'
  },
  {
    name: 'Design System',
    nameVi: 'Hệ thống thiết kế',
    folder: 'Design System(Hệ thống thiết kế)',
    category: 'frontend',
    status: 'elite',
    version: '1.8',
    date: '2026-04-10',
    pillars: 'Liquid Design, Design-as-Code, W3C Tokens',
    description: 'Build and maintain scalable design systems with design tokens and component libraries.'
  },

  // ─── Backend ───────────────────────────────
  {
    name: 'Backend Developer',
    nameVi: 'Nhà phát triển Backend',
    folder: 'Backend Developer(Nhà phát triển Backend)',
    category: 'backend',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Distributed, AI-Native, High-Performance, Autonomic',
    description: 'Server-side development with distributed systems, AI integration, and autonomous operations.'
  },
  {
    name: 'Backend Performance',
    nameVi: 'Tối ưu hiệu năng Backend',
    folder: 'Backend Performance(Tối ưu hiệu năng Backend)',
    category: 'backend',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'Caching, Connection Pooling, Query Optimization, Profiling',
    description: 'Backend performance tuning, profiling, and optimization strategies.'
  },
  {
    name: 'Java Developer',
    nameVi: 'Lập trình Java',
    folder: 'Java Developer(Lập trình Java)',
    category: 'backend',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Java 21+, Virtual Threads, GraalVM, Spring AI',
    description: 'Modern Java development with virtual threads, GraalVM native images, and AI integration.'
  },
  {
    name: 'Python Developer',
    nameVi: 'Lập trình viên Python',
    folder: 'Python Developer(Lập trình viên Python)',
    category: 'backend',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'AsyncIO, FastAPI, Type Hints, ML Integration',
    description: 'Professional Python development for web, data science, and automation.'
  },
  {
    name: 'Spring Boot',
    nameVi: 'Lập trình Spring Boot',
    folder: 'Spring Boot(Lập trình Spring Boot)',
    category: 'backend',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'Microservices, WebFlux, Security, Cloud-Native',
    description: 'Enterprise Java framework for building production-ready applications.'
  },
  {
    name: 'SQL Roadmap',
    nameVi: 'Lộ trình SQL',
    folder: 'SQL Roadmap(Lộ trình SQL)',
    category: 'backend',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Query Optimization, Indexing, Transactions, Analytics',
    description: 'Comprehensive SQL mastery from basics to advanced query optimization and analytics.'
  },
  {
    name: 'API Design',
    nameVi: 'Thiết kế và Xây dựng API',
    folder: 'API Design(Thiết kế và Xây dựng API)',
    category: 'backend',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'REST, GraphQL, gRPC, OpenAPI, Versioning',
    description: 'Design-first API development with REST, GraphQL, gRPC, and documentation standards.'
  },

  // ─── Full Stack & Mobile ───────────────────
  {
    name: 'FullStack Developer',
    nameVi: 'Nhà phát triển FullStack',
    folder: 'FullStack Developer(Nhà phát triển FullStack)',
    category: 'fullstack',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Unified Arch, Type-safe E2E, AI Orchestration',
    description: 'Full-stack development bridging frontend and backend with unified architectures.'
  },
  {
    name: 'Mobile App Developer',
    nameVi: 'Nhà phát triển Mobile',
    folder: 'Mobile App Developer (Nhà phát triển Mobile)',
    category: 'fullstack',
    status: 'elite',
    version: '4.0',
    date: '2026-04-11',
    pillars: 'React Native, Flutter, Swift, Kotlin, AI-Native',
    description: 'Cross-platform and native mobile development for iOS and Android.'
  },
  {
    name: 'WordPress',
    nameVi: 'Lập trình WordPress chuyên nghiệp',
    folder: 'WordPress(Lập trình WordPress chuyên nghiệp)',
    category: 'fullstack',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Gutenberg, REST API, Headless, Plugins, FSE',
    description: 'Professional WordPress development with modern block editor and headless architecture.'
  },

  // ─── DevOps & Security ─────────────────────
  {
    name: 'DevOps & SRE',
    nameVi: 'Kỹ sư DevOps & SRE',
    folder: 'DevOps(Kỹ sư DevOps & SRE)',
    category: 'devops',
    status: 'elite',
    version: '4.0',
    date: '2026-04-10',
    pillars: 'Autonomous Ops, Platform Eng, OTel',
    description: 'Site reliability engineering with autonomous operations, platform engineering, and observability.'
  },
  {
    name: 'DevSecOps',
    nameVi: 'Chuyên gia Bảo mật DevSecOps',
    folder: 'DevSecOps(Chuyên gia Bảo mật DevSecOps)',
    category: 'devops',
    status: 'elite',
    version: '3.5',
    date: '2026-04-10',
    pillars: 'Autonomous Governance, NHI, eBPF',
    description: 'Security-integrated DevOps with autonomous governance and non-human identity management.'
  },
  {
    name: 'Cyber Security Expert',
    nameVi: 'Chuyên gia An ninh mạng',
    folder: 'Cyber Security Expert(Chuyên gia An ninh mạng)',
    category: 'devops',
    status: 'elite',
    version: '2.5',
    date: '2026-04-10',
    pillars: 'Warfare Mastery, PQC, Agentic SOC',
    description: 'Advanced cybersecurity with post-quantum cryptography, agentic SOC, and threat hunting.'
  },
  {
    name: 'Cloud Native & IaC',
    nameVi: 'Kiến trúc Đám mây & IaC',
    folder: 'Cloud Native & IaC(Kiến trúc Đám mây & IaC)',
    category: 'devops',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'Kubernetes, Terraform, Serverless, GitOps',
    description: 'Cloud-native architecture with container orchestration, infrastructure as code, and GitOps.'
  },
  {
    name: 'Forensic Security Intelligence',
    nameVi: 'Trí tuệ Pháp y Bảo mật',
    folder: 'Forensic Security Intelligence(Trí tuệ Pháp y Bảo mật)',
    category: 'devops',
    status: 'elite',
    version: '2.0',
    date: '2026-04-11',
    pillars: 'File Forensics, Malware Detection, Remediation',
    description: 'Autonomous forensic engine for detecting malicious content and automated remediation.'
  },
  {
    name: 'Git & GitHub',
    nameVi: 'Quản lý mã nguồn với Git & GitHub',
    folder: 'Git and GitHub(Quản lý mã nguồn với Git & GitHub)',
    category: 'devops',
    status: 'elite',
    version: '3.5',
    date: '2026-04-10',
    pillars: 'GitOps, AI-Native, Advanced Recovery, CI/CD',
    description: 'Advanced Git workflows, GitHub Actions CI/CD, and AI-native version control.'
  },

  // ─── Architecture & Systems ────────────────
  {
    name: 'Software Design & Architecture',
    nameVi: 'Thiết kế và Kiến trúc Phần mềm',
    folder: 'Software Design and Architecture(Thiết kế và Kiến trúc Phần mềm)',
    category: 'architecture',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'Clean Arch, DDD, CQRS, Event Sourcing',
    description: 'Software architecture patterns, clean architecture, and domain-driven design.'
  },
  {
    name: 'System Design',
    nameVi: 'Lộ trình Thiết kế Hệ thống Quy mô lớn',
    folder: 'System Design(Lộ trình Thiết kế Hệ thống Quy mô lớn)',
    category: 'architecture',
    status: 'elite',
    version: '3.5',
    date: '2026-04-11',
    pillars: 'Scalability, Load Balancing, Distributed Systems',
    description: 'Design large-scale distributed systems, handle millions of users, and ace system design interviews.'
  },
  {
    name: 'System Analysis',
    nameVi: 'Phân tích Thiết kế HTTT',
    folder: 'System Analysis(Phân tích Thiết kế HTTT)',
    category: 'architecture',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'BPMN, DFD, ERD, UML, Requirements Eng',
    description: 'Information systems analysis with BPMN, data flow diagrams, and UML modeling.'
  },
  {
    name: 'Code Review',
    nameVi: 'Đánh giá mã nguồn',
    folder: 'Code Review(Đánh giá mã nguồn)',
    category: 'architecture',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Review Standards, Static Analysis, AI-Assisted Review',
    description: 'Effective code review processes, standards, and automated analysis integration.'
  },

  // ─── Management & Communication ────────────
  {
    name: 'Engineering Manager',
    nameVi: 'Quản lý kỹ thuật',
    folder: 'Engineering Manager(Quản lý kỹ thuật)',
    category: 'management',
    status: 'elite',
    version: '2.5',
    date: '2026-04-10',
    pillars: 'Org Flow, Strategic Influence, Talent Density',
    description: 'Technical leadership, team management, and organizational flow optimization.'
  },
  {
    name: 'Product Manager',
    nameVi: 'Quản lý sản phẩm',
    folder: 'Product Manager(Quản lý sản phẩm)',
    category: 'management',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Strategy, Metrics, Discovery, Delivery, AI-PLG',
    description: 'Product strategy, user research, prioritization frameworks, and delivery management.'
  },
  {
    name: 'Developer Relations',
    nameVi: 'Quan hệ nhà phát triển',
    folder: 'Developer Relations(Quan hệ nhà phát triển)',
    category: 'management',
    status: 'elite',
    version: '3.0',
    date: '2026-04-10',
    pillars: '8-Phase Ecosystem Mastery',
    description: 'Build developer ecosystems, advocacy programs, and technical community engagement.'
  },
  {
    name: 'Internal Comms',
    nameVi: 'Truyền thông nội bộ',
    folder: 'internal-comms(truyền thông nội bộ)',
    category: 'management',
    status: 'elite',
    version: '3.0',
    date: '2026-04-10',
    pillars: '3P Framework, Async Sync, Radical Candor, AI Flow',
    description: 'Effective internal communication with async-first frameworks and AI-assisted workflows.'
  },
  {
    name: 'Doc Co-authoring',
    nameVi: 'Đồng tác giả tài liệu',
    folder: 'doc-coauthoring(đồng tác giả tài liệu)',
    category: 'management',
    status: 'elite',
    version: '1.5',
    date: '2026-04-10',
    pillars: 'Collaborative Intelligence, Semantic Sync',
    description: 'Collaborative document creation with AI-assisted co-authoring workflows.'
  },
  {
    name: 'Brand Guidelines',
    nameVi: 'Hướng dẫn thương hiệu',
    folder: 'brand-guidelines(hướng dẫn thương hiệu)',
    category: 'management',
    status: 'elite',
    version: '2.0',
    date: '2026-04-11',
    pillars: 'Brand Identity, Visual Language, Tone, AI Branding',
    description: 'Comprehensive brand guidelines for consistent visual identity and communication.'
  },

  // ─── Creative & Automation ─────────────────
  {
    name: 'Algorithmic Art',
    nameVi: 'Nghệ thuật thuật toán',
    folder: 'algorithmic-art(nghệ thuật thuật toán)',
    category: 'creative',
    status: 'elite',
    version: '2.5',
    date: '2026-04-11',
    pillars: 'Generative Art, Shaders, Creative Coding',
    description: 'Create visual art through algorithms, shaders, and creative coding techniques.'
  },
  {
    name: 'Canvas Design',
    nameVi: 'Thiết kế Canvas',
    folder: 'canvas-design(thiết kế canvas)',
    category: 'creative',
    status: 'elite',
    version: '2.5',
    date: '2026-04-11',
    pillars: 'Canvas API, WebGL, Data Visualization',
    description: 'Advanced HTML5 Canvas and WebGL for interactive visualizations and animations.'
  },
  {
    name: 'Theme Factory',
    nameVi: 'Nhà máy chủ đề',
    folder: 'theme-factory(nhà máy chủ đề)',
    category: 'creative',
    status: 'elite',
    version: '2.5',
    date: '2026-04-11',
    pillars: 'Theming Systems, CSS Variables, Dynamic Themes',
    description: 'Build dynamic theming systems with CSS custom properties and design token pipelines.'
  },
  {
    name: 'Web Artifacts Builder',
    nameVi: 'Trình tạo hiện vật web',
    folder: 'web-artifacts-builder(trình tạo hiện vật web)',
    category: 'creative',
    status: 'elite',
    version: '2.5',
    date: '2026-04-11',
    pillars: 'Component Generation, Live Preview, Export',
    description: 'Generate web artifacts and interactive components with AI-assisted building.'
  },
  {
    name: 'Slack GIF Creator',
    nameVi: 'Công cụ tạo ảnh GIF Slack',
    folder: 'slack-gif-creator(công cụ tạo ảnh GIF Slack)',
    category: 'creative',
    status: 'elite',
    version: '2.0',
    date: '2026-04-11',
    pillars: 'GIF Generation, Slack Integration, Animation',
    description: 'Create and deploy custom GIF animations for Slack workspace communication.'
  },
  {
    name: 'Rapid Automation',
    nameVi: 'Tự động hóa & Low Code',
    folder: 'Rapid Automation(Tự động hóa & Low Code)',
    category: 'creative',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'No-Code, Zapier, n8n, Workflow Automation',
    description: 'Rapid automation with low-code platforms, workflow builders, and integration tools.'
  },
  {
    name: 'Skill Creator',
    nameVi: 'Người tạo kỹ năng',
    folder: 'skill-creator(người tạo kỹ năng)',
    category: 'creative',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Meta-skill, Template Systems, Knowledge Encoding',
    description: 'The meta-skill for creating and structuring AI skills and capability modules.'
  },
  {
    name: 'Antigravity Optimization',
    nameVi: 'Tối ưu hóa Antigravity',
    folder: 'Antigravity Optimization(Tối ưu hóa Antigravity)',
    category: 'creative',
    status: 'elite',
    version: '2.0',
    date: '2026-04-11',
    pillars: 'System Optimization, Workflow Tuning, AI Pipeline',
    description: 'Optimize the Antigravity ecosystem for maximum performance and developer experience.'
  },

  // ─── Web3 & Blockchain ─────────────────────
  {
    name: 'Web3 & Blockchain',
    nameVi: 'Nhà phát triển Web3',
    folder: 'Web3 and Blockchain(Nhà phát triển Web3)',
    category: 'web3',
    status: 'elite',
    version: '3.0',
    date: '2026-04-11',
    pillars: 'Smart Contracts, DeFi, dApps, L2 Scaling',
    description: 'Web3 development with smart contracts, DeFi protocols, and decentralized applications.'
  },
];
