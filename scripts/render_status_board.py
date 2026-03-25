#!/usr/bin/env python3
import json
import sys


def icon_bool(value, yes='✅', no='❌', unknown='🟡'):
    if value is True:
        return yes
    if value is False:
        return no
    return unknown


def fmt_cost(value):
    if value is None:
        return None
    try:
        v = float(value)
    except Exception:
        return str(value)
    if v >= 10:
        return f'🔥 ${v:.2f} today'
    return f'${v:.2f} today'


def fmt_context(value):
    if value is None:
        return None
    try:
        v = float(value)
    except Exception:
        return str(value)
    icon = '⚠️' if v >= 80 else '✅'
    return f'{icon} {int(round(v))}%'


def main():
    data = json.load(sys.stdin)
    title = data.get('title', '🛡️ Vanguard 状态面板')
    lines = [title, '']

    gateway = data.get('gateway')
    if gateway is not None:
        lines.append(f"Gateway: {gateway}")

    main_state = data.get('main')
    if main_state is not None:
        lines.append(f"Main: {main_state}")

    subagents = data.get('subagents')
    if subagents is not None:
        lines.append(f"Subagents: {subagents}")

    crons = data.get('crons')
    if crons is not None:
        lines.append(f"Crons: {crons}")

    cost = fmt_cost(data.get('cost_today'))
    if cost:
        lines.append(f"Cost: {cost}")

    context = fmt_context(data.get('context_percent'))
    if context:
        lines.append(f"Context: {context}")

    lcm = data.get('lcm')
    if lcm is not None:
        lines.append(f"LCM: {lcm}")

    for label, key in [
        ('Ollama(Qwen)', 'ollama'),
        ('Gemini', 'gemini'),
        ('GPT', 'gpt'),
    ]:
        val = data.get(key)
        if val is not None:
            lines.append(f"{label}: {val}")

    focus = data.get('focus') or []
    if focus:
        lines.extend(['', 'Focus:'])
        for item in focus[:5]:
            lines.append(f"- {item}")

    print('\n'.join(lines))


if __name__ == '__main__':
    main()
