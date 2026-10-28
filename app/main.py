import uuid
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ProjectCreate

app = FastAPI(
    title="Multi-Agent System API",
    description="Core asynchronous communication API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI and Docker!"}

@app.post("/api/v1/projects", status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    project_id = str(uuid.uuid4())
    return {
        "message": "Project creation accepted",
        "project_id": project_id,
        "status": "processing"
    }