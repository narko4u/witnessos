#!/usr/bin/env python3
"""Pinpoint the first unbalanced div in a body fragment (stack walk)."""
import pathlib, re, sys

BODIES = pathlib.Path("/mnt/c/VaultSentinel/witnessos-site/_bodies")

def walk(path):
    s = path.read_text()
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    stack = []
    line = 1
    for m in re.finditer(r"<(/?)(div|section)\b[^>]*?(/?)>|\n", s):
        tok = m.group(0)
        if tok == "\n":
            line += 1
            continue
        closing, tag, self_close = m.group(1), m.group(2), m.group(3)
        if self_close:
            continue
        if closing:
            if not stack:
                print(f"  {path.name}: stray </{tag}> at line {line}")
                return
            open_tag, open_line = stack.pop()
            if open_tag != tag:
                print(f"  {path.name}: </{tag}> at line {line} closes <{open_tag}> opened line {open_line}")
                return
        else:
            stack.append((tag, line))
    if stack:
        print(f"  {path.name}: UNCLOSED " + ", ".join(f"<{t}> line {l}" for t, l in stack))
    else:
        print(f"  {path.name}: balanced")

for name in ["products", "instructions", "pricing"]:
    walk(BODIES / f"{name}.body.html")
