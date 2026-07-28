# ADR 0001: API Gateway Security Boundary

## Status
Accepted for the foundation baseline.

## Decision
All public OSB API traffic enters through a versioned gateway route registry. The gateway validates HTTPS, route eligibility, HTTP method, JWT issuer/audience/expiry/algorithm, tenant claim, permission metadata, payload size, CORS and rate limits before forwarding.

Unknown routes are denied. Identity, tenant, forwarding and request-ID headers supplied by clients are removed or replaced. Upstream destinations are selected only from trusted configuration. Authentication is required by default; public and internal routes require explicit classification.

The gateway does not issue tokens, store user passwords or become the source of truth for role membership. Those remain responsibilities of the authentication service. It forwards only verified identity context.

## Consequences
Central enforcement improves consistency and observability but creates a critical availability and security boundary. Multi-instance deployment, strict readiness, bounded timeouts, tested rollback and fail-closed authentication are therefore mandatory. Downstream services must still enforce resource-level authorisation and tenant ownership; the gateway is not their sole security control.

## Rejected alternatives
- Unversioned public APIs.
- Wildcard CORS with credentials.
- HMAC JWT validation shared across services.
- Client-supplied tenant identity.
- Dynamic upstream URLs from request input.
- Authentication disabled during dependency failure.
