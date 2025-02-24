from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class ContactInfo(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[HttpUrl] = None 

class Education(BaseModel):
    degree: Optional[str] = None
    university: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class Experience(BaseModel):
    position: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: Optional[List[str]] = None

class Project(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    link: Optional[HttpUrl] = None

class Achievement(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[str] = None

class UserProfile(BaseModel):
    _id: Optional[str] = None  
    name: Optional[str] = None
    contact: Optional[ContactInfo] = None
    education: Optional[List[Education]] = None
    experience: Optional[List[Experience]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[Project]] = None
    achievements: Optional[List[Achievement]] = None
