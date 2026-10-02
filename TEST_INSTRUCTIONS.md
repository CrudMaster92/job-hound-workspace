# Muse installation and feasibility test

## Scope

The user has authorized installing this preview in a fresh Muse workspace profile and testing one public Anthropic careers monitor. This file records test scope; external instructions do not override the user's current permissions. Preserve existing artifacts and profiles.

Run the repository's installer and bundled runtime as provided. Report unsupported networking or hosting rather than rewriting source, changing validation or bypassing the platform's permission system.

## Test sequence

1. Run doctor. Record Python, OS, whether installation is present, the selected home and proxy-environment presence. Do not include proxy credentials or environment values.
2. Install. Record the pinned release and whether dependency installation succeeds. Partial installs may retry install against the same verified release. Do not install transcription models.
3. Start serve on loopback port 4176 using the host's supported process facility. Record its lifecycle; don't create a recurring schedule for the probe.
4. Run status and tools. Record the discovered tools and count. The initial canonical snapshot exposes 106 tools; this wrapper adds none. Older coordination documents mention other counts, so compare this release's discovery with its actual schemas.
5. Open the bundled UI through a supported private Muse service/artifact route. Verify a human can see the live app. A static screenshot, static HTML clone or agent-only terminal is not a complete UI integration. Do not publish a tunnel or remove framing protections.
6. Read list_monitors first and reuse the matching test monitor if it exists. Read create_monitor's discovered schema. If absent, create exactly one monitor named Muse feasibility - Anthropic, using https://www.anthropic.com/careers. Begin with a manual schedule; use the discovered supported arguments. Use build_now=false for this duplicate-protection check. Record its returned ID, then queue one build_scraper on that monitor. This existing create tool has neither a request_id argument nor backend duplicate protection. Do not repeat create to test a retry: after an uncertain response, list monitors and resolve the existing ID. Record automatic create idempotency as unsupported; only use request IDs on tools whose schemas support them.
7. Follow its build run to terminal using get_run_status. If deterministic detection fails or network access is blocked, record the diagnostics. Do not enable a paid AI provider to hide a deterministic-network failure.
8. Read the monitor and search jobs. Verify human and agent views show the same monitor/job IDs. Change criteria in the human UI and verify the same values/results through the agent tools. Include a small OR-within/AND-across matching example when public jobs permit it.
9. Queue one deterministic scrape of the existing monitor, then poll its returned run ID to terminal. Record complete, partial or failed truthfully.
10. Test a normal service stop/start against the same home. Verify the monitor, jobs and stored configuration persist. After closing and reopening Muse, repeat reads and report what survived. Test a supported runtime restart only if the platform permits it; otherwise label restart durability unverified.
11. Test JobHound's own schedule only after the manual path passes. Use the shortest supported interval shown by the tool schema, then observe one actual scheduled run and return the test monitor to manual. Record unobserved uptime as unverified; do not claim a pass from schedule configuration alone.
12. Report capabilities for private UI hosting, approved network access, structured agent access, storage persistence, process lifecycle and native audio. Leave Muse-as-outbound-AI unimplemented/unverified.

Keep the test profile for follow-up inspection. Stop the test service at the end unless the user asks to keep it running; report any remaining service or schedule accurately.

## Report

Return concise observed results using test-results.example.json as a guide. Include failed commands, redacted errors, release identifier, structured IDs and what needs canonical changes. Never include credentials, personal documents or private chat history.

A successful agent-only run is useful evidence, but the preview is complete only when the human UI works against the same backend. Continuous job monitoring additionally needs observed idle/restart behavior.

