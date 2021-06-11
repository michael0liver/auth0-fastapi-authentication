from fastapi import FastAPI

from app.config import config
from app.routes import router

app = FastAPI(
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/
    swagger_ui_init_oauth={
        "clientId": config.AUTH0_APPLICATION_CLIENT_ID,
        "usePkceWithAuthorizationCodeGrant": True,
    },
)
app.state.config = config
app.include_router(router)
