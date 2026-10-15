# Persistent records

All four implementation skills share this record contract. Use the run directory supplied by the
coordinator. When a step is invoked directly, establish the approved spec, target repo, and scope,
then create or resume a run using the same rules.

## Location and identity

Store records outside the target repo:

```text
~/.jc-implement/<repo-name>/<run-id>/
  review.md
  understand.md
```

Use the target repository root directory's name for `<repo-name>`. Create a unique, readable run ID,
such as `2026-10-15-token-refresh-a1b2c3`, and report its absolute directory. Never overwrite another
run. When asked to continue, use the existing run directory and verify its recorded identities;
repositories with the same directory name are distinguished by their absolute paths.

Create `review.md` at the beginning of the run. Record:

- Target repo and tech spec absolute paths, plus the approved implementation scope.
- Enough version information to identify the spec, implementation, and each reviewed state. For Git,
  include relevant commits or ranges and working tree changes, including untracked implementation
  files. Record material changes to the spec or scope.
- Current step, completed work and checks, next action, and any pending user decision. Keep enough
  Build state here for another session to resume unfinished implementation.

Update records as work, assessments, decisions, fixes, and checks occur, not just at the end of the
conversation. All participating agents use the same run directory. Give fresh review contexts only
the inputs for their pass; the full record may contain builder reasoning they must not receive.

## Review rounds

Keep each round separately within `review.md`, preserving previous rounds. Use stable finding IDs
that remain unambiguous across rounds, such as `R1-F1`. For each round retain:

- Reviewed scope and version, all original findings and supporting evidence.
- Challenge assessments and arguments, including rejected findings and unresolved disagreements.
- The actionable report: claim, location, evidence, consequence, recommended attention with reasons,
  autonomous-fix suitability with reasons, and relevant disagreement.
- User decisions, each finding's disposition (including rejection or deliberate deferral), applied
  fixes, and their checks. A finding awaiting a choice remains pending.
- The user's decision about another round.

Persist findings before the challenge pass receives them. Rejected false positives remain in the
record while being excluded from the actionable report.

## Understanding

Create `understand.md` when Understand begins. Identify the target repo, spec, scope, and implemented
version, and save the understanding report and material clarifications from follow-up discussion.
Keep workflow status and pending decisions in `review.md` throughout this step as well.
