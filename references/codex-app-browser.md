# Windows Codex App Browser Workflow

Use this reference only when operating LinkedIn in the Windows Codex app.

## Browser surface

Use the Codex Browser plugin's native in-app browser (`iab`). This is the preferred browser because it can use the browser session already visible to the user, including an existing LinkedIn login.

Do not start Browser Use CLI, a separate Chrome profile, a standalone Playwright browser, a remote browser, or a browser extension workflow for this skill.

## Startup pattern

1. Use the Browser skill before browser work.
2. Connect to the native in-app browser (`iab`).
3. Prefer the currently selected tab if it is already on LinkedIn or already logged in.
4. If there is no useful selected tab, open a new in-app browser tab and navigate to the user-provided LinkedIn URL or `https://www.linkedin.com/feed/`.
5. If LinkedIn shows a login screen, pause and ask the user to log in manually in that browser. Never ask for credentials or try to transfer cookies.

## State inspection

Use the cheapest state check that answers the next question:

- DOM snapshot for visible text, button names, form fields, and locator planning.
- Screenshot when visual layout, modals, reaction state, or comment box state matters.

After every click, scroll, navigation, modal open, or comment panel expansion, inspect the page again before acting. LinkedIn frequently re-renders visible controls.

## Locator rules

Prefer user-visible locators:

- button names such as `Comment`, `Like`, `React`, `Post`, `Send`, `Share`, `Repost`
- labels and placeholders around comment fields
- visible author names, timestamps, and post text
- role/text based selectors within the currently visible post container

Avoid:

- generated LinkedIn IDs
- deep CSS selectors
- brittle XPath chains
- hidden DOM data
- direct network calls

If a locator is ambiguous, narrow within the visible post container or use the screenshot to choose the correct visible control.

## Final action gates

A final action is any click or submit that creates external activity visible to others, including:

- Like or any reaction
- Post/Comment submit
- Share/Repost
- Follow
- Connect
- Message/Send

Final actions require explicit approval in the current conversation for that exact post and action. Pasting a draft into a comment field is not a final action only if the model stops before clicking submit.

## Stop conditions

Stop immediately and report briefly if LinkedIn shows:

- CAPTCHA
- verification or login challenge
- account warning
- restricted action
- unusual activity warning
- rate-limit or blocked-action notice
- unexpected payment, identity, or security prompt

Do not attempt to bypass these screens.
