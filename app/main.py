from fastapi import FastAPI
from app.studyplan.routes import router as study_plan_route         # CRUD simples
from app.studyplan.generate_routes import router as study_gen_route # geração (ML + regras) — rota separada
from app.profile.routes import router as profile_route
from app.auth.routes import router as auth_route
from app.config.database import engine, Base

app = FastAPI(
    title="StudyPlan API",
    version="0.1.0",
    description="API do TCC: perfis comportamentais e planos de estudo (CRUD + geração separada).",
)


app.include_router(study_plan_route)
app.include_router(study_gen_route)   
app.include_router(profile_route)
app.include_router(auth_route)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("tables created/verified.")

@app.get("/")
async def root():
    return {"message": "application started!"}
