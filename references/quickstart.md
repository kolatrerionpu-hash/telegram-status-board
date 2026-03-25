# Quickstart

## Minimal local test

Render the bundled example:

```bash
python3 scripts/render_status_board.py < references/example-input.json
```

## Collect + render from local OpenClaw

```bash
python3 scripts/collect_openclaw_status.py | python3 scripts/render_status_board.py
```

## What this gives you

A Telegram-friendly status card optimized for mobile reading.

## Current scope

Version 0.2.0 adds a basic local collector for OpenClaw environments. It is intentionally conservative and produces a compact board even when some metrics are unavailable.
