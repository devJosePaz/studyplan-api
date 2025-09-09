from fastapi import FastAPI
from app.db import Base, engine
from app.routers import auth, profile, plan

app = FastAPI(title="ML Plano de Estudo API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(plan.router)
