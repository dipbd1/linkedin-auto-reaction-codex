---
name: linkedin-auto-reaction-codex
description: Human-in-the-loop LinkedIn engagement workflow for the native Windows or macOS Codex app using the user's machine browser through @browser or @computer. Use when asked to review LinkedIn feeds, search results, profile activity, company pages, or post URLs; identify relevant posts; avoid duplicate reactions or comments; draft contextual comments; and perform only explicitly approved visible UI actions through the logged-in browser session.
---

# LinkedIn Auto Reaction Codex

## Core behavior

Use this skill to assist a LinkedIn engagement session in the native Windows or macOS Codex app. Operate through the user's machine browser with `@browser` when available, and use `@computer` only when native UI interaction is needed. Prefer the user's existing logged-in browser session when available.

Default to **review and draft mode**. Do not publish comments, send messages, connect, follow, repost, share, scrape, bypass limits, solve CAPTCHAs, or perform bulk activity. Only click a final reaction or submit a comment after the user explicitly approves that exact post and action in the current conversation.

## Safety and platform rules

LinkedIn restricts unauthorized automation, scraping, automated engagement, and inauthentic activity. Therefore:

1. Use the visible LinkedIn UI in the user's machine browser only, controlled through `@browser` or `@computer`.
2. Prefer the currently selected browser tab/session when it is already logged in.
3. If LinkedIn is not logged in, ask the user to log in manually in the browser. Never request credentials.
4. Keep a human in the loop for every final engagement action.
5. Stop immediately on CAPTCHA, verification, warning, restriction, unusual activity, blocked action, login challenge, or rate-limit notice.
6. Never use stealth, proxy, fingerprint evasion, hidden APIs, Voyager endpoints, copied cookies, extensions, or direct HTTP calls to LinkedIn.
7. Never collect or export profiles, contacts, email addresses, messages, connection lists, or large post datasets.
8. Never run infinite scrolling or high-volume traversal. Use the session budget below.
9. Do not produce generic, repetitive, misleading, harassing, discriminatory, political-ad-like, or engagement-bait comments.

If the user asks for fully autonomous liking/commenting, switch to assisted mode: discover candidate posts, draft comments, show approval cards, and ask for explicit approval before each final action.

## Session budget defaults

Unless the user provides stricter limits, use these maximums per session:

- review at most 20 visible posts
- draft at most 5 comments
- approve or perform at most 3 reactions
- approve or perform at most 2 posted comments
- avoid more than 1 engagement action for the same author per session
- stop after 3 consecutive low-relevance screens

These are not LinkedIn rate limits. They are conservative workflow limits to prevent spammy behavior and token waste.

## Operating loop

1. **Setup**
   - Use `@browser` to open or attach to LinkedIn in the user's default machine browser.
   - Use `@computer` only when `@browser` cannot access or operate the needed visible browser UI.
   - Reuse the selected/current browser tab if it is already on LinkedIn or already logged in.
   - Open only the target LinkedIn feed, search, hashtag, company, profile activity, or post URL supplied by the user.
   - Initialize the local ledger with `scripts/engagement_ledger.py`.

2. **Scan one viewport**
   - Read only visible posts in the current viewport.
   - Build at most 3 candidate records per viewport.
   - Each record must fit this shape:
     `id | author | age | url/status | topic | snippet<=280 | already_reacted? | already_commented? | score | skip_reason`

3. **Dedupe before drafting**
   - For each candidate, run the ledger `check` before writing a draft.
   - Skip if already reacted/commented/drafted/skipped, or if the UI shows the user already reacted/commented.

4. **Score**
   - Score 0 to 10 using the rubric below.
   - Only draft for score 7+.
   - Only propose reaction-only for score 8+ or user-targeted authors.

5. **Draft**
   - Draft one concise, specific comment grounded in the visible post.
   - Run `lint-comment` before showing it to the user.
   - If lint fails, rewrite once. If it still fails or feels generic, skip.

6. **Approval**
   - Show a compact approval card.
   - Do not click any final reaction/comment/share/connect/follow/send control until the user approves that exact action.

7. **Perform approved action**
   - Use visible UI controls only.
   - After performing, record the action in the ledger.
   - If the UI changes unexpectedly, stop and ask for manual confirmation.

8. **Advance**
   - Scroll down once, then repeat.
   - Stop when the session budget is reached or quality drops.

## Relevance scoring rubric

Start at 0. Add:

- +3 if the post matches the user's topic, niche, ICP, or engagement goal.
- +2 if the author is relevant to the user's network, industry, customer profile, or target list.
- +2 if the post has a clear opening for a useful comment: question, claim, data point, lesson, tension, or request for input.
- +1 if the post is recent enough for the context. Default: within 14 days; prefer newer when search/feed permits.
- +1 if the user can add a distinct perspective rather than praise.
- +1 if the tone is professional and safe.

Hard skip even if score is high:

- engagement bait: "comment yes", reaction polls, chain-letter prompts, empty virality hooks
- content outside user goals
- sensitive or heated topics unless the user explicitly requested them
- posts with no visible substance
- already engaged by the user
- author already engaged this session
- comment would be generic or forced

