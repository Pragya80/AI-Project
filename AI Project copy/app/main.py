from fastapi import FastAPI
from app.routes import content, profile, auth, trends, analytics
from app.models.models import Post
from app.database import engine, Base

app = FastAPI(
    title="LinkedIn Branding AI Agent",
    description="An AI agent that creates and posts LinkedIn content for personal branding",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # Alternative docs UI
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(content.router)
app.include_router(profile.router)
app.include_router(auth.router)
app.include_router(trends.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Backend is running!"}
