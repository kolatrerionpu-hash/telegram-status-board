# Installation Notes

## For OpenClaw users

Install this skill into your local skills directory, then use it when you want a Telegram-friendly status card instead of a browser dashboard.

Suggested location:

```bash
~/.openclaw/skills/telegram-status-board/
```

This skill currently provides:
- a Telegram-native status board layout
- a renderer script for consistent message formatting
- example input and usage guidance

## Intended usage

1. Collect runtime state from your OpenClaw environment
2. Normalize the metrics into a JSON payload
3. Pipe that payload into `scripts/render_status_board.py`
4. Send the rendered text to Telegram or use it as a reply template

## Example

```bash
python3 scripts/render_status_board.py < references/example-input.json
```
