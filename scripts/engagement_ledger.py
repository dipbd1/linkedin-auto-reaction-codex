#!/usr/bin/env python3
"""
Local LinkedIn engagement ledger and comment guard.

Purpose:
- Avoid redundant review, reactions, and comments.
- Keep a compact local history for small/medium models.
- Lint comments for generic wording, duplicate phrasing, and weak grounding.

This script stores only minimal local metadata supplied by the operator/model. It does
not log in, scrape LinkedIn, call LinkedIn APIs, or automate UI actions.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_LEDGER = os.environ.get("LINKEDIN_ENGAGEMENT_LEDGER", ".linkedin_engagement_ledger.json")

GENERIC_PATTERNS = [
    r"\bgreat post\b",
    r"\bthanks for sharing\b",
    r"\bthank you for sharing\b",
    r"\bvery insightful\b",
    r"\binsightful post\b",
    r"\blove this\b",
    r"\bwell said\b",
    r"\bcould(n't| not) agree more\b",
    r"\bthis is so true\b",
    r"\bspot on\b",
    r"\bvaluable insights?\b",
    r"\bkeep it up\b",
    r"\bawesome share\b",
]

LOW_VALUE_PHRASES = [
    "great post",
    "thanks for sharing",
    "very insightful",
    "well said",
    "love this",
    "spot on",
]


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-z0-9#@+./: -]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_post_id(url: str, author: str, snippet: str) -> str:
    url = url or ""
    patterns = [
        r"activity[-:]([0-9]{8,})",
        r"urn:li:activity:([0-9]{8,})",
        r"update/urn:li:activity:([0-9]{8,})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return "activity:" + m.group(1)
    key = normalize_text(author) + "|" + normalize_text(snippet)[:700]
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    return "hash:" + digest


def load_ledger(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {"version": 1, "created_at": utc_now(), "posts": {}, "events": []}
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ledger is not valid json: {p}: {exc}")
    data.setdefault("version", 1)
    data.setdefault("posts", {})
    data.setdefault("events", [])
    return data


def save_ledger(path: str, data: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    tmp.replace(p)


def actions_for(data: Dict[str, Any], post_id: str) -> List[str]:
    post = data.get("posts", {}).get(post_id, {})
    return list(post.get("actions", []))


def cmd_check(args: argparse.Namespace) -> int:
    data = load_ledger(args.ledger)
    post_id = args.post_id or extract_post_id(args.url, args.author, args.snippet)
    actions = set(actions_for(data, post_id))
    action = args.action
    skip = False
    reasons: List[str] = []

    if "skipped" in actions and not args.allow_revisit:
        skip = True
        reasons.append("post was previously skipped")
    if action in ("review", "any") and actions and not args.allow_revisit:
        skip = True
        reasons.append("post already has ledger actions: " + ",".join(sorted(actions)))
    if action == "react" and "reacted" in actions:
        skip = True
        reasons.append("reaction already recorded")
    if action == "comment" and ({"comment_posted", "comment_approved", "comment_drafted"} & actions):
        skip = True
        reasons.append("comment already drafted, approved, or posted")

    out = {
        "post_id": post_id,
        "seen": bool(actions),
        "actions": sorted(actions),
        "skip": skip,
        "reasons": reasons,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if not skip else 2


def cmd_record(args: argparse.Namespace) -> int:
    data = load_ledger(args.ledger)
    post_id = args.post_id or extract_post_id(args.url, args.author, args.snippet)
    post = data["posts"].setdefault(post_id, {
        "post_id": post_id,
        "first_seen_at": utc_now(),
        "author": args.author or "",
        "url": args.url or "",
        "snippet": (args.snippet or "")[:500],
        "actions": [],
    })
    if args.author:
        post["author"] = args.author
    if args.url:
        post["url"] = args.url
    if args.snippet:
        post["snippet"] = args.snippet[:500]
    post["last_seen_at"] = utc_now()
    if args.action not in post["actions"]:
        post["actions"].append(args.action)

    event = {
        "at": utc_now(),
        "post_id": post_id,
        "action": args.action,
        "status": args.status,
        "reason": args.reason or "",
    }
    if args.comment:
        event["comment"] = args.comment
    data["events"].append(event)
    save_ledger(args.ledger, data)
    print(json.dumps({"recorded": True, "post_id": post_id, "action": args.action}, indent=2))
    return 0


def prior_comments(data: Dict[str, Any], limit: int = 50) -> List[str]:
    comments = []
    for ev in reversed(data.get("events", [])):
        c = ev.get("comment")
        if c:
            comments.append(c)
        if len(comments) >= limit:
            break
    return comments


def cmd_lint_comment(args: argparse.Namespace) -> int:
    data = load_ledger(args.ledger)
    comment = args.comment.strip()
    post_text = args.post_text.strip()
    norm_comment = normalize_text(comment)
    norm_post = normalize_text(post_text)
    flags: List[str] = []

    if len(comment) < args.min_chars:
        flags.append(f"too short: {len(comment)} chars")
    if len(comment) > args.max_chars:
        flags.append(f"too long: {len(comment)} chars")
    if len(comment.split()) < args.min_words:
        flags.append(f"too few words: {len(comment.split())}")
    if comment.count("#") > 1:
        flags.append("too many hashtags")
    if re.fullmatch(r"[\W_\s]+", comment or ""):
        flags.append("emoji or punctuation only")
    for pat in GENERIC_PATTERNS:
        if re.search(pat, norm_comment):
            flags.append("generic phrase: " + re.sub(r"\\b", "", pat).replace("\\", ""))
            break

    # Require at least one meaningful token overlap with the post when post text is supplied.
    if norm_post:
        post_terms = {w for w in norm_post.split() if len(w) >= 5 and not w.startswith("http")}
        comment_terms = {w for w in norm_comment.split() if len(w) >= 5}
        if len(post_terms & comment_terms) == 0:
            flags.append("not grounded in visible post terms")

    for old in prior_comments(data):
        ratio = difflib.SequenceMatcher(None, norm_comment, normalize_text(old)).ratio()
        if ratio >= args.max_similarity:
            flags.append(f"too similar to prior comment: {ratio:.2f}")
            break

    score = 100
    score -= 18 * sum(1 for f in flags if f.startswith("generic phrase"))
    score -= 15 * sum(1 for f in flags if "similar" in f)
    score -= 12 * sum(1 for f in flags if "grounded" in f)
    score -= 8 * sum(1 for f in flags if "too short" in f or "too few" in f)
    score -= 8 * sum(1 for f in flags if "too long" in f)
    score -= 6 * sum(1 for f in flags if "hashtags" in f or "emoji" in f)
    score = max(0, score)

    out = {
        "pass": len(flags) == 0,
        "score": score,
        "flags": flags,
        "comment": comment,
        "rewrite_rules": [
            "anchor on one specific idea from the post",
            "add a concrete observation, consequence, question, or relevant experience",
            "avoid generic praise and repeated sentence rhythm",
            "keep it concise and professional",
        ],
        "low_value_phrases": LOW_VALUE_PHRASES,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["pass"] else 3


def cmd_summary(args: argparse.Namespace) -> int:
    data = load_ledger(args.ledger)
    counts: Dict[str, int] = {}
    for ev in data.get("events", []):
        counts[ev.get("action", "unknown")] = counts.get(ev.get("action", "unknown"), 0) + 1
    recent = data.get("events", [])[-args.limit:]
    out = {
        "ledger": args.ledger,
        "post_count": len(data.get("posts", {})),
        "event_count": len(data.get("events", [])),
        "counts": counts,
        "recent": recent,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="local ledger and comment guard for linkedin engagement workflows")
    p.add_argument("--ledger", default=DEFAULT_LEDGER, help="path to local json ledger")
    sub = p.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check", help="check whether a post/action is redundant")
    check.add_argument("--post-id", default="")
    check.add_argument("--url", default="")
    check.add_argument("--author", default="")
    check.add_argument("--snippet", default="")
    check.add_argument("--action", choices=["review", "react", "comment", "any"], default="review")
    check.add_argument("--allow-revisit", action="store_true")
    check.set_defaults(func=cmd_check)

    rec = sub.add_parser("record", help="record a post action")
    rec.add_argument("--post-id", default="")
    rec.add_argument("--url", default="")
    rec.add_argument("--author", default="")
    rec.add_argument("--snippet", default="")
    rec.add_argument("--action", required=True, choices=[
        "reviewed", "skipped", "reacted", "comment_drafted", "comment_approved", "comment_posted", "rejected"
    ])
    rec.add_argument("--status", default="done")
    rec.add_argument("--reason", default="")
    rec.add_argument("--comment", default="")
    rec.set_defaults(func=cmd_record)

    lint = sub.add_parser("lint-comment", help="lint a proposed comment")
    lint.add_argument("--comment", required=True)
    lint.add_argument("--post-text", default="")
    lint.add_argument("--min-chars", type=int, default=45)
    lint.add_argument("--max-chars", type=int, default=450)
    lint.add_argument("--min-words", type=int, default=9)
    lint.add_argument("--max-similarity", type=float, default=0.82)
    lint.set_defaults(func=cmd_lint_comment)

    summ = sub.add_parser("summary", help="summarize recent ledger activity")
    summ.add_argument("--limit", type=int, default=10)
    summ.set_defaults(func=cmd_summary)
    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
