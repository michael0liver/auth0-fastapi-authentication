from typing import List, Literal, cast

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from jose import jwt

from app.auth import Auth0OAuth2AuthorizationCodeBearer, TokenClaims
from app.config import config

Scope = Literal[
    "read:messages",
    "create:messages",
]


oauth2_scheme = Auth0OAuth2AuthorizationCodeBearer[Scope](
    domain=config.AUTH0_DOMAIN,
    audience=config.AUTH0_API_AUDIENCE,
    scopes={
        "read:messages": "Read Messages",
        "create:messages": "Create Messages",
    },
)

# Alias for convenience
Security = oauth2_scheme.security


async def get_verified_claims(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> TokenClaims:
    """Route dep"""

    # See https://datatracker.ietf.org/doc/html/rfc6750#section-3 for more info
    # on the WWW-Authenticate response header field.
    www_authenticate_base = "Bearer"
    www_authenticate_attrs: List[str] = []
    if security_scopes.scopes:
        www_authenticate_attrs.append(f'scope="{security_scopes.scope_str}"')

    def build_www_authenticate_value() -> str:
        attrs_comma_sep = ", ".join(www_authenticate_attrs)
        return f"{www_authenticate_base} {attrs_comma_sep}"

    # We fetch the JSON Web Key Set on every call, you could cache this for lower
    # latency.
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(oauth2_scheme.jwks_url)
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    jwks = response.json()

    try:
        verified_claims = jwt.decode(
            token=token,
            key=jwks,
            algorithms=["RS256"],
            audience=oauth2_scheme.audience,
        )

    except jwt.ExpiredSignatureError:
        www_authenticate_attrs.extend(
            [
                'error="invalid_token"',
                'error_description="The access token signature has expired."',
            ]
        )
        www_authenticate_value = build_www_authenticate_value()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": www_authenticate_value},
        )

    except jwt.JWTClaimsError as e:
        www_authenticate_attrs.extend(
            [
                'error="invalid_token"',
                f'error_description="{str(e)}"',
            ]
        )
        www_authenticate_value = build_www_authenticate_value()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": www_authenticate_value},
        )

    except jwt.JWTError:
        www_authenticate_attrs.extend(
            [
                'error="invalid_token"',
                'error_description="The access token signature is invalid"',
            ]
        )
        www_authenticate_value = build_www_authenticate_value()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": www_authenticate_value},
        )

    permissions = verified_claims.get("permissions") or []

    for scope in security_scopes.scopes:
        if scope not in permissions:
            www_authenticate_attrs.extend(
                [
                    'error="insufficient_scope"',
                    'error_description="The access token does not contain the required scope"',  # noqa: E501
                ]
            )
            www_authenticate_value = build_www_authenticate_value()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                headers={"WWW-Authenticate": www_authenticate_value},
            )
    return cast(TokenClaims, verified_claims)
