# WitnessOS Compliance CLI

Generates regulatory compliance reports from WitnessOS evidence.

## Standards

- `witnessos compliance --standard nsa-mcp` — NSA MCP Security Guidance report
- `witnessos compliance --standard eu-ai-act` — EU AI Act conformity report

## Architecture

Consumes mapping docs from `/mappings/` and templates from `/templates/` as data sources.
