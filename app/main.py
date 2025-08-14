from fastapi import FastAPI
from app.studyplan.routes import router as study_plan_route
from app.profile.routes import router as profile_route
from app.config.database import engine, Base

app = FastAPI()

app.include_router(study_plan_route)
app.include_router(profile_route)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("tables created/verified.")

@app.get("/")
async def root():
    return {"message": "application started!"}
