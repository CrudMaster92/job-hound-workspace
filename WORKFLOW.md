# Find useful roles first

## Before the first search

Run commands from the workspace repository, where `jobhound.py`,
`search-preferences.schema.json` and `search-preferences.example.json` live.
Choose one private durable home, for example `~/.local/share/jobhound`.
In these docs, `<home>` means that chosen directory; it is a placeholder,
not filesystem root. Use the same `--home` and network mode for every call.
After the reviewed release is available, run `python3 jobhound.py --home
"$HOME/.local/share/jobhound" install` once. Then `call`, `status` and the
launcher stdio `mcp` command automatically ensure the owned loopback service
is running; no separate daemon-start step is required. `tools` discovers
schemas without starting it. These commands use the installed backend.

Offer these behaviors when a human asks for job-search help: find roles, browse employers, refine searches, help with resumes/letters or interviews, and provide daily updates. Keep application tracking, platform shortcuts and dashboard editing optional. This workflow should be usable by any Muse agent without prior context.

## Small onboarding

Ask only titles/keywords, locations and remote/hybrid/onsite preference. Allow skipping and partial answers, then show useful results promptly. A resume is optional and requires the human's choice before importing private files. Keep preferences in supported host memory or an explicitly chosen private durable file; never commit them to a public repo. Discover schemas before offering extra refinements; do not invent fields or a global-profile tool.

Write the chosen search to `<home>/agent-search.json` after onboarding, using `search-preferences.schema.json` beside the launcher (generated from the canonical AgentSearchPreferences and BoardQuery contracts). Start from the repository's `search-preferences.example.json`, replace its example query with this human's choices, and keep daily_notification disabled unless a supported host reminder was actually created after their request. Read this private file for later checks and reminders; never copy it into a public proposal. Humans can inspect/edit it, and every query is still executed by the same search_public_jobs contract used by the app UI. Its `checkpoint` field holds `feed_generation`, `last_delivery_at` and `sent_job_ids`; these IDs are the returned board job IDs, not title fingerprints. Only update checkpoint after a successful visible delivery.

Tracking and other optional features are mentioned once, skipped by default, and available on request.

## Board, then presets, then optional contributions

1. Read get_public_board_status: inspect feed freshness, errors and actual collection IDs. Unavailable is a failure, not zero matches; label useful stale cached results.
2. Call search_public_jobs with a query from its discovered schema. Present a short page of titles, employers, locations, work mode and direct source links, plus total matches, displayed count and feed/retrieval dates. Use get_public_job for details. Refine instead of dumping hundreds of roles.
3. Browse list_company_presets, then get_company_preset or search_preset_companies. Reuse returned IDs to filter the shared board. Browsing never requires installing a scraper. If community_status=offline and catalog_source=release_snapshot, browsing still works; label catalog_generated_at and preserve the live error.
4. Optionally save a role with set_public_job_saved or show a dated snapshot using ARTIFACT_GUIDE.md. A job-list snapshot and an optional dashboard-card image are sufficient presentation patterns; complex widgets stay optional.
5. For a missing employer, explain the coverage gap and offer a public contribution. Only that human's explicit request starts this workflow. Read CONTRIBUTIONS.md. Direct public findings may help the requesting human immediately, labelled with source, probe date and 'unvalidated; absent from curated feed'. Never mix them into shared results.

Example (shell quoting differs by host):

    python3 jobhound.py --home "$HOME/.local/share/jobhound" call get_public_board_status --arguments '{}'
    python3 jobhound.py --home "$HOME/.local/share/jobhound" call search_public_jobs --arguments '{"query":{"query":"marketing","work_modes":["remote"],"limit":10}}'

Check ok and result.isError, then use result.structuredContent or its documented JSON content. Never parse the rendered app UI as the integration. Private monitor criteria use OR within categories and AND between populated categories; the board uses BoardQuery.

## Human-requested daily summaries

After a useful search, offer a short daily update. Only create a supported host reminder/cron when that human opts in. Confirm preferred time/timezone and short message versus quiet artifact refresh. Inspect existing reminders and update one rather than duplicate.

The reminder prompt should say: use the same durable JobHound home and network mode; inspect board freshness; search the human's saved criteria; report relevant matches not seen in the previous successful update using board job IDs; include direct links and feed date; keep the summary short. Persist the checkpoint in the `checkpoint` field of `<home>/agent-search.json` and update it only after actual delivery or a verified visible artifact. An unseen cached job is not necessarily newly posted. If the feed fails, report that once, retain the checkpoint and avoid retry floods.

If the host has no scheduling or notifications, retain the private search and offer conversational checks when the human asks "check my roles". Do not invent a cron capability.

Use the host's supported scheduling and notification facilities. No particular Muse agent's inbox, memory layout or artifact system is assumed. Await actual typed calls and delivery inside each reminder run; no fire-and-forget. This is a notification consumer of shared results, not a scraper schedule. JobHound owns deterministic collection; do not create per-agent scraper cron jobs. Keep an existing interim watch until replacement coverage is observed and its human explicitly chooses the transition.

## Other portable capabilities

For recruiter contacts or `/find_recruiters`, read
[skills/find-recruiters/SKILL.md](skills/find-recruiters/SKILL.md). For interview
practice or `/interview_prep`, read
[skills/interview-prep/SKILL.md](skills/interview-prep/SKILL.md). These guides
explain native Muse research/coaching alongside the typed backend contracts;
they work without a native slash menu or a separately configured AI provider.

All 111 tools and the bundled UI remain available through the same backend. Saves, application tracking, resumes/letters, interview preparation and dashboard cards can be used or suggested when relevant. Discover schemas, inspect before writes and respect document/provider consent. JobHound tracks applications; it does not submit them to employers. Private files and paid AI are optional.

Read get_jobhound_status capabilities before scraping or recording. The agent profile disables local scraper creation/execution by default. Explain a supported desktop handoff instead of retrying blocked operations or weakening DNS/TLS. Sustained uptime and private Muse UI mounting require actual host tests. A dated read-only artifact gives a useful human view while those remain unverified.

When a contribution is requested, its default shape is the public declarative package. Board/preset browsing remains the everyday entry point. A fully autonomous agent without its human present prepares a reviewable package, reports ready for review, and stops before OAuth, public writes or merge.
