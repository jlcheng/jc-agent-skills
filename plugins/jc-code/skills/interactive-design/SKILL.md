---
name: interactive-design
description: Walk the user from a fuzzy idea to a short written design they can hand off for building. Use when the user invokes it, or when a small-to-medium build request is fuzzy, such as one that leans on a reference or a feeling, describes an outcome without a mechanism, or names a conventional solution without the problem behind it. Do not use when the request is already clear enough to build, or for planning a whole project.
---

# Interactive Design

This skill implements the process described in `The Interactive Design Process.md`. If
that file is in reach and disagrees with this skill, the essay wins.

The skill is a model of the user's workflow. It guides them through the workflow so they build things
the same way each time. It ends with a short written result saved in the repo. Building comes
afterward, usually by an AI, and is not part of this skill.

## What, not how

Each step below says what it must produce and where the user checks in. It never says how to get
there. Interview, sketch, compare, or look things up however works best. Prescribing technique would
lock in today's guess, so use your judgment.

## Three tiers, by how clear the thing is

- **Clear -> Build.** No interview. Not this skill.
- **Fuzzy -> Interactive Design.** Small to medium. This skill.
- **Unknown -> Complex project.** Large and uncertain. Handled separately. Not this skill.

## Progress bar

Show the user where they are with one line over steps 2 to 7. Start it with a "Progress:" label and
mark every step: ✓ finished, ● current (also bold), ○ not started:

Progress: ✓ Size up › ● **Interview** › ○ Names › ○ Consequences › ○ Draft › ○ Save

Show it at Dispatch and again each time the step changes, so the user always knows where they are
and what is left, stays consistent with their own workflow, and can object if the job is in the wrong
place. One line is cheap enough to repeat. Mark a skipped step as skipped.

## Steps

### 1. Invoke

The user invokes the skill with a description of the thing, or the skill starts on its own because a
request looks fuzzy. Starting on its own is fine because Dispatch comes next and acts as the brake.

### 2. Dispatch

**Produces:** a sizing of the job (clear, fuzzy and small to medium, or unknown and large) with the
reason, the progress bar, and the question *Is this the workflow you want?* Stating the sizing lets
the user object if the job is in the wrong tier.

**Check-in:** wait for the answer. If the user says no, or the job is clear or large, step out of
this workflow. Say whether it looks ready to build or like a complex project, and stop guiding.

### 3. Interview

**Produces:** the thing is clear enough to write down.

Read `kinds-of-interviews.md` before starting. It describes four kinds of help users may need. The
user often doesn't know which kind they need and won't say. One kind may lead into another. Finding
facts in the codebase or environment is your job. Don't ask the user for what you can look up.

**Check-in:** throughout, as the interview goes.

### 4. Confirm domain vocabulary

**Produces:** agreed names for the things in the design, in the user's terms. This is almost always
needed, whatever kind of interview came before.

**Check-in:** the user confirms the names. The written result uses them.

### 5. Surface consequences

**Produces:** answers to the few high-impact questions about what the decisions commit the user to.
Ask only those. Box-ticking questions waste the user's attention.

You decide whether this step is worth running. If you skip it, say so. The user can always skip it
("I don't care about these"), and they should know they can.

**Check-in:** the user answers or skips.

### 6. Written result

**Produces:** a draft in chat that follows `written-result.md`: a summary of at most four sentences,
then details, decisions, and what is not in scope. It is a document the user will come back to, so
it uses the confirmed vocabulary and stands on its own without this conversation.

**Check-in:** the user reviews it. Revise until they are satisfied.

### 7. Save

**Produces:** the written result saved in the repo. There is no fixed location. Suggest one that fits
the repo's conventions.

**Check-in:** the user approves or edits the location before you write the file. After saving, the
skill is done. Building comes next, outside this skill.
