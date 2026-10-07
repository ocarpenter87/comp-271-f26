# COMP 271 Tools: How Feedback Works in This Course

This folder holds a self-check tool you can use on your own work
(`comp271_self_check_agent.md`), and this note explains the thinking behind it and behind how
your submissions are reviewed. I would rather you see how the process
works than wonder about it.

## The short version

- Your work is read by an AI assistant that I direct, and **I make the
  editorial decisions**. The assistant drafts; I decide what matters.
- Feedback is **qualitative**. There are no scores or letter grades in it.
  That is deliberate, and it follows the ungrading approach described in
  the course policies.
- Feedback is aimed at **learning**, not at penalizing. A mistake is how
  learning shows up, and feedback exists so the same mistake does not
  repeat.

## How a submission is reviewed

Review happens in two phases.

1. **Whole-class read first.** Before anyone gets individual comments,
   the assistant reads every submission and looks for patterns: mistakes
   several people share, unusual problems, missing or unreadable files.
   It reports those to me. It does not write individual feedback yet.
2. **My guidance, then individual feedback.** I read that report and tell
   the assistant what I think matters. Only then does it draft individual
   comments, and my guidance overrides its own read where the two differ.
   Afterwards I send the whole class an anonymous technical note covering
   the common issues. No names appear in it.

Why two phases? Judging a submission in isolation makes it easy to
mistake a common confusion (often a sign that *I* explained something
poorly) for an individual failing. Seeing the whole class first helps me
separate the two.

## What the feedback is supposed to look like

- **Specific to you.** Every point should quote a line, value, or error
  message from your own work. Generic comments that could apply to anyone
  are treated as a defect.
- **Something you did well first**, named specifically, not generic
  praise.
- **Then the mistake, the reason it is a mistake, and what to do
  differently.** Explaining the *why* is the point.
- **Held to what we have covered.** Your work is judged against what the
  course had actually taught by the submission date, not against style
  rules in the abstract or ideas from later weeks.
- **Honest.** Warm does not mean vague. If something is missing or does
  not work, the feedback says so plainly.
- **Never invented.** If a file cannot be read, it is flagged to me
  instead of guessed at, and I follow up with you.

## What is specific to COMP 271

Here the substance is design: classes, encapsulation, and keeping a data
structure's own invariants true (for example, that a size field stays
accurate through every add, remove and resize). Feedback assumes your
basic programming mechanics are solid and focuses on where an invariant
breaks, naming the method and line. If a test file ships with the
assignment, feedback notes whether you pass it, but explains *why* a
failing test fails rather than just reporting it. Repo-wide style rules
(named constants for literals other than `0`, `1`, `-1`, and a single
`return` per method) apply in full.


## About the self-check tool

`comp271_self_check_agent.md` gives you the same kind of feedback before you submit. It is
built on the same principles, with one addition: **it will not write the
solution for you.** It points to where something is wrong and why, and
leaves the fixing to you. It gives no score, and it is not the review
your submission receives; that is separate.

Suggested use: finish an honest attempt, run the tool, revise, then
submit. If the tool and I ever disagree, I am the one to ask. Come to
office hours or email me.

## Limits, stated plainly

AI assistants make mistakes. They can misread code, misjudge a
derivation, or sound sure while wrong. Treat the self-check as a
knowledgeable classmate rather than an authority. If feedback seems
wrong to you, say so; that is useful information for me.
