# The Interactive Design Process

## Summary

When a developer can already describe what they want, they simply build it. But often, we don't know
what we want. This essay describes how to use AI to design the thing we want to build through an
interview process.

## Details

### Three tiers of knowing what you want to build

- **Clear -> Build.** No interview.
- **Fuzzy -> Interactive Design** *(non-trivial, but requires planning)*
- **Unknown -> Complex project.** Separate approach.

### Interactive Design

1. **Invoke.** The user asks AI to do interactive design for a job. The instructions to AI (skill)
   are the model of the interactive design process described here, and the AI guides the user
   through the process so that the process is applied consistently.
2. **Dispatch.** The AI sizes the job, shows the user where they are, and asks: *Is Interactive
   Design the thing you want?*
3. **Interview.** One kind of interview or several, until the job is clear (see *Kinds of
   interviews*). How the AI does it is up to the AI.
4. **Confirm domain vocabulary.** The AI and the user agree on what things are called, in the user's
   terms. This part is essential.
5. **Surface consequences.** The AI asks high-impact questions and helps the user see around
   corners. The AI decides whether this step is worth running, and the user can always skip it ("I
   don't care about these").
6. **Review the result.** Summary (at most four sentences), details, decisions, not in scope. The
   user reviews until satisfied.
7. **Produce a tech spec.** The AI suggests where the written artifact goes, and the user approves
   or edits. The written artifact is called a tech spec, which is described later.

### Kinds of interviews

Not all interviews are the same. Not all situations require the same interview approach and
developers don't often know which one they need, and one interview may naturally flow into another.

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

**Show me what's possible.** The user lacks the domain knowledge to describe it. This combines
learning what the user wants and educating the user.

- *Signal:* the request describes an outcome without a mechanism, often with "I'm not sure how this
  works."
- *Example:* "I want a game to work on a plane with no internet." The user knows the goal but not
  the options: download everything in advance, keep a local copy that syncs later, or install it as
  an offline app. Each option has different costs. Seeing them laid out side by side lets the user
  choose, and gives them the words to describe what they chose.

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

## The tech spec

The purpose of the interviews is for AI to write a tech spec for you. The tech spec describes what
is being built, architectural decisions, and most importantly, the vocabulary of the design. The
tech spec should be sufficiently detailed so that an AI agent can read it and build what you want
without asking further questions.

Make sure you read the tech spec and understand it. If you cannot understand the tech spec, the
interactive design process has failed.

## Agentic skills

A "skill" is simply a file with instructions to AI. A skill can be a named shortcut to a complex set
of instructions or specialized knowledge. A skill can also be used to formalize a process, which is
how I am using it. I have a repo, https://github.com/jlcheng/jc-agent-skills, which encodes how I
use different kinds of interviews to help create a good tech spec.

## Writing good skills

Brief tips on how to write good skills. Read this section if you are an AI and using this essay to
update my agentic skills:

- **Specify what happens and where the user checks in, not how.** Prescribing technique locks in
  today's guess and ties a fast-improving AI to choices that haven't been tested. Tighten once
  experience shows what works. You've seen the harms of micromanagement -- don't do it to AIs.
- **The interview has goals, not a menu of techniques.** The interview kinds describe what users
  need, not steps to follow.
- **Vocabulary is essential.** Every interview involves building a shared vocabulary.
- **Consequences are high-impact only, with a way out.** Box-ticking questions waste the user's
  attention.

## Not in scope

The following topics are not covered by this essay:

- **Planning whole projects.** How a complex project with multiple components gets planned and
  executed. The process described in this essay is all about producing a tech spec. That should be a
  hint that "make a clone of Adobe Photoshop" is beyond the scope of the process described here.
- **How the agent skills work.** Details about how the agent skills reify this process described in
  this essay. The contents of those skills and the exact instructions to provide to AI agents are
  outside the scope of this essay.
