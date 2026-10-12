# How To Contribute to John's Agent Skills

Read this to understand the process for improving the agent skills in this repo.

## Contributors

- Maintainer: John Cheng (me)
- Maintainer's AI: A coding agent

## Contribution Process

1. I document my process for creating software, i.e., in `JCHENG-SOFTWARE-WORKFLOW.md`.
2. I use agent skills as the tool to model my process and enforce consistency.
3. I record my experiences, ideas, and doubts about my workflow and tools in a `$JOURNAL` system.
4. I periodically review the `$JOURNAL` and create concrete features in a `$TODO` system.
5. I triage the features and implement the most important ones.

## Originals

The `JCHENG-SOFTWARE-WORKFLOW.md` file describes how I view the software development process. It is
a copy of an original I manage elsewhere. The entire design behind this repo is also managed
elsewhere. This repo represents the tools I use to aid in my development process. The actual mental
model behind this repo lives elsewhere -- mostly in my head.

When I make updates to my development process, I start by updating "the originals." Then I ask AI to
update the skills and documentation in this repo to reflect my updated thinking. AI can obtain
additional context about the "source code" of my mental model by reading
`~/.config/jc-agent-skills/development.md`.

## What are `$JOURNAL` and `$TODO`?

The `$JOURNAL` and `$TODO` systems are intentionally vague. They might be markdown or org-mode files
or they might be concrete issue tracking software. The principles are the same: Write down your
experiences, review them, and make changes.

A file at `~/.config/jc-agent-skills/development.md` defines these systems concretely. This is a way
to have different systems on different machines.

### A sample "configuration"

The simplest system for recording experiences and managing a to-do list is just using files. Here is
a sample configuration.

```text
# Developing jc-agent-skills

Private, per-machine notes for working on `~/privprjs/agent-skills`.

- **To-do system:** `<some path>/TODO.md`.
  Planned improvements to the skills and to John's software engineering workflow.
- **Originals:** `JCHENG-SOFTWARE-WORKFLOW.md` and `FORMALIZING-WORKFLOWS.md` in
  `~/Documents`. These are the source of
  truth and the only copies John edits. When John is ready to publish changes, we should copy the
  originals into the repo; `git diff` then shows what changed.
- **Journal system:**
  `<some path>/journals/`, one file per
  skill per month. John's experiences using each skill, newest entry first.
```
