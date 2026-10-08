---
name: rtk
description: >
  Rust Token Killer (RTK) CLI integration. Filters and compresses shell command output
  before it enters the LLM context, saving 60-90% tokens. Use whenever running shell commands,
  terminal tools, git, python, make, or inspecting file trees.
---

# RTK — Rust Token Killer

CLI proxy for command execution that filters noise and minimizes LLM context token usage.

## Core Rule

Whenever running terminal commands, **ALWAYS** prepend with `rtk` if supported:

```bash
# Git operations
rtk git status
rtk git diff
rtk git log -n 5

# Python & Pipeline
rtk python scripts/download.py sources.yaml ipv4 data/ipv4
rtk python scripts/merge.py sources.yaml ipv4 data/ipv4 merged_ipv4.tsv
rtk python scripts/convert.py merged_ipv4.tsv geoip_ipv4.mmdb 4
rtk make -n
rtk make deps

# File inspection & search
rtk ls -la
rtk grep "pattern" scripts/
rtk find "*.py" scripts/
```

## Useful RTK Commands

- `rtk gain`: Displays total tokens saved across previous commands.
- `rtk gain --history`: Shows command execution history with individual savings.
- `rtk discover`: Analyzes missed optimization opportunities.
- `rtk proxy <cmd>`: Runs command raw without compression (for low-level debugging).

## Why Use RTK

Terminal outputs frequently contain hundreds of lines of dataset progress logs, download transfers, and compiler noise. RTK strips this noise before it hits the prompt window, keeping the conversation fast, focused, and token-efficient.
