#!/usr/bin/env python3
"""
MCP Server Evaluation Harness

This script evaluates MCP servers by running test questions (from XML) against them
using Claude (Anthropic API). It measures accuracy, tool usage, and provides feedback.

Usage examples:
    # Evaluate local stdio server
    python evaluation.py -t stdio -c python -a my_server.py eval.xml

    # Evaluate remote SSE server
    python evaluation.py -t sse -u https://example.com/mcp -H "Authorization: Bearer token" eval.xml

    # Resume from checkpoint
    python evaluation.py --resume eval.xml --checkpoint results.json
"""

import argparse
import asyncio
import json
import logging
import re
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from anthropic import Anthropic, APIError, APITimeoutError
from tqdm import tqdm

# Import your connection module (adjust if needed)
from connections import create_connection, MCPConnection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = """You are an AI assistant with access to tools.

When given a task, you MUST:
1. Use the available tools to complete the task
2. Provide summary of each step in your approach, wrapped in <summary> tags
3. Provide feedback on the tools provided, wrapped in <feedback> tags
4. Provide your final response, wrapped in <response> tags

Summary Requirements:
- Explain steps taken, tools used (order and why), inputs/outputs, and how you arrived at the response.

Feedback Requirements:
- Comment on tool names: clear? descriptive?
- Comment on input parameters: well-documented? required vs optional clear?
- Comment on descriptions: accurate?
- Comment on errors encountered (too many tokens, failures).
- Suggest specific improvements with reasons.

Response Requirements:
- Concise, directly address the question.
- Always wrap in <response> tags.
- If cannot solve, return <response>NOT_FOUND</response>.
- For numeric responses: just the number.
- For IDs: just the ID.
- For names/text: exact text requested.
"""


