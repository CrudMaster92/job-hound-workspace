---
name: interview-prep
description: Prepare or practise for a selected role using the posting, sourced company research, interview questions and coaching. Also use for the conversational alias /interview_prep.
---

# Interview prep with JobHound and Muse

Read the workspace [AGENTS.md](../../AGENTS.md) for transport and ID rules.
Resolve the selected role through `get_job` or `get_public_job`; retain its
posting/source URL. Do not make tracking setup or a resume a prerequisite.

For a stored integer job ID, call `prepare_interview` without `sections` to
retrieve its canonical choices. Present them without preselection, unless the
human has already explicitly chosen the areas. Keep questions at three unless
they ask for another number. Follow-ups use the existing context/pack; a fresh
backend generation is needed only when requested.

Choose the available path honestly:

- **Configured JobHound AI:** inspect `get_jobhound_status` first, then call
  `prepare_interview` with the actual job ID and chosen section IDs. Return its
  source links and warnings. Do not configure a paid provider just for this.
- **Muse coaching:** if no outbound provider is configured, or the role exists
  only on the public board, Muse can still help from the retrieved posting and
  supported host public research. Ask which areas the human wants, then coach
  in chat. Label it "Muse interview coaching"; it is not a generated/stored
  JobHound preparation pack. Saving a role or connecting a provider is optional.
  If the posting is inaccessible, use the human's pasted text and state the limit.

Separate posting facts, dated public company sources and assumptions. Draw role
priorities only from the posting; cite URLs for company research. Use STAR prompts
to help the human form their own answers, not invented achievements or metrics.
Unpublished salary/benefits stay unknown. Do not present suggested tools as
requirements unless the posting names them.

A resume is optional. Obtain permission before reading/importing a private file
and before sending it to another provider. For a backend resume, use the real
active document ID and the explicitly approved `document_consent_connection`.
Muse-local coaching does not authorize sending that resume to a separate service.
Do not apply, contact employers, publish private prep notes or imply native audio
capture works on a Linux host.
