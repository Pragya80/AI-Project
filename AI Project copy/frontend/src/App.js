import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Set base URL for API calls
axios.defaults.baseURL = 'http://localhost:8000';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/generate" element={<ContentGenerator />} />
            <Route path="/posts" element={<PostLibrary />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/trends" element={<Trends />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function Header() {
  return (
    <header className="app-header">
      <h1>LinkedIn AI Agent</h1>
      <nav>
        <ul>
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/profile">Profile</Link></li>
          <li><Link to="/generate">Generate</Link></li>
          <li><Link to="/posts">Posts</Link></li>
          <li><Link to="/analytics">Analytics</Link></li>
          <li><Link to="/trends">Trends</Link></li>
        </ul>
      </nav>
    </header>
  );
}

function Dashboard() {
  const [stats, setStats] = useState({
    totalPosts: 0,
    scheduledPosts: 0,
    publishedPosts: 0
  });

  useEffect(() => {
    // Fetch dashboard stats
    const fetchStats = async () => {
      try {
        const response = await axios.get('/content/list');
        const posts = response.data.posts;
        setStats({
          totalPosts: posts.length,
          scheduledPosts: posts.filter(p => p.status === 'scheduled').length,
          publishedPosts: posts.filter(p => p.status === 'posted').length
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Posts</h3>
          <p>{stats.totalPosts}</p>
        </div>
        <div className="stat-card">
          <h3>Scheduled</h3>
          <p>{stats.scheduledPosts}</p>
        </div>
        <div className="stat-card">
          <h3>Published</h3>
          <p>{stats.publishedPosts}</p>
        </div>
      </div>
      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <Link to="/generate" className="btn">Generate New Post</Link>
        <Link to="/trends" className="btn">View Trends</Link>
      </div>
    </div>
  );
}

function Profile() {
  const [profile, setProfile] = useState({
    name: '',
    headline: '',
    about: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch existing profile
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/profile/');
        if (response.data && response.data.name) {
          setProfile({
            name: response.data.name || '',
            headline: response.data.headline || '',
            about: response.data.about || ''
          });
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post('/profile/', null, {
        params: {
          name: profile.name,
          headline: profile.headline,
          about: profile.about
        }
      });
      alert('Profile saved successfully!');
    } catch (error) {
      console.error('Error saving profile:', error);
      alert('Error saving profile');
    }
    setLoading(false);
  };

  const handleChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="profile">
      <h2>Profile Management</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={profile.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="headline">Headline:</label>
          <input
            type="text"
            id="headline"
            name="headline"
            value={profile.headline}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="about">About:</label>
          <textarea
            id="about"
            name="about"
            value={profile.about}
            onChange={handleChange}
            rows="4"
          />
        </div>
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Saving...' : 'Save Profile'}
        </button>
      </form>
    </div>
  );
}

function ContentGenerator() {
  const [prompt, setPrompt] = useState('');
  const [generatedContent, setGeneratedContent] = useState('');
  const [hashtags, setHashtags] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/content/generate', { prompt });
      setGeneratedContent(response.data.post.content);
      setHashtags(response.data.post.hashtags);
    } catch (error) {
      console.error('Error generating content:', error);
      alert('Error generating content');
    }
    setLoading(false);
  };

  const handleSave = async () => {
    // In a real app, you might want to save the generated content
    alert('Content saved as draft!');
    navigate('/posts');
  };

  return (
    <div className="content-generator">
      <h2>Content Generator</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="prompt">Enter your content prompt:</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows="3"
            placeholder="e.g., Write a post about the latest AI trends..."
            required
          />
        </div>
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Content'}
        </button>
      </form>
      
      {generatedContent && (
        <div className="generated-content">
          <h3>Generated Content:</h3>
          <div className="content-preview">
            <p>{generatedContent}</p>
            <p className="hashtags">{hashtags}</p>
          </div>
          <button onClick={handleSave} className="btn">Save as Draft</button>
        </div>
      )}
    </div>
  );
}

function PostLibrary() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/content/list');
      setPosts(response.data.posts);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
    setLoading(false);
  };

  const handleSchedule = async (postId) => {
    const delay = prompt('Enter delay in minutes (e.g., 5 for 5 minutes from now):');
    if (!delay) return;
    
    try {
      await axios.post('/content/schedule', null, {
        params: {
          post_id: postId,
          delay_minutes: parseInt(delay)
        }
      });
      alert('Post scheduled successfully!');
      fetchPosts(); // Refresh the list
    } catch (error) {
      console.error('Error scheduling post:', error);
      alert('Error scheduling post');
    }
  };

  return (
    <div className="post-library">
      <h2>Post Library</h2>
      <button onClick={fetchPosts} className="btn">Refresh</button>
      {loading ? (
        <p>Loading posts...</p>
      ) : (
        <div className="posts-list">
          {posts.map(post => (
            <div key={post.id} className={`post-card status-${post.status}`}>
              <h3>Post #{post.id}</h3>
              <p><strong>Status:</strong> {post.status}</p>
              <p><strong>Content:</strong> {post.content}</p>
              <p><strong>Hashtags:</strong> {post.hashtags}</p>
              {post.scheduled_time && (
                <p><strong>Scheduled for:</strong> {new Date(post.scheduled_time).toLocaleString()}</p>
              )}
              {post.posted_at && (
                <p><strong>Posted at:</strong> {new Date(post.posted_at).toLocaleString()}</p>
              )}
              <div className="post-actions">
                {post.status === 'draft' && (
                  <button onClick={() => handleSchedule(post.id)} className="btn">Schedule</button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/analytics/');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
    setLoading(false);
  };

  if (loading) return <p>Loading analytics...</p>;
  
  if (!analytics) return <p>No analytics data available</p>;

  return (
    <div className="analytics">
      <h2>Analytics</h2>
      <button onClick={fetchAnalytics} className="btn">Refresh</button>
      <div className="analytics-summary">
        <h3>Summary</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <h4>Total Posts</h4>
            <p>{analytics.total_posts || 0}</p>
          </div>
          <div className="stat-card">
            <h4>Total Likes</h4>
            <p>{analytics.total_likes || 0}</p>
          </div>
          <div className="stat-card">
            <h4>Total Comments</h4>
            <p>{analytics.total_comments || 0}</p>
          </div>
          <div className="stat-card">
            <h4>Total Shares</h4>
            <p>{analytics.total_shares || 0}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Trends() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTrends();
  }, []);

  const fetchTrends = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/trends/');
      setTrends(response.data.trends);
    } catch (error) {
      console.error('Error fetching trends:', error);
    }
    setLoading(false);
  };

  return (
    <div className="trends">
      <h2>Industry Trends</h2>
      <button onClick={fetchTrends} className="btn">Refresh</button>
      {loading ? (
        <p>Loading trends...</p>
      ) : (
        <div className="trends-list">
          <h3>Latest Trends</h3>
          <ul>
            {trends.map((trend, index) => (
              <li key={index}>{trend}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;