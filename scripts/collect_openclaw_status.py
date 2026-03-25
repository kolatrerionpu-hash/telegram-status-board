#!/usr/bin/env python3
import json
import subprocess
import sys
from typing import Any, Dict, List


def run_json(cmd: List[str]) -> Any:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    text = (p.stdout or '').strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def main() -> None:
    status = run_json(['openclaw', 'status', '--json']) or {}
    sessions = run_json(['openclaw', 'sessions', 'list', '--json']) or []

    gateway = '🟡 Unknown'
    if isinstance(status, dict):
        if status.get('gateway', {}).get('running') is True:
            gateway = '✅ Online'
        elif status.get('gateway', {}).get('running') is False:
            gateway = '❌ Offline'

    active_sessions = 0
    subagent_running = 0
    if isinstance(sessions, list):
        active_sessions = len(sessions)
        for s in sessions:
            key = str(s.get('sessionKey', ''))
            if ':subagent:' in key:
                subagent_running += 1

    payload: Dict[str, Any] = {
        'title': '🛡️ Vanguard 状态面板',
        'gateway': gateway,
        'main': '✅ Active' if active_sessions > 0 else '💤 Idle',
        'subagents': '💤 none' if subagent_running == 0 else f'✅ {subagent_running} running',
        'crons': '🟡 Check via cron tool',
        'lcm': '✅ Enabled',
        'ollama': '🟡 Unknown',
        'gemini': '🟡 Unknown',
        'gpt': '🟡 Unknown',
        'focus': [
            '查看系统运行状态',
            '跟踪当前会话与子代理',
            '用于 Telegram 快速总览'
        ]
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
