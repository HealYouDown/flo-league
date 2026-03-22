from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import auth, matches, players, rounds, seasons
from src.lifespan import lifespan
from src.openapi import custom_openapi, generate_openapi_id


def create_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        generate_unique_id_function=generate_openapi_id,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "https://flo-league.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(players.router)
    app.include_router(seasons.router)
    app.include_router(rounds.router)
    app.include_router(matches.router)

    app.openapi = lambda app=app: custom_openapi(app)

    return app
