# ADR 0001: Agents Use Approved Tools Only

## Status

Accepted

## Context

UrbanFlow exposes operational and analytical data. An LLM must not become the source of truth for metrics or execute unrestricted browser-provided SQL.

## Decision

Agents call backend allowlisted tools. Tool responses include provenance. Write operations are disabled by default and require RBAC plus explicit confirmation.

## Consequences

Agent answers may refuse unavailable metrics. This is preferred over unsupported estimates.

