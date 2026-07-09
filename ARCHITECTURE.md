# Architecture - osb-services-api-gateway

## Overview
API gateway, routing, request governance, rate limits and edge controls. This repository is part of the OmSaravanaBhava Learning Ecosystem Enterprise Architecture v1.0.

## Context diagram
```mermaid
graph TD
    User[User / Service] --> Repo[osb-services-api-gateway]
    Repo --> Standards[osb-engineering-standards]
    Repo --> Platform[osb-platform-foundation]
```

## Architecture principles
- Secure by default
- Observable by default
- API-first where applicable
- Documentation-as-code
- ADR-controlled change

## Dependencies
See `ROADMAP.md` for implementation sequence and dependency notes.
