# Python MCP Server Implementation: Elite 2026 Standard

> [!NOTE]
> This guide defines the professional implementation standard for MCP Servers using the Python SDK and **FastMCP** framework (v2.x). All production servers must adhere to these patterns to ensure maximum reliability and agentic alignment.

## 📖 Architecture Overview

Python MCP development centers on **FastMCP**, a high-level framework that abstracts the underlying protocol details while providing deep integration with the Python type system and Pydantic validation.

### Core Stack
- **Framework**: FastMCP (MCP Python SDK 2.x+)
- **Validation**: Pydantic v2
- **Networking**: HTTPX (Async)
- **Serialization**: UTF-8 / JSON 2026

---

## 🏗️ Elite Server Initialization

Experience shows that a well-structured server entry point is critical for maintainability and discovery.

```python
import httpx
import logging
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict

# [Elite Convention] Server naming: {service}_mcp
mcp = FastMCP(
    "nexus_bridge_mcp",
    title="Nexus Bridge: Universal API Adapter",
    description="Professional enterprise connector for multi-SaaS orchestration."
)

# Standardized logging to stderr to prevent stdio protocol corruption
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp.nexus_bridge")
```

---

## ⚡ Agentic-First Tool Design

In 2026, tools are designed for **Autonomous Agents**, not just humans. The `description` field is the primary mechanism for **Agentic Context Engineering (ACE)**.

### Tool Pattern: Context-Aware Reasoning
```python
class SearchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    query: str = Field(..., description="High-intent search query. Support filtering syntax (e.g. 'type:bug status:open')")
    limit: int = Field(default=20, ge=1, le=100)
    response_format: str = Field(default="markdown", description="Output format: 'markdown' for human-like summary, 'json' for raw data.")

@mcp.tool(
    name="nexus_search_resources",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
async def search_resources(params: SearchInput, ctx: Context) -> str:
    """
    [Elite ACE] Strategically search through connected Nexus nodes.
    
    Strategy: 
    1. Use this tool when the user asks for cross-service information.
    2. If multiple services match, priority goes to 'internal_wiki' then 'slack_archive'.
    3. Documentation: https://docs.nexus-bridge.com/search
    """
    await ctx.info(f"Initiating search for: {params.query}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Implementation logic here
            result = {"status": "success", "data": []} # Mock
            
            if params.response_format == "markdown":
                return f"### Search Results for '{params.query}'\n- Found {len(result['data'])} items."
            return str(result)
            
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Error: Failed to execute search. {str(e)}"
```

---

## 🛠️ Advanced Capability Patterns

### 1. Resource Templates
Use resources for semi-static data that agents need to browse or inspect.

```python
@mcp.resource("nexus://logs/{service}/{date}.log")
async def get_service_logs(service: str, date: str) -> str:
    """Provides direct access to historical service logs."""
    # Implementation path logic
    return f"Log contents for {service} on {date}..."
```

### 2. Lifespan & State Management
Properly manage API clients and database connections.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def server_lifespan(server: FastMCP):
    # Setup: Initialize shared HTTPX client
    client = httpx.AsyncClient()
    try:
        yield {"http_client": client}
    finally:
        # Teardown: Close all connections
        await client.aclose()

mcp = FastMCP("stateful_mcp", lifespan=server_lifespan)
```

---

## 🇻🇳 Vietnam-Specific Implementation Notes

When building for the Vietnamese market:
1. **Unicode Integrity**: Ensure all strings are handled as UTF-8. FastMCP handles this by default, but external API calls must explicitly set `headers={"Accept-Charset": "utf-8"}` if using legacy endpoints.
2. **Localization Tools**: If your MCP server interacts with internal systems (ERP/CRM), provide tools to convert `vi_VN` currency/date formats to standard ISO for the model, or vice-versa for the response.

---

## ✅ Elite Quality Checklist

- [ ] **Naming**: Server name follows `{service}_mcp` format.
- [ ] **Safety**: Destructive operations use `destructiveHint` and include confirmation logic.
- [ ] **Validation**: Pydantic v2 schemas are strictly typed with clear `Field` descriptions.
- [ ] **ACE**: Tool docstrings provide strategic advice (When/When Not to use).
- [ ] **Logging**: All internal logs go to `stderr`. Never print to `stdout`.
- [ ] **Async**: All I/O operations utilize `async/await` and `httpx.AsyncClient`.
- [ ] **Errors**: Error messages are helpful and suggest specific recovery steps for the Agent.

---

## 🚀 Execution Standard
To run the server in the Elite 2026 environment:

```bash
# Standard stdio execution
python -m mcp_server.main

# Enterprise Streamable HTTP (for high-availability)
python -m mcp_server.main --transport streamable_http --port 8000
```

---
*Standard: MCP-ELITE-PYTHON-2026.04*
