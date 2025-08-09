from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Analytics, Post
from app.services.mock_publisher import get_mock_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Get analytics summary for all posts.
    """
    analytics_data = get_mock_analytics()
    
    if not analytics_data:
        return {"message": "No analytics data available", "total_posts": 0}
    
    # If it's a list, calculate totals
    if isinstance(analytics_data, list):
        total_likes = sum(a.likes for a in analytics_data)
        total_comments = sum(a.comments for a in analytics_data)
        total_shares = sum(a.shares for a in analytics_data)
        total_impressions = sum(a.impressions for a in analytics_data)
        
        return {
            "total_posts": len(analytics_data),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_impressions": total_impressions,
            "average_engagement": {
                "likes": total_likes / len(analytics_data) if analytics_data else 0,
                "comments": total_comments / len(analytics_data) if analytics_data else 0,
                "shares": total_shares / len(analytics_data) if analytics_data else 0
            }
        }
    else:
        # Single analytics record
        return {
            "post_id": analytics_data.post_id,
            "likes": analytics_data.likes,
            "comments": analytics_data.comments,
            "shares": analytics_data.shares,
            "impressions": analytics_data.impressions
        }

@router.get("/post/{post_id}")
def get_post_analytics(post_id: int, db: Session = Depends(get_db)):
    """
    Get analytics for a specific post.
    """
    analytics = db.query(Analytics).filter(Analytics.post_id == post_id).first()
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not analytics:
        return {"message": "No analytics found for this post", "post_id": post_id}
    
    return {
        "post_id": post_id,
        "post_content": post.content[:100] + "..." if post and len(post.content or "") > 100 else (post.content if post else ""),
        "analytics": {
            "likes": analytics.likes,
            "comments": analytics.comments,
            "shares": analytics.shares,
            "impressions": analytics.impressions
        }
    }

@router.get("/top-performing")
def get_top_performing_posts(limit: int = 5, db: Session = Depends(get_db)):
    """
    Get top performing posts based on engagement.
    """
    # Simple engagement score: likes + comments * 2 + shares * 3
    top_posts = db.query(Analytics, Post).join(Post).order_by(
        (Analytics.likes + Analytics.comments * 2 + Analytics.shares * 3).desc()
    ).limit(limit).all()
    
    result = []
    for analytics, post in top_posts:
        engagement_score = analytics.likes + analytics.comments * 2 + analytics.shares * 3
        result.append({
            "post_id": post.id,
            "post_preview": post.content[:100] + "..." if len(post.content or "") > 100 else (post.content or ""),
            "analytics": {
                "likes": analytics.likes,
                "comments": analytics.comments,
                "shares": analytics.shares,
                "impressions": analytics.impressions
            },
            "engagement_score": engagement_score
        })
    
    return {"top_posts": result}