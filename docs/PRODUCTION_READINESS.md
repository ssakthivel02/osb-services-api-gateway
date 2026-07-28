# API Gateway Production Readiness

Production remains **NO-GO** until every mandatory control has dated evidence.

## Mandatory gates
- Public DNS, TLS, certificate renewal and HSTS verified.
- Only approved versioned routes exposed; unknown routes deny.
- Real identity-provider issuer, audience, JWKS and key rotation tested.
- Cross-tenant negative tests pass using real tokens.
- Exact CORS origins configured for each environment.
- Rate limits and burst behaviour load-tested.
- Request body limit, upstream timeout, bounded retry and circuit breaker tested.
- Identity, tenant and forwarding headers are overwritten at ingress.
- Security headers verified on success and error responses.
- Logs prove credential, cookie, token, code and sensitive-query redaction.
- Health and readiness endpoints integrated with monitoring.
- p95/p99 latency, 4xx/5xx, saturation and upstream dependency alerts active.
- Canary deployment and tested rollback available.
- DDoS/WAF controls assigned to an accountable platform owner.
- Backup/version control exists for route and policy configuration.
- Incident, privacy and on-call escalation paths approved.
- Capacity and failure-mode tests completed.

## Evidence record
For each gate record owner, environment, date, commit, test command or dashboard, result and exception approval. Policy-only completion is not production evidence.
