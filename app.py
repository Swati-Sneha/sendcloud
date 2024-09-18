from fastapi import FastAPI
from src.routes.timer import timerRoutes
from src.utilities.logging_config import setup_logging

setup_logging()

app = FastAPI(redirect_slashes=False)

app.include_router(timerRoutes, prefix="/timer")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)