from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FinLedger Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # local only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is working 🎉"}

@app.get("/health")
def health():
    return {"status": "ok"}
