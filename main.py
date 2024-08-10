import uvicorn
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        log_level=settings.app.log_level,
    )
