# app/routes/content.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models.models import Post, Analytics
import os, requests, random, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"  # keep if using Groq

router = APIRouter(prefix="/content", tags=["Content"])

# Start background scheduler
scheduler = BackgroundScheduler()
scheduler.start()


# ---------------------------
# Helper: call Groq (or fallback)
# ---------------------------
def call_groq_chat(prompt: str) -> str:
    if not GROQ_API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a professional LinkedIn copywriter. Produce a concise LinkedIn post and suggest 3 hashtags."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            # Groq / OpenAI-like response shape:
            return data["choices"][0]["message"]["content"]
        else:
            print("Groq API error:", r.status_code, r.text)
            return None
    except Exception as e:
        print("Groq request failed:", e)
        return None

def simple_local_generate(prompt: str) -> str:
    # Minimal safe fallback for offline/demo use.
    hashtags = " #AI #Marketing #PersonalBranding"
    out = f"{prompt}\n\nThis is a generated LinkedIn-style post (demo).{hashtags}"
    return out

# ---------------------------
# Helper: publish (mock)
# ---------------------------
def publish_post_and_create_analytics(post_id: int):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            print("publish_post: post not found", post_id)
            return False
        # Mock publishing: mark posted_at, status
        post.posted_at = datetime.datetime.utcnow()
        post.status = "posted"
        # tag as posted
        post.hashtags = (post.hashtags or "") + " #AutoPosted"
        db.add(post)
        db.commit()

        # Create mock analytics
        likes = random.randint(20, 300)
        comments = random.randint(0, 50)
        shares = random.randint(0, 30)
        impressions = likes * random.randint(10, 30)

        analytics = Analytics(
            post_id=post.id,
            likes=likes,
            comments=comments,
            shares=shares,
            impressions=impressions
        )
        db.add(analytics)
        db.commit()
        print(f"[AUTO-POST] Published post {post_id} -> likes {likes}, comments {comments}")
        return True
    except Exception as e:
        db.rollback()
        print("publish_post error:", e)
        return False
    finally:
        db.close()


# ---------------------------
# Background poller job
# ---------------------------
def check_and_publish_due_posts():
    db = SessionLocal()
    try:
        now = datetime.datetime.utcnow()
        due_posts = db.query(Post).filter(
            Post.status == "scheduled",
            Post.scheduled_time != None,
            Post.scheduled_time <= now
        ).all()
        for p in due_posts:
            print("Publishing due post:", p.id)
            # publish (mock) and create analytics
            publish_post_and_create_analytics(p.id)
    except Exception as e:
        print("check_and_publish_due_posts error:", e)
    finally:
        db.close()

# schedule the poller every minute (safe for demo)
scheduler.add_job(check_and_publish_due_posts, "interval", minutes=1)


# ---------------------------
# Endpoints
# ---------------------------

@router.post("/generate")
def generate_content(prompt: str, db: Session = Depends(get_db)):
    """
    Generate content using Groq (or fallback), save to DB as draft and return it.
    Request body: {"prompt": "Your prompt here"}
    """
    # build enriched prompt if you want (pull profile/trends here if desired)
    # For demo we just use the prompt
    ai_text = call_groq_chat(prompt)
    if not ai_text:
        ai_text = simple_local_generate(prompt)

    # attempt to extract hashtags if present (simple heuristic)
    hashtags = None
    # naive: last line hashtags if starts with '#'
    last_lines = ai_text.strip().splitlines()
    if last_lines and last_lines[-1].strip().startswith("#"):
        hashtags = last_lines[-1].strip()
    else:
        hashtags = "#AI #LinkedIn"

    post = Post(prompt=prompt, content=ai_text, hashtags=hashtags, status="draft")
    db.add(post)
    db.commit()
    db.refresh(post)

    return {"message": "Generated and saved (draft)", "post": {"id": post.id, "content": post.content, "hashtags": post.hashtags}}


@router.get("/list")
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return {
        "total": len(posts),
        "posts": [
            {
                "id": p.id,
                "prompt": p.prompt,
                "content": (p.content[:800] + "...") if len(p.content or "") > 800 else p.content,
                "hashtags": p.hashtags,
                "status": p.status,
                "scheduled_time": p.scheduled_time,
                "posted_at": p.posted_at
            } for p in posts
        ]
    }


@router.post("/schedule")
def schedule_post(post_id: int, scheduled_time: datetime.datetime = None, delay_minutes: int = None, db: Session = Depends(get_db)):
    """
    Schedule a post either by absolute datetime (ISO) or by delay_minutes.
    Example (JSON form fields):
    - post_id: integer
    - scheduled_time: "2025-08-09T15:30:00"  (optional)
    - delay_minutes: 10  (optional)
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if delay_minutes is not None:
        run_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(delay_minutes))
    elif scheduled_time is not None:
        # if client passed a string, FastAPI will parse into datetime
        run_at = scheduled_time
        # ensure UTC naive -> treat as UTC
        if run_at.tzinfo is not None:
            run_at = run_at.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    else:
        raise HTTPException(status_code=400, detail="Provide scheduled_time or delay_minutes")

    # save schedule in DB
    post.scheduled_time = run_at
    post.status = "scheduled"
    db.add(post)
    db.commit()
    db.refresh(post)

    # (optional) also add a scheduled job to run exactly at run_at to publish
    scheduler.add_job(publish_post_and_create_analytics, "date", run_date=run_at, args=[post.id])

    return {"message": "Post scheduled", "post_id": post.id, "run_at": run_at.isoformat()}


@router.get("/analytics")
def content_analytics(db: Session = Depends(get_db)):
    """
    Returns analytics summary for all posts and per-post metrics.
    """
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    analytics_rows = db.query(Analytics).all()
    analytics_by_post = {}
    for a in analytics_rows:
        analytics_by_post[a.post_id] = {
            "likes": a.likes,
            "comments": a.comments,
            "shares": a.shares,
            "impressions": a.impressions
        }

    rows = []
    for p in posts:
        rows.append({
            "post_id": p.id,
            "status": p.status,
            "content_preview": (p.content[:200] + "...") if p.content and len(p.content) > 200 else (p.content or ""),
            "analytics": analytics_by_post.get(p.id, {"likes": 0, "comments": 0, "shares": 0, "impressions": 0})
        })

    return {"total_posts": len(posts), "rows": rows}
