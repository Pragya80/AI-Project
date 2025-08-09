from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Profile

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/")
def create_profile(name: str, headline: str = None, about: str = None, db: Session = Depends(get_db)):
    profile = Profile(name=name, headline=headline, about=about)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"message": "Profile created successfully", "profile": profile.__dict__}

@router.get("/")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        return {"message": "No profile found"}
    return profile.__dict__
