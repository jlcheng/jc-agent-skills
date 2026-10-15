---
name: implement-understand
description: Explain key implementation decisions and tradeoffs beyond the approved tech spec. Use when explicitly invoked or delegated the Understand step by implement.
disable-model-invocation: true
---

# Implement Understand

Use the shared run directory and follow the
[persistent record guide](../implement/references/records.md). Record the Understand step and create
`understand.md` when this step begins.

Read the spec and implementation. Produce a simple report explaining key implementation decisions
and tradeoffs that the spec did not already anticipate. Use current user guidance and your judgment
to choose what deserves attention and how much explanation it needs. Ground the explanation in the
actual implementation; if there are no material decisions beyond the spec, say so.

Save the report in `understand.md` and present it to the user. Allow follow-up discussion and save
material clarifications as they arise. This initial version does not learn or store preferences
across runs.
