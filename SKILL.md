---
name: jobhound-workspace
description: Inspect and operate the experimental JobHound installation through shared typed tools.
---

# JobHound workspace

Read TEST_INSTRUCTIONS.md before this preview's first use. Read status, tools and the relevant records before writes. Use jobhound.py with the same home and port on every call.

Use tools to discover typed MCP schemas. Invoke only registered JobHound operations through call. The web UI and JSON command interface share the same backend. Preserve OR within criteria categories and AND across populated categories.

Build, scrape and repair return run IDs; poll get_run_status until terminal. Never describe queued work as completed. Reuse request IDs on retry when the discovered schema supports them. Monitor creation currently has no backend retry deduplication: list first, create only if absent, and reuse its returned ID. After an uncertain create response, inspect state instead of repeating create. Read returned partial/failed states before deciding the next action; do not recreate a monitor to repair an existing one.

Use JobHound manual, interval, daily and weekly schedules. The host may manage the service lifecycle using supported facilities; it must not duplicate monitor schedules with agent browsing jobs.

Initial testing uses a fresh profile and one public Anthropic careers monitor, as authorized in TEST_INSTRUCTIONS.md. Do not transfer private documents or an existing user's profile, configure paid AI, expose the app publicly, or disable security to pass tests.

Choose a supported private host UI mount. If unavailable, report human-interface parity as blocked rather than claiming the integration is complete. Report Linux native audio capture as unsupported.

If stdio MCP registration is supported, use doctor to obtain its exact command, arguments, working directory and loopback URL. Otherwise use the local JSON CLI. Model-level MCP support is not evidence of consumer-product registration.

