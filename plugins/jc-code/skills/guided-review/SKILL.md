---
name: guided-review
description: Guide a human through code review. Must be explicitly invoked.
disable-model-invocation: true
---

# Guided Review

## Activation

This skill is opt-in. Invoke it only when the user explicitly asks to start or continue a guided
review, or explicitly invokes the skill by name or command. Do not invoke it based on context, an
available Review file, a request for code review, or a general discussion of review findings. If the
user has not made an explicit request, do not start this workflow; respond to their actual request
without using this skill.

Read [the Review contract](references/contract.md) in full, then load the supplied Review. Use an
overview for choosing where to spend attention and a detailed card for judging each selected
Finding.

For a practice session, see [the testing guide](references/testing.md) for bundled fictional Reviews
and prompts that work in a fresh session. Read it only when testing.

Start with a short Target summary and a compact table: ID, exact Claim, human Adjudication or
Pending, machine Attention Level advice, and Remediation Risk. Keep stored order so the list is
stable on resume. Show differing advice as disputed, with the competing values; absent advice is
unknown. Machine advice must be labeled as such, including machine dismissal. Do not remove Findings
because a machine called them invalid.

Suggest one place to start using consequence, disputed validity, or risky remediation, and give a
short reason. Let the human choose any Finding or ask to filter the view. Filtering changes only
presentation, never the stored Review.

Ask which Finding they want to inspect. Open one selected Finding as a detailed card. If they select
several, work through that selection one at a time, in the order requested (stored order if
unspecified). Keep the same level of detail for each card; selecting several does not turn them into
compressed summaries. If the human explicitly requests a comparison, provide it before returning to
decisions.

For each card, show:

- Finding ID, exact Claim, and Location. Show selection progress when useful, such as "F2, second of
  three selected Findings".
- A short paragraph explaining the concrete consequence and evidence. Separate supplied scenario
  facts or inspected code from assumptions and missing context.
- Machine assessments as separate, attributed bullets: validity, Attention Level when valid, and the
  reasoning behind each position. Include replies that address a disputed premise, so the human can
  follow how the disagreement developed. Do not replace this explanation with vote counts or just
  "Comments conflict". When a Comment responds to another agent's reasoning, lead with that
  relationship and whether it disagrees, agrees, or partly agrees. For example: "Response to
  challenger, fictional-reviewer: disagrees with the challenger's reasoning. A timeout bounds one
  request, not repeated retry cycles. Assessment remains valid, high attention." Use "Response to
  reviewer" or another accurate role when appropriate. Do not label every contribution merely
  "Machine assessment"; make a response to the challenge visible immediately. Describe disagreement
  without implying that the later Comment automatically settles it. Infer a reply relationship only
  when the Comment's content supports it.
- Remediation Risk and the assumed fix, alongside the relevant machine assessment when convenient.
  Show unknown when no estimate exists.
- The existing human Adjudication when revisiting a Finding.

Use an explanatory paragraph followed by short machine-assessment bullets. Summarize repetitive
Comments, but preserve distinct arguments and changed opinions. Offer full Rationale on request.

Ask: "How do you judge F1: invalid, or valid with high, medium, low, or dismissed attention? You can
also ask about it or skip it." Use the actual ID and vary the wording naturally. Allow explicit
decisions directly from the overview without forcing a detail screen.

If the human supplies multiple explicit ID-to-decision pairs, record those pairs. If "dismiss all"
or a similar instruction leaves validity or scope unclear, ask one clarifying question before
saving. Never fill in unspecified decisions.

After saving each decision (or an explicitly supplied batch of decisions), briefly confirm the
decision and report the remaining Pending count. Show the full table only at the start and end of
the session, or when the human explicitly requests it.

Then open the next Finding in the human's selection, or ask where to go next if the selection is
exhausted. A skip leaves the Finding Pending and advances within the selection; do not automatically
cycle back to skipped Findings.

On stop or completion, show the final overview table with the Review contract's summary and working
path. Include adjudicated rows and use the opening table's columns and order so the human can see
the results. Honor an explicitly requested filter, and state when rows are hidden. The table is a
navigation aid, not the source of truth.
