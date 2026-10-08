from fastapi import FastAPI

from app.database import Base,engine
from app.models import GenerationJob,Certificate
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="Bulk Certificate Generator API",
    description="API for generating certificates in bulk",
    version="1.0.0"
)

app.include_router(router,prefix="/api")