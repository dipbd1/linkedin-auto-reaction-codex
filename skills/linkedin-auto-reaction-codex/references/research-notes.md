# Research notes behind the workflow

This skill was designed from four categories of guidance.

## LinkedIn platform constraints

LinkedIn's current public rules and help materials warn against unauthorized third-party software, bots, browser extensions, scraping, automated activity, and inauthentic engagement. Public help pages also describe possible account restrictions for automated activity, high-volume content sharing, excessive page views, excessive invitation requests, and repetitive/irrelevant comments.

Design implication:

- Keep the workflow human-in-the-loop.
- Use visible UI only.
- Do not use hidden APIs, scraping, stealth, proxies, CAPTCHA-solving, or bulk activity.
- Stop on warnings or restrictions.

## Codex Chrome reliability

The native Windows and macOS Codex apps can operate the user's signed-in Chrome browser through the Codex Chrome plugin/extension, with `@computer` available for OS-level fallback. This is the required browser surface for this skill because it can reuse the user's visible Chrome session and existing LinkedIn login instead of launching a separate automation-only browser.

Design implication:

- Use the Codex Chrome plugin/extension for normal page work and `@computer` only for native UI fallback.
- Prefer the currently selected/logged-in Chrome tab.
- Inspect DOM snapshots or screenshots after every UI change.
- Prefer role/text/label locators.
- Do not hard-code LinkedIn DOM classes or generated ids.

## Forum and practitioner patterns

Recent practitioner discussions about LinkedIn automation repeatedly emphasize that fully automated engagement creates account and brand risk, while discovery + drafting + human review is more useful. Common failure modes include generic AI comments, repeated timing/action patterns, weak targeting, and treating automation as a substitute for judgment.

Design implication:

- Automate scanning and drafting, not judgment.
- Use a ledger to prevent duplicates.
- Use small session budgets.
- Score relevance before drafting.
- Reject generic comments.

## Token efficiency findings

Small/medium models perform better with a strict state machine, compact candidate rows, deterministic local checks, and no long post transcripts.

Design implication:

- Process one viewport at a time.
- Keep only a 220-280 character digest per post.
- Use skip codes.
- Show at most 3 approval cards.
- Use the local ledger and linter for repeatable decisions.
