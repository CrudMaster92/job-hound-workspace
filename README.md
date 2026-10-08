# JobHound agent workspace preview

Run the existing JobHound app inside Meta Muse or a similar agent workspace. The backend, bundled web UI and 111 typed MCP tools come from canonical JobHound. This experimental distribution keeps the full app while testing a board-first agent workflow; it does not add Muse as an outbound AI provider.

Preview 6 has passed real Muse and GitHub Linux tests: full-feed search, identical HTTP/MCP role IDs, 111 tools, automatic startup/reuse and stop/restart with retained notes. Proxy-aware board access and the dated preset snapshot work. Local scraper execution is disabled in the agent profile; blocked live preset refresh retains its original error and offline snapshot. Human UI mounting, full VM restart persistence and sustained background operation remain unverified.

Preview 7 adds readers for losslessly compressed public job details and removes
the arbitrary 500-search-page limit. The 200 MB aggregate index budget and
hash/generation checks remain. Update/reinstall this release before the feed
enables `.json.gz` detail pages; a feed update does not update installed code.
The packaged catalog snapshot includes all nine current collections and keeps
its original capture date. Windows reader/build tests pass; this release's
fresh Muse-host lifecycle has not yet been observed.

## Fresh conversations and lightweight skills

Read [AGENTS.md](AGENTS.md) as the entry point. A fresh Muse conversation may not automatically load this repository or register its files in a native skill catalog. You can introduce it with: "Use JobHound from CrudMaster92/job-hound-workspace; read AGENTS.md and use its workflows when I ask for job-search help."

Ask naturally for roles, recruiter contacts or interview practice. `/find_recruiters` and `/interview_prep` are conversational aliases for the [recruiter guide](skills/find-recruiters/SKILL.md) and [interview guide](skills/interview-prep/SKILL.md); `/skills` is the embedded app's menu, not a required Muse command. Muse can run public recruiter research using the backend's query and do sourced interview coaching without a separate outbound AI provider. Empty backend recruiter candidates do not prove the Google query has no matches.

## Install and keep the same profile

Python 3.11+ and Node.js 18+ are required (Node runs the shared public-board query engine). Clone this public repository. Read [AGENTS.md](AGENTS.md), [SKILL.md](SKILL.md) and [WORKFLOW.md](WORKFLOW.md). Use [TEST_INSTRUCTIONS.md](TEST_INSTRUCTIONS.md) for validation.

    python3 jobhound.py doctor
    python3 jobhound.py install
    python3 jobhound.py status
    python3 jobhound.py tools

Choose durable app storage: default home is ~/.local/share/jobhound, outside the clone. Keep notes in <home>/notes/. An existing clone-local profile is never silently moved; supply its --home explicitly. Supply the same --home and --port before every command if you choose another location. Releases/venvs are separate from home/data; updating this clone and installing a new release preserves the profile. Stop the previous service before starting the new release on the same home/port. Never run two releases against one profile at once.

Status/call and stdio MCP automatically start one locked, identity-checked loopback service. Managed services stop after ten idle minutes without active work; CLI/MCP clients keep it alive during calls. start/stop are explicit lifecycle commands. Serve remains optional and runs in the foreground on http://127.0.0.1:4176. Keep it running using supported host facilities; a closed terminal may stop it. The installer verifies the archive checksum and reuses completed installs. It does not install browser binaries or transcription models.

In another terminal:

    python3 jobhound.py status
    python3 jobhound.py tools
    python3 jobhound.py call get_public_board_status --arguments '{}'
    python3 jobhound.py call search_public_jobs --arguments '{"query":{"limit":10}}'

Discover schemas before using tools. Commands call existing typed MCP contracts; inspect ok and result.isError. Doctor also returns optional stdio MCP registration details; use them only if the host supports registration.

## Workspaces that require a proxy

External board, preset HTTP and scraper HTTP clients default to direct transport. If the host requires its ambient proxy/CA setup, opt in when starting the service:

    python3 jobhound.py --network-mode environment serve

Equivalently set JOBHOUND_EXTERNAL_NETWORK_MODE=environment in the service environment. HTTPX then honors HTTP_PROXY/HTTPS_PROXY/ALL_PROXY/NO_PROXY (including lowercase variants), plus SSL_CERT_FILE/SSL_CERT_DIR. Use the host's existing approved configuration; do not print credentials, guess proxy URLs or disable certificate verification. Loopback agent-to-app HTTP remains direct regardless of these variables. Doctor reports selected mode and boolean presence without exposing proxy credentials.

