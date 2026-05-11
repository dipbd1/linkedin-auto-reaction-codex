# LinkedIn Auto Reaction Codex

A Codex plugin for reviewing LinkedIn in your signed-in Chrome session, drafting grounded comments, and preventing duplicate engagement.

It works through your signed-in Chrome browser using the Codex Chrome plugin/extension, with `@computer` only as a fallback for visible native UI. It does not scrape LinkedIn, call hidden APIs, copy cookies, bypass platform protections, or publish anything without your explicit approval.

> This plugin reviews, scores, drafts, and lints. You approve every final reaction or comment before anything visible is clicked.

## Install In Codex

Use this path if you just want the plugin installed. No build step, package install, or Python setup is required.

### 1. Install The Chrome Plugin

This LinkedIn plugin needs the Codex Chrome plugin because it works inside your real signed-in browser session.

1. Open Codex.
2. Go to **Plugins**.
3. Install and enable **Chrome**.
4. Follow the setup flow until the Chrome extension is connected.
5. Open Chrome, sign in to LinkedIn, and confirm the Codex extension says it is connected.

Setup guide: [Codex Chrome extension](https://developers.openai.com/codex/app/chrome-extension)

### 2. Add This Plugin Marketplace

In Codex:

1. Go to **Plugins**.
2. Choose **Add marketplace** or **Add plugin source**.
3. Paste this repository URL:

```text
https://github.com/dipbd1/linkedin-auto-reaction-codex
```

4. Add the marketplace.
5. Open **LinkedIn Engagement Plugins**.
6. Install **LinkedIn Auto Reaction Codex**.

If Codex asks you to restart after adding the marketplace, restart Codex and return to **Plugins**.

### 3. Start A New Chat

After installation, start a new Codex chat and try:

```text
@Chrome review my LinkedIn feed and draft comments for posts about AI engineering. Do not submit anything.
```

Codex should use the installed LinkedIn engagement skill and ask for your approval before any final LinkedIn action.

## Quick Checklist

- Codex desktop app is installed.
- Chrome plugin is installed in Codex.
- Codex Chrome extension is connected.
- You are signed in to LinkedIn in Chrome.
- **LinkedIn Auto Reaction Codex** is installed from **LinkedIn Engagement Plugins**.

## Troubleshooting Install

### I do not see "LinkedIn Engagement Plugins"

Restart Codex once after adding the marketplace. If it still does not appear, remove the marketplace and add it again with the repository URL:

```text
https://github.com/dipbd1/linkedin-auto-reaction-codex
```

### I see the marketplace but not the plugin

Make sure the marketplace source is the repository root, not a subfolder. The repository contains `.agents/plugins/marketplace.json`, which tells Codex where the plugin package lives.

### The plugin installs but does not control LinkedIn

Check the Chrome setup:

1. Chrome is open.
2. You are signed in to LinkedIn.
3. The Codex Chrome extension says **Connected**.
4. Codex has permission to use `linkedin.com` for the current chat.

### Advanced CLI Install

Most people should use the Codex app flow above. If the UI flow is unavailable, you can add the marketplace from a terminal:

```powershell
codex plugin marketplace add https://github.com/dipbd1/linkedin-auto-reaction-codex
```

Then restart Codex, open **Plugins**, choose **LinkedIn Engagement Plugins**, and install **LinkedIn Auto Reaction Codex**.

## Requirements

- Native Codex app on Windows or macOS.
- Google Chrome with the Codex Chrome plugin/extension installed, enabled, and connected.
- A Chrome session where you can manually log in to LinkedIn.
- Python 3 only if you want to run the ledger CLI yourself. The script uses the Python standard library only.

## Quick Start

Give Codex a LinkedIn destination and a goal:

```text
@Chrome review this LinkedIn post URL and draft one specific comment. Do not submit it.
```

Or:

```text
@Chrome scan my LinkedIn feed for up to 3 posts about MLOps that are worth commenting on.
```

The plugin will open or reuse LinkedIn in Chrome, inspect one visible viewport at a time, score candidate posts, draft grounded comments, run the comment linter, and show you an approval card before any final click.

## Why Use This

- Human approval for every final LinkedIn action.
- Local JSON ledger to prevent duplicate reactions or comments.
- Comment linter that blocks generic praise and repetitive replies.
- Conservative session limits that keep the workflow focused.
- Chrome-extension-backed visible browser workflow. No hidden browser, no scraping, no credential handling.

## What It Does

- Opens only the LinkedIn URL or page you provide: feed, search, hashtag, company page, profile activity, or a specific post.
- Uses the Codex Chrome plugin/extension for signed-in LinkedIn browser work.
- Reuses your existing logged-in Chrome session when available.
- Reviews one viewport at a time and surfaces at most 3 candidate posts per scroll.
- Scores each candidate from 0 to 10 using a transparent relevance rubric.
- Drafts at most one concise, post-grounded comment per candidate.
- Checks every draft against length, hashtag, generic phrase, post-grounding, and similarity rules.
- Records reviewed, skipped, drafted, reacted, and commented actions in a local ledger.

## What It Will Not Do

- Ask for LinkedIn credentials.
- Scrape LinkedIn or use Voyager, hidden APIs, copied cookies, proxies, stealth, or fingerprint evasion.
- Solve CAPTCHAs or bypass verification screens.
- Run bulk activity, infinite scroll, profile exports, contact exports, or message exports.
- Automatically react, comment, connect, follow, repost, share, or send messages.
- Submit generic comments such as "great post", "thanks for sharing", or "very insightful".

## How It Works

1. Codex opens or reuses LinkedIn in Chrome through the Codex Chrome plugin/extension, with `@computer` as a fallback for native UI.
2. The bundled skill initializes a local ledger at `.linkedin_engagement_ledger.json`, unless you configure another path.
3. It scans the current viewport and builds a short list of candidate posts.
4. It checks each candidate against the ledger to avoid duplicate engagement.
5. It scores relevant posts and drafts comments only for strong candidates.
6. It lints each draft before showing it to you.
7. It displays an approval card.
8. It waits for your explicit approval before clicking any final reaction or comment button.
9. It records the approved action in the local ledger.

Example approval card:

```text
Candidate 1
post: Jane Doe | 3h | MLOps observability | 8/10
why: concrete data point on drift detection, opening for use-case angle
digest: short visible summary of the post
action: react=Insightful comment=yes
comment: "This is a specific, grounded draft based on the post."
checks: dedupe=pass, lint=pass, risk=low
reply: approve 1 / edit 1: ... / skip 1
```

Nothing is clicked until you reply with an approval such as `approve 1`.

## Session Limits

Default per-session limits are intentionally conservative:

- Review up to 20 visible posts.
- Draft up to 5 comments.
- Perform up to 3 approved reactions.
- Post up to 2 approved comments.
- Perform at most 1 engagement action per author.
- Stop after 3 consecutive low-relevance screens.

You can ask for stricter limits at the start of a session.

## Ledger CLI

`plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py` is the plugin's local memory and comment quality gate. Codex calls it during the workflow, and you can also run it manually.

No package install is required:

```powershell
python plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py --help
```

On some Windows Codex setups, `python` may not be on `PATH`. If it fails, use the Python executable reported by Codex dependency setup and substitute it for `python` in the examples below.

### Check Whether A Post Is Already Handled

```powershell
python plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json check `
  --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" --action comment
```

Exit codes:

- `0`: ok to proceed.
- `2`: skip because it was already handled or previously skipped.

### Record An Action

Valid `--action` values are `reviewed`, `skipped`, `reacted`, `comment_drafted`, `comment_approved`, `comment_posted`, and `rejected`.

```powershell
python plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json record `
  --url "POST_URL" --author "AUTHOR" --snippet "VISIBLE_SNIPPET" `
  --action comment_posted --comment "FINAL_COMMENT"
```

### Lint A Proposed Comment

```powershell
python plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json lint-comment `
  --comment "PROPOSED_COMMENT" --post-text "VISIBLE_POST_TEXT"
```

The command returns JSON with `pass`, `score`, `flags`, and rewrite hints. Exit code `3` means the comment failed the lint checks.

Checks include:

- Character and word count.
- Hashtag count.
- Emoji-only comments.
- Generic phrase blocklist.
- At least one meaningful token overlap with the visible post text.
- Similarity to prior comments in the ledger.

### View A Session Summary

```powershell
python plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py --ledger .linkedin_engagement_ledger.json summary --limit 10
```

### Ledger Location

By default, the ledger is stored at:

```text
.linkedin_engagement_ledger.json
```

You can override it globally with `LINKEDIN_ENGAGEMENT_LEDGER` or per command with `--ledger PATH`.

Use a durable path, such as a file in your user folder, if you run sessions across multiple days. The ledger is how the skill avoids re-commenting on posts you already handled.

The ledger stores only minimal metadata passed by the agent: post ID, author string, URL, a short snippet, action history, and event log. It does not store DOM dumps, cookies, credentials, or private LinkedIn data.

## Project Structure

```text
linkedin-engagement-navigator/
|-- .agents/
|   `-- plugins/
|       `-- marketplace.json
|-- plugins/
|   `-- linkedin-engagement-navigator/
|       |-- .codex-plugin/
|       |   `-- plugin.json
|       |-- assets/
|       |   |-- icon.png
|       |   |-- icon.svg
|       |   |-- logo.png
|       |   |-- logo.svg
|       |   |-- screenshot-1.png
|       |   `-- screenshot-1.svg
|       `-- skills/
|           `-- linkedin-auto-reaction-codex/
|               |-- SKILL.md
|               |-- agents/
|               |   `-- openai.yaml
|               |-- references/
|               |   |-- native-machine-browser.md
|               |   |-- comment-quality.md
|               |   |-- session-template.md
|               |   `-- research-notes.md
|               `-- scripts/
|                   `-- engagement_ledger.py
|-- .gitignore
|-- LICENSE
`-- README.md
```

## Configuration

- Adjust session budgets, scoring, and reaction mapping in `plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/SKILL.md`.
- Tune comment lint thresholds with `--min-chars`, `--max-chars`, `--min-words`, and `--max-similarity`.
- Edit generic phrase rules in `plugins/linkedin-engagement-navigator/skills/linkedin-auto-reaction-codex/scripts/engagement_ledger.py` through `GENERIC_PATTERNS` and `LOW_VALUE_PHRASES`.
- Set `LINKEDIN_ENGAGEMENT_LEDGER` to keep one ledger across sessions.

## Safety Model

This project is designed for assisted engagement, not autonomous LinkedIn automation.

- Every visible UI action requires your approval in chat.
- The workflow stops on CAPTCHA, verification, warnings, restrictions, login challenges, or rate-limit notices.
- LinkedIn credentials are never requested.
- The browser session stays on your machine.
- The ledger is local JSON.
- The comment linter blocks low-effort, repetitive, and inauthentic drafts.

If you ask for fully autonomous liking or commenting, the skill refuses that mode and falls back to draft-and-approve assistance.

## Maintainer Notes

- Codex discovers this repository through `.agents/plugins/marketplace.json`.
- The marketplace entry points at `./plugins/linkedin-engagement-navigator`.
- The plugin manifest lives at `plugins/linkedin-engagement-navigator/.codex-plugin/plugin.json`.
- After changing plugin metadata, commit and push the repository so users can upgrade the marketplace from Codex.

## License

MIT. Use responsibly and in line with LinkedIn's User Agreement and Professional Community Policies.
