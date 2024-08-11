import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints.users import router as user_router

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        log_level=settings.app.log_level,
    )
