---
name: implement-review
description: Review an implementation against its approved tech spec using fresh finding and challenge contexts, then resolve findings. Use when explicitly invoked or delegated the Review step by implement.
disable-model-invocation: true
---

# Implement Review

Use the shared run directory and follow the
[persistent record guide](../implement/references/records.md). Record the Review step and the scoped
implementation version before starting a round.

## Generate findings

Delegate to a fresh agent context to review maintainability, security, correctness against the
approved spec, and over-engineering. Supply the spec, target repo, implementation scope and reviewed
version, review lens, and shared run directory. Let the reviewer inspect surrounding code.

Do not inherit the builder's conversation or provide its summary or reasoning history. Review
agents inspect the implementation without changing it. Persist every finding and its supporting
evidence in the round's section of `review.md`, with stable IDs, before proceeding to challenge.

## Challenge findings

Use another fresh context, separate from the builder and finding generator, to challenge the saved
findings against the spec and actual code. Supply the same review inputs plus the original findings
and evidence. Exclude builder reasoning, conversation history, and the understanding report from
both passes; provide relevant excerpts rather than the full workflow record.

Save each finding's challenge assessment and arguments. Retain all findings and assessments in the
record. Exclude clearly rejected false positives from the actionable report; bring unresolved
disagreements to the user with both arguments. The later assessment does not settle a disagreement
merely by being later.

If fresh contexts are unavailable, record the pending pass and explain what is needed to continue.
Do not substitute a reread in the builder's context for either independent pass.

## Produce an actionable report

For each actionable finding provide:

- Claim, location, evidence, and concrete consequence.
- Recommended attention level and reasoning.
- Whether an autonomous fix is appropriate, with reasoning.
- Relevant disagreement from the challenge pass.

Attention and suitability for autonomous fixing are separate judgments: a serious issue may need a
user choice, while a minor issue may have a clear remedy. Save the report in `review.md` and present
it clearly to the user.

## Resolve findings

Fix issues with clear remedies that follow from the spec and current instructions. Check applied
fixes and record their results. Reassess affected findings if the implementation changes during the
round so evidence and dispositions still describe the reviewed code.

When resolution requires choosing between reasonable alternatives, explain the finding, options,
and recommendation, then ask the user. Present one decision at a time; related findings may share a
decision. Prioritize choices that unblock other work. Record decisions and each finding's
disposition, including rejected or deliberately deferred findings. Unresolved disagreements require
the user's decision before resolution.

## Complete the round

A round finishes when every finding has a recorded disposition and every applied fix has been
checked. Ask whether the user wants another review round before proceeding to Understand, even if
the round found no actionable issues. Save the pending question and the user's answer.

If requested, start another round in the same `review.md`, preserving prior rounds and identifying
the new reviewed version. Otherwise hand the result back to the coordinator for Understand, or end
the directly invoked review with its record path.
