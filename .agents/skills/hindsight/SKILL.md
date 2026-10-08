---
name: hindsight
description: >
  Long-term memory, mental models, and knowledge retention for AI pair programming using Hindsight MCP.
  Use when learning user preferences, retaining key architectural decisions, recalling project history,
  synthesizing insights across sessions, or updating persistent mental models.
---

# Hindsight — Persistent Memory & Mental Models

Guidelines for utilizing the **Hindsight MCP** toolset to maintain long-term context, recall historical decisions, and persist user preferences for **GeoIP All-in-One Data Pipeline**.

## Available Tools (Hindsight MCP)

1. **`recall`**:
   - Query long-term memory for relevant decisions, dataset sources, merge algorithm tweaks, and team conventions.
   - Run before starting complex modifications to voting algorithms, sweep-line tables, or MMDB schema.
2. **`retain` / `sync_retain`**:
   - Proactively persist important information:
     - Architectural decisions (e.g., "Always use `MMDBWriter(database_type='GeoIP2-City')`").
     - User preferences for country voting priority or coordinate spread threshold.
     - Known dataset anomalies (e.g., unassigned IP ranges, CIDR overlap nuances).
3. **`reflect`**:
   - Synthesizes multiple memories into cohesive insights and mental models.
4. **`create_mental_model` / `update_mental_model`**:
   - Maintains structured understanding of project subsystems (e.g., "GeoIP Sweep-Line Engine", "GeoIP Timezone Calculation").
5. **`create_directive`**:
   - Enforces permanent behavioral constraints across sessions.

## Best Practices

- **When to Retain**: When the user explicitly establishes a voting rule, prefers a specific library or optimization, or resolves a tricky range parsing bug.
- **Tagging**: Use descriptive tags such as `geoip`, `python`, `mmdb`, `tzfpy`, `sweep_line`, `rules`.
- **Bank Identification**: Store project-specific memories in the bank ID: `geoip-all-in-one`.
