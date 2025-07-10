from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.routes import users, auth, tasks


app = FastAPI()

# Allow CORS for all domains (or specify the domains you want)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to your frontend's URL, e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routes with /api prefix
app.include_router(router=users.router, prefix="/api")
app.include_router(router=auth.router, prefix="/api")
app.include_router(router=tasks.router, prefix="/api")

# Simple get to test Database Connection
@app.get("/")
def read_root():
    return {
        "message":"Welcome to my FastAPI Project",
        "status" : "The API is waiting for calls"
    }

@app.post("/echo")
def echo(data: dict):
    return {"message" : f"You said {data.get('text')}"}