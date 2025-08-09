import random
from datetime import datetime
from app.database import SessionLocal
from app.models.models import Post, Analytics

def mock_publish_post(post_id: int):
    """
    Mock publishing a post to LinkedIn.
    In a real implementation, this would connect to LinkedIn API.
    """
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            print(f"Post {post_id} not found")
            return False
            
        # Update post status to "posted"
        post.status = "posted"
        post.posted_at = datetime.utcnow()
        
        # Add a mock hashtag to indicate it was published
        if post.hashtags:
            post.hashtags += " #Published"
        else:
            post.hashtags = "#Published"
            
        db.add(post)
        db.commit()
        
        # Create mock analytics
        create_mock_analytics(post_id)
        
        print(f"Mock published post {post_id}")
        return True
    except Exception as e:
        print(f"Error publishing post {post_id}: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def create_mock_analytics(post_id: int):
    """
    Create mock analytics for a published post.
    """
    db = SessionLocal()
    try:
        # Generate realistic mock analytics
        likes = random.randint(10, 500)
        comments = random.randint(0, 50)
        shares = random.randint(0, 30)
        impressions = likes * random.randint(5, 20)
        
        analytics = Analytics(
            post_id=post_id,
            likes=likes,
            comments=comments,
            shares=shares,
            impressions=impressions
        )
        
        db.add(analytics)
        db.commit()
        print(f"Created mock analytics for post {post_id}")
    except Exception as e:
        print(f"Error creating analytics for post {post_id}: {e}")
        db.rollback()
    finally:
        db.close()

def get_mock_analytics(post_id: int = None):
    """
    Get mock analytics for a post or all posts.
    """
    db = SessionLocal()
    try:
        if post_id:
            analytics = db.query(Analytics).filter(Analytics.post_id == post_id).first()
        else:
            analytics = db.query(Analytics).all()
            
        return analytics
    finally:
        db.close()