# Assignment 2 Reflection

**Name:** Diego Carpenter 
**Option:** Option B 
**Date:** July 2, 2026

---

## Tool Design Decisions

### Tools Implemented
1. list_tasks: Lists tasks from a Google Tasks list, defaulting to the user's @default list and to incomplete tasks only, with an option to include completed ones.
2. create_task: Adds a new task with a title and optional notes/due date, returning the created task so the agent can confirm it back to the user.
3. complete_task: Marks a task as completed by ID, used when the user says they finished something.
4. update_task: Modifies an existing task's title, notes, or due date.
5. delete_task: Permanently removes a task by ID.

### Why These Tools?
Together these five cover the full lifecycle of a task — create, read, update, complete, delete — which mirrors how someone actually manages a to-do list. I used Google Tasks' @default tasklist shortcut so the agent doesn't need a separate "look up my tasklist ID" step before every operation, which keeps the common path simple while still allowing a specific tasklist_id to be passed if needed.

### Description Strategy
I wrote eaach tool to state what it does in the first line, followed by an return breakdown so the LLM has a clear signal for both when to call it and what parameters it expects. I leaned on action-verb names so the model can map user intent without trouble. The system instruction also spells out specific behavioral rules. look up a task's ID via list_tasks first if the user refers to a task by name, and always confirm before deleting — to reduce the chance of the agent guessing at IDs or taking destructive actions unprompted.
---

## Challenges Encountered

Challenge 1: Session not found in main.py's interactive CLI


Problem: Running python main.py --interactive immediately threw google.adk.errors.session_not_found_error.SessionNotFoundError on the first query. The provided main.py was written assuming InMemoryRunner would auto-create a session on first use, but the installed google-adk version (2.3.0) requires the session to be explicitly created first.

Solution: Added an explicit asyncio.run(runner.session_service.create_session(...)) call in main() right after the runner is constructed, before entering interactive/query mode. This is a version-mismatch issue between the starter scaffolding and the currently installed ADK release, not a bug in the tool implementations themselves.


Challenge 2: Gemini API key rejected with 401 ACCESS_TOKEN_TYPE_UNSUPPORTED

Problem: After getting past the session issue, every query failed at the model call with ACCESS_TOKEN_TYPE_UNSUPPORTED. This turned out to be a live, Google-side bug: Google AI Studio recently began issuing a new "auth key" format in place of the older Standard keys, and these new keys are currently being rejected by the Gemini API for many users. I confirmed this by calling the key directly through Google's own google-genai SDK, completely outside of ADK, and got the identical error. I also tried generating an old-style Standard key directly through Cloud Console as a workaround, but Google has since blocked restricting Standard keys to the Gemini API specifically, closing off that path too.

Solution: Switching authentication to another AI, and swapping the model to OpenAI, using my already-funded OpenAI account.
---

## Error Handling Approach

Every tool wraps its Google API call in a try/except block and returns a consistent message. On error, the message gives a plain-language description, so the agent can relay something a user can act on. Create_task and update_task also validate inputs before making an API call at all, this avoids a wasted round trip for an obviously invalid request. The system instruction tells the agent to explain tool errors in plain language and suggest a next step, rather than surfacing the raw error to the user. 
---

## Ideas for Improvement

If you had more time, what would you add or change?

1. Add a find_task_by_title helper so the agent doesn't have to fetch the full list and scan it client-side every time the user refers to a task by name instead of ID.
2. Support multiple task lists more explicitly — e.g., a list_tasklists tool — rather than defaulting everything to @default.
3. Add retry/backoff handling for transient Google API errors (rate limits, timeouts) instead of surfacing them as an immediate failure.

---

## Key Learnings

I learned a lot, first off, the tool implementation itself was the most straightforward part of this assignment. Wrapping a REST API with straight forward Python functions with clear docstrings is a pattern that translates directly to how we have been taught. The harder, more instructive part was everything else. Cersion drift between the starter scaffolding and the currently installed ADK release, and a platform-level failure that had nothing to do with my code at all. 

That second issue was a good lesson in debugging methodology. Isolating the problem by testing the API key against Google's SDK directly, outside of ADK, was what confirmed it wasn't something in my agent or tool code before spending more time chasing the wrong thing. It also reinforced the value of checking what the grading process actually depends on: once I confirmed the autograder mocks the model call entirely, I could stop treating the live API issue as a blocker and instead treat the workarounds (OpenAI). 

More broadly, this assignment made clear that building an agent is a lot of work. All the surrounding issues (auth, sessions, environment/version compatibility) that has to hold together before the agent logic even gets a chance to run, is another step I didn't know about. 