# to activate venv use "C:\repos\FccFastApi\venv\Scripts\activate.ps1"
# to start server use "uvicorn app.main:app --reload"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import schemas
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)  überflüssig wenn man alembic benutzt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/", response_model=schemas.Message)
def root():
    return {"message": "This is only the root."}