#!/usr/bin/env python3
"""PR-14 sample — best-effort web search (stdlib).

Obeys docs/menu-system/CODE-CALL-DISPLAY.md.
Requires network; fails gracefully with markdown error offline.
Not a production search product.
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request


def main(argv: list[str] | None = None) -> int:
    """Attempt DuckDuckGo instant-answer API; print markdown."""
    p = argparse.ArgumentParser(description="Web search sample for TUI menu output")
    p.add_argument("--q", "--query", dest="q", default="textual python tui")
    p.add_argument("--timeout", type=float, default=12.0)
    args = p.parse_args(argv)

    print("TUI_RENDER: markdown", flush=True)
    print("TUI_TITLE: Web search (sample)", flush=True)
    print(f"## Web search\n\n**Query:** `{args.q}`\n", flush=True)

    # DuckDuckGo Instant Answer API (no key; best-effort)
    url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode(
        {"q": args.q, "format": "json", "no_html": 1, "skip_disambig": 1}
    )
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "TUI.inhouse-capability-demo/0.1 (sample)"},
        )
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
    except urllib.error.URLError as exc:
        print("### Offline or network error\n", flush=True)
        print(f"```\n{exc}\n```\n", flush=True)
        print("_Demo continues; fix network to see results._", flush=True)
        return 2  # partial
    except Exception as exc:  # noqa: BLE001
        print("### Error\n", flush=True)
        print(f"```\n{exc}\n```\n", flush=True)
        return 1

    heading = data.get("Heading") or ""
    abstract = data.get("AbstractText") or data.get("Abstract") or ""
    abstract_url = data.get("AbstractURL") or ""
    related = data.get("RelatedTopics") or []

    if heading or abstract:
        print(f"### {heading or 'Result'}\n", flush=True)
        if abstract:
            print(f"{abstract}\n", flush=True)
        if abstract_url:
            print(f"[Source]({abstract_url})\n", flush=True)
    else:
        print("_No abstract; related topics:_\n", flush=True)

    print("### Related\n", flush=True)
    count = 0
    for item in related:
        if count >= 8:
            break
        if isinstance(item, dict) and item.get("Text"):
            text = item.get("Text", "")
            link = item.get("FirstURL", "")
            if link:
                print(f"- [{text[:120]}]({link})", flush=True)
            else:
                print(f"- {text[:120]}", flush=True)
            count += 1
        elif isinstance(item, dict) and "Topics" in item:
            for sub in item.get("Topics") or []:
                if count >= 8:
                    break
                if isinstance(sub, dict) and sub.get("Text"):
                    text = sub.get("Text", "")
                    link = sub.get("FirstURL", "")
                    print(f"- [{text[:120]}]({link})" if link else f"- {text[:120]}", flush=True)
                    count += 1
    if count == 0 and not abstract:
        print("_No structured results in response._", flush=True)
    print("\n_Sample only — not a production search client._\n", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
