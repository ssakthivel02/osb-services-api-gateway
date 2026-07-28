# API Gateway Threat Model

## Trust boundary
The gateway is the only public ingress for versioned OSB APIs. It validates transport, route, token, tenant, permission, payload-size and rate-limit controls before forwarding.

## Principal threats and controls
- Token substitution or downgrade: validate issuer, audience, expiry, tenant claim and RS256/ES256 only.
- Cross-tenant access: derive tenant context only from verified claims; never trust request parameters.
- Route bypass: deny unknown routes and require an explicit registry entry.
- CORS abuse: exact origin allow-list; no wildcard with credentials.
- Request smuggling: reject malformed transfer semantics and conflicting content lengths at implementation time.
- SSRF: upstream targets come only from static service discovery, never user input.
- Header spoofing: overwrite identity, tenant, forwarding and request-ID headers at the trust boundary.
- Replay and credential stuffing: short token lifetimes, rate limits, anomaly telemetry and auth-service revocation.
- Sensitive-data leakage: redact credentials, cookies, tokens and configured query keys; bodies off by default.
- Resource exhaustion: body limit, timeout, concurrency controls, circuit breakers and bounded retries.
- Method abuse: block TRACE, TRACK and CONNECT.
- Cache poisoning: authenticated responses are private/no-store unless explicitly reviewed.

## Required evidence
CI policy validation, negative tests, integration tests with the real auth service, cross-tenant denial, rate-limit tests, timeout/circuit-breaker tests and sanitised-log inspection.
