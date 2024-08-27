from fastapi import FastAPI
import uvicorn
from .base import router as base_router
from .someapi import router as someapi_router
from ..services.mainservice import MainService


def create_app(mainservice: MainService):
    app = FastAPI(title="Template Service")
    # Include all routes, this way the API routes can be easily split into several files
    app.include_router(base_router)
    app.include_router(someapi_router)
    app.mainservice = mainservice # Inject service here so it can be used by the routes
    return app


def run_api(mainservice: MainService):
    """Blocking entrypoint to run the APIs, must be called last as it blocks and never returns"""
    # Init app
    app = create_app(mainservice)
    # Run app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
