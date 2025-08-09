# Testing Guide for LinkedIn Personal Branding AI Agent

This guide will walk you through testing all components of the application step by step.

## Prerequisites

1. Python 3.8+ (for backend)
2. Node.js 16+ (for frontend)
3. Groq API key (free tier available)

## 1. Environment Setup

### Step 1: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys
nano .env
```

Add your Groq API key to the .env file:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

Note: For testing, you can use the existing key in the .env file, but it may have rate limits.

## 2. Running the Application with Docker (Recommended)

### Step 2: Build and Start All Services
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### Step 3: Verify Services Are Running
- Backend API: http://localhost:8000
- Frontend Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## 2b. Running the Application Without Docker (Local Development)

### Step 2b.1: Using the Run Script
```bash
# Make sure the script is executable
chmod +x run-local.sh

# Run the application
./run-local.sh
```

### Step 2b.2: Manual Setup
1. Set up Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. In another terminal, set up the frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Step 2b.3: Verify Services Are Running
- Backend API: http://localhost:8000
- Frontend Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## 4. Testing Backend API Endpoints

### Step 5: Test Root Endpoint
```bash
curl http://localhost:8000/
```
Expected response: `{"message": "Backend is running!"}`

### Step 6: Test Content Generation
```bash
curl -X POST http://localhost:8000/content/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "AI trends in 2025"}'
```

### Step 7: Test Profile Management
```bash
# Create a profile
curl -X POST "http://localhost:8000/profile/?name=Test%20User&headline=AI%20Developer&about=Testing%20the%20LinkedIn%20AI%20agent"

# Get profile
curl http://localhost:8000/profile/
```

### Step 8: Test Content Management
```bash
# List posts
curl http://localhost:8000/content/list

# Schedule a post (use an actual post ID from the list response)
curl -X POST "http://localhost:8000/content/schedule?post_id=1&delay_minutes=1"
```

### Step 9: Test Analytics
```bash
# Get analytics summary
curl http://localhost:8000/analytics/

# Get trends
curl http://localhost:8000/trends/
```

## 5. Testing the Frontend

### Step 10: Access the Dashboard
1. Open your browser and go to http://localhost:3000
2. You should see the dashboard with navigation menu

### Step 11: Test Profile Management
1. Click on "Profile" in the navigation
2. Fill in your profile information
3. Click "Save Profile"
4. Refresh the page to verify the information was saved

### Step 12: Test Content Generation
1. Click on "Generate" in the navigation
2. Enter a prompt like "Latest trends in artificial intelligence"
3. Click "Generate Content"
4. Verify the generated content appears
5. Click "Save as Draft"

### Step 13: Test Post Library
1. Click on "Posts" in the navigation
2. You should see your generated post in "draft" status
3. Click "Schedule" for the draft post
4. Enter "1" for delay minutes
5. Verify the post status changes to "scheduled"

### Step 14: Test Analytics
1. Click on "Analytics" in the navigation
2. You should see analytics data (mock data for MVP)

### Step 15: Test Trends
1. Click on "Trends" in the navigation
2. You should see industry trends

## 6. Testing Automated Scheduling

### Step 16: Verify Scheduled Posts Are Published
1. Create and schedule a post with a 1-minute delay
2. Wait for 1-2 minutes
3. Check the post library - the post status should change to "posted"
4. Check analytics - mock analytics should be generated for the post

## 7. Running Automated Tests

### Step 17: Run Backend Tests
```bash
# If running locally
pip install -r requirements.txt
python3 -m pytest tests/ -v

# If running with Docker
docker-compose exec backend python -m pytest tests/ -v
```

### Step 18: Run Frontend Tests (if available)
```bash
# Navigate to frontend directory
cd frontend

# Run frontend tests (if any were created)
npm test
```

## 8. Manual Testing Checklist

Go through this checklist to ensure all features work:

### Backend Features
- [ ] Root endpoint returns success message
- [ ] Content generation creates posts
- [ ] Profile creation and retrieval works
- [ ] Post scheduling works
- [ ] Scheduled posts are automatically published
- [ ] Analytics data is generated for published posts
- [ ] Trend data is returned

### Frontend Features
- [ ] Dashboard loads and shows stats
- [ ] Profile management saves and retrieves data
- [ ] Content generation works and saves drafts
- [ ] Post library shows posts with correct status
- [ ] Scheduling posts works
- [ ] Analytics page displays data
- [ ] Trends page shows industry trends

### Integration Features
- [ ] Generated content appears in post library
- [ ] Scheduled posts automatically publish
- [ ] Published posts get mock analytics
- [ ] All pages navigate correctly

## 9. Troubleshooting

### Common Issues

1. **Port already in use**:
   - Stop existing services: `docker-compose down` (if using Docker)
   - Kill processes on ports 8000 or 3000: `lsof -i :8000` and `kill -9 <PID>`

2. **Database errors**:
   - Clear volumes: `docker-compose down -v` (if using Docker)
   - Delete database files: `rm linkedin_ai.db` (for local development)

3. **Frontend not connecting to backend**:
   - Check if backend is running on http://localhost:8000
   - Verify API endpoints work with curl
   - Check browser console for CORS errors

4. **API key issues**:
   - Verify your Groq API key in .env
   - Check if you've hit rate limits

### Checking Logs
```bash
# View Docker logs (if using Docker)
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# For local development, check terminal outputs
```

## 10. Stopping the Application

### If using Docker:
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### If running locally:
```bash
# Press Ctrl+C in the terminals running the servers
# Or find and kill the processes:
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

This completes the full testing guide. You should now have a working MVP of the LinkedIn Personal Branding AI Agent!