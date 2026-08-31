---
name: guided-review
version: 0.1.0
description: Interactive, multi-phase code review. Wraps the built-in code-review skill, then checks each Finding with an adversarial verifier to strip false alarms, fixes what is safe to fix, explains the rest, trims stale code comments, and writes a report. Use when the user wants to work through review findings step by step and decide on each one, rather than get a one-shot list. Trigger on explicit invocation, or when the user asks to "walk through" a review, triage review findings, or check whether review findings are real.
requires: The built-in `code-review` skill. If it is not available, stop and tell the user.
---

# Guided Review

The built-in `code-review` skill hands you a list and walks away. This skill turns that list
into a session: every Finding gets attacked by a fresh adversarial verifier, the survivors get
sorted into what the agent can just fix and what needs your judgement, and what is left becomes
a report you can turn into tickets.

## Vocabulary

These words mean exactly one thing each. Use them in the code, in the state file, and when
talking to the user. Do not substitute synonyms.

**Changeset** - the set of changes under review. Established once in Phase 1 and recorded in the
state file. Never re-derive it later: by Phase 6 the working tree no longer matches the diff that
was reviewed, because this workflow has been editing it.

**Finding** - one problem reported by the built-in `code-review` skill. This is that skill's own
word, kept deliberately so nothing has to be translated. It is not a GitHub Issue.

**Adversarial Verifier** - a sub-agent that tries to disprove a single Finding. One per Finding.
See Phase 2 for the mechanism.

**Verdict** - the answer to "is this Finding true?". One of:

| Verdict      | Meaning                                     |
| ------------ | ------------------------------------------- |
| `Unverified` | Not yet checked. Every Finding starts here. |
| `Upheld`     | Survived the attack. Treat as real.         |
| `Refuted`    | Disproved. A false alarm.                   |

**Adjudicator** - whoever set the current Verdict: `verifier` or `human`. The Adversarial Verifier
sets it by default. A human may override a Verdict at any point, which rewrites both the Verdict
and the Adjudicator. Overrides are expected, not exceptional: a verifier cannot know that a code
path is dead for reasons that live outside the repo.

**Disposition** - what was decided about an Upheld Finding. One starting state, three endings:

```
                          ┌─→ Fixed      (changed in this run)
Open  ── user decides ────┼─→ Dismissed  (real, but not worth fixing)
                          └─→ Deferred   (real, fix later, carry into the report)
```

`Deferred` is terminal for this run. The report is the handoff to a ticket system. Re-running this
skill on the same code starts a Deferred Finding over at `Open`.

A `Refuted` Finding leaves the workflow immediately after Phase 2. It gets no Disposition and
appears in the report only under removed false alarms.

**Mechanical Fix** - a fix meeting all three tests:

1. The change is fully determined by the Finding. There is no design choice to make.
2. It touches only the code the Finding points at.
3. It needs no new test and no change to an existing test.

**Judgement Fix** - anything that fails any one of those tests. **When unsure, call it a Judgement
Fix.** Err on the side of caution.

**Code Comment** - a comment in source code. This is *not* a review comment on a pull request.
Phase 6 removes Code Comments only and never touches GitHub.

## Workflow rules

These apply to every phase.

- **Each phase asks before it runs.** Declining skips that phase and moves to the next one. The
  workflow stops only when the user says stop.
- **Use whatever interactive UI is available** for asking and for selecting Findings. Do not make
  the user type "A/B/C" if the harness offers something better.
- **Never pass `--fix` to the built-in `code-review` skill.** It applies every Finding at once,
  which skips the Adversarial Verifier entirely and ignores the Mechanical / Judgement split. That
  one flag collapses this whole workflow. Phases 3 and 5 do their own editing.
- **The state file is the source of truth**, not the conversation. Read it at the start of each
  phase and update it at the end. It has to survive a long session and a context compaction.
- Re-invoking this skill when `.guided-review/findings.md` already exists resumes from the recorded
  state instead of reviewing from scratch. Ask the user which they want.

## State

Everything lives in `.guided-review/` at the repo root:

- `findings.md` - the Changeset and one row per Finding.
- `fixed.md` - Phase 7 report: what was changed.
- `remaining.md` - Phase 7 report: what is left.

Add `.guided-review/` to `.gitignore` in Phase 1 if it is not already there, so a half-finished
review never lands in a commit.

`findings.md` records the Changeset at the top, then a table:

