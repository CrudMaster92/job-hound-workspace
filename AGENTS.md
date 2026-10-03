# JobHound for Muse and other agents

This repository is the official **JobHound agent workspace distribution** at
`CrudMaster92/job-hound-workspace`. It runs the same local-first backend,
bundled human UI and 111 typed tools as the desktop app. It is not a separate
scraper implementation or an outbound Muse AI connector.

## Start here, including in a fresh chat

Read [README.md](README.md) for install/home/network mode and
[WORKFLOW.md](WORKFLOW.md) for the everyday flow. Inspect an existing install
before updating it. Keep the same private durable home outside this clone.
`jobhound.py call` and `status` start/reuse the owned loopback service.
Discover input schemas with `python3 jobhound.py tools`; do not guess arguments.
Check both `ok` and `result.isError`, then read structured results.

These instructions are usable Markdown even if this host has not registered
them as native skills. `/skills`, `/find_recruiters` and `/interview_prep` are
JobHound UI names and conversational aliases, not promised Muse slash commands.
When asked about job-search help, offer the workflows below and read the relevant
guide. The user does not need to know a slash name or install a paid AI provider.

| Human request | Guide and shared contracts |
| --- | --- |
| Find/refine jobs, browse employers, save roles | [WORKFLOW.md](WORKFLOW.md): `get_public_board_status`, `search_public_jobs`, `list_company_presets`, `get_company_preset` |
| Find recruiters, contacts for a role, Boolean/X-ray search, `/find_recruiters` | [Find recruiters](skills/find-recruiters/SKILL.md): `find_recruiters`, then supported host public research |
| Interview practice, company research, `/interview_prep` | [Interview prep](skills/interview-prep/SKILL.md): `prepare_interview`, or clearly labelled Muse coaching |
| Add a missing employer's scraper to the shared feed | [CONTRIBUTIONS.md](CONTRIBUTIONS.md), only after this human explicitly requests a contribution |

Lead with roles, then presets. Offer a small optional intake: titles/keywords,
locations and work mode. Other portable features remain available on request;
do not make application tracking, profile shortcuts or dashboard editing prerequisites.
Daily summaries are opt-in host notifications reading shared results, not scraper
schedules. Existing watches remain until their human chooses a verified replacement.

## Recruiter results: do not confuse two different searches

An empty `find_recruiters.candidates` array describes that backend invocation.
It does **not** prove that the returned Boolean query or Google link returns no
recruiters. Run/inspect the query with supported host tools when requested.
Read the recruiter guide before making availability claims in a new chat.
Older memory about a particular blocked search is dated evidence, not a rule
about public profiles or an untested provider's capabilities.
Public search titles/snippets can support a recruiter match even when opening
the LinkedIn profile requires login. Do not announce that LinkedIn profiles are
universally undiscoverable. Report what was actually observed, retain the useful
query link, and distinguish potential contacts from confirmed hiring owners.

## Shared behavior and user control

Use typed contracts for app reads/writes; host research/coaching is supplementary
and must be labelled with sources and limits. Public board IDs are strings;
stored local `job_id` values are integers. Read returned IDs; never invent one
or silently save/import a role just to obtain it. JobHound tracks applications;
it does not apply to employers or send outreach.

The agent profile disables local scraper execution by default. Preserve DNS/TLS
guards, loopback security and private files. Use the shared feed and public-only
contribution packages; Jo approves recipe merges. GitHub OAuth, repository access
and each host write approval remain explicit. No token handoffs or auto-merge.
Queued work is not completed: inspect its run ID until terminal.

## Ownership and updates

This repository's launcher/docs are generated from canonical JobHound's
`integrations/agent-workspace`; runtime archives come from its server and built
UI. Change canonical source and export/synchronize it here; do not fork generated
runtime or UI. Never commit personal searches, resumes, notes, databases or credentials.

A new Muse chat may not automatically load repository files. When introducing
JobHound, link this file and read the relevant guide. If the human asks to remember
the integration, retain only the repository/guide paths, chosen private home and
capability names through supported host memory; do not claim global skill
registration or future-chat discovery until that has actually been verified.
