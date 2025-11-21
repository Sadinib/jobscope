from fastapi import APIRouter

router = APIRouter()

@router.get("/jobs")
async def get_jobs():
    return {"message": "Jobs endpoint - por implementar"}