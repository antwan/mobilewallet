import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from starlette.config import Config
from starlette.responses import RedirectResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from src import settings
from .resources import database
from .views import login, logout, balances, transactions


middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET, https_only=False)
]

routes = [
    Route("/transactions", endpoint=transactions, methods=["GET", "POST"]),
    Route("/balances", endpoint=balances, methods=["GET"]),
    Route("/login", endpoint=login, methods=["POST"]),
    Route("/logout", endpoint=logout, methods=["GET", "POST"]),
    Mount('/docs/', app=StaticFiles(directory='docs'), name="docs"),
    Route('/docs', endpoint=lambda request: RedirectResponse("/docs/index.html"), name="docs")
]

app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)
