# LinkedIn Auto Reaction Codex

A **human-in-the-loop** Codex skill for reviewing LinkedIn in the native Windows or macOS Codex app using the user's machine browser through `@browser` or `@computer`, drafting contextual comments, and avoiding duplicate engagement without scraping, automation, or bypassing the platform.

> **This skill never publishes anything on its own.** It reviews, scores, drafts, and lints. You explicitly approve every final reaction or comment click in chat.

---

## What it does

- Opens only the LinkedIn URL you give it (feed, search, hashtag, company, profile activity, or a specific post) in your normal machine browser via `@browser`, reusing your existing logged-in session when available.
- Scans **one viewport at a time** and surfaces at most 3 candidate posts per scroll.
- Scores each candidate 0–10 against a transparent rubric (topic fit, author relevance, comment opening, recency, etc.).
- Drafts at most one concise, post-grounded comment per candidate.
- Lints every draft against generic-phrase blocklists, hashtag/emoji limits, post-text grounding, and similarity to your previous comments.
- Shows a compact **approval card** before any final UI click.
- Records every reviewed / skipped / drafted / reacted / commented action in a local JSON ledger so the same post never gets engaged twice.

## What it deliberately won't do

- No credential prompts, no scraping, no Voyager / hidden APIs, no copied cookies, no hidden or remote automation browser.
- No CAPTCHA solving, no stealth, no proxy or fingerprint evasion.
- No bulk activity, no infinite scroll, no exporting profiles / contacts / messages.
- No automatic reactions, comments, connects, follows, reposts, shares, or sends. You approve each one in chat.
- No generic praise ("great post", "thanks for sharing", "very insightful", …) — these are blocked by the linter.

## Session budget (defaults)

Conservative per-session caps to keep behavior human-paced:

| Limit                                       | Default |
|---------------------------------------------|---------|
| Posts reviewed                              | 20      |
| Comments drafted                            | 5       |
| Reactions approved/performed                | 3       |
| Comments approved/posted                    | 2       |
| Engagement actions per author               | 1       |
| Stop after consecutive low-relevance screens| 3       |

Override by telling the agent stricter limits at the start of a session.

---

## Folder layout

```
linkedin-auto-reaction-codex/
├── SKILL.md                  # entry point Codex loads (frontmatter + rules)
├── README.md                 # this file (for humans)
├── agents/
│   └── openai.yaml           # display name and product targeting
├── references/               # extended docs the agent reads on demand
│   ├── native-machine-browser.md # @browser/@computer workflow
│   ├── comment-quality.md    # drafting/linting examples
│   ├── session-template.md   # runtime templates for small models
│   └── research-notes.md     # design notes
└── scripts/
    └── engagement_ledger.py  # local ledger + comment linter CLI
```

## Installation

1. Copy the entire `linkedin-auto-reaction-codex/` folder into your Codex skills directory:
   - Windows: `C:\Users\<you>\.agents\skills\linkedin-auto-reaction-codex\`
2. Make sure `SKILL.md` sits at the root of that folder (not nested).
3. Restart the Codex app so the skill is picked up.
4. Confirm Codex shows it as available; trigger it by asking for help with LinkedIn engagement.

No `pip install` is needed — `scripts/engagement_ledger.py` uses only Python's standard library.

> On Windows Codex desktop, `python` may not be on PATH. If `python` fails, use the bundled Python executable that `load_workspace_dependencies` reports and substitute it for `python` in every command below.

## How to use it

Just start a chat with Codex and describe what you want, for example:

- "Review my LinkedIn feed and find 3 posts worth commenting on about MLOps."
- "Here's a post URL: <link>. Draft a comment grounded in the post, don't submit."
- "Scan this hashtag page, score the top viewport, propose reactions only."

The skill will:

1. Open / reuse a LinkedIn tab in your machine browser using `@browser`, with `@computer` as a fallback for native UI.
2. Initialize a local ledger at `.linkedin_engagement_ledger.json` (configurable).
3. Scan one viewport, score candidates, dedupe against the ledger.
4. Draft + lint comments for anything that passes the rubric.
5. Show an approval card like:

   ```
   Candidate 1
   post: Jane Doe | 3h | MLOps observability | 8/10
   why: concrete data point on drift detection, opening for use-case angle
   digest: ...
   action: react=Insightful comment=yes
   comment: "..."
   checks: dedupe=pass, lint=pass, risk=low
   reply: approve 1 / edit 1: ... / skip 1
   ```

6. Wait. Nothing is clicked until you reply `approve 1` (or similar).
7. After an approved click, record it in the ledger and move on.

---

## The ledger CLI (`scripts/engagement_ledger.py`)

The script is the skill's **memory and quality gate**. The agent calls it between browser steps; you can also call it directly.

### Check whether a post is already handled

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json check `
  --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" --action comment
```

Exit codes: `0` = ok to proceed, `2` = skip (already engaged / previously skipped).

### Record an action

Valid `--action` values: `reviewed`, `skipped`, `reacted`, `comment_drafted`, `comment_approved`, `comment_posted`, `rejected`.

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json record `
  --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" `
  --action comment_posted --comment "FINAL_COMMENT"
```

### Lint a proposed comment

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json lint-comment `
  --comment "PROPOSED_COMMENT" --post-text "VISIBLE_POST_TEXT"
```

Returns a JSON object with `pass`, `score` (0–100), `flags`, and rewrite hints. Exit code `3` = lint failed.

Checks include: length / word count, hashtag count, emoji-only, generic-phrase blocklist, ≥1 ≥5-char token overlap with the post text, and ≥0.82 similarity to any prior comment in the ledger.

### Session summary

```powershell
python scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json summary --limit 10
```

### Where the ledger lives

By default: `.linkedin_engagement_ledger.json` in the current working directory.
Override globally with the `LINKEDIN_ENGAGEMENT_LEDGER` environment variable, or per-call with `--ledger PATH`. Use a durable path (e.g. in your user folder) if you run sessions across days — it's how the skill avoids re-commenting on posts you already engaged with weeks ago.

The ledger stores only minimal metadata the agent passes in: post ID (derived from the LinkedIn `activity:` URN or a hash of `author + snippet`), author string, URL, a ≤500-char snippet, an action list, and an event log. No DOM dumps, no cookies, no private LinkedIn data.

---

## Safety summary

This skill exists because LinkedIn explicitly restricts unauthorized automation, scraping, and inauthentic engagement. It is designed so that:

- Every visible UI click is approved by you in chat.
- The agent stops on CAPTCHA, verification, restriction, login challenge, or rate-limit notice.
- No data leaves your machine; the ledger is a local JSON file.
- The comment linter blocks the cliché phrases that get accounts flagged for inauthentic activity.

If you ask for fully autonomous liking/commenting, the skill is instructed to refuse and fall back to assisted mode (draft + approval cards).

## Customizing behavior

- Tighten or loosen lint thresholds via `--min-chars`, `--max-chars`, `--min-words`, `--max-similarity` on `lint-comment`.
- Edit the generic-phrase blocklist in `scripts/engagement_ledger.py` (`GENERIC_PATTERNS`, `LOW_VALUE_PHRASES`).
- Adjust session budgets, scoring rubric, or reaction mapping by editing `SKILL.md` directly — Codex will pick up the new rules on the next session.

## License

Personal-use skill. Use responsibly and in line with LinkedIn's User Agreement and Professional Community Policies.
