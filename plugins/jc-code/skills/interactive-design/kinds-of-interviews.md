# Kinds of interviews

These are what users may need from the interview. Users often don't know which kind they need, won't
say, and one kind may lead into another. The examples show what each kind is. They are not a
technique for meeting it.

## Fill in from context

The answer is mostly in the codebase and earlier decisions.

- *Signal:* the request is short and refers to things the project already has.
- *Example:* "Add a login page." The repo already has a session library, form components, and a
  route convention. The interview is mostly confirmation: "I'll reuse the existing session handling
  and the settings-page form style. The one open question is passwords or magic links?" This kind is
  closest to the Clear -> Build tier, and it often ends after one or two questions.

## Help me recognize it

The user knows it when they see it, but has a hard time naming it.

- *Signal:* the request uses a reference, a feeling, or "that thing that..." instead of a
  specification.
- *Example:* "Make it look like the old Macs, 90s or early 2000s." That covers at least two very
  different looks: the gray, beveled 90s style and the glossy, translucent early-2000s style.
  Showing both gets "that one" in seconds, where describing it would have taken several rounds. The
  result then needs a name the user will use later, which happens when confirming domain vocabulary.

## Show me what's possible

The user lacks the domain knowledge to describe it.

- *Signal:* the request describes an outcome without a mechanism, often with "I'm not sure how this
  works."
- *Example:* "I want the kids' game to work on a plane with no internet." The user knows the goal but
  not the options: download everything in advance, keep a local copy that syncs later, or install it
  as an offline app. Each option has different costs. Seeing them laid out side by side lets the user
  choose, and gives them the words to describe what they chose.

## Check whether the ask is a stand-in

What the user asked for may be standing in for what they actually want.

- *Signal:* the request names a conventional solution ("a dashboard," "add caching," "a settings
  page") without the problem behind it.
- *Example:* "Build me a dashboard for our metrics." A few questions in, the real need turns out to
  be a list of which experiments are running, because they're scattered across documents. That's a
  different thing, a smaller one, and much more useful. *(This example is from Addy Osmani's
  interview-me skill.)*

## How they lead into each other

- *Recognize -> fill in from context.* Once the user picks the gray 90s look, the AI checks what the
  codebase already has (fonts, styles) and asks only about what's missing.
- *Show what's possible -> stand-in.* While comparing offline options, the user realizes the real
  need is "works on the road trip next month." Downloading everything in advance is enough, and
  syncing is out of scope.
- *Stand-in -> any of the others.* Once the real ask is found, the interview restarts with whichever
  kind fits the real ask.
