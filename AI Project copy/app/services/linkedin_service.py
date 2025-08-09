import random
from app.database import SessionLocal
from app.models.models import Profile

def analyze_linkedin_profile(profile_id: int = None):
    """
    Mock LinkedIn profile analysis.
    In a real implementation, this would connect to LinkedIn API.
    """
    db = SessionLocal()
    try:
        # Get profile from database if ID provided, otherwise get first profile
        if profile_id:
            profile = db.query(Profile).filter(Profile.id == profile_id).first()
        else:
            profile = db.query(Profile).first()
            
        if not profile:
            # Return a default profile for demo purposes
            return {
                "name": "Demo User",
                "headline": "AI Enthusiast & Developer",
                "about": "Passionate about AI and technology. Sharing insights on LinkedIn.",
                "skills": ["AI", "Machine Learning", "Python", "Data Science"],
                "interests": ["Technology", "Innovation", "Startups"],
                "experience": "5+ years in tech industry"
            }
        
        # Extract mock skills and interests based on profile content
        skills = extract_mock_skills(profile)
        interests = extract_mock_interests(profile)
        
        return {
            "name": profile.name,
            "headline": profile.headline or "Professional",
            "about": profile.about or "LinkedIn user",
            "skills": skills,
            "interests": interests,
            "experience": "Experience level unknown"
        }
    finally:
        db.close()

def extract_mock_skills(profile):
    """Extract mock skills from profile content."""
    # In a real implementation, this would use NLP to extract skills
    base_skills = ["Communication", "Leadership", "Problem Solving", "Teamwork"]
    
    # Add skills based on profile content
    if profile.about:
        if "ai" in profile.about.lower() or "artificial intelligence" in profile.about.lower():
            base_skills.extend(["AI", "Machine Learning"])
        if "data" in profile.about.lower():
            base_skills.extend(["Data Analysis", "Statistics"])
        if "python" in profile.about.lower():
            base_skills.append("Python")
        if "marketing" in profile.about.lower():
            base_skills.extend(["Digital Marketing", "Content Strategy"])
    
    return base_skills[:5]  # Limit to 5 skills

def extract_mock_interests(profile):
    """Extract mock interests from profile content."""
    # In a real implementation, this would use NLP to extract interests
    base_interests = ["Technology", "Innovation", "Professional Development"]
    
    # Add interests based on profile content
    if profile.about:
        if "ai" in profile.about.lower() or "artificial intelligence" in profile.about.lower():
            base_interests.extend(["AI Research", "Machine Learning"])
        if "data" in profile.about.lower():
            base_interests.append("Data Science")
        if "startup" in profile.about.lower():
            base_interests.append("Entrepreneurship")
        if "marketing" in profile.about.lower():
            base_interests.extend(["Digital Marketing", "Personal Branding"])
    
    return base_interests[:4]  # Limit to 4 interests

def get_mock_trends(industry_keywords: list = None):
    """
    Get mock industry trends.
    In a real implementation, this would connect to news APIs or RSS feeds.
    """
    if not industry_keywords:
        industry_keywords = ["technology", "AI", "innovation"]
    
    trends = [
        f"Latest developments in {random.choice(industry_keywords)}",
        f"How {random.choice(industry_keywords)} is changing the industry",
        f"Future of {random.choice(industry_keywords)} in business",
        f"Best practices for {random.choice(industry_keywords)} implementation",
        f"Emerging {random.choice(industry_keywords)} trends to watch"
    ]
    
    return trends