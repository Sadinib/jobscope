# api/models/user_models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sql_db.database import Base
import enum

class ExperienceLevel(enum.Enum):
    intern = "intern"
    junior = "junior" 
    mid = "mid"
    senior = "senior"
    lead = "lead"
    principal = "principal"

class JobType(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    freelance = "freelance"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con perfil
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    skills = relationship("UserSkill", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    experience_level = Column(Enum(ExperienceLevel))
    location = Column(String(100))
    salary_expectation = Column(Integer)  # En COP mensuales
    bio = Column(Text)
    preferred_job_type = Column(Enum(JobType))
    availability = Column(String(50))  # "immediate", "1_month", "3_months"
    website = Column(String(255))
    github = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="profile")

class UserSkill(Base):
    __tablename__ = "user_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    skill_level = Column(Integer)  # 1-5, donde 5 es experto
    category = Column(String(50))  # "programming", "framework", "tool", "soft"
    years_experience = Column(Integer)
    
    user = relationship("User", back_populates="skills")