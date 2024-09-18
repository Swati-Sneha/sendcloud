from fastapi import FastAPI
from src.routes.timer import timerRoutes

app = FastAPI()

app.include_router(timerRoutes, prefix="/timer")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)