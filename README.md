# JobHound agent workspace preview

Run the existing JobHound app inside Meta Muse or a similar agent workspace. The backend, bundled web UI and 106 typed MCP tools come from canonical JobHound. This experimental distribution keeps the full app while testing a board-first agent workflow; it does not add Muse as an outbound AI provider.

Lou's first Muse test verified install, agent access, bundled UI serving and normal stop/start persistence. Global-board access failed through Muse's required proxy; scraper detection rejected synthetic DNS. Preview 2 adds opt-in environment transport and packages the public board's canonical Node query engine. Preview 3 additionally fixes the first feed fetch on a newly booted VM (the cache interval now applies only after a check). Preview 4 adds the complete packaged public preset catalog for offline browsing and recipe resolution. Muse retesting is required. Human UI mounting, full VM restart persistence and sustained background operation remain unverified.

## Install and keep the same profile

Python 3.11+ and Node.js 18+ are required (Node runs the shared public-board query engine). Clone this public repository. Read [SKILL.md](SKILL.md) and [WORKFLOW.md](WORKFLOW.md). Use [TEST_INSTRUCTIONS.md](TEST_INSTRUCTIONS.md) for validation.

    python3 jobhound.py doctor
    python3 jobhound.py install
    python3 jobhound.py serve

Choose durable app storage: default home is .jobhound in this clone. Supply the same --home and --port before every command if you choose another location. Releases/venvs are separate from home/data; updating this clone and installing a new release preserves the profile. Stop the previous service before starting the new release on the same home/port. Never run two releases against one profile at once.

Serve runs in the foreground on http://127.0.0.1:4176. Keep it running using supported host facilities; a closed terminal may stop it. The installer verifies the archive checksum and reuses completed installs. It does not install browser binaries or transcription models.

In another terminal:

    python3 jobhound.py status
    python3 jobhound.py tools
    python3 jobhound.py call get_public_board_status --arguments '{}'
    python3 jobhound.py call search_public_jobs --arguments '{"query":{"limit":10}}'

Discover schemas before using tools. Commands call existing typed MCP contracts; inspect ok and result.isError. Doctor also returns optional stdio MCP registration details; use them only if the host supports registration.

## Workspaces that require a proxy

External board, preset HTTP and scraper HTTP clients default to direct transport. If the host requires its ambient proxy/CA setup, opt in when starting the service:

    python3 jobhound.py --network-mode environment serve

Equivalently set JOBHOUND_EXTERNAL_NETWORK_MODE=environment in the service environment. HTTPX then honors HTTP_PROXY/HTTPS_PROXY/ALL_PROXY/NO_PROXY (including lowercase variants), plus SSL_CERT_FILE/SSL_CERT_DIR. Use the host's existing approved configuration; do not print credentials, guess proxy URLs or disable certificate verification. Loopback agent-to-app HTTP remains direct regardless of these variables. Doctor reports selected mode and boolean presence only; it cannot inspect an already-running service's mode.

This opt-in does not remove host, redirect, size, checksum, TLS or DNS/IP validation. Scrapers and remote presets may still reject Muse's synthetic/non-public DNS; report those failures. The board feed's fixed configured origin uses its existing validation. Browser automation and AI-provider networking are separate and are not changed by this mode. A proxy is an explicitly trusted egress dependency, not an unrestricted JobHound endpoint.

## Present results to the human

Offer features and optional onboarding, use the global board first, and prefer existing presets before building scrapers. Use [ARTIFACT_GUIDE.md](ARTIFACT_GUIDE.md) to author a dated read-only Muse job list from backend results. This gives the human a useful view while full bundled-UI hosting is unresolved. A snapshot does not provide automatic refresh or the entire app's interactive controls.

## Other limits

- Monitor creation lacks backend retry deduplication: list first and reuse its ID after uncertainty.
- Native audio recording requires Windows; a cloud Linux VM cannot capture the human's laptop microphone through this app.
- Private documents, paid AI and outbound agent-provider configuration are optional separate setup.
- Profiles do not synchronize with a Windows installation. Schedules belong to JobHound; do not duplicate them with agent cron.
- Do not expose public tunnels or weaken loopback/framing protection to host the app.

## Ownership

Repository files are generated from canonical integrations/agent-workspace. The release includes canonical runtime, built UI and the same public-board query engine, with per-file hashes. Personal data, databases, credentials and installed environments are excluded. Fix source in canonical JobHound, then export a new release; do not fork the generated runtime. Installation/searching never submits applications.

## Packaged full preset catalog (preview 4)

This release includes a verified snapshot of all public preset collections, company/member/search pages and recipe artifacts. When online catalog access fails and no downloaded catalog is available, JobHound uses this read-only release snapshot through the existing UI/API/MCP contracts. No profile data is copied or monitors installed by fallback. It reports community_status=offline, catalog_status=stale, catalog_source=release_snapshot, generation/capture dates and the underlying live error. Offline does not mean the preset list is empty.

Use list_company_presets and get_company_preset normally, including marketing-agencies-canada. Forced refresh retries the live catalog and may still return the snapshot. The snapshot is fixed to this release, not a live update: install a newer workspace release to get a newer snapshot when online access is blocked. A downloaded catalog retains priority; mismatched artifact revisions never silently resolve to older recipes. Existing preview/revision checks and recipe validation remain required for explicit installs. Careers-page scraper networking is separate and may still fail on synthetic DNS.
