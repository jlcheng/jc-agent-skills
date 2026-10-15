---
name: implement
description: Coordinate an approved tech spec through building, review, and understanding. Use when explicitly asked to start or resume this implementation workflow.
disable-model-invocation: true
---

# Implement

This is a template skill: it defines the workflow and delegates each step to an overridable skill.
An override means editing that step's skill instructions directly. There is no inheritance or
separate override loader. Invoking this workflow authorizes using its three explicit-only step
skills below.

## Start or resume

Identify the approved tech spec, target repository root, and implementation scope from the request
and available context. Ask only for information needed to proceed. Follow the
[persistent record guide](references/records.md) to create or resume the run before building.
Report the absolute run directory and make the current step and any pending decision clear.

## Workflow

Read and follow each step's current instructions when reaching it; let that skill determine how to
complete its step. Pass along the approved spec, target repo, implementation scope, shared run
directory, and enough state to continue.

1. **Build:** use [implement-build](../implement-build/SKILL.md).
2. **Review:** use [implement-review](../implement-review/SKILL.md). Complete resolution and the
   user's decision about another review round before advancing.
3. **Understand:** use [implement-understand](../implement-understand/SKILL.md). Allow follow-up
   discussion and save material clarifications.

Keep `review.md` current at step transitions and user decisions so another session can resume.
Resume from the saved state rather than rerunning completed work. Mark the workflow complete after
Understand's report is saved and the requested discussion is handled; report the record paths.

This initial version keeps run records, not preference memory. Commits, publication, and deployment
are outside this workflow's automatic actions.
