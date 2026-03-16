import uvicorn
from fastapi import FastAPI
from app.core.config import settings

import app.api.routers.events as events
import app.api.routers.stats as stats
import app.api.routers.users as users

app = FastAPI(title=settings.app_name)
app.include_router(events.router)
app.include_router(stats.router)
app.include_router(users.router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)