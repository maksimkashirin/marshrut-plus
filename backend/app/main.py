from fastapi import FastAPI, HTTPException

from app.api.routes.cases import router as cases_router
from app.api.routes.users import router as users_router
from app.database import check_database_connection
from app.api.routes.route_steps import router as route_router
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.recommendations import router as recommendations_router


app = FastAPI(
    title="Маршрут+ API",
    description=(
        "Backend сервиса сопровождения родителей "
        "после получения заключения ПМПК"
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(cases_router)
app.include_router(route_router)
app.include_router(recommendations_router)


@app.get("/")
def root():
    return {
        "service": "Маршрут+",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.get("/health/db")
def database_health():
    try:
        check_database_connection()

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        ) from exc