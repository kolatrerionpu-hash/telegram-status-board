---
name: telegram-status-board
description: Create and refresh a Telegram-friendly status panel for OpenClaw. Use when the user wants a concise, mobile-friendly control card in Telegram showing gateway health, active sessions, sub-agents, crons, model/runtime readiness, costs, and current focus. Especially useful when replacing a web dashboard with a chat-native status board or when summarizing system state into a single editable Telegram message.
---

# Telegram Status Board

Build a Telegram-native status panel instead of a browser dashboard.

The goal is not to mimic a full web UI. The goal is to produce a compact, scannable status card that works well in Telegram chat.

## Core Output Shape

Prefer a single compact message with:
- a short title
- health/status emojis
- 6-12 high-signal lines
- optional task/focus section
- optional lightweight action hints

Keep it readable on mobile.

## Use This Skill To Produce

- a one-shot status snapshot
- a refreshable status message format
- a standard field layout for Telegram
- a status summary suitable for pinning or frequent reposting

## Telegram Design Rules

### 1. Optimize for narrow screens
Use short lines.
Avoid markdown tables.
Prefer one metric per line.

### 2. Lead with operational state
Show the highest-signal items first:
- gateway
- main session
- sub-agents
- cron health
- cost/context pressure
- local model readiness

### 3. Use stable labels
Prefer labels like:
- Gateway
- Main
- Subagents
- Crons
- Cost
- Context
- LCM
- Ollama
- Gemini
- GPT
- Focus

### 4. Prefer status emojis over prose
Use:
- ✅ healthy / ready
- ⚠️ degraded / attention needed
- ❌ down / failed
- 🟡 partial / unknown
- 💤 idle
- 🔥 elevated load/cost

Do not over-decorate.

## Recommended Board Layout

Use this default structure:

```text
🛡️ Vanguard 状态面板

Gateway: ✅ Online
Main: ✅ Active
Subagents: 2 running
Crons: ⚠️ 1 failed / 8 total
Cost: 🔥 $3.42 today
Context: ✅ 61%
LCM: ✅ Enabled
Ollama(Qwen): ✅ Ready
Gemini: ✅ Ready
GPT: ✅ Ready

Focus:
- 修 dashboard
- 跑 skill 安装
- 做 Telegram 状态卡
```

If there is no current focus, omit the section.

## Priority Logic

When data is incomplete, still produce a useful board.

Priority order:
1. gateway status
2. active session count / main session state
3. sub-agent activity
4. cron failures or next-run health
5. model/runtime readiness
6. cost and context pressure
7. current focus / active work

If some lower-priority data is missing, omit it instead of guessing.

## Field Guidance

### Gateway
- ✅ Online
- ⚠️ Not ready
- ❌ Offline

### Main
- ✅ Active
- 💤 Idle
- ❌ Missing

### Subagents
Use count + state summary.
Examples:
- `Subagents: 💤 none`
- `Subagents: ✅ 1 running`
- `Subagents: ⚠️ 3 running, 1 stuck`

### Crons
Prefer health summary rather than dumping all jobs.
Examples:
- `Crons: ✅ 8 healthy`
- `Crons: ⚠️ 1 failed / 8 total`

### Cost
Only show if meaningful.
Examples:
- `Cost: $0.42 today`
- `Cost: 🔥 $12.70 today`

### Context
Use percentage when available.
Examples:
- `Context: ✅ 44%`
- `Context: ⚠️ 81%`

### Model Readiness
Keep one line per major lane when relevant:
- `Ollama(Qwen): ✅ Ready`
- `Gemini: ✅ Ready`
- `GPT: ✅ Ready`

If unknown, use `🟡 Unknown`.

## Refresh Strategy

For Telegram, prefer one of these patterns:

### Pattern A: Repost snapshot
Post a fresh snapshot on request.
Use when message editing is not available.

### Pattern B: Single living board
Maintain one main status message and refresh it.
Use when the integration supports message editing.

### Pattern C: Snapshot + drill-down replies
Post the compact board first, then reply with details only when asked.

Prefer Pattern C for human usability.

## Drill-Down Views

When the user asks for more detail, break out into focused follow-ups:
- sessions detail
- sub-agent runs
- cron failures
- cost/model breakdown
- current focus / execution queue

Do not overload the main status board.

## Data Sources To Prefer

Use first-class OpenClaw tools when possible:
- `session_status` for runtime/session state
- `sessions_list` for active sessions/sub-agents
- `cron` for scheduled jobs and failures
- `subagents` for run visibility

Use local tools or scripts only to normalize output when needed.

## Bundled Script

Use `scripts/collect_openclaw_status.py` to gather a compact local OpenClaw snapshot.
Then use `scripts/render_status_board.py` to render a Telegram-friendly board from the JSON payload.

Input contract for the renderer:
- a JSON object with key metrics already resolved
- the script formats the board consistently

Recommended local pipeline:

```bash
python3 scripts/collect_openclaw_status.py | python3 scripts/render_status_board.py
```

Use the scripts when you need consistent rendering across repeated status updates.

## Output Policy

Always keep the main board compact.
If the board exceeds ~15 lines, compress it.
If there are many alerts, show only the top 3 in the main board and move the rest to a follow-up.

## What Good Looks Like

Good:
- short
- operational
- mobile-readable
- easy to refresh
- easy to compare across time

Bad:
- wall of text
- raw JSON dump
- many low-value metrics
- pretending Telegram is Grafana
