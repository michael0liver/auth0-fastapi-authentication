from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    TypedDict,
    TypeVar,
    Union,
)
from urllib.parse import urlencode

from fastapi import params
from fastapi.security import OAuth2AuthorizationCodeBearer


class TokenClaims(TypedDict):
    """Auth0 access token claims.

    See https://auth0.com/docs/tokens/access-tokens for more.
    """

    iss: str
    sub: str
    aud: Union[str, List[str]]
    iat: int
    exp: int
    azp: str
    scope: Optional[str]
    permissions: Optional[List[str]]


ScopeT = TypeVar("ScopeT", bound=str)


class Auth0OAuth2AuthorizationCodeBearer(
    Generic[ScopeT], OAuth2AuthorizationCodeBearer
):
    """Implements the OAuth2AuthorizationCodeBearer for Auth0.

    Args:
        domain: Auth0 domain.
        audience: API audience.
        scheme_name: Optional; Name used in the OpenAPI document.
            Defaults to the class name if not provided.
        scopes: Optional; A dictionary mapping scope names to the
            corresponding descriptions, these are used in the OpenAPI document.
        auto_error: Optional; Whether to automatically raise an HTTP error
            for a missing or invalid Authorization header.
    """

    def __init__(
        self,
        domain: str,
        audience: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[ScopeT, str]] = None,
        auto_error: bool = True,
    ) -> None:
        self.domain = domain
        self.audience = audience

        self.base_url = f"https://{self.domain}"
        audience_qs = urlencode({"audience": self.audience})
        self.authorization_url = f"{self.base_url}/authorize?{audience_qs}"
        self.token_url = f"{self.base_url}/oauth/token"
        self.jwks_url = f"{self.base_url}/.well-known/jwks.json"

        if not scopes:
            scopes = {}

        super().__init__(
            authorizationUrl=self.authorization_url,
            tokenUrl=self.token_url,
            refreshUrl=None,
            scheme_name=scheme_name,
            scopes=scopes,
            auto_error=auto_error,
        )

    def security(
        self,
        dependency: Callable[..., Any],
        *,
        scopes: Optional[Sequence[ScopeT]] = None,
        use_cache: bool = True,
    ) -> Any:
        """Declare a callable dependency with scopes.

        This function wraps `fastapi.Security` but allows for the scopes argument
        to be type checked. See the example below for how to use this feature.

        Example::

            from typing import Literal

            from fastapi import FastAPI

            app = FastAPI()

            Scope = Literal["read:users", "write:users"]

            auth0_scheme = Auth0OAuth2AuthorizationCodeBearer[Scope](
                domain="example.auth0.com",
                audience="https://example-audience.com",
                # The keys of the scopes dictionary can be type checked
                scopes={
                    "read:users": "Read users",
                    "write:users": "Write users",
                },
            )

            Security = auth0_scheme.security


            async def foo() -> str:
                return ""


            # The scopes passed to `Security` can be type checked
            @app.get("/bar")
            async def bar(foo: str = Security(foo, scopes=["read:users"])):
                pass
        """
        return params.Security(
            dependency=dependency, scopes=scopes, use_cache=use_cache
        )
