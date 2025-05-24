import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import init_db
from app.api.webhook import router as webhook_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Run this on startup
    init_db()
    print("✅ Application startup complete.")
    yield
    # ❌ Optional: Code here runs on shutdown (if needed)

# ✅ Use the lifespan context when initializing FastAPI
app = FastAPI(lifespan=lifespan)

app.include_router(webhook_router)

@app.get("/")
def read_root():
    return {"message": "Email AI Assistant is live!"}

if __name__ == "__main__":
    # `main:app` ensures reload works correctly if main.py is reloaded
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)