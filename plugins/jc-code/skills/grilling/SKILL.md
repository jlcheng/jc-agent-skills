---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

# Vocabulary

The **design tree** is the model of the subject: decisions with decisions hanging off them. The
**frontier** is the set of decisions whose prerequisites are all settled — the only questions that
can honestly be asked yet. A **round** is one frontier, asked in full and answered in full.

# The Skill

Interview the user relentlessly until you reach a shared understanding. Do not ask questions for the
sake of questions. The purpose of the questions is to reach a shared understand. If you believe
there is a shared understanding, state it instead of asking questions for effect.

Map this as a **design tree**: every decision branches into the decisions that hang off it. Work the
tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the
questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole
frontier in one round: number each question and give your recommended answer. Then wait for the
user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and
unblock questions that depended on them. Recompute the frontier and ask the next round. A question
whose answer depends on another question still open in this round belongs to a _later_ round, not
this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the
environment (filesystem, tools, etc.). Don't ask the user for anything you could find yourself.
Dispatch sub-agents for fact-finding as necessary and consider asking other questions while the
sub-agents are looking for facts in the background.

The session is done when the frontier is empty: every branch of the design tree visited, nothing
left silently assumed. Restate the shared understanding in your own words back to the user.