This opt-in does not remove host, redirect, size, checksum, TLS or DNS/IP validation. Scrapers and remote presets may still reject Muse's synthetic/non-public DNS; report those failures. The board feed's fixed configured origin uses its existing validation. Browser automation and AI-provider networking are separate and are not changed by this mode. A proxy is an explicitly trusted egress dependency, not an unrestricted JobHound endpoint.

## Present results to the human

Offer features and optional onboarding, use the global board first, and prefer existing presets before building scrapers. Use [ARTIFACT_GUIDE.md](ARTIFACT_GUIDE.md) to author a dated read-only Muse job list from backend results. This gives the human a useful view while full bundled-UI hosting is unresolved. A snapshot does not provide automatic refresh or the entire app's interactive controls.

## Other limits

- Monitor creation lacks backend retry deduplication: list first and reuse its ID after uncertainty.
- Native audio recording requires Windows; a cloud Linux VM cannot capture the human's laptop microphone through this app.
- Private documents, paid AI and outbound agent-provider configuration are optional separate setup.
- Profiles do not synchronize with a Windows installation. Scraper schedules belong to JobHound. Optional human-requested host reminders may read the shared feed and send summaries.
- Do not expose public tunnels or weaken loopback/framing protection to host the app.

## Ownership

Repository files are generated from canonical integrations/agent-workspace. The release includes canonical runtime, built UI and the same public-board query engine, with per-file hashes. Personal data, databases, credentials and installed environments are excluded. Fix source in canonical JobHound, then export a new release; do not fork the generated runtime. Installation/searching never submits applications.

## Packaged full preset catalog (preview 4)

This release includes a verified snapshot of all public preset collections, company/member/search pages and recipe artifacts. When online catalog access fails and no downloaded catalog is available, JobHound uses this read-only release snapshot through the existing UI/API/MCP contracts. No profile data is copied or monitors installed by fallback. It reports community_status=offline, catalog_status=stale, catalog_source=release_snapshot, generation/capture dates and the underlying live error. Offline does not mean the preset list is empty.

Use list_company_presets and get_company_preset normally, including marketing-agencies-canada. Forced refresh retries the live catalog and may still return the snapshot. The snapshot is fixed to this release, not a live update: install a newer workspace release to get a newer snapshot when online access is blocked. A downloaded catalog retains priority; mismatched artifact revisions never silently resolve to older recipes. Existing preview/revision checks and recipe validation remain required for explicit installs. Careers-page scraper networking is separate and may still fail on synthetic DNS.

## Contribution profile (preview 6)

Board roles and presets come first. The default agent profile retains the full app and 111 tools but disables local scraper execution; supported desktop hosts retain it. Read CONTRIBUTIONS.md for human-requested public-only packages, trusted runtime validation, the maintainer's merge and automatic collection. No auto-merge or arbitrary plugins. Native/uptime/UI limitations are explicit in status capabilities. Preview 5 fixes malformed IPv6 NO_PROXY patterns without weakening DNS/TLS. GitHub OAuth and per-write approval remain host responsibilities. Live Muse PR creation is unverified until its human connects GitHub and that gate is observed.

Preview 6 fixes full-feed search above the old 64 MiB query input limit. The
shared runner has a bounded 256 MiB byte budget for the supported 200 MB feed
plus saved/local overlays. Slow requests return deadline/status guidance;
they do not imply the service is offline or direct Linux users to a Windows
launcher. PR checks install the exact checked-in archive on Linux and compare
live public role IDs through HTTP and MCP.

## Baseline host requirements and storage

Choose --network-mode direct for ordinary public egress or environment when the host requires its approved proxy/CA setup; decide explicitly before the first call. Required baseline capabilities are Python/Node, shell/file IO in an explicitly durable home and outbound public HTTPS. Artifact rendering and host scheduling are optional; chat links and conversational checks are the fallback. Human involvement is required for OAuth, write approval and merge.

On-demand startup detaches its service (a new session on POSIX; a hidden process group on Windows), so a completed transient CLI/cron invocation does not terminate it. Startup/service OS locks are separate; an OS releases them when the owner exits/crashes, so a stale text PID cannot reserve the home after reboot. Reuse also requires the same home/release/profile identity and healthy port. No foreign PID is killed. --home/data contains durable app state; notes/, agent-search.json and contributions/ stay outside releases and clone updates.
