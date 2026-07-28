# API Gateway Operations Runbook

## Health model
- `/health`: process liveness only; no confidential dependency detail.
- `/ready`: internal readiness covering route configuration, identity metadata availability and required upstream reachability.
- Readiness must fail closed when authentication validation cannot be trusted.

## Incident procedures
### Elevated 5xx rate
1. Correlate by request ID, route and upstream.
2. Confirm gateway saturation, timeout and circuit-breaker state.
3. Remove unhealthy upstreams from service discovery.
4. Do not disable authentication or tenant enforcement to restore service.

### Authentication validation failure
1. Verify issuer metadata and JWKS reachability.
2. Confirm clock synchronisation and accepted key IDs.
3. Fail protected traffic closed.
4. Escalate unknown signing keys or algorithm changes as a security incident.

### Suspected cross-tenant access
1. Disable affected route if containment is required.
2. Preserve sanitised logs and request IDs.
3. Revoke affected sessions through the auth service.
4. Notify security and privacy owners.

### Rate-limit attack
Apply the configured anonymous/authenticated/privileged classes, block abusive sources upstream where appropriate, and preserve evidence without logging credentials.

## Deployment and rollback
Validate policy and route registry, deploy canary, verify health/readiness, authentication, CORS, headers, rate limiting and representative routes. Roll back application and configuration together. Record commit, environment, approver and validation evidence.

## Mandatory monitoring
Request rate, status class, latency percentiles, denied routes, JWT failures, tenant failures, rate-limit decisions, upstream timeouts, circuit state and saturation. Never log bearer tokens, cookies, authorisation codes, passwords or private keys.
