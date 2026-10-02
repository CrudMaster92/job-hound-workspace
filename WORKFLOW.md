# Help the human get value first

## Introduce and onboard

Offer a brief feature menu: search the shared global board; browse company presets; follow employers with deterministic monitors; save roles and track applications; work with resumes and letters; prepare for interviews; review dashboard summaries. Some capabilities need additional setup, documents or a supported human interface. Do not claim every feature was tested in Muse.

Offer a quick onboarding: desired titles/keywords, location(s), remote/hybrid/onsite preference, preferred companies or sectors, and any employment/salary preferences supported by the discovered schema. Let the user skip, give partial answers or refine after seeing results. A resume is optional; ask before importing private files. Keep preferences in the conversation or supported host memory. There is no invented global-profile write tool; inspect JobHound tools before persisting anything.

## Global board before local scraping

1. Read get_public_board_status. Inspect freshness, error, collections and source coverage. An unavailable feed is a failure, not zero matching jobs. Stale cached results can be useful if clearly labeled.
2. Call search_public_jobs with a query object supported by its schema. Supported fields include query, location, company_ids, collection_ids, work_modes, employment_types, salary_listed, posted_within_days, sort, view, limit and offset. Use returned IDs; do not guess collection IDs. A collection filter browses shared results without installing monitors.
3. Present a short first page with title, employer, location, work mode and direct source link. Show retrieval/feed dates, total matches and how many are displayed. Be clear about pagination and missing salary data. Use get_public_job for details when needed.
4. Offer to refine the search, save a selected role, or create a visible host artifact. For saving, inspect the role and the set_public_job_saved schema first. Neither saving nor installing a monitor submits an application.

Example (shell quoting may differ by host):

    python3 jobhound.py call get_public_board_status --arguments '{}'
    python3 jobhound.py call search_public_jobs --arguments '{"query":{"query":"marketing","work_modes":["remote"],"limit":20}}'

Calls return an MCP envelope. Check both ok and result.isError, then read result.structuredContent or the documented content. Do not scrape presentation text when structured results exist.

## Presets before scraper creation

If the human wants ongoing monitoring or a missing employer, inspect existing monitors and catalog/preset tools. Prefer a matching existing monitor, then a validated preset recipe. Read the install schema and resulting run status; installing a preset is a write and can queue work. An existing global-board role does not require a local monitor merely to view or save it.

Only build a new scraper when the requested source is absent or no suitable recipe exists. Inspect the public careers URL, reuse a matching monitor, start manual, queue the build and poll to terminal. Normal checks remain deterministic. Add a supported JobHound schedule only when the manual path works and the user wants ongoing checks. A blocked synthetic-DNS build remains blocked; a proxy setting does not authorize weakening address validation.

## Host portability

Keep these instructions independent of Muse-specific process, artifact and memory tools. A host adapter should provide installation, lifecycle and presentation capabilities; JobHound owns searches, criteria, saves, recipes and schedules. Hermes/OpenClaw can use the same workflow and MCP contracts, with their own supported UI/installation paths. A small presentation adapter can consume results without duplicating business rules.
