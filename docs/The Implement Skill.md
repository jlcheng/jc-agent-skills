Read this to understand how to use skills to implement a tech spec.

## The Implementation Phase
My software development process looks roughly like this:

1. Write a tech spec. I use my `interactive-design` skill to organize my thoughts. The AI becomes a design partner who interviews me and organize my thoughts. It then generates a tech spec that can be given to an coding agent to build something. Always read the generated tech spec to make sure it is correct. 
2. Build and review
	1. Implement the tech spec: You give the tech spec to an AI coding agent, preferably in a new session, and tell it to start implementing.
	2. Review the changes: Once the coding agent says it is done with implementation, you should ask a new agent to review the generated code.  
3. Understand. Have a coding agent create a report of the generated software. The report will have an overview of the key decisions that AIs made during Phase 2. You should walk away with an understanding of the trade-offs made by the AI and the AI should learn what kind of feedback is important to you.

## The implement skills
I created the `implement` skill to apply this workflow consistently. The `implement` skill dispatches work to other skills so each step can be overridden.

* `implement` - The skill template. It describes the build, review, and understand steps. It dispatches how to build, review, and understand to other skills.
* `implement-build` - Instructions for building. In my experience these instructions can be simple, e.g., "Read the tech spec and build it."
* `implement-review` - In my experience, this skill requires the most customization. It needs to know what is the right review effort for you and it needs to know when it can fix a finding autonomously and when it needs your feedback.
* `implement-understand` - Create a report to help you understand the implementation. It should learn how you like changes explained.


## An initial version of the implement skills

I think the initial version of these skills should look like this:

* implement-build: very simple
* implement-review: 
	* Look at the change and determine the expected effort for reviewing it. Recall the effort expectations for a particular codebase: Different codebases have different maintainers and thus different expectations on how to review. This means the skill should create a file (or files?) somewhere to track effort expectations for different repos.
	* For the initial version, assume we want an AI agent with a new context to review the code for maintainability, security, correctness-vs-spec, and over-engineered code. The AI Agent should be given the tech spec and a description of the review lens.
	* Perform the review.
	* De-noise: Get rid of the false positives from reviews. This should be done by a new agent with a new context, in a separate pass. This is the adversarial verification of the generating findings.
	* Generate a report: Organize the findings into an actionable report. A report has a list of findings and AI-generated recommendations on the attention level of each finding and whether it should be autonomously fixed.
	* Review the report and decide what to fix. For findings that require the user's attention, explain the finding to the user and find out how it should be fixed.
	* After all findings have been resolved, ask the user if the review process should be repeated again
	* Update relevant "memory" file or files
		* Record, for the given repo, what the user's preferences were for effort, what kind of findings require human attention
* implement-understand: keep this simple, describes the key decisions made by the implementations that was not anticipated in the tech spec. Use a memory file to learn what kind of understanding the user prefers.