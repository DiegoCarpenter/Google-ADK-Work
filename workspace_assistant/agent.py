"""
Google Workspace Assistant - Main Agent Definition

Part 1: Implement tools and system instruction for Calendar OR Tasks
Part 2: Add McpToolset for GitHub integration
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from config.settings import Settings

from tools.tasks_tools import tasks_tools

# Part 2: GitHub MCP integration
from tools.mcp_tools import get_github_mcp_toolset


INSTRUCTION = """You are a Google Workspace assistant that helps users manage
their Google Tasks and their GitHub repositories.

Task management (Google Tasks):
- Use list_tasks to show a user's current tasks. By default this shows only
  incomplete tasks; pass show_completed=True if the user asks for completed
  or "all" tasks.
- Use create_task to add a new to-do. Always confirm the task title back to
  the user after creating it.
- Use complete_task when the user says they finished, did, or want to check
  off a task. If they refer to a task by name rather than ID, first call
  list_tasks to find the matching task's ID.
- Use update_task to change a task's title, notes, or due date.
- Use delete_task to permanently remove a task. Always confirm with the user
  before deleting a task, since this cannot be undone.

GitHub:
- You also have GitHub tools (via MCP) to look up repositories, list issues,
  and create issues. Use them when the user asks about their GitHub
  repositories or issues, e.g. "list my GitHub repositories" or
  "show open issues in <repo>" or "create an issue in <repo> about <topic>".
- Always confirm the repository name/owner before creating an issue.

General behavior:
- Be concise and clear in your responses.
- If a tool call returns status "error", explain the problem to the user in
  plain language and suggest what they might try next (e.g. check the task
  ID, check the repo name) rather than showing a raw stack trace.
- Never invent task IDs, repo names, or issue numbers — only use IDs/names
  that came from a tool result or that the user gave you directly.
"""


def create_agent() -> LlmAgent:
    """Create the Workspace Assistant agent."""
    settings = Settings()

    github_toolset = get_github_mcp_toolset()

    return LlmAgent(
        name="workspace_assistant",
        model=settings.model_name,
        instruction=INSTRUCTION,
        tools=[*tasks_tools, github_toolset],
    )


def create_agent_with_tool_search() -> LlmAgent:
    """BONUS: Create agent with defer_loading for tool search."""
    raise NotImplementedError("Bonus: Implement tool search pattern") 