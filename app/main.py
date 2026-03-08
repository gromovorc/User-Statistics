import uvicorn
from fastapi import FastAPI
from app.core.config import settings

from app.api.routers.events import events_router
from app.api.routers.stats import stats_router

app = FastAPI(title=settings.app_name)
app.include_router(events_router)
app.include_router(stats_router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)