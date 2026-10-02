---
name: jobhound-workspace
description: Help a user find jobs with JobHound in an agent workspace, introduce its features and optional onboarding, search the global board and existing presets first, and present results in a host artifact when the bundled UI cannot be shown.
---

# JobHound in an agent workspace

Read README.md for installation and transport. Use WORKFLOW.md for onboarding and job search; use ARTIFACT_GUIDE.md when the human needs a visible board. TEST_INSTRUCTIONS.md describes preview acceptance checks, not a requirement to create a monitor for every user.

Introduce JobHound as a personal job-search assistant with a shared global job board, company presets and monitors, saved roles and application tracking, resume/letter support, interview preparation and dashboard summaries. Explain which features are available in this host. Offer a short onboarding, allow skipping it, and provide useful results promptly.

Search the global board first. Inspect its status and collections, then use search_public_jobs with the discovered schema. Prefer its existing company/collection coverage. If the user wants ongoing local monitoring, look for a preset recipe before building a new scraper. Creating a scraper is a fallback for a missing source, not the installation demo or default first step.

Use jobhound.py with the same home and port throughout. Discover typed tools; inspect state before writes. Invoke registered contracts only. The web UI and agent interface share backend behavior. Private monitor criteria use OR within categories and AND across populated categories; public-board filters use their own BoardQuery contract. Do not translate preferences into invented query fields or a second matching implementation.

Build, scrape and repair return run IDs; poll get_run_status until terminal. Queued work is not completed. Use request IDs only when the schema supports them. Monitor creation has no request ID or backend retry deduplication: list first, reuse its ID, and inspect after an uncertain response instead of repeating create. Repair the existing monitor rather than creating a duplicate.

Use JobHound's manual, interval, daily or weekly schedules. Do not duplicate them with agent cron or repeated browser sessions. Report partial, stale, failed and offline states accurately. Never bypass a DNS/IP guard, disable TLS verification, expose a tunnel or remove framing protection to pass a test.

A host artifact is a presentation of results from the same backend, not a replacement app. Label snapshots with their retrieval time and refresh instructions; do not invent live connectivity or working write buttons. Preserve the bundled UI. Full human UI hosting in Muse and durable background operation remain unverified. Linux native audio capture is unsupported.

If supported, use doctor's exact stdio MCP registration; otherwise use the typed JSON CLI. Do not claim that Muse can act as JobHound's outbound AI provider. Private documents and paid AI need the user's choice; neither is necessary for browsing global jobs.

When presets report community_status=offline with catalog_source=release_snapshot, the full packaged catalog is usable. Browse and inspect it normally; label it with catalog_generated_at and describe it as a release snapshot. Preserve the underlying live error. Do not claim unavailable presets or fresh online verification merely from the offline flag. Explicit installation still uses the normal preview, revision and validation contracts; snapshot availability does not establish that a scraper can access its careers site.
