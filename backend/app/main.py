from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import persons

app = FastAPI(title="Arab Genealogy Tree API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(persons.router)


@app.get("/health")
def health():
    return {"status": "ok"}
