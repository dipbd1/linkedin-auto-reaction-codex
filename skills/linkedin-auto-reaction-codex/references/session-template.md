# Compact session templates

Use these templates to save tokens during runtime.

## Candidate row

```text
CAND id=<short_id> author=<name> age=<age> topic=<topic> score=<0-10> reacted=<y/n/?> commented=<y/n/?> skip=<reason|none> snip="<=220 chars"
```

## Skip reasons

Use short codes:

- dup: in ledger or visible prior engagement
- bait: engagement bait or reaction poll
- thin: insufficient substance
- off: off-topic
- old: too old for session goal
- author-repeat: author already engaged this session
- sensitive: sensitive/heated topic
- generic-risk: no non-generic comment available
- ui-risk: modal, warning, or unclear UI

## Approval card

```text
Candidate <n>
post: <author> | <age> | <topic> | <score>/10
why: <one sentence>
digest: <one short digest>
action: <reaction type or none> + <comment draft or none>
comment: "<comment>"
checks: dedupe=<pass/fail>, lint=<pass/fail>, risk=<low/medium/high>
reply: approve <n> / edit <n>: ... / skip <n>
```

## Session summary

```text
Session summary
reviewed=<n> skipped=<n> drafts=<n> approved_reactions=<n> approved_comments=<n>
main skips=<top 2 skip codes>
recommended next session=<feed/search/author/topic>
ledger=<path>
```

## Small model instruction block

When context is tight, follow only this block:

```text
Visible browser only. No hidden APIs. Stop on warnings/CAPTCHA/restrictions. Review max 20 posts. Use ledger before drafting. Candidate row only. Score 7+ to draft. Run comment lint. Show max 3 approval cards. Never click Like/React/Post/Send/Share/Connect/Follow without explicit approval for that exact action. Record completed actions.
```
