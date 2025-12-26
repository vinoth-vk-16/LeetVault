# LeetVault GitHub Integration Service

FastAPI backend service for managing GitHub App integration, LeetCode credentials, and repository activation for LeetVault.

## 🚀 Features

- **User Management**: Check/create users with email-based IDs
- **GitHub App Integration**: Handle GitHub App installation and OAuth flow
- **Repository Management**: Activate/deactivate repositories for LeetCode sync
- **LeetCode Credentials**: Store and retrieve user LeetCode session cookies and CSRF tokens

## 📋 API Endpoints

### User Management
- `POST /api/users/check` - Check if user exists, create if not
- `GET /api/users/{email}` - Get user information by email

### LeetCode Credentials
- `POST /api/leetcode/credentials` - Store/update LeetCode credentials
- `GET /api/leetcode/credentials/{email}` - Get LeetCode credentials

### GitHub Integration
- `GET /api/auth/github/install?email={email}` - Get GitHub App installation URL
- `GET /api/auth/github/callback` - Handle GitHub App installation callback
- `GET /api/github/installations/{installation_id}/repositories` - List repositories

### Repository Management
- `POST /api/repos/activate` - Activate a repository for sync
- `DELETE /api/repos/deactivate/{email}` - Deactivate user's repository

### Health Check
- `GET /health` - Service health check with database status

## ⚙️ Appwrite Function Configuration

| Setting           | Value                             |
| ----------------- | --------------------------------- |
| Runtime           | Python (3.12)                     |
| Entrypoint        | `main.py`                         |
| Build Commands    | `pip install -r requirements.txt` |
| Permissions       | `any`                             |
| Timeout (Seconds) | 30                                |

## 🔒 Environment Variables

Required environment variables for Appwrite Function:

```bash
APPWRITE_ENDPOINT=https://sgp.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id
FRONTEND_URL=https://your-frontend-url.com
GITHUB_APP_ID=your_github_app_id
GITHUB_PRIVATE_KEY_PATH=your_github_private_key
```

## 📦 Dependencies

- `fastapi` - Web framework
- `appwrite` - Appwrite SDK
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management
- `httpx` - Async HTTP client
- `PyJWT` - JWT token generation for GitHub App
- `cryptography` - Required for JWT RS256 algorithm
- `email-validator` - Email validation for Pydantic

## 🏗️ Project Structure

```
LeetVault-gitleet/
├── main.py              # FastAPI app with Appwrite wrapper
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── API_DOCS.md         # Detailed API documentation
```

## 🔧 Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with required environment variables

3. Run locally:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## 📚 Documentation

For detailed API documentation with request/response examples, see [API_DOCS.md](./API_DOCS.md)

## 🐛 Troubleshooting

### "request cannot have request body" error
- Ensure you're using the latest Appwrite Python SDK (4.1.0+)
- Check that the Appwrite wrapper is using the correct pattern (synchronous `main(context)`)

### GitHub JWT errors
- Verify `GITHUB_APP_ID` is correct
- Ensure `GITHUB_PRIVATE_KEY_PATH` contains the full private key with proper newlines
- Check that your GitHub App has "Contents: Read and write" permission

### Database connection errors
- Verify all Appwrite credentials are correct
- Ensure collection IDs match your Appwrite database schema
