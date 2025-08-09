# LinkedIn Personal Branding AI Agent

An AI agent that researches, creates, and posts LinkedIn content for personal branding.

## Features

- **Content Generation**: AI-powered LinkedIn post generation
- **Profile Management**: Store and manage your LinkedIn profile information
- **Content Scheduling**: Schedule posts for future publishing
- **Analytics**: Track post performance with mock analytics
- **Trend Analysis**: Get industry trends and content suggestions
- **Automated Posting**: Automatic posting of scheduled content

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: React, Axios
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Services**: Groq API (Llama3)
- **Deployment**: Docker, Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Node.js 16+ (for frontend development)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd linkedin-ai-agent
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
  - Frontend: http://localhost:3000
  - Backend API: http://localhost:8000
  - API Documentation: http://localhost:8000/docs

### Running Without Docker

If you prefer to run the application without Docker:

1. Make the local run script executable and run it:
  ```bash
  chmod +x run-local.sh
  ./run-local.sh
  ```

2. Or set up and run manually:
  ```bash
  # Set up Python virtual environment
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  
  # Start backend (in one terminal)
  uvicorn app.main:app --reload
  
  # Set up and start frontend (in another terminal)
  cd frontend
  npm install
  npm start
  ```

### Local Development

#### Quick Setup
```bash
chmod +x setup-dev.sh
./setup-dev.sh
```

#### Manual Setup

##### Backend

1. Set up Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

##### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Run the frontend:
   ```bash
   npm start
   ```

## API Endpoints

### Content
- `POST /content/generate` - Generate LinkedIn content
- `GET /content/list` - List all posts
- `POST /content/schedule` - Schedule a post

### Profile
- `POST /profile/` - Create/update profile
- `GET /profile/` - Get profile

### Analytics
- `GET /analytics/` - Get analytics summary
- `GET /analytics/post/{post_id}` - Get analytics for a specific post

### Trends
- `GET /trends/` - Get industry trends
- `GET /trends/suggestions` - Get content suggestions

## Testing

For detailed testing instructions, see [TESTING.md](TESTING.md).

Run backend tests:
```bash
pytest tests/
```

## Project Structure

```
├── app/                 # Backend application
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   ├── database.py      # Database configuration
│   └── main.py          # Application entry point
├── frontend/            # React frontend
│   ├── src/             # Source code
│   └── package.json     # Dependencies
├── tests/               # Backend tests
├── requirements.txt     # Python dependencies
├── Dockerfile           # Backend Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # This file
```

## MVP Features Implemented

1. ✅ Content Generation with AI
2. ✅ Profile Management
3. ✅ Content Scheduling
4. ✅ Mock Analytics
5. ✅ Trend Analysis
6. ✅ Automated Posting (mock)
7. ✅ Web Dashboard
8. ✅ Docker Deployment

## What's Missing (Future Enhancements)

1. Actual LinkedIn API Integration
2. Advanced Content Strategy
3. A/B Testing
4. Compliance & Ethics Engine
5. Advanced Analytics Visualization
6. Real Industry Research (News APIs)