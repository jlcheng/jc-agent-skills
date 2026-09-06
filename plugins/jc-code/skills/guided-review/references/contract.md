# Review contract

Read this entire file before guiding a Review. It adapts the vocabulary in John's
`ai-code-reviews.md` journal entry dated 2026-09-06. The JSON representation and session rules below
define this skill's file format and behavior. Resolve the skill's relative reference to this file
against the skill directory, not the session's working directory. This contract contains the
necessary vocabulary; the original journal and earlier conversation are not required.

## Stored objects

- **Review**: one stored examination of one **Target**. `state` is `active` or `completed`. `target`
  is one prose string explaining what was reviewed and where to find it, with enough context for
  another agent to resume. `findings` is an array.
- **Finding**: `id`, `claim`, `location`, `comments`, and `adjudication`. **Claim** is a required,
  short statement of the alleged problem. **Location** is a readable string. Keep the Finding's
  identity, Claim, and Location unchanged. A different Claim needs a new Finding, not an edit
  disguised as clarification.
- **Comment**: a structured machine contribution with `id`, `author`, and boolean `is_valid`. A
  valid assessment includes `attention_level`; `remediation_risk` and `rationale` are optional.
  **Rationale** is one prose string, including facts and their Locations when available. Append
  Comments; never change or remove existing ones. A changed machine opinion is another Comment.
- **Adjudication**: `null` means **Pending**. Otherwise it is either `{"is_valid": false}` or
  `{"is_valid": true, "attention_level": "high"}` (with the chosen Attention Level). Only the human
  supplies this judgment. Keep only the latest Adjudication, replacing it when the human changes
  their decision during an active Review. No rationale is required. It overrides all Comments.
- **Valid**: the judge believes the Claim holds in the actual context. Machine validity and human
  validity are distinct judgments; a machine opinion never changes a Pending Finding into an
  adjudicated one.
- **Attention Level**: `high`, `medium`, `low`, or `dismissed`. It recommends how much attention the
  author should give a valid Finding. **Dismissed** means valid but no action recommended. Machine
  dismissal still leaves the Finding Pending.
- **Remediation Risk**: `high`, `medium`, or `low`. It estimates the chance and harm of an unwanted
  outcome from resolving a valid Finding, considering the proposed change's reach, complexity, and
  uncertainty. State what remediation the estimate assumes. Unknown risk stays absent and is
  displayed as unknown, not low.

Example Finding (fictional):

```json
{
  "id": "F1",
  "claim": "The loop has no limit on repeated 429 responses.",
  "location": "client/retry.py:84-103",
  "comments": [{
    "id": "C1",
    "author": "initial-reviewer",
    "is_valid": true,
    "attention_level": "high",
    "remediation_risk": "medium",
    "rationale": "The loop repeats on 429. Adding an attempt limit changes failure behavior for callers."
  }],
  "adjudication": null
}
```

## Starting and resuming

This skill guides an existing Review supplied by path. If the input is a raw diff or a legacy
`findings.md`, explain that it needs an initial Review object; do not silently translate machine
Verdicts into human Adjudications.

Read the entire input. Check required fields, enums, unique Review-local Finding IDs and
Finding-local Comment IDs, and Adjudication shape before saving. Preserve unrecognized fields. If
malformed data would change the meaning of a decision, explain the specific problem and ask for its
correction before proceeding.

Store one JSON file per Review under `~/.jc-guided-review/<repo-name>/` by default.
Use the directory name of the reviewed repository's root for `<repo-name>`, not the
skill repository or an unrelated session working directory. Record the reviewed repository's
absolute path in the Target prose so repositories with the same directory name remain
distinguishable. If the repository cannot be determined from the input or user request, ask which
repository the Review concerns. For fictional fixture tests, use `fictional-tests` as the folder.

Choose a filename such as `2026-09-06-retry-client-<unique-suffix>.json`, with a short descriptive
slug and a fresh suffix for each new Review. Create the containing directory as needed and never
overwrite an existing Review when starting another. Honor an explicitly requested output path,
including temporary paths for tests. Expand `~` to the user's home directory and report the exact
absolute working path when the session starts.

When starting from a fixture or another input supplied for a new Review, copy it to the new working
path before the first interaction; preserve the source input. If the user supplies a working
Review to resume, use that file in place without copying or moving it.

Re-read the working Review before presenting or saving decisions. Persist each explicit human
judgment immediately. Preserve every unrelated field and existing Comment. Confirm the stored
decision briefly; do not require a second approval.

The same file holds the active Review and the completed Review. On completion, update its `state`
to `completed` in place; do not create a separate final JSON or move it to an archive directory.

`completed` Reviews are read-only. Offer a fresh Review if more work is requested.
Do not silently reopen one.

## Conversation rules

Use the interaction described in SKILL.md. Ask one focused question at a time and accept ordinary
language. You may show several facts or Findings at once; the user should know exactly which
Finding a decision concerns.

Only explicit human judgments become Adjudications. "Next", silence, "skip", and "stop" do not imply
invalidity or dismissal. If the user says only "valid", ask for Attention Level before storing it.
"Dismiss this" can mean invalid or valid but no action: clarify unless the meaning is already
explicit. Do not infer an Attention Level from the machine's recommendation.

Show existing human decisions accurately. Machine disagreement must remain available for inspection
but cannot override them. When summarizing Comments, identify who said what; do not combine
conflicting opinions into a consensus. Show exact Claims when asking for judgment. Explain
unfamiliar code in plain language and distinguish cited evidence, assumptions, and missing context.

If asked to investigate, inspect available code and append a Comment for a new or changed
assessment. The fixture Targets explicitly identify fictional code and supply scenario facts: use
those facts, cite them as scenario context, and never pretend to have opened those paths or run
tests. If a necessary fact is absent, ask for it or leave the Finding Pending. Human context may
inform a new machine Comment; it does not by itself constitute an Adjudication.

Reviewing and adjudicating do not authorize fixing code. Remediation Risk informs the discussion;
low risk is not permission to act. A separate request to implement a fix can start separate
implementation work, preserving this Review's history.

On stop, save any explicit decisions and summarize remaining Pending Findings; leave `state` active.
Once every Finding has an Adjudication, ask whether the human is finished unless they already said
so. Mark completed only with that confirmation. If they ask to finish while Findings are Pending,
name the unresolved Findings and leave active rather than inventing judgments. An empty Review
follows the same human confirmation rule.

At completion, summarize valid Findings by human Attention Level, then invalid Findings. Report the
working path. Never describe dismissed Findings as false alarms, or an assessment as a completed
fix.
