
from backend.database import Base, engine
from fastapi import FastAPI
from backend.services.v1.router import v1_router

app = FastAPI(title="Kindergarten App")
app.include_router(v1_router, prefix="/api/v1")


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"V1:"}
