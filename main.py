import uvicorn
from fastapi import FastAPI
from app.db.db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Email AI Assistant is live!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)