# api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_db.database import get_db
from api.models.user_models import User, UserProfile, UserSkill
from api.auth import get_current_active_user
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Schemas
class ProfileUpdate(BaseModel):
    experience_level: Optional[str] = None
    location: Optional[str] = None
    salary_expectation: Optional[int] = None
    bio: Optional[str] = None
    preferred_job_type: Optional[str] = None
    availability: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None

class SkillCreate(BaseModel):
    skill_name: str
    skill_level: int
    category: str
    years_experience: Optional[int] = None

@router.put("/users/profile")
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Actualizar campos
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return {"message": "Profile updated successfully", "profile": profile}

@router.post("/users/skills")
async def add_skill(
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    skill = UserSkill(
        user_id=current_user.id,
        **skill_data.dict()
    )
    
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    return {"message": "Skill added successfully", "skill": skill}

@router.get("/users/skills")
async def get_skills(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    return {"skills": skills}

@router.delete("/users/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    skill = db.query(UserSkill).filter(
        UserSkill.id == skill_id, 
        UserSkill.user_id == current_user.id
    ).first()
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(skill)
    db.commit()
    
    return {"message": "Skill deleted successfully"}