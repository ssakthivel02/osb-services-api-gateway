#!/usr/bin/env python3
from __future__ import annotations
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
policy = json.loads((ROOT / 'config/gateway-policy.json').read_text())
routes = json.loads((ROOT / 'config/routes.json').read_text())

def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)

require('none' not in policy['allowedJwtAlgorithms'], 'Unsigned JWT is allowed')
require(not {'HS256','HS384','HS512'} & set(policy['allowedJwtAlgorithms']), 'Shared-secret JWT algorithm is allowed')
require(policy['cors']['allowWildcardOrigin'] is False, 'Wildcard CORS is enabled')
require(policy['securityHeaders']['strictTransportSecurity'] is True, 'HSTS is disabled')
require(policy['securityHeaders']['frameOptions'] == 'DENY', 'Clickjacking protection is weak')
require(policy['rateLimits']['anonymousRequestsPerMinute'] < policy['rateLimits']['authenticatedRequestsPerMinute'], 'Anonymous limit must be lower')
require(all(r['authentication'] != 'public' for r in routes['routes'] if '/admin/' in r['path']), 'Admin route is public')

mutated = deepcopy(policy)
mutated['allowedMethods'].append('TRACE')
require('TRACE' in mutated['allowedMethods'], 'Negative method mutation did not execute')
mutated = deepcopy(policy)
mutated['cors']['allowWildcardOrigin'] = True
require(mutated['cors']['allowWildcardOrigin'] is True, 'Negative CORS mutation did not execute')
print('Gateway negative security cases passed.')
