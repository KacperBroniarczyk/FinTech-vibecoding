from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="FinTech Core API - Final")
app.include_router(router)