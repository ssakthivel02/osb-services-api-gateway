#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
policy = json.loads((ROOT / 'config/gateway-policy.json').read_text())
routes = json.loads((ROOT / 'config/routes.json').read_text())

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

require(policy['apiPrefix'].startswith('/api/v'), 'API prefix must be versioned')
require(policy['requireHttps'] is True, 'HTTPS must be mandatory')
require(policy['requireAuthenticationByDefault'] is True, 'Authentication must default to required')
require(policy['defaultDenyRoutes'] is True, 'Unknown routes must default deny')
require(set(policy['allowedJwtAlgorithms']) <= {'RS256','ES256'}, 'Only asymmetric JWT algorithms are allowed')
require(not {'TRACE','TRACK','CONNECT'} & set(policy['allowedMethods']), 'Dangerous HTTP method allowed')
require(set(policy['blockedMethods']) >= {'TRACE','TRACK','CONNECT'}, 'Dangerous methods must be blocked')
require(policy['maxRequestBodyBytes'] <= 10 * 1024 * 1024, 'Request body limit is excessive')
require(policy['upstreamTimeoutMilliseconds'] <= 30000, 'Upstream timeout is excessive')
require(policy['cors']['allowWildcardOrigin'] is False, 'Wildcard CORS must be disabled')
require(policy['logging']['redactAuthorization'] is True, 'Authorization must be redacted')
require(policy['logging']['redactCookies'] is True, 'Cookies must be redacted')
require(policy['logging']['logRequestBody'] is False, 'Request bodies must not be logged by default')

seen = set()
for route in routes['routes']:
    require(route['id'] not in seen, f"Duplicate route id: {route['id']}")
    seen.add(route['id'])
    require(route['path'].startswith('/') and '..' not in route['path'], f"Unsafe path: {route['id']}")
    require(set(route['methods']) <= set(policy['allowedMethods']), f"Disallowed method: {route['id']}")
    require(route['authentication'] in {'public','required','internal'}, f"Invalid authentication mode: {route['id']}")
    if route['authentication'] == 'required':
        require(bool(route.get('permissions')), f"Protected route lacks permissions: {route['id']}")
    if route['authentication'] == 'public':
        require(route['rateLimitClass'] == 'anonymous', f"Public route must use anonymous limit: {route['id']}")
    if route['path'].startswith('/api/'):
        require(route['path'].startswith(policy['apiPrefix']), f"Unversioned API route: {route['id']}")

print(f"Gateway baseline valid: {len(seen)} routes")
