# Codex Chrome Browser Workflow

Use this reference only when operating LinkedIn in the native Windows or macOS Codex app.

## Browser surface

Use the user's signed-in Chrome browser through the Codex Chrome plugin/extension first. This is the required surface for reviewing LinkedIn pages because it can operate in the same Chrome profile the user normally uses, including an existing logged-in LinkedIn session.

Use `@computer` only when Chrome cannot access the needed visible browser UI, such as choosing an already-open Chrome window, handling an OS permission prompt, or interacting with a control that is only available through screen-level automation.

Do not start a hidden browser, remote browser, separate automation-only profile, copied-cookie workflow, non-Codex extension workflow, or direct HTTP/API workflow for this skill.

If the Codex Chrome plugin/extension is not installed, enabled, connected, and allowed for `linkedin.com`, stop and ask the user to complete the setup guide: `https://developers.openai.com/codex/app/chrome-extension`.

## Startup pattern

1. Use the Codex Chrome plugin/extension for browser work.
2. Open or attach to the user's Chrome browser.
3. Prefer the currently selected Chrome tab if it is already on LinkedIn or already logged in.
4. If there is no useful selected tab, open a normal browser tab and navigate to the user-provided LinkedIn URL or `https://www.linkedin.com/feed/`.
5. If LinkedIn shows a login screen, pause and ask the user to log in manually in that browser. Never ask for credentials or try to transfer cookies.
6. If browser selection, focus, or permissions require OS-level interaction, use `@computer`, then return to Chrome for page inspection when possible.

## State inspection

Use the cheapest state check that answers the next question:

- Chrome page snapshot for visible text, button names, form fields, and locator planning.
- Chrome screenshot when visual layout, modals, reaction state, or comment box state matters.
- `@computer` screenshot only when operating native OS/browser chrome or when Chrome cannot observe the relevant state.

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

If a locator is ambiguous, narrow within the visible post container or use a screenshot to choose the correct visible control.

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
