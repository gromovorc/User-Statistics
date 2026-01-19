import uvicorn
from fastapi import FastAPI
from app.core.config import settings

from app.api.events import events_router

app = FastAPI(title=settings.app_name)
app.include_router(events_router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)