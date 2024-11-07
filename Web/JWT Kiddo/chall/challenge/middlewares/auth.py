from flask import request, g, current_app as app
from uuid import uuid4
import jwt

CACHED_PRIVATE_KEYS = {}
CACHED_PUBLIC_KEYS = {}
JWT_ALG = 'RS256'
AUTH_COOKIE = 'access_token'
AUTH_GUEST = {'user': 'guest'}


def _get_public_key(kid: str) -> str:
    if kid not in CACHED_PUBLIC_KEYS:
        with open(f'public/keys/{kid}') as f:
            CACHED_PUBLIC_KEYS[kid] = f.read()
    return CACHED_PUBLIC_KEYS[kid]


def _get_private_key(kid: str) -> str:
    if kid not in CACHED_PRIVATE_KEYS:
        with open(f'private/keys/{kid}') as f:
            CACHED_PRIVATE_KEYS[kid] = f.read()
    return CACHED_PRIVATE_KEYS[kid]


def _create_jwt(payload):
    kid = 'key-0.pem'
    key = _get_private_key(kid)
    return jwt.encode(payload, key=key, algorithm=JWT_ALG, headers={"kid": kid})


def handle_auth():
    g.auth = {'user': f'guest-{uuid4().hex[:8]}'}
    
    token = request.cookies.get(AUTH_COOKIE)
    if token is None:
        g.set_auth = True
        return
    
    header = jwt.get_unverified_header(token)
    try:
        key = _get_public_key(header['kid'])
    except Exception as e:
        app.logger.error(e)
        return str(e), 500

    try:
        g.auth = jwt.decode(token, key, algorithms=[JWT_ALG])
    except Exception as e:
        app.logger.error(e)
        return "Pourquoi être aussi corrompu ? Tu as touché à ton access_token sans ma permission", 401


def response_auth(response):
    if getattr(g, 'set_auth', False):
        response.set_cookie(AUTH_COOKIE, _create_jwt(g.auth))