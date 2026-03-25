#!/usr/bin/env python3
import json
import subprocess
from typing import Any, Dict, List, Optional


def run(cmd: List[str]) -> Optional[str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return (p.stdout or '').strip() or None


def run_json(cmd: List[str]) -> Any:
    text = run(cmd)
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def detect_gateway(status: Dict[str, Any]) -> str:
    gateway = status.get('gateway') or {}
    svc = status.get('gatewayService') or {}
    if gateway.get('reachable') is True:
        return '✅ Online'
    if svc.get('runtimeShort'):
        return f"⚠️ {svc.get('runtimeShort')}"
    return '❌ Offline'


def detect_main(status: Dict[str, Any]) -> str:
    recent = ((status.get('sessions') or {}).get('recent') or [])
    if not recent:
        return '💤 Idle'
    top = recent[0]
    model = top.get('model') or 'unknown'
    used = top.get('percentUsed')
    if used is not None:
        return f'✅ Active ({model}, {used}%)'
    return f'✅ Active ({model})'


def detect_subagents(status: Dict[str, Any]) -> str:
    recent = ((status.get('sessions') or {}).get('recent') or [])
    count = 0
    for s in recent:
        key = str(s.get('key', ''))
        if ':subagent:' in key:
            count += 1
    if count == 0:
        return '💤 none'
    return f'✅ {count} recent'


def detect_context(status: Dict[str, Any]) -> Optional[float]:
    recent = ((status.get('sessions') or {}).get('recent') or [])
    if not recent:
        return None
    used = recent[0].get('percentUsed')
    return float(used) if used is not None else None


def detect_lcm() -> str:
    cfg = run_json(['openclaw', 'config', 'get', 'plugins', '--json']) or {}
    enabled = (((cfg.get('entries') or {}).get('lossless-claw') or {}).get('enabled'))
    return '✅ Enabled' if enabled else '❌ Disabled'


def detect_crons() -> str:
    data = run_json(['openclaw', 'cron', 'list', '--json']) or {}
    jobs = data.get('jobs') or []
    total = len(jobs)
    if total == 0:
        return '💤 none'
    enabled = sum(1 for j in jobs if j.get('enabled', True))
    return f'✅ {enabled}/{total} enabled'


def detect_today_cost() -> Optional[float]:
    dash = run_json(['/bin/cat', '/Users/lzgmini/.openclaw/dashboard/data.json'])
    if not isinstance(dash, dict):
        return None
    vals = dash.get('costBreakdownToday') or []
    total = 0.0
    found = False
    for item in vals:
        try:
            total += float(item.get('cost', 0) or 0)
            found = True
        except Exception:
            pass
    return total if found else None


def detect_channel_health() -> Optional[str]:
    dash = run_json(['/bin/cat', '/Users/lzgmini/.openclaw/dashboard/data.json'])
    if not isinstance(dash, dict):
        return None
    cs = (((dash.get('agentConfig') or {}).get('channelStatus')) or {}).get('telegram') or {}
    if not cs:
        return None
    if cs.get('configured') and cs.get('connected'):
        return '✅ Telegram connected'
    if cs.get('configured'):
        return '⚠️ Telegram configured'
    return '❌ Telegram missing'


def detect_ollama() -> str:
    out = run(['ollama', 'list'])
    if not out:
        return '❌ Unavailable'
    if 'qwen' in out.lower():
        return '✅ Ready (Qwen installed)'
    return '⚠️ Ready (no Qwen found)'


def detect_model_lane(status: Dict[str, Any], name: str) -> str:
    recent = ((status.get('sessions') or {}).get('recent') or [])
    models = ' '.join(str(s.get('model', '')) for s in recent).lower()
    key = name.lower()
    if key in models:
        return '✅ Active recently'
    if key == 'gpt' and 'gpt-' in models:
        return '✅ Active recently'
    if key == 'gemini' and 'gemini' in models:
        return '✅ Active recently'
    return '🟡 Not seen recently'


def main() -> None:
    status = run_json(['openclaw', 'status', '--json']) or {}
    telegram_health = detect_channel_health()
    focus = [
        '查看当前主会话状态',
        '跟踪近期子代理痕迹',
        '用于 Telegram 快速总览'
    ]
    if telegram_health:
        focus.insert(0, telegram_health)

    payload: Dict[str, Any] = {
        'title': '🛡️ Vanguard 状态面板',
        'gateway': detect_gateway(status),
        'main': detect_main(status),
        'subagents': detect_subagents(status),
        'crons': detect_crons(),
        'cost_today': detect_today_cost(),
        'context_percent': detect_context(status),
        'lcm': detect_lcm(),
        'ollama': detect_ollama(),
        'gemini': detect_model_lane(status, 'gemini'),
        'gpt': detect_model_lane(status, 'gpt'),
        'focus': focus
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
