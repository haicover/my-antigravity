# Node / TypeScript MCP Server — Implementation Guide

> **SDK**: `@modelcontextprotocol/sdk ^1.6.1`  
> **Node**: `>=18` | **TypeScript**: `^5.7` | **Zod**: `^3.23`  
> **Xem thêm**: [MCP Best Practices](./MCP_BEST_PRACTICES.md) cho các quy tắc chung

---

## Mục lục

1. [Bắt đầu nhanh](#1-bat-dau-nhanh)
2. [Cấu trúc project](#2-cau-truc-project)
3. [Cấu hình](#3-cau-hinh)
4. [Khởi tạo Server](#4-khoi-tao-server)
5. [Thiết kế và đăng ký Tools](#5-thiet-ke-va-dang-ky-tools)
6. [Zod Schema & Validation](#6-zod-schema--validation)
7. [Response Formats](#7-response-formats)
8. [Pagination & Character Limit](#8-pagination--character-limit)
9. [Error Handling](#9-error-handling)
10. [Shared Utilities](#10-shared-utilities)
11. [Transport](#11-transport)
12. [Advanced: Resources & Notifications](#12-advanced-resources--notifications)
13. [TypeScript Best Practices](#13-typescript-best-practices)
14. [Complete Working Example](#14-complete-working-example)
15. [Quality Checklist](#15-quality-checklist)

---

## 1. Bắt đầu nhanh

### Cài đặt dependencies

```bash
npm install @modelcontextprotocol/sdk axios zod
npm install -D typescript tsx @types/node
```

### Khởi tạo project

```bash
mkdir my-service-mcp-server && cd my-service-mcp-server
npm init -y
npx tsc --init
mkdir -p src/{tools,services,schemas}
touch src/index.ts src/constants.ts src/types.ts
```

### Chạy development

```bash
npm run dev    # tsx watch — hot reload
npm run build  # tsc — compile sang dist/
npm start      # node dist/index.js
```

---

## 2. Cấu trúc project

```
{service}-mcp-server/
├── package.json
├── tsconfig.json
├── README.md
└── src/
    ├── index.ts          ← Entry point: khởi tạo McpServer, connect transport
    ├── constants.ts      ← Hằng số dùng chung (API_BASE_URL, CHARACTER_LIMIT...)
    ├── types.ts          ← TypeScript interfaces và type definitions
    ├── tools/            ← Tool implementations, mỗi file = một domain
    │   ├── users.ts
    │   ├── projects.ts
    │   └── messages.ts
    ├── services/         ← API clients, HTTP utilities
    │   └── api.ts
    └── schemas/          ← Zod schemas tái sử dụng (Pagination, ResponseFormat...)
        └── common.ts
```

> **Quy tắc tổ chức**: Mỗi file trong `tools/` chỉ chứa tools thuộc cùng một domain. Logic API đặt trong `services/`, không viết lẫn vào tool handlers.

---

## 3. Cấu hình

### `package.json`

```json
{
  "name": "{service}-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for {Service} API integration",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "clean": "rm -rf dist"
  },
  "engines": {
    "node": ">=18"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "axios": "^1.7.9",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2"
  }
}
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### `src/constants.ts`

```typescript
export const API_BASE_URL = "https://api.yourservice.com/v1";
export const CHARACTER_LIMIT = 25_000; // Max response size (chars)
export const REQUEST_TIMEOUT = 30_000; // HTTP timeout (ms)
export const DEFAULT_LIMIT = 20; // Default pagination size
export const MAX_LIMIT = 100; // Max pagination size
```

---

## 4. Khởi tạo Server

### Key imports

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import express from "express";
```

### Tạo server instance

```typescript
// src/index.ts
const server = new McpServer({
  name: "myservice-mcp-server", // Theo format: {service}-mcp-server
  version: "1.0.0",
});
```

### ⚠️ API cũ đã bị deprecated — KHÔNG dùng

```typescript
// ❌ Deprecated — không dùng
server.tool("tool_name", handler);
server.setRequestHandler(ListToolsRequestSchema, handler);

// ✅ Đúng — luôn dùng register* methods
server.registerTool("tool_name", config, handler);
server.registerResource(config, handler);
server.registerPrompt(config, handler);
```

---

## 5. Thiết kế và đăng ký Tools

### Quy tắc đặt tên

**Format**: `{service}_{action}_{resource}` — snake_case, có service prefix

```
✅  slack_send_message
✅  github_create_issue
✅  jira_list_tickets
✅  stripe_get_invoice

❌  sendMessage       (thiếu prefix → conflict với MCP server khác)
❌  slackMsg          (không phải snake_case)
❌  do_stuff          (không action-oriented)
❌  github_v2_create  (có version number)
```

### Cấu trúc registerTool

```typescript
server.registerTool(
  "service_action_resource",        // Tên tool
  {
    title:       "Display Name",    // Hiển thị trong UI
    description: "...",             // AI đọc để quyết định dùng tool — viết kỹ
    inputSchema: ZodSchemaObject,   // Zod schema (KHÔNG phải JSON schema)
    annotations: {
      readOnlyHint:    boolean,     // Tool không thay đổi dữ liệu?
      destructiveHint: boolean,     // Có thể xóa/ghi đè không thể hoàn tác?
      idempotentHint:  boolean,     // Gọi nhiều lần với cùng args an toàn?
      openWorldHint:   boolean,     // Tương tác với hệ thống ngoài?
    }
  },
  async (params) => {
    // Handler: nhận params đã validated bởi Zod
    return {
      content: [{ type: "text", text: "..." }],
      structuredContent: { ... }    // Modern pattern — trả về cả structured data
    };
  }
);
```

### Ví dụ tool hoàn chỉnh

```typescript
// src/tools/users.ts
import { server } from "../index.js";
import { makeRequest } from "../services/api.js";
import { handleError } from "../services/errors.js";
import {
  PaginationSchema,
  ResponseFormat,
  ResponseFormatSchema,
} from "../schemas/common.js";
import { CHARACTER_LIMIT } from "../constants.js";
import { z } from "zod";

const SearchUsersSchema = z
  .object({
    query: z
      .string()
      .min(2, "Query phải có ít nhất 2 ký tự")
      .max(200, "Query không được vượt quá 200 ký tự")
      .describe("Chuỗi tìm kiếm — khớp với name hoặc email"),
    ...PaginationSchema.shape,
    response_format: ResponseFormatSchema,
  })
  .strict();

type SearchUsersInput = z.infer<typeof SearchUsersSchema>;

server.registerTool(
  "example_search_users",
  {
    title: "Search Users",
    description: `
Search for users in the Example system by name or email.

Supports partial matches. Returns paginated results.
Does NOT create or modify users — read-only operation.

Args:
  query (string): Search string, min 2 chars
  limit (number): Max results, 1–100, default 20
  offset (number): Pagination offset, default 0
  response_format: 'markdown' (default) or 'json'

Returns (json):
  {
    total: number,
    count: number,
    offset: number,
    users: [{ id, name, email, team?, active }],
    has_more: boolean,
    next_offset?: number
  }

Examples:
  - "Find all marketing members"  → query="team:marketing"
  - "Search for John's account"   → query="john"
  - Need to create a user?        → use example_create_user instead
    `.trim(),
    inputSchema: SearchUsersSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: SearchUsersInput) => {
    try {
      const data = await makeRequest<{ users: any[]; total: number }>(
        "users/search",
        "GET",
        undefined,
        { q: params.query, limit: params.limit, offset: params.offset },
      );

      const { users = [], total = 0 } = data;

      if (users.length === 0) {
        return {
          content: [
            { type: "text", text: `No users found matching '${params.query}'` },
          ],
        };
      }

      const output = {
        total,
        count: users.length,
        offset: params.offset,
        users: users.map((u) => ({
          id: u.id,
          name: u.name,
          email: u.email,
          ...(u.team ? { team: u.team } : {}),
          active: u.active ?? true,
        })),
        has_more: total > params.offset + users.length,
        ...(total > params.offset + users.length
          ? { next_offset: params.offset + users.length }
          : {}),
      };

      const text =
        params.response_format === ResponseFormat.JSON
          ? JSON.stringify(output, null, 2)
          : formatUsersMarkdown(output);

      // Truncate nếu vượt CHARACTER_LIMIT
      const safeText = truncate(text, output, CHARACTER_LIMIT);

      return {
        content: [{ type: "text", text: safeText }],
        structuredContent: output,
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: handleError(error) }],
      };
    }
  },
);

function formatUsersMarkdown(output: ReturnType<typeof buildOutput>): string {
  const lines = [
    `# User Search Results`,
    `Found ${output.total} users (showing ${output.count})`,
    "",
  ];
  for (const u of output.users) {
    lines.push(`## ${u.name} \`${u.id}\``);
    lines.push(`- **Email**: ${u.email}`);
    if (u.team) lines.push(`- **Team**: ${u.team}`);
    lines.push(`- **Status**: ${u.active ? "Active" : "Inactive"}`);
    lines.push("");
  }
  return lines.join("\n");
}
```

---

## 6. Zod Schema & Validation

### Schemas dùng chung — `src/schemas/common.ts`

```typescript
import { z } from "zod";

// Pagination — tái sử dụng trong mọi list tool
export const PaginationSchema = z.object({
  limit: z
    .number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("Max items to return (1–100, default 20)"),
  offset: z
    .number()
    .int()
    .min(0)
    .default(0)
    .describe("Number of items to skip for pagination"),
});

// Response format
export enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json",
}
export const ResponseFormatSchema = z
  .nativeEnum(ResponseFormat)
  .default(ResponseFormat.MARKDOWN)
  .describe("Output format: 'markdown' (default) or 'json'");
```

### Validation patterns

```typescript
import { z } from "zod";

const CreateUserSchema = z
  .object({
    // String constraints
    name: z.string().min(1, "Name is required").max(100),
    email: z.string().email("Invalid email format"),

    // Number constraints
    age: z.number().int("Must be a whole number").min(0).max(150),

    // Optional với default
    role: z.enum(["admin", "member", "viewer"]).default("member"),

    // Optional không có default
    bio: z.string().max(500).optional(),
  })
  .strict(); // .strict() — reject extra fields không khai báo

type CreateUserInput = z.infer<typeof CreateUserSchema>;
```

### ✅ Dùng Zod parse để validate external data

```typescript
// ✅ Runtime validation — safe
async function getUser(id: string): Promise<User> {
  const raw = await apiCall(`/users/${id}`);
  return UserSchema.parse(raw); // Throws ZodError nếu schema không match
}

// ❌ Không validate — unsafe
async function getUser(id: string): Promise<any> {
  return await apiCall(`/users/${id}`);
}
```

---

## 7. Response Formats

### Markdown (default) — cho người đọc

```typescript
function formatChannelMarkdown(channel: Channel): string {
  return [
    `## #${channel.name}`,
    "",
    `**Creator**: ${channel.creator_name} (\`${channel.creator_id}\`)`,
    `**Members**: ${channel.num_members}`,
    `**Created**: ${new Date(channel.created * 1000).toLocaleDateString()}`,
    `**Topic**: ${channel.topic || "—"}`,
    "",
    `Status: ${channel.is_archived ? "Archived" : "Active"}`,
  ].join("\n");
}
```

### JSON — cho programmatic processing

```typescript
function formatChannelJson(channel: Channel): string {
  return JSON.stringify(
    {
      id: channel.id,
      name: channel.name,
      creator_id: channel.creator_id,
      num_members: channel.num_members,
      created_at: channel.created, // Unix timestamp — giữ nguyên
      topic: channel.topic,
      is_archived: channel.is_archived,
    },
    null,
    2,
  );
}
```

**Quy tắc chung:**

| Markdown                                 | JSON                                       |
| ---------------------------------------- | ------------------------------------------ |
| Timestamps dạng readable ("Dec 4, 2024") | Timestamps dạng Unix epoch                 |
| `Alice Johnson (U012ABC)`                | `{ name: "Alice Johnson", id: "U012ABC" }` |
| Bỏ verbose metadata                      | Giữ tất cả fields                          |
| Headers + lists cho hierarchy            | Flat hoặc nested objects                   |

---

## 8. Pagination & Character Limit

### Pagination schema và response

```typescript
// src/schemas/common.ts — đã định nghĩa PaginationSchema ở mục 6

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  count: number;
  offset: number;
  has_more: boolean;
  next_offset?: number;
}

function paginate<T>(
  items: T[],
  total: number,
  offset: number,
): PaginatedResponse<T> {
  return {
    items,
    total,
    count: items.length,
    offset,
    has_more: total > offset + items.length,
    next_offset:
      total > offset + items.length ? offset + items.length : undefined,
  };
}
```

### Character limit & truncation

```typescript
// src/constants.ts
export const CHARACTER_LIMIT = 25_000;

// src/services/truncate.ts
export function truncate<T extends { items?: unknown[] }>(
  text: string,
  data: T,
  limit: number,
): string {
  if (text.length <= limit) return text;

  // Nếu có items array: cắt bớt items rồi re-render
  if (Array.isArray(data.items) && data.items.length > 1) {
    const halfItems = data.items.slice(0, Math.ceil(data.items.length / 2));
    const truncated = {
      ...data,
      items: halfItems,
      truncated: true,
      truncation_message:
        `Response truncated: showing ${halfItems.length}/${data.items.length} items. ` +
        `Use 'offset' or add filters to see more.`,
    };
    return JSON.stringify(truncated, null, 2);
  }

  // Fallback: cắt raw text
  return (
    text.slice(0, limit) +
    "\n\n[Response truncated. Use filters to narrow results.]"
  );
}
```

---

## 9. Error Handling

### Error handler tập trung — `src/services/errors.ts`

```typescript
import axios, { AxiosError } from "axios";
import { ZodError } from "zod";

export function handleError(error: unknown): string {
  // Axios / HTTP errors
  if (axios.isAxiosError(error)) {
    return handleAxiosError(error);
  }

  // Zod validation errors (không nên xảy ra nếu schema đúng, nhưng để phòng)
  if (error instanceof ZodError) {
    const issues = error.issues
      .map((i) => `  - ${i.path.join(".")}: ${i.message}`)
      .join("\n");
    return `Validation error:\n${issues}`;
  }

  // Unknown errors — không expose internal details
  if (error instanceof Error) {
    return `Unexpected error: ${error.message}. Please try again.`;
  }

  return "An unexpected error occurred. Please try again.";
}

function handleAxiosError(error: AxiosError): string {
  // Có HTTP response
  if (error.response) {
    switch (error.response.status) {
      case 400:
        return "Bad request. Check the parameters and try again.";
      case 401:
        return "Authentication failed. Verify your API token is valid.";
      case 403:
        return "Permission denied. You don't have access to this resource.";
      case 404:
        return "Resource not found. Verify the ID is correct.";
      case 409:
        return "Conflict. The resource already exists or is in a conflicting state.";
      case 422:
        return "Invalid data. Check the required fields and formats.";
      case 429:
        return "Rate limit exceeded. Wait before making more requests.";
      case 500:
        return "Service error. Please try again in a moment.";
      case 503:
        return "Service temporarily unavailable. Please try again later.";
      default:
        return `API error (HTTP ${error.response.status}). Please try again.`;
    }
  }

  // Không có response
  if (error.code === "ECONNABORTED")
    return "Request timed out. Please try again.";
  if (error.code === "ENOTFOUND")
    return "Service unreachable. Check your network connection.";

  return `Network error: ${error.message}`;
}
```

### Dùng trong tool handler

```typescript
async (params) => {
  try {
    const result = await performOperation(params);
    return {
      content: [{ type: "text", text: formatResult(result) }],
      structuredContent: result,
    };
  } catch (error) {
    // Log đầy đủ server-side (stderr — không stdout)
    console.error("[tool_name] Error:", error);

    // Trả về message hữu ích, không expose internal details
    return {
      content: [{ type: "text", text: handleError(error) }],
    };
  }
};
```

---

## 10. Shared Utilities

### HTTP client — `src/services/api.ts`

```typescript
import axios from "axios";
import { API_BASE_URL, REQUEST_TIMEOUT } from "../constants.js";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export async function makeRequest<T>(
  endpoint: string,
  method: HttpMethod = "GET",
  body?: unknown,
  params?: Record<string, unknown>,
): Promise<T> {
  const apiKey = process.env.MY_SERVICE_API_KEY;
  if (!apiKey) throw new Error("MY_SERVICE_API_KEY is not configured");

  const response = await axios<T>({
    method,
    url: `${API_BASE_URL}/${endpoint}`,
    data: body,
    params,
    timeout: REQUEST_TIMEOUT,
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
  });

  return response.data;
}
```

### Validate API key on startup

```typescript
// src/index.ts
function validateEnv(): void {
  const required = ["MY_SERVICE_API_KEY"];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    console.error(
      `ERROR: Missing required environment variables:\n${missing.map((k) => `  - ${k}`).join("\n")}`,
    );
    process.exit(1);
  }
}
```

---

## 11. Transport

### stdio — local / command-line tools

```typescript
// ⚠️ KHÔNG log ra stdout — corrupt MCP protocol stream
// Dùng stderr cho tất cả logging

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

async function runStdio(): Promise<void> {
  validateEnv();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running via stdio"); // stderr ✅
}
```

### Streamable HTTP — remote / multi-client

```typescript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";

async function runHTTP(): Promise<void> {
  validateEnv();
  const app = express();
  const port = parseInt(process.env.PORT ?? "3000", 10);
  app.use(express.json());

  app.post("/mcp", async (req, res) => {
    // Tạo transport mới cho mỗi request — stateless, tránh ID collision
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });
    res.on("close", () => transport.close());
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  });

  app.listen(port, "127.0.0.1", () => {
    console.error(`MCP server running on http://localhost:${port}/mcp`);
  });
}
```

### Chọn transport theo environment

```typescript
// src/index.ts — entry point
const transport = process.env.TRANSPORT ?? "stdio";

const run = transport === "http" ? runHTTP : runStdio;
run().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

---

## 12. Advanced: Resources & Notifications

### Resources — URI-based data access

Dùng khi data có thể identify bằng URI đơn giản, không cần validation phức tạp:

```typescript
server.registerResource(
  {
    uri: "file://documents/{name}",
    name: "Document",
    description: "Access documents by name",
    mimeType: "text/plain",
  },
  async (uri: string) => {
    const match = uri.match(/^file:\/\/documents\/(.+)$/);
    if (!match) throw new Error(`Invalid URI: ${uri}`);

    const content = await loadDocument(match[1]);
    return {
      contents: [{ uri, mimeType: "text/plain", text: content }],
    };
  },
);
```

**Resources vs Tools:**

|                  | Resources              | Tools                    |
| ---------------- | ---------------------- | ------------------------ |
| **Dùng khi**     | Data access, URI-based | Operations, side effects |
| **Params**       | Đơn giản, từ URI       | Phức tạp, cần validation |
| **Side effects** | Không                  | Có thể có                |
| **Ví dụ**        | `file://docs/readme`   | `github_create_issue`    |

### Notifications — báo client khi server thay đổi

```typescript
// Chỉ dùng khi capabilities thực sự thay đổi — không spam
server.notification({ method: "notifications/tools/list_changed" });
server.notification({ method: "notifications/resources/list_changed" });
```

---

## 13. TypeScript Best Practices

### ✅ Dùng proper types — tránh `any`

```typescript
// ✅ Type-safe
interface UserResponse {
  id: string;
  name: string;
  email: string;
  team?: string;
  active: boolean;
}

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  team: z.string().optional(),
  active: z.boolean(),
});

type User = z.infer<typeof UserSchema>; // Derive type từ schema — single source of truth

async function getUser(id: string): Promise<User> {
  const data = await makeRequest<unknown>(`/users/${id}`);
  return UserSchema.parse(data); // Runtime validation
}

// ❌ Unsafe
async function getUser(id: string): Promise<any> {
  return makeRequest(`/users/${id}`); // Không có type safety hay runtime check
}
```

### ✅ Async/await — tránh promise chains

```typescript
// ✅ Readable, debuggable
async function fetchWithRetry(url: string, retries = 3): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      await sleep(1000 * 2 ** i); // Exponential backoff
    }
  }
  throw new Error("Unreachable");
}

// ❌ Harder to debug
function fetchWithRetry(url: string): Promise<Response> {
  return fetch(url).catch((e) => fetch(url).catch((e2) => fetch(url)));
}
```

### ✅ Null safety

```typescript
// Optional chaining và nullish coalescing
const userName = user?.profile?.name ?? "Unknown";
const memberCount = channel?.num_members ?? 0;
const teamName = member?.team?.name; // undefined nếu không có — không throw

// Type guards
function isAxiosError(error: unknown): error is AxiosError {
  return axios.isAxiosError(error);
}
```

### Checklist TypeScript

- [ ] `strict: true` trong tsconfig.json
- [ ] Không dùng `any` — dùng `unknown` hoặc proper type
- [ ] Tất cả async functions có explicit `Promise<T>` return type
- [ ] Interfaces cho mọi data structure
- [ ] Zod `.parse()` cho mọi external data (API responses)
- [ ] Error handling dùng `axios.isAxiosError()` và `instanceof ZodError`

---

## 14. Complete Working Example

File `src/index.ts` hoàn chỉnh, có thể chạy được:

```typescript
#!/usr/bin/env node
/**
 * Example MCP Server
 * Connects Claude to the Example Service API.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import axios, { AxiosError } from "axios";
import express from "express";
import { z } from "zod";

// ── Constants ──────────────────────────────────────────────────────────────

const API_BASE_URL = "https://api.example.com/v1";
const CHARACTER_LIMIT = 25_000;
const REQUEST_TIMEOUT = 30_000;

// ── Enums & Schemas ────────────────────────────────────────────────────────

enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json",
}

const PaginationSchema = z.object({
  limit: z
    .number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("Max items (1–100)"),
  offset: z.number().int().min(0).default(0).describe("Pagination offset"),
});

const SearchUsersSchema = z
  .object({
    query: z.string().min(2).max(200).describe("Search string (name or email)"),
    ...PaginationSchema.shape,
    response_format: z
      .nativeEnum(ResponseFormat)
      .default(ResponseFormat.MARKDOWN),
  })
  .strict();

type SearchUsersInput = z.infer<typeof SearchUsersSchema>;

// ── Utilities ──────────────────────────────────────────────────────────────

async function makeRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  body?: unknown,
  params?: Record<string, unknown>,
): Promise<T> {
  const apiKey = process.env.EXAMPLE_API_KEY;
  if (!apiKey) throw new Error("EXAMPLE_API_KEY not configured");

  const response = await axios<T>({
    method,
    url: `${API_BASE_URL}/${endpoint}`,
    data: body,
    params,
    timeout: REQUEST_TIMEOUT,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
  });
  return response.data;
}

function handleError(error: unknown): string {
  if (axios.isAxiosError(error) && error.response) {
    const status = error.response.status;
    if (status === 401) return "Authentication failed. Check your API key.";
    if (status === 403) return "Permission denied.";
    if (status === 404) return "Resource not found.";
    if (status === 429) return "Rate limit exceeded. Please wait.";
    return `API error (HTTP ${status}).`;
  }
  if (error instanceof Error) return `Error: ${error.message}`;
  return "An unexpected error occurred.";
}

function truncateIfNeeded(text: string, limit: number): string {
  if (text.length <= limit) return text;
  return (
    text.slice(0, limit) +
    "\n\n[Response truncated. Use offset or filters to narrow results.]"
  );
}

// ── Server & Tools ─────────────────────────────────────────────────────────

const server = new McpServer({ name: "example-mcp-server", version: "1.0.0" });

server.registerTool(
  "example_search_users",
  {
    title: "Search Users",
    description: `Search users by name or email. Returns paginated results.
Read-only — does not create or modify users.

Args: query (string, min 2), limit (1–100), offset, response_format
Returns: { total, count, offset, users[{id,name,email,team?,active}], has_more, next_offset? }`,
    inputSchema: SearchUsersSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: SearchUsersInput) => {
    try {
      const data = await makeRequest<{ users: any[]; total: number }>(
        "users/search",
        "GET",
        undefined,
        { q: params.query, limit: params.limit, offset: params.offset },
      );

      const { users = [], total = 0 } = data;
      if (!users.length) {
        return {
          content: [
            { type: "text", text: `No users found for '${params.query}'` },
          ],
        };
      }

      const output = {
        total,
        count: users.length,
        offset: params.offset,
        users: users.map((u) => ({
          id: u.id,
          name: u.name,
          email: u.email,
          ...(u.team ? { team: u.team } : {}),
          active: u.active ?? true,
        })),
        has_more: total > params.offset + users.length,
        ...(total > params.offset + users.length
          ? { next_offset: params.offset + users.length }
          : {}),
      };

      const text =
        params.response_format === ResponseFormat.JSON
          ? JSON.stringify(output, null, 2)
          : [
              `# Users matching '${params.query}'`,
              `Found ${total} (showing ${users.length})`,
              "",
              ...output.users.flatMap((u) => [
                `## ${u.name} \`${u.id}\``,
                `- **Email**: ${u.email}`,
                ...(u.team ? [`- **Team**: ${u.team}`] : []),
                `- **Status**: ${u.active ? "Active" : "Inactive"}`,
                "",
              ]),
            ].join("\n");

      return {
        content: [
          { type: "text", text: truncateIfNeeded(text, CHARACTER_LIMIT) },
        ],
        structuredContent: output,
      };
    } catch (error) {
      console.error("[example_search_users]", error);
      return { content: [{ type: "text", text: handleError(error) }] };
    }
  },
);

// ── Entry Point ────────────────────────────────────────────────────────────

function validateEnv(): void {
  if (!process.env.EXAMPLE_API_KEY) {
    console.error("ERROR: EXAMPLE_API_KEY environment variable is required");
    process.exit(1);
  }
}

async function runStdio(): Promise<void> {
  validateEnv();
  await server.connect(new StdioServerTransport());
  console.error("MCP server running via stdio");
}

async function runHTTP(): Promise<void> {
  validateEnv();
  const app = express();
  const port = parseInt(process.env.PORT ?? "3000", 10);
  app.use(express.json());

  app.post("/mcp", async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });
    res.on("close", () => transport.close());
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  });

  app.listen(port, "127.0.0.1", () =>
    console.error(`MCP server at http://localhost:${port}/mcp`),
  );
}

const mode = process.env.TRANSPORT ?? "stdio";
(mode === "http" ? runHTTP : runStdio)().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
```

---

## 15. Quality Checklist

### 🏗️ Thiết kế

- [ ] Tool names theo format `{service}_{action}_{resource}`, snake_case
- [ ] Tools có service prefix — không conflict với MCP server khác
- [ ] Mỗi tool atomic — làm đúng một việc
- [ ] Descriptions đủ để AI hiểu khi nào dùng và dùng như thế nào
- [ ] Annotations đúng (readOnly, destructive, idempotent, openWorld)

### 💻 Implementation

- [ ] Dùng `registerTool` — không dùng deprecated `server.tool()`
- [ ] Mọi tool có đủ: `title`, `description`, `inputSchema`, `annotations`
- [ ] Zod schemas với `.strict()` và error messages có nghĩa
- [ ] `structuredContent` được trả về cùng với text content
- [ ] Pagination trả về đủ: `total`, `count`, `offset`, `has_more`, `next_offset?`
- [ ] Response lớn được truncate với thông báo rõ ràng
- [ ] Common logic được extract — không copy-paste giữa các tools

### 🔒 Bảo mật & Reliability

- [ ] API keys từ env variables — không hardcode
- [ ] `validateEnv()` chạy trước khi server start
- [ ] Mọi external data được validate bằng `ZodSchema.parse()`
- [ ] Error handler tập trung — không expose internal details
- [ ] stdio server logging ra `stderr`, không phải `stdout`
- [ ] HTTP server bind vào `127.0.0.1` (không phải `0.0.0.0`) khi chạy local

### 🔷 TypeScript

- [ ] `strict: true` trong tsconfig.json
- [ ] Không có `any` — dùng `unknown` hoặc proper types
- [ ] Tất cả async functions có `Promise<T>` return type tường minh
- [ ] Error type guards: `axios.isAxiosError()`, `instanceof ZodError`
- [ ] Types derive từ Zod schemas: `z.infer<typeof Schema>`

### ⚙️ Project & Build

- [ ] Server name: `{service}-mcp-server`
- [ ] `package.json`: `"type": "module"`, `"main": "dist/index.js"`, Node `>=18`
- [ ] `npm run build` chạy thành công, không errors
- [ ] `dist/index.js` tồn tại và executable
- [ ] `node dist/index.js` khởi động không lỗi

---

## Tham chiếu

- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Zod Documentation](https://zod.dev)
- [Axios Documentation](https://axios-http.com)
- [MCP Best Practices](./MCP_BEST_PRACTICES.md) ← general conventions
