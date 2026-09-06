# Trying guided review

The bundled inputs are fictional, AI-generated Reviews. Their Targets supply
scenario facts; their code paths do not exist. Machine claims can be wrong, and
the resumed example includes fictional prior human decisions.

Each session needs only the skill and its input files. No context from the
development conversation is required. The skill copies test inputs to a new
working file, preserving them for another run.

With the plugin installed, invoke `/jc-code:guided-review` and ask to test using
the bundled `assets/retry-client.json`, resolved relative to the skill directory.
Without installing, paste this in a fresh session with access to a local clone,
replacing `<repo-root>` with the absolute path of that clone:

```text
Read <repo-root>/plugins/jc-code/skills/guided-review/SKILL.md and follow it.
Let me test this skill using <repo-root>/plugins/jc-code/skills/guided-review/assets/retry-client.json.
Begin the guided review and use the default storage location.
```

Default storage for fictional tests is
`~/.jc-guided-review/fictional-tests/<date>-<description>-<unique-suffix>.json`.
Real Reviews use the reviewed repository's root directory name instead of
`fictional-tests`. You can request an explicit output path for a test. Keep the
reported working path to resume in another session with the same skill.

Available inputs:

- [retry-client.json](../assets/retry-client.json): all Pending; machine disagreement,
  a response to the challenger, and machine advice to dismiss a valid Finding.
- [account-deletion.json](../assets/account-deletion.json): important Findings with
  risky remediation and missing context.
- [resumed-review.json](../assets/resumed-review.json): fictional prior human
  judgments, machine disagreement with a human decision, and one Pending Finding.

Try selecting several Findings: each should open as a detailed card, one at a
time. The full table should appear at the start and end, or on request. Between
Findings, expect a decision confirmation and remaining count. A reply to a
challenger should lead with its agreement or disagreement before its reasoning.

"Skip" leaves a Finding Pending. "Valid, dismissed" records a valid Finding with
no action recommended. "Stop" leaves the Review active. Once all Findings have
human judgments, confirming completion updates the same file to `completed`.
No fixes are performed as part of these sessions.
