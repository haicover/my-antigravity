#!/usr/bin/env python3
"""
Lightweight connection handling for MCP servers.

This module provides async context managers for connecting to MCP servers
via three transport protocols: stdio, SSE, and Streamable HTTP.

Example usage:
    async with create_connection("stdio", command="python", args=["server.py"]) as conn:
        tools = await conn.list_tools()
        result = await conn.call_tool("my_tool", {"arg": "value"})
"""

from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client


class MCPConnection(ABC):
    """Base class for MCP server connections."""

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self._stack: Optional[AsyncExitStack] = None

    @abstractmethod
    def _create_context(self):
        """Create the connection context based on connection type."""

    async def __aenter__(self):
        """Initialize MCP server connection."""
        self._stack = AsyncExitStack()
        await self._stack.__aenter__()

        try:
            ctx = self._create_context()
            result = await self._stack.enter_async_context(ctx)

            # Different transports return different tuple lengths
            if len(result) == 2:
                read, write = result
            elif len(result) == 3:
                read, write, _ = result
            else:
                raise ValueError(f"Unexpected context result: {result}")

            session_ctx = ClientSession(read, write)
            self.session = await self._stack.enter_async_context(session_ctx)
            await self.session.initialize()
            return self
        except BaseException:
            await self._stack.__aexit__(None, None, None)
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up MCP server connection resources."""
        if self._stack:
            await self._stack.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None
        self._stack = None

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Retrieve available tools from the MCP server.

        Returns:
            List of dicts with keys: name, description, input_schema.
        """
        response = await self.session.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the MCP server with provided arguments.

        Args:
            tool_name: Name of the tool to call.
            arguments: Dictionary of arguments matching the tool's input schema.

        Returns:
            The content returned by the tool (typically a list of content objects).
        """
        result = await self.session.call_tool(tool_name, arguments=arguments)
        return result.content


class MCPConnectionStdio(MCPConnection):
    """MCP connection using standard input/output (local subprocess)."""

    def __init__(
        self,
        command: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
    ):
        super().__init__()
        self.command = command
        self.args = args or []
        self.env = env

    def _create_context(self):
        return stdio_client(
            StdioServerParameters(command=self.command, args=self.args, env=self.env)
        )


class MCPConnectionSSE(MCPConnection):
    """MCP connection using Server-Sent Events (remote)."""

    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__()
        self.url = url
        self.headers = headers or {}

    def _create_context(self):
        return sse_client(url=self.url, headers=self.headers)


class MCPConnectionHTTP(MCPConnection):
    """MCP connection using Streamable HTTP (remote)."""

    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__()
        self.url = url
        self.headers = headers or {}

    def _create_context(self):
        return streamablehttp_client(url=self.url, headers=self.headers)


def create_connection(
    transport: str,
    command: Optional[str] = None,
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None,
    url: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
) -> MCPConnection:
    """Factory function to create the appropriate MCP connection.

    Args:
        transport: Connection type ("stdio", "sse", or "http" / "streamable_http").
        command: Command to run (required for stdio).
        args: Command arguments (optional, stdio only).
        env: Environment variables (optional, stdio only).
        url: Server URL (required for sse and http).
        headers: HTTP headers (optional, sse/http only).

    Returns:
        An instance of MCPConnectionStdio, MCPConnectionSSE, or MCPConnectionHTTP.

    Raises:
        ValueError: If required parameters are missing or transport is unknown.
    """
    transport = transport.lower()

    if transport == "stdio":
        if not command:
            raise ValueError("Command is required for stdio transport")
        return MCPConnectionStdio(command=command, args=args, env=env)

    elif transport == "sse":
        if not url:
            raise ValueError("URL is required for sse transport")
        return MCPConnectionSSE(url=url, headers=headers)

    elif transport in ("http", "streamable_http", "streamable-http"):
        if not url:
            raise ValueError("URL is required for http transport")
        return MCPConnectionHTTP(url=url, headers=headers)

    else:
        raise ValueError(
            f"Unsupported transport type: {transport}. Use 'stdio', 'sse', or 'http'"
        )