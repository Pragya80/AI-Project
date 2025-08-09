from fastapi import APIRouter
from app.services.linkedin_service import get_mock_trends

router = APIRouter(prefix="/trends", tags=["Trends"])

@router.get("/")
def get_trends(industry: str = None):
    """
    Get mock industry trends.
    In a real implementation, this would connect to news APIs or RSS feeds.
    """
    keywords = [industry] if industry else None
    trends = get_mock_trends(keywords)
    return {"trends": trends, "count": len(trends)}

@router.get("/suggestions")
def get_content_suggestions():
    """
    Get content suggestions based on trends.
    """
    trends = get_mock_trends()
    suggestions = [f"Write about: {trend}" for trend in trends[:3]]
    return {"suggestions": suggestions}