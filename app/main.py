from fastapi import FastAPI
from app.studyplan.routes import router as study_plan_route

app = FastAPI()

app.include_router(study_plan_route)

@app.get("/")
async def root():
    return {"message":"application started!"}