def parse_evaluation_file(file_path: Path) -> List[Dict[str, str]]:
    """Parse XML evaluation file containing <qa_pair> elements.

    Args:
        file_path: Path to XML file.

    Returns:
        List of dicts with keys 'question' and 'answer'.

    Raises:
        FileNotFoundError: If file does not exist.
        ET.ParseError: If XML is malformed.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        evaluations = []

        for qa_pair in root.findall(".//qa_pair"):
            question_elem = qa_pair.find("question")
            answer_elem = qa_pair.find("answer")

            if question_elem is not None and answer_elem is not None:
                evaluations.append({
                    "question": (question_elem.text or "").strip(),
                    "answer": (answer_elem.text or "").strip(),
                })

        logger.info(f"Loaded {len(evaluations)} evaluation pairs from {file_path}")
        return evaluations
    except ET.ParseError as e:
        logger.error(f"XML parsing error: {e}")
        raise


def extract_xml_content(text: str, tag: str) -> Optional[str]:
    """Extract content from the last occurrence of XML tag.

    Args:
        text: The full text containing XML tags.
        tag: Tag name (e.g., 'response').

    Returns:
        Extracted content or None if not found.
    """
    pattern = rf"<{tag}>(.*?)</{tag}>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[-1].strip() if matches else None


async def call_tool_with_retry(
    connection: MCPConnection,
    tool_name: str,
    arguments: Dict[str, Any],
    max_retries: int = 2,
    retry_delay: float = 1.0,
) -> Any:
    """Call an MCP tool with retry logic.

    Args:
        connection: MCP connection instance.
        tool_name: Name of the tool.
        arguments: Tool arguments.
        max_retries: Maximum number of retries.
        retry_delay: Delay between retries in seconds.

    Returns:
        Tool result content.

    Raises:
        Exception: After all retries fail.
    """
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return await connection.call_tool(tool_name, arguments)
        except Exception as e:
            last_exception = e
            logger.warning(f"Tool {tool_name} failed (attempt {attempt+1}/{max_retries+1}): {e}")
            if attempt < max_retries:
                await asyncio.sleep(retry_delay)
    raise last_exception


async def agent_loop(
    client: Anthropic,
    model: str,
    question: str,
    tools: List[Dict[str, Any]],
    connection: MCPConnection,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    max_iterations: int = 20,
) -> Tuple[Optional[str], Dict[str, Any]]:
    """Run the agent loop to answer a question using available MCP tools.

    Args:
        client: Anthropic client.
        model: Model name (e.g., "claude-3-7-sonnet-20250219").
        question: The user question.
        tools: List of tool definitions.
        connection: MCP connection for calling tools.
        system_prompt: System prompt for Claude.
        max_iterations: Maximum number of tool-use iterations.

    Returns:
        Tuple of (final response text, tool_metrics dictionary).
    """
    messages = [{"role": "user", "content": question}]
    tool_metrics = {}
    iteration = 0

    response = await asyncio.to_thread(
        client.messages.create,
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=messages,
        tools=tools,
    )
    messages.append({"role": "assistant", "content": response.content})

    while response.stop_reason == "tool_use" and iteration < max_iterations:
        iteration += 1
        # Find the tool_use block
        tool_use = next((block for block in response.content if block.type == "tool_use"), None)
        if not tool_use:
            break

        tool_name = tool_use.name
        tool_input = tool_use.input

        start_ts = time.time()
        try:
            tool_result = await call_tool_with_retry(connection, tool_name, tool_input)
            # Convert result to string for Claude
            tool_response = json.dumps(tool_result) if isinstance(tool_result, (dict, list)) else str(tool_result)
        except Exception as e:
            tool_response = f"Error executing tool {tool_name}: {str(e)}\n{traceback.format_exc()}"
            logger.error(f"Tool {tool_name} failed after retries: {e}")
        duration = time.time() - start_ts

        # Update metrics
        if tool_name not in tool_metrics:
            tool_metrics[tool_name] = {"count": 0, "durations": []}
        tool_metrics[tool_name]["count"] += 1
        tool_metrics[tool_name]["durations"].append(duration)

        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_response,
            }]
        })

        response = await asyncio.to_thread(
            client.messages.create,
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            tools=tools,
        )
        messages.append({"role": "assistant", "content": response.content})

    if iteration >= max_iterations:
        logger.warning(f"Reached max iterations ({max_iterations}) for question: {question[:100]}")

    # Extract final response from last assistant message
    final_text = None
    for block in reversed(response.content):
        if hasattr(block, "text") and block.text:
            final_text = block.text
            break

    return final_text, tool_metrics


async def evaluate_single_task(
    client: Anthropic,
    model: str,
    qa_pair: Dict[str, str],
    tools: List[Dict[str, Any]],
    connection: MCPConnection,
    task_index: int,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    task_timeout: float = 120.0,
) -> Dict[str, Any]:
    """Evaluate a single QA pair.

    Args:
        client: Anthropic client.
        model: Model name.
        qa_pair: Dict with 'question' and 'answer'.
        tools: List of tool definitions.
        connection: MCP connection.
        task_index: Index (for logging).
        system_prompt: System prompt.
        task_timeout: Timeout in seconds for the entire task.

    Returns:
        Dictionary with evaluation results.
    """
    start_time = time.time()
    logger.info(f"Task {task_index+1}: {qa_pair['question'][:100]}...")

    try:
        response, tool_metrics = await asyncio.wait_for(
            agent_loop(client, model, qa_pair["question"], tools, connection, system_prompt),
            timeout=task_timeout,
        )
    except asyncio.TimeoutError:
        logger.error(f"Task {task_index+1} timed out after {task_timeout}s")
        response = "<response>TIMEOUT</response>"
        tool_metrics = {}
    except Exception as e:
        logger.error(f"Task {task_index+1} failed: {e}")
        response = f"<response>ERROR: {str(e)}</response>"
        tool_metrics = {}

    actual_answer = extract_xml_content(response or "", "response")
    summary = extract_xml_content(response or "", "summary")
    feedback = extract_xml_content(response or "", "feedback")

    duration = time.time() - start_time
    is_correct = (actual_answer == qa_pair["answer"]) if actual_answer else False

    return {
        "question": qa_pair["question"],
        "expected": qa_pair["answer"],
        "actual": actual_answer,
        "score": 1 if is_correct else 0,
        "total_duration": duration,
        "tool_calls": tool_metrics,
        "num_tool_calls": sum(len(m["durations"]) for m in tool_metrics.values()),
        "summary": summary or "N/A",
        "feedback": feedback or "N/A",
    }


def save_checkpoint(results: List[Dict[str, Any]], checkpoint_path: Path) -> None:
    """Save intermediate results to a checkpoint file."""
    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info(f"Checkpoint saved to {checkpoint_path}")


def load_checkpoint(checkpoint_path: Path) -> List[Dict[str, Any]]:
    """Load previous results from a checkpoint file."""
    if not checkpoint_path.exists():
        return []
    with open(checkpoint_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def run_evaluation(
    eval_path: Path,
    connection: MCPConnection,
    model: str = "claude-3-7-sonnet-20250219",
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    resume: Optional[Path] = None,
    task_timeout: float = 120.0,
) -> str:
    """Run full evaluation with progress bar and optional resume.

    Args:
        eval_path: Path to XML evaluation file.
        connection: MCP connection.
        model: Claude model name.
        system_prompt: System prompt for Claude.
        resume: Optional checkpoint file to resume from.
        task_timeout: Timeout per task.

    Returns:
        Markdown report string.
    """
    logger.info("Starting evaluation...")
    client = Anthropic()

    # Load tools from MCP server
    tools = await connection.list_tools()
    logger.info(f"Loaded {len(tools)} tools from MCP server")

    # Load QA pairs
    qa_pairs = parse_evaluation_file(eval_path)
    total = len(qa_pairs)

    # Load previous results if resuming
    previous_results = load_checkpoint(resume) if resume else []
    start_index = len(previous_results)
    results = previous_results.copy()

    if start_index > 0:
        logger.info(f"Resuming from checkpoint: {start_index}/{total} tasks already completed")

    # Run remaining tasks with progress bar
    with tqdm(total=total, initial=start_index, desc="Evaluating", unit="task") as pbar:
        for i in range(start_index, total):
            result = await evaluate_single_task(
                client, model, qa_pairs[i], tools, connection, i, system_prompt, task_timeout
            )
            results.append(result)
            pbar.update(1)

            # Save checkpoint every 5 tasks
            if resume and (i + 1) % 5 == 0:
                save_checkpoint(results, resume)

    if resume:
        save_checkpoint(results, resume)  # final save

    # Calculate statistics
    correct = sum(r["score"] for r in results)
    accuracy = (correct / total) * 100 if total else 0
    avg_duration = sum(r["total_duration"] for r in results) / total if total else 0
    avg_tool_calls = sum(r["num_tool_calls"] for r in results) / total if total else 0
    total_tool_calls = sum(r["num_tool_calls"] for r in results)

    # Build report
    report_lines = [
        "# Evaluation Report\n",
        "## Summary\n",
        f"- **Accuracy**: {correct}/{total} ({accuracy:.1f}%)",
        f"- **Average Task Duration**: {avg_duration:.2f}s",
        f"- **Average Tool Calls per Task**: {avg_tool_calls:.2f}",
        f"- **Total Tool Calls**: {total_tool_calls}\n",
        "---\n",
    ]

    for i, (qa, res) in enumerate(zip(qa_pairs, results)):
        report_lines.extend([
            f"### Task {i+1}\n",
            f"**Question**: {qa['question']}",
            f"**Ground Truth Answer**: `{qa['answer']}`",
            f"**Actual Answer**: `{res['actual'] or 'N/A'}`",
            f"**Correct**: {'✅' if res['score'] else '❌'}",
            f"**Duration**: {res['total_duration']:.2f}s",
            f"**Tool Calls**:\n```json\n{json.dumps(res['tool_calls'], indent=2)}\n```",
            f"**Summary**\n{res['summary']}",
            f"**Feedback**\n{res['feedback']}",
            "---\n",
        ])

    return "\n".join(report_lines)


def parse_headers(header_list: Optional[List[str]]) -> Dict[str, str]:
    """Parse header strings 'Key: Value' into a dictionary."""
    headers = {}
    if not header_list:
        return headers
    for header in header_list:
        if ":" in header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        else:
            logger.warning(f"Ignoring malformed header: {header}")
    return headers


def parse_env_vars(env_list: Optional[List[str]]) -> Dict[str, str]:
    """Parse environment variable strings 'KEY=VALUE' into a dictionary."""
    env = {}
    if not env_list:
        return env
    for item in env_list:
        if "=" in item:
            key, value = item.split("=", 1)
            env[key.strip()] = value.strip()
        else:
            logger.warning(f"Ignoring malformed env var: {item}")
    return env


async def main():
    parser = argparse.ArgumentParser(
        description="Evaluate MCP servers using test questions and Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("eval_file", type=Path, help="Path to evaluation XML file")
    parser.add_argument("-t", "--transport", choices=["stdio", "sse", "http"], default="stdio",
                        help="Transport type (default: stdio)")
    parser.add_argument("-m", "--model", default="claude-3-7-sonnet-20250219",
                        help="Claude model (default: claude-3-7-sonnet-20250219)")
    parser.add_argument("--timeout", type=float, default=120.0,
                        help="Timeout per task in seconds (default: 120)")
    parser.add_argument("--resume", type=Path, help="Checkpoint file to resume from")
    parser.add_argument("-o", "--output", type=Path, help="Output file for report (default: stdout)")

    # Transport-specific groups
    stdio_group = parser.add_argument_group("stdio options")
    stdio_group.add_argument("-c", "--command", help="Command to run MCP server (stdio only)")
    stdio_group.add_argument("-a", "--args", nargs="+", help="Arguments for the command (stdio only)")
    stdio_group.add_argument("-e", "--env", nargs="+", help="Environment variables in KEY=VALUE format (stdio only)")

    remote_group = parser.add_argument_group("sse/http options")
    remote_group.add_argument("-u", "--url", help="MCP server URL (sse/http only)")
    remote_group.add_argument("-H", "--header", nargs="+", dest="headers",
                              help="HTTP headers in 'Key: Value' format (sse/http only)")

    args = parser.parse_args()

    # Validate eval file
    if not args.eval_file.exists():
        logger.error(f"Evaluation file not found: {args.eval_file}")
        sys.exit(1)

    # Prepare connection parameters
    headers = parse_headers(args.headers) if args.headers else None
    env_vars = parse_env_vars(args.env) if args.env else None

    try:
        connection = create_connection(
            transport=args.transport,
            command=args.command,
            args=args.args,
            env=env_vars,
            url=args.url,
            headers=headers,
        )
    except ValueError as e:
        logger.error(f"Connection creation failed: {e}")
        sys.exit(1)

    logger.info(f"Connecting to MCP server via {args.transport}...")
    async with connection:
        logger.info("Connected successfully")
        report = await run_evaluation(
            eval_path=args.eval_file,
            connection=connection,
            model=args.model,
            resume=args.resume,
            task_timeout=args.timeout,
        )

        if args.output:
            args.output.write_text(report, encoding="utf-8")
            logger.info(f"Report saved to {args.output}")
        else:
            print("\n" + report)


if __name__ == "__main__":
    asyncio.run(main())