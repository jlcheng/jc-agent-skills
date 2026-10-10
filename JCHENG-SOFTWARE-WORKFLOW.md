# JCheng's Software Building Workflow — v1.0

## Summary

When the user can already describe what they want, they build it. When it's fuzzy and small to
medium, they invoke a skill that walks them through this workflow: the AI sizes the job, shows where
they are, interviews them until the thing is clear, confirms the names for things, and raises the
consequences that matter. The result is a short written document, reviewed in chat and saved in the
repo, which the user usually hands to an AI to build. Large, uncertain projects are handled
separately.

## The workflow graph

We can think of a workflow as a graph, which we will refer to as **the workflow graph** from now on.
Each step is a node, and the arrows are the moves between steps. Unlike a checklist, the graph has
branches (which tier a request goes to, whether consequences get skipped) and loops (one kind of
interview leading into another, revising the written result until the user is satisfied). "You are
here" marks the current node. The AI shows the workflow graph at Dispatch so the user can see where
the job sits, stay consistent with their own workflow, and object if the job is in the wrong place.

```
                         request
                            │
        ┌───────────────────┼───────────────────┐
      Clear               Fuzzy              Unknown
        │                   │                   │
      Build            1. Invoke         Complex project
                            │              (separate)
                       2. Dispatch ── not this workflow ──► Build or Complex project
                            │
                       3. Interview ◄──┐  kinds lead into
                            │  └───────┘  each other
                       4. Confirm domain vocabulary
                            │
                       5. Surface consequences   (AI may skip; user can always skip)
                            │
                       6. Written result ◄──┐  revise until
                            │  └────────────┘  satisfied
                       7. Save
                            │
                          Build   (afterward, usually by an AI)
```

## Details

### Three tiers, by how clear the thing is

- **Clear -> Build.** No interview.
- **Fuzzy -> Interview First** *(small to medium; name TBD)*
- **Unknown -> Complex project.** Separate approach.

### Interview First

1. **Invoke.** The user invokes the skill with a description of the thing. The skill is the model of
   the user's workflow and guides them through it so they build things consistently.
2. **Dispatch.** The AI sizes the job, shows this workflow graph with "you are here," and asks: *Is
   this the workflow you want?*
3. **Interview.** One kind of interview or several, until the thing is clear (see *Kinds of
   interviews*). How the AI does it is up to the AI.
4. **Confirm domain vocabulary.** The AI and the user agree on what things are called, in the user's
   terms. Almost always needed.
5. **Surface consequences.** The AI asks only the high-impact questions about what the decisions
   commit the user to. The AI decides whether this step is worth running, and the user can always
   skip it ("I don't care about these").
6. **Written result.** Drafted in chat: summary (≤4 sentences), details, decisions, not in scope.
   The user reviews until satisfied.
7. **Save.** The AI suggests where it goes in the repo, and the user approves or edits.

### Kinds of interviews

What users may need. They often don't know which, won't say, and one may lead into another. The
examples help illustrate each kind, not a technique for meeting it.

**Fill in from context.** The answer is mostly in the codebase and earlier decisions.

- *Signal:* the request is short and refers to things the project already has.
- *Example:* "Add a login page." The repo already has a session library, form components, and a
  route convention. The interview is mostly confirmation: "I'll reuse the existing session handling
  and the settings-page form style. The one open question is passwords or magic links?" This kind is
  closest to the Clear -> Build tier, and it often ends after one or two questions.

**Help me recognize it.** The user knows it when they see it, but has a hard time naming it.

- *Signal:* the request uses a reference, a feeling, or "that thing that..." instead of a
  specification.
- *Example:* "Make it look like the old Macs, 90s or early 2000s." That covers at least two very
  different looks: the gray, beveled 90s style and the glossy, translucent early-2000s style.
  Showing both gets "that one" in seconds, where describing it would have taken several rounds. The
  result then needs a name the user will use later, which happens with the domain vocabulary.

**Show me what's possible.** The user lacks the domain knowledge to describe it.

- *Signal:* the request describes an outcome without a mechanism, often with "I'm not sure how this
  works."
- *Example:* "I want the kids' game to work on a plane with no internet." The user knows the goal
  but not the options: download everything in advance, keep a local copy that syncs later, or
  install it as an offline app. Each option has different costs. Seeing them laid out side by side
  lets the user choose, and gives them the words to describe what they chose.

**Check whether the ask is a stand-in.** What the user asked for may be standing in for what they
actually want.

- *Signal:* the request names a conventional solution ("a dashboard," "add caching," "a settings
  page") without the problem behind it.
- *Example:* "Build me a dashboard for our metrics." A few questions in, the real need turns out to
  be a list of which experiments are running, because they're scattered across documents. That's a
  different thing, a smaller one, and much more useful. *(This example is from Addy Osmani's
  interview-me skill.)*

**How they lead into each other**

- *Recognize -> fill in from context.* Once the user picks the gray 90s look, the AI checks what the
  codebase already has (fonts, styles) and asks only about what's missing.
- *Show what's possible -> stand-in.* While comparing offline options, the user realizes the real
  need is "works on the road trip next month." Downloading everything in advance is enough, and
  syncing is out of scope.
- *Stand-in -> any of the others.* Once the real ask is found, the interview restarts with whichever
  kind fits the real ask.

## Decisions

- **Show the workflow graph first.** It keeps the user consistent with their own workflow. Showing
  "you are here" invites them to object without being asked.
- **Specify what happens and where the user checks in, not how.** Prescribing technique locks in
  today's guess and ties a fast-improving AI to choices that haven't been tested. Tighten once
  experience shows what works.
- **The interview has goals, not a menu of techniques.** The kinds describe what users need, not
  steps to follow.
- **Vocabulary and consequences are their own steps.** They apply across every kind of interview.
- **Consequences are high-impact only, with a way out.** Box-ticking questions waste the user's
  attention.
- **The written result is a document the user comes back to.** Results live in the repo, with no
  fixed location.

## Not in scope

- Planning whole projects
- Prescribing how sketches look for UIs, APIs, CLIs, etc.
- A fixed rule for where results go in the repo
- Building, which comes afterward
