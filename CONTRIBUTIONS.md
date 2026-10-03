# Contribute only when your human asks

Run from the workspace repository beside `jobhound.py`. Here, `<home>` means
the private durable directory chosen with `--home`, such as
`~/.local/share/jobhound`; substitute its actual path. It never means `/`.
After `install`, launcher `call` and stdio `mcp` automatically ensure the
owned service is running. Keep the same home and network mode throughout.

Search shared jobs and presets first. Contributions are optional coverage improvements, never automatic consequences of ordinary searches. Check current main, identities, existing ATS mappings, open PRs and platform proposals before authoring another.

1. Read the presets repository CONTRIBUTING.md and actual JSON schemas. Prefer a known ATS, public JSON API, HTML/JSON-LD, then a supported bounded browser recipe. generic_json often avoids adding an adapter.
2. Author a Proposal: exact base_commit; normalized company and monitor documents; optional full collections preserving unrelated members and incrementing revision once; a trimmed real public fixture with source_url, fetched_at, payload; ownership with official company_url, explanation, shared_feed and representative job links. Discover the tool schema. Exclude private profile data and credentials.
3. Call preview_scraper_contribution. Offline parsing is provisional and author verification becomes unverified. A stale base, duplicate identity or pending PR needs repair/reuse. Offline inspection permits keeping a draft, not submission.
4. On the human's explicit public-contribution request, prepare_scraper_contribution with unique request_id, human_requested=true, public_submission=true and the Proposal. Poll get_scraper_contribution to terminal and inspect include_content=true. Preview 5 supports `python3 jobhound.py --home /your/durable/home call prepare_scraper_contribution --arguments-file /absolute/file.json`: this file contains the tool argument object. Discover its schema first; do not copy private search preferences into it.
5. Use that human's supported GitHub connector to push exactly the authored JSON package and open a draft against CrudMaster92/job-hound-presets main. Include the supplied PR body. No scripts, workflows or generated files belong in a recipe PR. JobHound never pushes, merges or accepts GitHub credentials.
6. Muse requires its supported human OAuth and selected-repository installation, then per-write approval. Read its GitHub skill. If disconnected, present the supported connection URL to the human; never ask for a pasted token or bypass approvals. Discover actual fork/branch/commit/PR capabilities after connecting rather than promising unobserved tools.
7. record_scraper_contribution_submission verifies actual pr_number, exact head_commit and file scope. Reuse that contribution/PR after uncertainty; never duplicate blindly.
8. Refresh get_scraper_contribution(refresh=true). Preparation, trusted runtime validation, Jo's review/merge and public publication are separate. Jo alone approves ownership and merges. Eligible revisions enter the next scheduled successful collection without a second lock PR. Require the matching published source hash before saying live.

An unsupported platform needs a separate runtime-support proposal with dated public fixtures, desired behavior and bounded offline tests. Search existing proposals first. Do not install executable plugins or edit generated runtime; canonical maintainers implement and export support.

While waiting, directly fetched public findings can help that requesting human if labelled with date/source and 'unvalidated; not in curated feed'. Keep them separate. Human approval of GitHub writes and Jo's merge approval are both required. Never auto-merge.

Prepared files and receipts are persisted in `<home>/data/jobhound.sqlite3` and retrievable through `get_scraper_contribution(include_content=true)`; the ZIP is generated from that stored content. If saving it separately, use `<home>/contributions/<contribution-id>/`, outside the clone/releases. Keep notes under `<home>/notes/`. Trusted verdicts live on the canonical presets repository `review-receipts` branch at `receipts/<pr-number>/<exact-head>.json` and appear in refreshed contribution status. Source schema checks use `scripts/validate_presets.py` and `scripts/build_catalog.py`; the trusted runtime entry point is `server.contributions.cli`. Receipts bind base/head, normalized monitor/proposal/runtime hashes, live count/pages/completeness and ownership review requirements.
