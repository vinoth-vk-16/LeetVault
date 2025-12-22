# LeetVault

> Automate your LeetCode progress tracking with seamless GitHub integration

LeetVault is a full-stack application that automatically syncs your LeetCode submissions to GitHub repositories, providing beautiful progress tracking and organized code storage.

## 🚀 Features

- **🔐 Google Authentication**: Secure login with Firebase
- **🐙 GitHub Integration**: Connect repositories via GitHub App
- **📊 Automatic Sync**: Parallel processing for 1000+ users simultaneously
- **📈 Progress Tracking**: Beautiful markdown reports with statistics
- **🗂️ Organized Structure**: Problems organized by difficulty and topic
- **⚡ High Performance**: Async/parallel processing for maximum efficiency
- **🎨 Modern UI**: Dark theme with animated backgrounds
- **🔄 Auto-Refresh**: Expired LeetCode sessions automatically refreshed

## 📁 Project Structure

```
leetvault/
├── leetVault-fe/           # React frontend (Vite + Tailwind)
├── LeetVault-gitleet/      # GitHub integration API (FastAPI)
├── leetcode_fetch/         # LeetCode sync service (FastAPI)
├── DEPLOYMENT.md           # Deployment guide
└── README.md               # This file
```

## 🏗️ Architecture

### Frontend (React + Vite)
- Modern React 19 with Vite
- Firebase Authentication (Google Sign-In)
- Tailwind CSS for styling
- WebGL animated backgrounds
- React Router for navigation

### Backend Services

#### 1. LeetVault-gitleet (GitHub Integration)
- FastAPI backend
- GitHub App OAuth flow
- Repository management
- User authentication
- LeetCode credentials storage

#### 2. leetcode_fetch (Sync Service)
- **Appwrite Scheduled Execution**: Automatically triggered by Appwrite cron (daily at 6:20 PM UTC)
- **Parallel Processing**: Syncs ALL active repos simultaneously
- Fetches LeetCode submissions via GraphQL
- Pushes to GitHub repositories
- Auto-refreshes expired sessions
- Scalable to 1000+ users

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.9+
- Appwrite account
- Firebase project
- GitHub App

### 1. Frontend Setup

```bash
cd leetVault-fe
npm install
cp env.example .env
# Edit .env with your Firebase credentials
npm run dev
```

### 2. Backend Setup

Both backend services use Appwrite Functions:

```bash
# LeetVault-gitleet
cd LeetVault-gitleet
pip install -r requirements.txt
# Configure .env with Appwrite & GitHub credentials
# Deploy to Appwrite Functions

# leetcode_fetch
cd leetcode_fetch
pip install -r requirements.txt
# Configure .env with Appwrite & GitHub credentials
# Deploy to Appwrite Functions
```

## 📖 Documentation

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Complete deployment guide
- **[leetVault-fe/README.md](./leetVault-fe/README.md)** - Frontend documentation
- **[leetcode_fetch/README.md](./leetcode_fetch/README.md)** - Sync service documentation
- **[LeetVault-gitleet/API_DOCS.md](./LeetVault-gitleet/API_DOCS.md)** - API documentation

## 🔄 How It Works

### User Flow

1. **Sign Up**: User signs in with Google
2. **Connect GitHub**: Install LeetVault GitHub App
3. **Select Repository**: Choose a repo to sync
4. **Add LeetCode Credentials**: Provide session cookie & CSRF token
5. **Automatic Sync**: Appwrite scheduler triggers sync daily at 6:20 PM UTC

### Sync Process (Scheduled & Parallel)

```
Appwrite Scheduler (Daily at 6:20 PM UTC)
    ↓
Detect Scheduled Execution
    ↓
Fetch ALL Active Repos (from Appwrite)
    ↓
Create Tasks for Each Repo
    ↓
Execute in Parallel (asyncio.gather)
    ↓
For Each Repo (concurrent):
    - Fetch LeetCode submissions
    - Generate markdown files
    - Push to GitHub
    - Update database
    ↓
Return Results
```

**Manual Trigger**: Also available via `/sync` endpoint for immediate sync.

### Performance

| Users | Time (Parallel) | Speed vs Sequential |
|-------|----------------|---------------------|
| 1     | ~5-10s         | 1x                  |
| 100   | ~5-15s         | 100x                |
| 1000  | ~10-20s        | 500x+               |

## 📊 Repository Structure (Generated)

When synced, your GitHub repository will contain:

```
your-repo/
├── LeetcodeProgress.md           # Main progress report
├── easy-problems.md              # All easy problems
├── medium-problems.md            # All medium problems
├── hard-problems.md              # All hard problems
└── leetcode/
    ├── two-sum/
    │   ├── README.md             # Problem description
    │   └── solution.py           # Your solution
    ├── reverse-linked-list/
    │   ├── README.md
    │   └── solution.cpp
    └── ...
```

## 🔧 Configuration

### Environment Variables

#### Frontend (.env)
```env
VITE_FIREBASE_API_KEY=your_key
VITE_FIREBASE_AUTH_DOMAIN=your_domain
VITE_FIREBASE_PROJECT_ID=your_project
VITE_FIREBASE_STORAGE_BUCKET=your_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

#### Backend Services (.env)
```env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id
GITHUB_APP_ID=your_app_id
GITHUB_PRIVATE_KEY_PATH="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
FRONTEND_URL=https://your-frontend.com
```

## 🎯 API Endpoints

### LeetVault-gitleet
- `POST /api/users/check` - Check/create user
- `GET /api/auth/github-install/{email}` - Get GitHub install URL
- `GET /api/auth/github/callback` - Handle GitHub callback
- `GET /api/github/installations/{id}/repositories` - List repos
- `POST /api/repos/activate` - Activate repository
- `DELETE /api/repos/deactivate/{email}` - Deactivate repository
- `POST /api/leetcode/credentials` - Save credentials
- `GET /api/leetcode/credentials/{email}` - Get credentials

### leetcode_fetch
- `POST /sync` - Trigger parallel sync for all active repos
- `GET /status` - Get sync status
- `GET /health` - Health check

## 🔐 Security

- Firebase Authentication for user management
- GitHub App for secure repository access
- Appwrite for encrypted data storage
- Environment variables for sensitive data
- CORS configuration for API security

## 📈 Monitoring

Check sync status:
```bash
curl https://your-function-url/status
```

Response:
```json
{
  "status": "completed",
  "message": "Synced 950/1000 repositories with 4523 problems",
  "last_fetch_time": "2025-12-22T12:00:00",
  "problems_processed": 4523
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT

## 🙏 Acknowledgments

- LeetCode for the amazing platform
- GitHub for the powerful API
- Appwrite for the backend infrastructure
- Firebase for authentication services
