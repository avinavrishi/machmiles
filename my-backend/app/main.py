from fastapi import FastAPI, Header, HTTPException
from database.session import engine
from database import models
from fastapi.middleware.cors import CORSMiddleware

from routers import auth

# from core.config import CRQ_SECRET_KEY


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers here
app.include_router(auth.router, prefix="/rest/v1/auth", tags=["Authentication"])


if __name__ == "__main__":
    import uvicorn

    uvicorn_params = {
        "app": "main:app",
        "host": "127.0.0.1",
        "port": 8000,
        "reload": True,
    }

    uvicorn.run(**uvicorn_params)