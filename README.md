# JobHound agent workspace preview

This is an experimental installation channel for the existing JobHound app, starting with Meta Muse. It is not a separately authored app. The backend, web UI, matching rules and MCP tools are exported from the canonical JobHound source.

**Status: prepared for testing; operation inside Muse is unverified.** This release does not add Muse as JobHound's outbound AI provider.

## For Muse

Read [TEST_INSTRUCTIONS.md](TEST_INSTRUCTIONS.md), then [SKILL.md](SKILL.md). Use a fresh profile and report observed results. Do not modify the generated runtime to make a test pass; report the compatibility issue so it can be fixed in the canonical app.

Clone this repository using the normal GitHub URL. Python 3.11 or later is required.

Choose a durable location for third-party app data. Commands default to .jobhound in this clone; supply the same --home location before every command if your platform offers a better persistent path.

    python3 jobhound.py doctor
    python3 jobhound.py install
    python3 jobhound.py serve

Serve is a foreground process at http://127.0.0.1:4176. Keep it running using a supported workspace service facility; closing a terminal may stop it. Do not assume Muse's own background tasks guarantee third-party uptime. The installer verifies the release checksum, keeps test data separate from release code, and reuses a completed install on retry. It does not install browser binaries or transcription models automatically.

In another terminal:

    python3 jobhound.py status
    python3 jobhound.py tools
    python3 jobhound.py call list_monitors --arguments '{}'
    python3 jobhound.py call search_jobs --arguments '{}'

The tools command returns current input schemas and annotations. The call command uses the existing typed MCP contracts, not a generic HTTP or database interface. Human users use the same bundled web UI and backend. Call results use the canonical MCP envelope, including structuredContent and isError.

Doctor returns an optional stdio MCP registration specification. Use it only if the host has a supported registration mechanism. Otherwise use the focused JSON commands through a custom skill.

## Known limits to test

- Monitor creation currently has no backend retry deduplication. List first and reuse a resolved ID; do not blindly repeat create after an uncertain response.
- JobHound disables ambient proxies in its external clients. Muse's approved egress may require an explicit canonical transport adaptation; report blocked DNS, proxy or network calls instead of bypassing controls.
- A human's browser cannot reach this workspace by fetching its own localhost. Opening the app inside Muse needs a supported private service/artifact route.
- The app restricts iframe ancestors. Do not remove that protection or expose an unauthenticated tunnel to embed it.
- Native interview recording currently requires Windows; it does not capture a user's laptop audio from a Linux cloud VM.
- Credentials and local agent CLIs may be unavailable. Known ATS adapters and validated recipes can operate without an AI provider.
- The profile lives inside the selected agent workspace. It does not synchronize with an existing Windows installation.
- Schedules remain in JobHound; do not create an AI cron for each monitor.

## Ownership and updates

This repository's files are generated from the canonical app's integrations/agent-workspace. The release archive contains canonical runtime source and its prebuilt web UI, with per-file hashes. Personal data, local databases, credentials, caches and installed environments are excluded by the export allowlist.

Fixes belong in canonical JobHound and are exported as a new preview release. Existing profiles remain under the selected home/data directory. Neither installing nor starting this preview submits job applications.

See [TEST_INSTRUCTIONS.md](TEST_INSTRUCTIONS.md) for the acceptance gates and [test-results.example.json](test-results.example.json) for the report format.

