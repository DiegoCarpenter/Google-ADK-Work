## Grade: 99 / 100

**Assignment:** Google Workspace Assistant + GitHub MCP (ADK)  
**Attempt:** 1 of 2  ·  **Graded:** 2026-07-11  ·  Commit `af11c92`

> **Note: provided files were modified.** These instructor-provided files (not meant to be changed) differ from the originals: `workspace_assistant/main.py`. No automatic deduction was applied. If this was a necessary setup fix, no action is needed.

### Score breakdown
| Criterion | Max | Earned | Notes |
|-----------|-----|--------|-------|
| tool_design | 18 | 18 | Option B implemented with 5 plain-function tools (list/create/complete/update/delete_task), all with action-verb names, complete Args/Returns docstrings and typed parameters, collected into the tasks_tools list. (`workspace_assistant/tools/tasks_tools.py:175`) |
| agent_instructions | 14 | 14 | System instruction is clear and scoped: it maps each Tasks tool to user intent, requires confirming before deleting, tells the agent to look up IDs via list_tasks first, and forbids inventing IDs/repo names. (`workspace_assistant/agent.py:22`) |
| error_handling | 14 | 14 | Every tool wraps its API call in try/except and returns a consistent {status, message} dict; create_task and update_task also validate inputs (empty title, no-op update) before making a request. (`workspace_assistant/tools/tasks_tools.py:47`) |
| functionality | 14 | 14 | Statically correct: each tool authenticates via get_tasks_service() and calls the right Tasks API method with correct params - tasks().list (showCompleted/maxResults), insert, patch (complete/update), delete. (`workspace_assistant/tools/tasks_tools.py:29`) |
| code_quality | 10 | 9 | Readable, well-organized, well-documented code wired into an LlmAgent via create_agent(). Minor nit: a few stray whitespace-only lines in tasks_tools.py (lines 11, 14). (`workspace_assistant/agent.py:55`) |
| mcp_configured | 10 | 10 | McpToolset configured correctly for the GitHub MCP server over stdio (npx @modelcontextprotocol/server-github) and attached to the agent via tools=[*tasks_tools, github_toolset] in agent.py:65. (`workspace_assistant/tools/mcp_tools.py:50`) |
| github_queries | 15 | 15 | GitHub operations (list repos, list/create issues) are wired to route through the MCP toolset; the instruction guides tool selection and the toolset exposes the server's GitHub tools. Statically correct wiring. (`workspace_assistant/agent.py:38`) |
| mcp_error_handling | 5 | 5 | Missing GITHUB_PERSONAL_ACCESS_TOKEN raises a clear ValueError at toolset construction, and the instruction directs the agent to explain error-status results in plain language rather than showing raw traces. (`workspace_assistant/tools/mcp_tools.py:41`) |
| Integrity deduction | — | 0 | Provided files MODIFIED — flagged, no deduction (workspace_assistant/main.py) |
| **Total** | **100** | **99** | |

### What went well
- Complete task lifecycle coverage (create/read/update/complete/delete) with clean, action-verb tool names and thorough Args/Returns docstrings that give the LLM strong tool-selection signals.
- Consistent, user-friendly error handling: uniform {status, message} dicts plus proactive input validation in create_task/update_task to avoid wasted API round-trips.
- Safe agent instruction that requires confirmation before destructive deletes, looking up IDs via list_tasks, and never inventing IDs or repo names.
- GitHub MCP integration is correctly configured (direct stdio config plus an optional file-based config path) and cleanly attached to the agent.

### What to improve (actionable)
- Attempt the bonus: implement search_github_tools, set defer_loading=True on the McpToolset, and finish create_agent_with_tool_search() with the token/context comparison in the reflection.
- Add a find_task_by_title helper so the agent does not have to fetch and scan the full list every time a task is referenced by name (student already notes this).
- Tighten code hygiene by removing the stray whitespace-only lines in tasks_tools.py.
- Consider retry/backoff for transient Google API errors (rate limits, timeouts) rather than surfacing them as immediate failures.

### Automated checks
- ✅ All required files implemented
- ⚠️ Provided files MODIFIED — flagged, no deduction (workspace_assistant/main.py)
- ✅ 0/0 output artifacts committed
- ✅ Reflection 904 words

### Resubmission
You may resubmit **once**. Push fixes to this repo, then notify the instructor; we'll re-grade as **Attempt 2 (final)**. This is attempt 1 of 2.

---
*Graded automatically with Claude Code against the course rubric. Questions → contact the instructor.*


---
<sub>🔎 **Autograder record** — attempt 1 of 2 · graded at commit `af11c92` · delivered 2026-07-11T18:00:59Z. Commits pushed to `main` after this timestamp are treated as a resubmission.</sub>
