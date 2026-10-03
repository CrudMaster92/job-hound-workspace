---
name: find-recruiters
description: Find potential recruiters for a selected JobHound role, inspect Boolean/X-ray search results, or help refine a recruiter search. Also use for the conversational alias /find_recruiters.
---

# Find recruiters with JobHound and Muse

Read the workspace [AGENTS.md](../../AGENTS.md) for transport and ID rules.
This is a lightweight workflow, not a requirement for a native Muse slash menu.

1. Resolve the role with `search_jobs`/`get_job`, or `get_public_job` for a public
   board role. Use its actual employer, title, location and source URL. The
   `find_recruiters` tool currently needs a stored integer `job_id`; use a
   returned `local_job_id` if present. Otherwise offer saving that public role
   with the human's agreement before invoking the backend. A human-provided
   Boolean query can be inspected directly without saving anything.
2. On Muse, call `find_recruiters` with `live_search=false` to obtain the canonical
   Boolean query and Google `search_url` without an outbound AI provider. If the
   human wants JobHound's configured-provider search, use `live_search=true`.
   Discover the schema first. Neither mode configures a provider for them.
3. For a request to find people, inspect the returned search URL/query using
   supported host public search/browser tools. Query generation and public
   discovery are separate steps. A backend warning or empty candidates array
   is not evidence that the human's Google results are empty. If the human
   reports results, inspect them rather than contradicting them from an older
   backend result. Use public result titles/snippets as evidence; opening every
   profile is unnecessary. Login/CAPTCHA/access blocks describe that attempt,
   not whether public profiles exist. Keep the link usable if inspection is blocked.

Present up to three supported potential contacts with public HTTPS LinkedIn
`/in/` URLs, the visible name/headline and the employer/recruiting/location
signals that support each match. Include the search link, date and relevant
warnings. Label host-discovered contacts separately from backend candidates;
do not pretend they were returned or stored by JobHound. Fewer supported matches
are fine. An empty search observed today is not a permanent coverage claim.

If useful, refine an overly narrow query by relaxing one location or function
constraint and label that refinement. Do not repeatedly restart the backend
skill for a conversational follow-up. Never invent names, infer personal contact
details, claim someone owns the requisition, bypass access controls or send outreach.