| ID  | Location         | Claim                                  | Verdict | Adjudicator | Disposition | Class      | Files touched |
| --- | ---------------- | -------------------------------------- | ------- | ----------- | ----------- | ---------- | ------------- |
| F1  | `src/auth.py:42` | Token expiry is compared in local time | Upheld  | verifier    | Fixed       | Mechanical | `src/auth.py` |

`Class` is `Mechanical` or `Judgement`, set in Phase 3. `Files touched` is filled in by Phases 3
and 5 and is what Phase 6 uses to find comments this workflow added itself.

## Announce the workflow

Before Phase 1, print this to the user verbatim:

```text
Guided review. Seven phases, and I will ask before each one. Declining skips just that
phase; say stop to end the whole thing.

1. Review        - run the built-in code-review skill and collect Findings.
2. Verify        - attack each Finding with a fresh adversarial verifier and drop the
                   false alarms.
3. Mechanical    - fix the Findings where there is no judgement call to make.
4. Explain       - talk through the Findings that are left. Pick the ones you want.
5. Judgement     - fix the ones you choose.
6. Trim comments - remove stale or needless comments in the source, including any I added.
7. Report        - write up what was fixed and what remains.
```

## Phase 1 - Review

Forward the user's target and effort arguments to the built-in `code-review` skill unchanged. It
accepts a target (current diff, PR number, branch, path) and an effort level. Never add `--fix`.

Create `.guided-review/`, add it to `.gitignore`, and write `findings.md`: the Changeset at the
top, then one row per Finding with `Verdict = Unverified`, `Adjudicator` blank, `Disposition = Open`.

## Phase 2 - Verify

For each Finding, spawn a **fresh sub-agent with no shared context**. This is not optional. A
verifier that inherits the reviewer's context will confirm everything it is shown, which makes the
phase worthless.

Give each verifier exactly one Finding and the code it points at. Instruct it to *disprove* the
Finding: it should assume the Finding is wrong and let the code talk it out of that, not the other
way round.

A Finding is usually wrong because it rests on a false premise. Tell the verifier to name the
premise the Finding depends on and try to break that, rather than arguing with the conclusion.
(Cut this paragraph if it stops helping. The fresh-context requirement above is not cuttable.)

Run the verifiers in parallel. Each returns a Verdict and one sentence of reasoning.

Write each Verdict to `findings.md` with `Adjudicator = verifier`. Show the user the Refuted
Findings and what the verifier said, so they can override any of them. Refuted Findings take no
further part in the workflow.

## Phase 3 - Mechanical Fixes

Applies to Upheld Findings with `Disposition = Open`.

Classify each one as `Mechanical` or `Judgement` using the three tests in the vocabulary, and record
the class. When unsure, `Judgement`.

Fix the Mechanical ones in a single pass, then report what changed. Record `Disposition = Fixed`
and the files touched for each.

## Phase 4 - Explain

Read-only. This phase changes nothing in `findings.md`.

List the Upheld Findings still `Open` (that is, the Judgement ones) and let the user pick which to
have explained. Explain what the Finding means, why it matters here, and what fixing it would
involve.

## Phase 5 - Judgement Fixes

Let the user pick from the Upheld Findings still `Open`, and choose per Finding: fix it, dismiss
it, or defer it.

Fix the chosen ones, then report what changed. Record the Disposition and the files touched. Any
Finding the user does not act on stays `Open`.

## Phase 6 - Trim Code Comments

Source-code comments only. This phase never touches a pull request or anything on GitHub.

Scope: comments inside the Changeset, plus comments this workflow added in Phases 3 and 5 (use the
`Files touched` column). Remove comments that restate what the code already says, that describe
work rather than behaviour ("added this to fix F3"), or that are now stale. Keep comments that
explain *why*.

Show the user the removals before applying them.

## Phase 7 - Report

Write two files and print a short summary in the conversation, so the user does not have to open
anything to learn what happened.

`fixed.md` - every Finding with `Disposition = Fixed`: what it was, what changed, which files.

`remaining.md` - the handoff. `Deferred` Findings first, written so each can become a ticket
without further digging. Then `Dismissed`, with the reason. Then anything still `Open`.

Both files end with a tally: how many Findings the built-in skill reported, how many the verifier
Refuted, and how many Verdicts a human overrode. Read over a few runs, those three numbers say
whether the reviewer is noisy or the verifier is too soft.
