from fastapi import APIRouter

from app.route_dependencies import Security, get_verified_claims

router = APIRouter()


@router.get("/public")
async def ping() -> str:
    """Public route."""
    return "Success. You don't need to be authenticated to call this"


@router.get("/authenticated", dependencies=[Security(get_verified_claims)])
def secured_ping() -> str:
    """Authenticated route."""
    return "Success. You only get this message if you're authenticated"


@router.get(
    "/messages", dependencies=[Security(get_verified_claims, scopes=["read:messages"])]
)
def get_messages() -> str:
    """Get messages."""
    return "Success, authenticated with the 'read:messages' scope"


@router.post(
    "/messages",
    dependencies=[Security(get_verified_claims, scopes=["create:messages"])],
)
def create_message() -> str:
    """Create a new message."""
    return "Success, authenticated with the 'create:messages' scope"
