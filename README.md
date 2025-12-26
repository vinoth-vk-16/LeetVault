# LeetVault

Automate your LeetCode progress tracking with GitHub integration.

## 📁 Project Structure

```
leetvault/
├── leetVault-fe/          # React frontend (Vite + Tailwind CSS)
├── LeetVault-gitleet/     # GitHub integration service (Appwrite Function)
├── leetcode_fetch/        # LeetCode sync service (Appwrite Function)
└── README.md             # This file
```

## 🚀 Services

### 1. Frontend (`leetVault-fe`)
- **Tech Stack**: React.js, Vite, Tailwind CSS, Firebase Auth
- **Features**:
  - Google Sign-In with Firebase
  - LeetCode credentials management
  - GitHub App installation and repository activation
  - Modern dark-themed UI

### 2. GitHub Integration (`LeetVault-gitleet`)
- **Tech Stack**: FastAPI, Appwrite SDK, PyJWT
- **Deployment**: Appwrite Function
- **Features**:
  - User management with email-based IDs
  - GitHub App OAuth flow handling
  - Repository activation/deactivation
  - LeetCode credentials storage
  - JWT-based GitHub App authentication

### 3. LeetCode Sync (`leetcode_fetch`)
- **Tech Stack**: FastAPI, Appwrite SDK, Requests, html2text
- **Deployment**: Appwrite Function with scheduled execution
- **Features**:
  - Parallel repository syncing
  - Automatic LeetCode session refresh
  - GitHub file creation/updates
  - Email notifications with progress reports
  - User-specific or all-user sync modes

## 🔧 Setup

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.12+ (for backend services)
- Firebase project with Google Auth enabled
- GitHub App with Contents: Read & Write permission
- Appwrite Cloud account or self-hosted instance
- Gmail account with App Password (for email notifications)

### Frontend Setup

```bash
cd leetVault-fe
npm install
cp env.example .env
# Edit .env with your Firebase credentials
npm run dev
```

### Backend Services Setup

Both backend services are deployed as Appwrite Functions.

#### LeetVault-gitleet (GitHub Integration)

1. Create an Appwrite Function in your project
2. Configure environment variables:
   ```
   APPWRITE_ENDPOINT=https://sgp.cloud.appwrite.io/v1
   APPWRITE_PROJECT_ID=your_project_id
   APPWRITE_API_KEY=your_api_key
   APPWRITE_DATABASE_ID=your_database_id
   FRONTEND_URL=https://your-frontend-url.com
   GITHUB_APP_ID=your_github_app_id
   GITHUB_PRIVATE_KEY_PATH=your_github_private_key
   ```
3. Deploy the function from `LeetVault-gitleet/` directory
4. Set entrypoint to `main.py`
5. Build command: `pip install -r requirements.txt`

#### leetcode_fetch (LeetCode Sync)

1. Create an Appwrite Function in your project
2. Configure environment variables:
   ```
   APPWRITE_ENDPOINT=https://sgp.cloud.appwrite.io/v1
   APPWRITE_PROJECT_ID=your_project_id
   APPWRITE_API_KEY=your_api_key
   APPWRITE_DATABASE_ID=your_database_id
   GITHUB_APP_ID=your_github_app_id
   GITHUB_PRIVATE_KEY_PATH=your_github_private_key
   GMAIL_USER=your_gmail@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   ```
3. Deploy the function from `leetcode_fetch/` directory
4. Set entrypoint to `main.py`
5. Build command: `pip install -r requirements.txt`
6. Configure schedule: `0 18 * * *` (daily at 6 PM UTC)

## 📊 Database Schema

### Collections

1. **users** (`694101bf003792f1a56b`)
   - email, name, Github_status, Repo_activation, createdAt, updatedAt

2. **github_installations** (`694101cf003c5c9bba86`)
   - userId, githubInstallationId, isActive, installedAt, updatedAt

3. **activated_repos** (`694101df002d9f1c8ed3`)
   - userId, installationId, repoFullName, defaultBranch, isActive, activatedAt, lastSyncAt, updatedAt

4. **leetcode_credentials** (`694101f900308ac95c21`)
   - userId, sessionCookie, csrfToken, leetcodeUsername, isValid, lastValidatedAt, createdAt, updatedAt

5. **sync_logs** (`6941020f001a701ab9ae`)
   - userId, repoId, status, problemsSynced, syncedAt, errorMessage

## 🔄 How It Works

1. **User Authentication**: Users sign in with Google via Firebase
2. **LeetCode Setup**: Users provide their LeetCode session cookie and CSRF token
3. **GitHub Connection**: Users install the LeetVault GitHub App and select repositories
4. **Repository Activation**: Users activate one repository for syncing
5. **Automatic Sync**: The `leetcode_fetch` service runs daily (or on-demand) to:
   - Fetch all accepted LeetCode submissions
   - Create/update problem folders with solutions
   - Generate progress reports (`LeetcodeProgress.md`, `easy-problems.md`, etc.)
   - Push changes to GitHub
   - Send email notifications to users

## 📧 Email Notifications

After each successful sync, users receive an HTML email with:
- Total problems synced
- Breakdown by difficulty (Easy, Medium, Hard)
- Repository name
- Sync timestamp
- LeetVault branding

## 🛠️ Development

### Local Testing

**Frontend:**
```bash
cd leetVault-fe
npm run dev
```

**Backend Services:**
```bash
cd LeetVault-gitleet  # or leetcode_fetch
python main.py
```

### Appwrite Function Deployment

Both backend services use the **standard Appwrite Python function pattern**:

```python
def main(context):
    # Direct request handling
    path = context.req.path
    method = context.req.method
    
    # Route and respond
    if path == "/health":
        return context.res.json({"status": "healthy"})
    
    # ... more routes
```

**Key Points:**
- ✅ Synchronous `def main(context)` (not `async def`)
- ✅ Direct use of `context.req` and `context.res`
- ✅ No FastAPI TestClient wrapper
- ✅ Use `context.log()` and `context.error()` for logging
- ✅ Use `asyncio.run()` for async operations within the function

## 📚 Documentation

- [Frontend README](./leetVault-fe/README.md)
- [GitHub Integration API Docs](./LeetVault-gitleet/API_DOCS.md)
- [LeetCode Sync API Docs](./leetcode_fetch/API.md)

## 🐛 Troubleshooting

### "request cannot have request body" Error
- **Cause**: Incorrect Appwrite function wrapper pattern
- **Solution**: Ensure you're using the standard Appwrite Python function pattern (not FastAPI TestClient)

### GitHub JWT Errors
- **Cause**: Incorrect private key format or App ID
- **Solution**: Verify GitHub App ID and regenerate private key with proper newline formatting

### Email Not Sending
- **Cause**: Missing or incorrect Gmail credentials
- **Solution**: Verify `GMAIL_USER` and `GMAIL_APP_PASSWORD` environment variables

### LeetCode Session Expired
- **Cause**: Session cookie is invalid
- **Solution**: The service will automatically attempt to refresh using CSRF token. If that fails, user needs to update credentials.

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

This is a personal project. Feel free to fork and modify for your own use.