## Comment quality rules

Every comment must do at least one of these:

- add a specific observation from the post
- ask a precise, non-obvious question
- share a relevant experience or implication
- respectfully challenge or qualify one point
- connect the post to a concrete use case

Never post comments that are only praise, agreement, or filler. Avoid these phrases unless embedded in a richer comment: `great post`, `thanks for sharing`, `very insightful`, `well said`, `love this`, `spot on`, `could not agree more`.

Preferred shape:

`Specific anchor from post + useful implication/question + optional concise perspective.`

Length target: 1 to 3 sentences, 45 to 350 characters. No more than one hashtag. No emoji-only comments. No fake personal claims.

## Reaction choice rules

Do not react to every relevant post. Propose a reaction only when the post is clearly relevant and the reaction is natural.

Default reaction mapping:

- Like: neutral acknowledgement or lightweight support.
- Celebrate: promotion, launch, win, award, milestone.
- Support: hardship, hiring transition, vulnerability, community help.
- Insightful: data, lesson, framework, practical analysis.
- Love: values-driven or deeply aligned post.
- Funny: only when the author clearly intended humor and it is professional.

If unsure, use Like or skip. Never use reactions to manipulate engagement.

## Ledger usage

Use `scripts/engagement_ledger.py` to avoid redundant work and repeated comments. Use a durable ledger path if the user runs multiple sessions. Keep only minimal excerpts needed for dedupe.

On Windows Codex desktop, `python` may not be on PATH. If a `python` command fails, use the bundled Python executable reported by `load_workspace_dependencies` and substitute it for `python` in the commands below.

Check before drafting or action:

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json check --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" --action comment
```

Record a reviewed post:

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json record --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" --action reviewed --reason "candidate scored"
```

Lint a comment:

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json lint-comment --comment "COMMENT" --post-text "VISIBLE_POST_TEXT"
```

Record a draft:

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json record --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" --action comment_drafted --comment "COMMENT"
```

Record after approved UI action:

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json record --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" --action comment_posted --comment "COMMENT"
```

## Native machine browser protocol

For detailed browser instructions, read `references/native-machine-browser.md` only when operating the browser.

Core rules:

1. Use `@browser` first for navigation, DOM snapshots, screenshots, form filling, scrolling, and visible UI clicks in the user's machine browser.
2. Use `@computer` as a fallback for OS-level browser selection, permission prompts, or visible UI controls unavailable to `@browser`.
3. Reuse the selected tab and logged-in session when possible. Do not launch a hidden, remote, or separate automation-only browser profile.
4. Inspect visible page state with `@browser` snapshots/screenshots, or with `@computer` screenshots when operating native UI.
5. Use user-visible locators: role, text, label, placeholder, and visible post containers. Avoid brittle CSS/XPath chains and LinkedIn generated IDs.
6. After every scroll, click, modal open, comment panel expansion, or navigation, inspect the page again before acting.
7. Never click a final `Post`, `Comment`, `Send`, `Share`, `Repost`, `Connect`, `Follow`, `Like`, or reaction control unless the user approved that exact action.
8. Pasting a draft into a comment box is allowed only when the user asked for assisted drafting; stop before final submit unless approval is explicit.

## UI traversal heuristics

Use visible LinkedIn structure, not DOM internals.

Candidate extraction per post:

- author or page name
- timestamp/age if visible
- visible post text summary, max 280 chars
- visible topic tags only if relevant
- post permalink if available without opening profiles or menus excessively
- whether user has already reacted/commented if visible
- visible counts only if useful for prioritization

Efficient traversal:

- Process the current viewport first.
- Skip ads, suggested jobs, people cards, polls with engagement bait, unrelated reposts, and low-text posts.
- Use `Most recent` only if easily visible and useful; do not fight the UI.
- Open comment panels only for candidates that pass score/dedupe.
- Do not open author profiles unless the user asked for target-author engagement.
- Scroll in medium increments; after each scroll, summarize only new candidates.

## Approval card format

Show this compact card before any final action:

```text
Candidate N
post: AUTHOR | AGE | TOPIC | SCORE/10
why: one sentence
digest: <=220 chars
action: react=TYPE? comment=yes/no
comment: "..."
checks: dedupe=pass, lint=pass, risk=low
reply: approve N / edit N: ... / skip N
```

If multiple candidates are ready, show at most 3 approval cards at once.

## Output style during sessions

Keep output short while operating the browser:

- Report only candidates, skip reasons, approval cards, and completed approved actions.
- Do not narrate every click.
- Do not paste long post text.
- Do not expose private ledger internals unless asked.

Session summary format:

```text
Session summary
reviewed: X
skipped: Y
comment drafts: Z
approved reactions: A
approved comments: B
best follow-up: one sentence
ledger: path
```

## Reference files

- `references/native-machine-browser.md`: native Windows/macOS machine browser workflow using `@browser` and `@computer`.
- `references/comment-quality.md`: comment drafting, linting, and examples.
- `references/session-template.md`: compact runtime templates for small/medium models.
- `references/research-notes.md`: platform, browser, and workflow design notes.
