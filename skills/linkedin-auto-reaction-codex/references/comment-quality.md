# LinkedIn comment quality guide

Use this reference when drafting or revising comments.

## Good comment patterns

### 1. Specific observation

Formula:

`The point about [specific idea] matters because [specific implication].`

Example:

`The part about onboarding friction is the key one for me. Small UX delays often look harmless, but they compound into lower activation before a team can even see the product's value.`

### 2. Useful question

Formula:

`How are you thinking about [specific tradeoff] when [condition]?`

Example:

`How are you thinking about measuring quality when the workflow saves time but still needs human review at the final step? That tradeoff is where many AI tools get blurry.`

### 3. Relevant experience

Formula:

`I have seen a similar pattern in [context]: [concrete lesson].`

Example:

`I have seen the same pattern in sales workflows: the bottleneck is rarely the first draft, it is deciding which conversations deserve a thoughtful response.`

### 4. Respectful challenge

Formula:

`I agree with [point], but I would separate it from [adjacent issue].`

Example:

`I agree that consistency matters, but I would separate posting cadence from comment quality. A smaller number of specific comments can outperform a larger generic routine.`

## Bad comment patterns

Avoid comments that could fit almost any post:

- `Great post, thanks for sharing.`
- `Very insightful.`
- `This is so true.`
- `Well said.`
- `Love this perspective.`
- `Could not agree more.`

Avoid fake authority:

- Do not claim personal experience the user did not provide.
- Do not say "we did this at my company" unless the user supplied that fact.
- Do not imply a relationship with the author unless visible or user-provided.

Avoid engagement bait:

- Do not ask readers to DM, comment, like, or follow.
- Do not add irrelevant hashtags.
- Do not promote the user unless the user explicitly requested promotional copy and the post context supports it.

## Rewrite checklist

Before showing the user a comment, verify:

1. It names or implies one specific idea from the post.
2. It adds a consequence, question, example, or tradeoff.
3. It does not contain generic praise as the main value.
4. It can only fit this post or a narrow set of similar posts.
5. It is professional and not argumentative.
6. It is 1 to 3 sentences.
7. It passes `scripts/engagement_ledger.py lint-comment`.

## Drafting with limited context

If only a short post snippet is visible, do not invent details. Use a question or careful observation:

`This seems especially important when [visible condition]. What signals do you use to decide when the process is working well enough to scale?`

If the post is too thin to support a non-generic comment, skip it.
