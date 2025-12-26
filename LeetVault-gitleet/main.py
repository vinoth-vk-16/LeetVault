"""
LeetVault FastAPI Application
Manages GitHub App integration and LeetCode submission syncing
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, Field
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.exception import AppwriteException
from appwrite.query import Query
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import httpx
import jwt
import time
import json

# Load environment variables
load_dotenv()

# Configuration
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT", "https://sgp.cloud.appwrite.io/v1")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
APPWRITE_DATABASE_ID = os.getenv("APPWRITE_DATABASE_ID")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# GitHub App Configuration
GITHUB_APP_ID = int(os.getenv("GITHUB_APP_ID"))  # Must be integer
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")

# Initialize Appwrite client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

databases = Databases(client)

# Initialize FastAPI app
app = FastAPI(
    title="LeetVault API",
    description="API for syncing LeetCode submissions to GitHub",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCheckRequest(BaseModel):
    """Request model for checking/creating user"""
    email: EmailStr = Field(..., description="User's email address")

class UserResponse(BaseModel):
    """Response model for user operations"""
    success: bool
    message: str
    user_id: str
    email: str
    name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_new_user: bool
    github_status: bool = False
    installation_id: Optional[str] = None
    repo_activation: bool = False
    activated_repo: Optional[Dict[str, Any]] = None

class LeetCodeCredentialsRequest(BaseModel):
    """Request model for storing LeetCode credentials"""
    email: EmailStr = Field(..., description="User's email address")
    session_cookie: str = Field(..., description="LeetCode session cookie (LEETCODE_SESSION)", min_length=1)
    csrf_token: str = Field(..., description="LeetCode CSRF token", min_length=1)
    leetcode_username: Optional[str] = Field(None, description="LeetCode username (optional)")

class LeetCodeCredentialsResponse(BaseModel):
    """Response model for LeetCode credentials"""
    success: bool
    message: str
    configured: bool
    email: str
    session_cookie: Optional[str] = None
    csrf_token: Optional[str] = None
    leetcode_username: Optional[str] = None
    is_valid: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class RepoActivationRequest(BaseModel):
    """Request model for activating a repository"""
    email: EmailStr = Field(..., description="User's email address")
    installation_id: str = Field(..., description="GitHub installation ID")
    repo_name: str = Field(..., description="Repository full name (e.g., username/repo)")
    default_branch: str = Field(default="main", description="Default branch name")

class RepoActivationResponse(BaseModel):
    """Response model for repository activation"""
    success: bool
    message: str
    email: str
    repo_full_name: str
    default_branch: str
    installation_id: str
    activated_at: str
    is_active: bool

# Helper functions
def email_to_id(email: str) -> str:
    """
    Convert email to a valid document ID by replacing @ and . with _
    Example: user@example.com -> user_example_com
    """
    return email.replace("@", "_").replace(".", "_")

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"

def generate_jwt_token():
    """Generate JWT for GitHub App authentication"""
    try:
        # Check if GITHUB_PRIVATE_KEY_PATH is a file path or the key content itself
        if os.path.exists(GITHUB_PRIVATE_KEY_PATH):
            # It's a file path, read the file
            print(f"🔑 Reading private key from file: {GITHUB_PRIVATE_KEY_PATH}")
            with open(GITHUB_PRIVATE_KEY_PATH, "r") as key_file:
                private_key = key_file.read()
        else:
            # It's the key content directly (from environment variable)
            # Replace both \\n and \n with actual newlines
            print(f"🔑 Using private key from environment variable (length: {len(GITHUB_PRIVATE_KEY_PATH)} chars)")
            private_key = GITHUB_PRIVATE_KEY_PATH.replace('\\n', '\n')
            
            # If still no newlines, try single backslash (common in .env files)
            if '\n' not in private_key:
                # Split by literal \n string and rejoin with actual newlines
                private_key = private_key.replace(r'\n', '\n')
            
            # Strip any extra quotes that might have been added
            private_key = private_key.strip().strip('"').strip("'")
            
            print(f"🔑 After processing: {len(private_key)} chars, contains {private_key.count(chr(10))} newlines")
            print(f"🔑 Key starts with: {private_key[:50]}")
            print(f"🔑 Key ends with: {private_key[-50:]}")

        # JWT requires integer timestamps (Unix timestamps)
        current_time = int(time.time())
        payload = {
            "iat": current_time,
            "exp": current_time + 600,  # 10 minutes from now
            "iss": GITHUB_APP_ID
        }

        print(f"🔐 JWT payload: iat={payload['iat']}, exp={payload['exp']}, iss={payload['iss']} (type: {type(payload['iss'])})")
        token = jwt.encode(payload, private_key, algorithm="RS256")
        print(f"✅ JWT token generated successfully (length: {len(token)} chars)")
        return token
    except Exception as e:
        print(f"❌ JWT generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate JWT: {str(e)}")

async def get_installation_token(installation_id: str) -> str:
    """Generate installation access token from installation ID"""
    try:
        jwt_token = generate_jwt_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.github.com/app/installations/{installation_id}/access_tokens",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
            )
            
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to get installation token: {response.text}"
                )
            
            token_data = response.json()
            return token_data["token"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate installation token: {str(e)}")

# Appwrite Collection IDs - Hardcoded from your database
COLLECTION_USERS = "694101bf003792f1a56b"
COLLECTION_GITHUB_INSTALLATIONS = "694101cf003c5c9bba86"
COLLECTION_ACTIVATED_REPOS = "694101df002d9f1c8ed3"
COLLECTION_LEETCODE_CREDENTIALS = "694101f900308ac95c21"
COLLECTION_SYNC_LOGS = "6941020f001a701ab9ae"

def get_collection_id(collection_name: str) -> str:
    """Get collection ID by name - returns hardcoded IDs"""
    collection_map = {
        "users": COLLECTION_USERS,
        "github_installations": COLLECTION_GITHUB_INSTALLATIONS,
        "activated_repos": COLLECTION_ACTIVATED_REPOS,
        "leetcode_credentials": COLLECTION_LEETCODE_CREDENTIALS,
        "sync_logs": COLLECTION_SYNC_LOGS
    }
    
    collection_id = collection_map.get(collection_name)
    if not collection_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Collection '{collection_name}' not found in mapping"
        )
    return collection_id

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "LeetVault API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/api/users/check", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def check_or_create_user(request: UserCheckRequest):
    """
    Check if user exists in database, create if not exists
    
    - **email**: User's email address
    
    Returns user information and whether the user was newly created
    """
    try:
        email = request.email.lower()  # Normalize email to lowercase
        user_id = email_to_id(email)
        
        # Get users collection ID
        users_collection_id = get_collection_id("users")
        
        # Try to get existing user by document ID
        try:
            user_doc = databases.get_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=users_collection_id,
                document_id=user_id
            )
            
            # Check GitHub status and fetch installation_id if connected
            github_status = bool(user_doc.get('Github_status', False))
            installation_id = None
            
            if github_status:
                try:
                    github_installations_collection_id = get_collection_id("github_installations")
                    installations = databases.list_documents(
                        database_id=APPWRITE_DATABASE_ID,
                        collection_id=github_installations_collection_id,
                        queries=[Query.equal('userId', user_id)]
                    )
                    if installations['total'] > 0:
                        installation_id = installations['documents'][0].get('githubInstallationId')
                except Exception as e:
                    print(f"Error fetching installation: {e}")
            
            # Check repo activation status and fetch activated repo if true
            repo_activation = bool(user_doc.get('Repo_activation', False))
            activated_repo = None
            
            if repo_activation:
                try:
                    activated_repos_collection_id = get_collection_id("activated_repos")
                    repos = databases.list_documents(
                        database_id=APPWRITE_DATABASE_ID,
                        collection_id=activated_repos_collection_id,
                        queries=[Query.equal('userId', user_id)]
                    )
                    if repos['total'] > 0:
                        repo_doc = repos['documents'][0]
                        activated_repo = {
                            "repo_full_name": repo_doc.get('repoFullName'),
                            "default_branch": repo_doc.get('defaultBranch'),
                            "is_active": repo_doc.get('isActive'),
                            "activated_at": repo_doc.get('activatedAt'),
                            "last_sync_at": repo_doc.get('lastSyncAt')
                        }
                except Exception as e:
                    print(f"Error fetching activated repo: {e}")
            
            # User exists, return user data with GitHub and repo info
            return UserResponse(
                success=True,
                message="User already exists in database",
                user_id=user_doc['$id'],
                email=user_doc['email'],
                name=user_doc.get('name'),
                created_at=user_doc.get('createdAt'),
                updated_at=user_doc.get('updatedAt'),
                is_new_user=False,
                github_status=github_status,
                installation_id=installation_id,
                repo_activation=repo_activation,
                activated_repo=activated_repo
            )
            
        except AppwriteException as e:
            # User doesn't exist (404 error), create new user
            if e.code == 404:
                current_time = get_current_timestamp()
                
                # Create new user document
                new_user = databases.create_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=users_collection_id,
                    document_id=user_id,  # Use email-based ID
                    data={
                        'email': email,
                        'name': None,  # Can be updated later
                        'Github_status': False,  # Default false
                        'Repo_activation': False,  # Default false
                        'createdAt': current_time,
                        'updatedAt': current_time
                    }
                )
                
                return UserResponse(
                    success=True,
                    message="User created successfully",
                    user_id=new_user['$id'],
                    email=new_user['email'],
                    name=new_user.get('name'),
                    created_at=new_user.get('createdAt'),
                    updated_at=new_user.get('updatedAt'),
                    is_new_user=True,
                    github_status=False,
                    installation_id=None,
                    repo_activation=False,
                    activated_repo=None
                )
            else:
                # Some other error occurred
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {str(e)}"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/api/users/{email}")
async def get_user_by_email(email: str):
    """
    Get user information by email
    
    - **email**: User's email address
    """
    try:
        email = email.lower()
        user_id = email_to_id(email)
        
        # Get users collection ID
        users_collection_id = get_collection_id("users")
        
        # Get user document
        user_doc = databases.get_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=users_collection_id,
            document_id=user_id
        )
        
        return {
            "success": True,
            "user": {
                "user_id": user_doc['$id'],
                "email": user_doc['email'],
                "name": user_doc.get('name'),
                "created_at": user_doc.get('createdAt'),
                "updated_at": user_doc.get('updatedAt'),
                "github_status": bool(user_doc.get('Github_status', False)),
                "repo_activation": bool(user_doc.get('Repo_activation', False))
            }
        }
        
    except AppwriteException as e:
        if e.code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@app.post("/api/leetcode/credentials", response_model=LeetCodeCredentialsResponse, status_code=status.HTTP_201_CREATED)
async def store_leetcode_credentials(request: LeetCodeCredentialsRequest):
    """
    Store or update LeetCode credentials for a user
    
    - **email**: User's email address
    - **session_cookie**: LeetCode session cookie (LEETCODE_SESSION)
    - **csrf_token**: LeetCode CSRF token
    - **leetcode_username**: Optional LeetCode username
    
    Returns stored credentials information
    """
    try:
        email = request.email.lower()
        user_id = email_to_id(email)
        
        # Get leetcode_credentials collection ID
        leetcode_creds_collection_id = "694101f900308ac95c21"
        
        # Check if user exists in users collection first
        users_collection_id = get_collection_id("users")
        try:
            databases.get_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=users_collection_id,
                document_id=user_id
            )
        except AppwriteException as e:
            if e.code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with email '{email}' not found. Please create user first using /api/users/check endpoint."
                )
            raise
        
        current_time = get_current_timestamp()
        
        # Check if credentials already exist for this user
        try:
            # Try to find existing credentials by userId
            existing_creds = databases.list_documents(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=leetcode_creds_collection_id,
                queries=[Query.equal('userId', user_id)]
            )
            
            if existing_creds['total'] > 0:
                # Update existing credentials
                cred_doc = existing_creds['documents'][0]
                updated_cred = databases.update_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=leetcode_creds_collection_id,
                    document_id=cred_doc['$id'],
                    data={
                        'sessionCookie': request.session_cookie,
                        'csrfToken': request.csrf_token,
                        'leetcodeUsername': request.leetcode_username,
                        'isValid': True,
                        'lastValidatedAt': current_time,
                        'updatedAt': current_time
                    }
                )
                
                return LeetCodeCredentialsResponse(
                    success=True,
                    message="LeetCode credentials updated successfully",
                    configured=True,
                    email=email,
                    session_cookie=updated_cred['sessionCookie'],
                    csrf_token=updated_cred['csrfToken'],
                    leetcode_username=updated_cred.get('leetcodeUsername'),
                    is_valid=updated_cred.get('isValid', True),
                    created_at=updated_cred.get('createdAt'),
                    updated_at=updated_cred.get('updatedAt')
                )
            else:
                # Create new credentials
                new_cred = databases.create_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=leetcode_creds_collection_id,
                    document_id=ID.unique(),
                    data={
                        'userId': user_id,
                        'sessionCookie': request.session_cookie,
                        'csrfToken': request.csrf_token,
                        'leetcodeUsername': request.leetcode_username,
                        'isValid': True,
                        'lastValidatedAt': current_time,
                        'createdAt': current_time,
                        'updatedAt': current_time
                    }
                )
                
                return LeetCodeCredentialsResponse(
                    success=True,
                    message="LeetCode credentials stored successfully",
                    configured=True,
                    email=email,
                    session_cookie=new_cred['sessionCookie'],
                    csrf_token=new_cred['csrfToken'],
                    leetcode_username=new_cred.get('leetcodeUsername'),
                    is_valid=new_cred.get('isValid', True),
                    created_at=new_cred.get('createdAt'),
                    updated_at=new_cred.get('updatedAt')
                )
                
        except AppwriteException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/api/leetcode/credentials/{email}", response_model=LeetCodeCredentialsResponse)
async def get_leetcode_credentials(email: str):
    """
    Get LeetCode credentials for a user by email
    
    - **email**: User's email address
    
    Returns stored LeetCode credentials (session cookie and CSRF token)
    """
    try:
        email = email.lower()
        user_id = email_to_id(email)
        
        # Get leetcode_credentials collection ID
        leetcode_creds_collection_id = "694101f900308ac95c21"
        
        # Find credentials by userId
        creds = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=leetcode_creds_collection_id,
            queries=[Query.equal('userId', user_id)]
        )
        
        if creds['total'] == 0:
            # No credentials found - return configured: false
            return LeetCodeCredentialsResponse(
                success=True,
                message="No LeetCode credentials configured for this user",
                configured=False,
                email=email
            )
        
        cred_doc = creds['documents'][0]
        
        return LeetCodeCredentialsResponse(
            success=True,
            message="LeetCode credentials retrieved successfully",
            configured=True,
            email=email,
            session_cookie=cred_doc['sessionCookie'],
            csrf_token=cred_doc['csrfToken'],
            leetcode_username=cred_doc.get('leetcodeUsername'),
            is_valid=cred_doc.get('isValid', True),
            created_at=cred_doc.get('createdAt'),
            updated_at=cred_doc.get('updatedAt')
        )
        
    except HTTPException:
        raise
    except AppwriteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

# ============= GITHUB APP INSTALLATION ENDPOINTS =============

@app.get("/api/auth/github/install")
async def get_installation_url(email: str):
    """
    Return the GitHub App installation URL
    Frontend can use this directly or backend can redirect
    """
    user_id = email_to_id(email.lower())
    install_url = f"https://github.com/apps/leetvault/installations/new?state={user_id}"
    return {"installation_url": install_url, "user_id": user_id}

@app.get("/api/auth/github/callback")
async def github_installation_callback(
    installation_id: str,
    setup_action: str,
    state: str,  # This is user_id
    code: str = None  # Optional - GitHub sends this too
):
    """
    Handle GitHub App installation callback
    GitHub redirects here after user installs the app and selects repositories
    """
    user_id = state
    print(f"🔗 GitHub callback received: installation_id={installation_id}, user_id={user_id}, setup_action={setup_action}")
    
    if setup_action == "cancel":
        return RedirectResponse(f"{FRONTEND_URL}/error?message=GitHub App installation cancelled")
    
    try:
        # Generate JWT for App authentication
        print(f"🔑 Generating JWT with App ID: {GITHUB_APP_ID} (type: {type(GITHUB_APP_ID)})")
        jwt_token = generate_jwt_token()
        print(f"✅ JWT generated successfully (first 20 chars): {jwt_token[:20]}...")
        
        # Get installation access token
        async with httpx.AsyncClient() as client:
            # Request installation access token
            print(f"📡 Requesting installation token for installation_id={installation_id}")
            token_response = await client.post(
                f"https://api.github.com/app/installations/{installation_id}/access_tokens",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
            )
            
            print(f"📥 Token response status: {token_response.status_code}")
            if token_response.status_code != 201:
                error_detail = token_response.text
                print(f"❌ GitHub API error: {error_detail}")
                raise HTTPException(
                    status_code=token_response.status_code,
                    detail=f"Failed to get installation token: {error_detail}"
                )
            
            token_data = token_response.json()
            access_token = token_data["token"]
            
            # Get installation details to get the account info
            print(f"📡 Getting GitHub installation details...")
            install_response = await client.get(
                f"https://api.github.com/app/installations/{installation_id}",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
            )
            print(f"📥 Installation API response status: {install_response.status_code}")
            if install_response.status_code != 200:
                print(f"❌ Installation API error: {install_response.text}")
                raise HTTPException(status_code=500, detail=f"Failed to get installation details: {install_response.text}")

            install_data = install_response.json()
            github_username = install_data.get("account", {}).get("login")

            # Fallback: if we can't get username from installation, use part of email
            if not github_username:
                # Extract username from user_id (which is email-based)
                email_username = user_id.replace("_", ".")
                github_username = email_username.split("_")[0] if "_" in email_username else user_id
                print(f"⚠️  Using fallback username: '{github_username}' (couldn't get from GitHub API)")

            print(f"✅ Got GitHub username from installation: '{github_username}' (account data: {install_data.get('account')})")
            
            # Get repositories that user selected during installation
            repos_response = await client.get(
                f"https://api.github.com/user/installations/{installation_id}/repositories",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json"
                }
            )
            repos_data = repos_response.json()
            repositories = repos_data.get("repositories", [])
            print(f"📦 Found {len(repositories)} repositories accessible by this installation")
        
        # Store the installation in Appwrite database
        try:
            current_time = get_current_timestamp()
            users_collection_id = get_collection_id("users")
            github_installations_collection_id = get_collection_id("github_installations")

            # Check if user already has an installation (should be only one per user)
            existing_installations = databases.list_documents(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=github_installations_collection_id,
                queries=[Query.equal("userId", user_id)]
            )

            if existing_installations.get("total", 0) > 0:
                # Update existing installation
                existing_installation = existing_installations["documents"][0]
                installation_doc_id = existing_installation["$id"]
                print(f"🔄 Updating existing installation for user {user_id} with new installation {installation_id}")

                databases.update_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=github_installations_collection_id,
                    document_id=installation_doc_id,
                    data={
                        "githubInstallationId": installation_id,
                        "isActive": True,
                        "updatedAt": current_time
                    }
                )
                print(f"✅ GitHub installation updated successfully for user: {user_id}")
            else:
                # Create new installation
                print(f"💾 Creating new GitHub installation for user: {user_id}")
                databases.create_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=github_installations_collection_id,
                    document_id=ID.unique(),
                    data={
                        "userId": user_id,
                        "githubInstallationId": installation_id,
                        "isActive": True,
                        "installedAt": current_time,
                        "updatedAt": current_time
                    }
                )
                print(f"✅ GitHub installation created successfully")
            
            # Update user's Github_status to true
            databases.update_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=users_collection_id,
                document_id=user_id,
                data={
                    "Github_status": True,
                    "updatedAt": current_time
                }
            )
            print(f"✅ User Github_status updated to true")
        
        except Exception as db_error:
            print(f"❌ Failed to store installation in database: {str(db_error)}")
            # Don't fail the whole flow, just log the error
        
        # Redirect to frontend with installation data
        return RedirectResponse(
            f"{FRONTEND_URL}/home"
            f"?user_id={user_id}"
            f"&installation_id={installation_id}"
            f"&github_username={github_username}"
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        return RedirectResponse(f"{FRONTEND_URL}/error?message={str(e)}")

@app.get("/api/github/installations/{installation_id}/repositories")
async def get_installation_repositories(installation_id: str):
    """
    Fetch repositories accessible by this installation
    Frontend calls this instead of GitHub API directly
    """
    try:
        print(f"📡 Fetching repositories for installation: {installation_id}")
        
        # Generate fresh installation token
        token = await get_installation_token(installation_id)
        
        # Fetch repositories
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/installation/repositories",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
            )
            
            if response.status_code != 200:
                print(f"❌ GitHub API error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=f"GitHub API error: {response.text}")
            
            data = response.json()
            repositories = data.get("repositories", [])
            print(f"✅ Found {len(repositories)} repositories")
            
            # Format repository data for frontend
            formatted_repos = [
                {
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "private": repo["private"],
                    "html_url": repo["html_url"],
                    "description": repo.get("description"),
                    "default_branch": repo.get("default_branch", "main")
                }
                for repo in repositories
            ]
            
            return {
                "success": True,
                "repositories": formatted_repos,
                "total_count": len(formatted_repos)
            }
    
    except Exception as e:
        print(f"❌ Error fetching repositories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {str(e)}")

# ============= REPOSITORY ACTIVATION ENDPOINTS =============

@app.post("/api/repos/activate", response_model=RepoActivationResponse, status_code=status.HTTP_201_CREATED)
async def activate_repository(request: RepoActivationRequest):
    """
    Activate a repository for LeetCode submissions sync
    Only one repository can be activated per user
    
    - **email**: User's email address
    - **installation_id**: GitHub installation ID
    - **repo_name**: Repository full name (e.g., username/repo)
    - **default_branch**: Default branch name (default: main)
    """
    try:
        email = request.email.lower()
        user_id = email_to_id(email)
        
        # Get collection IDs
        users_collection_id = get_collection_id("users")
        activated_repos_collection_id = "694101df002d9f1c8ed3"
        
        # Check if user exists
        try:
            user_doc = databases.get_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=users_collection_id,
                document_id=user_id
            )
        except AppwriteException as e:
            if e.code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with email '{email}' not found. Please create user first."
                )
            raise
        
        # Check if user already has an activated repository
        existing_repos = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=activated_repos_collection_id,
            queries=[Query.equal('userId', user_id)]
        )
        
        current_time = get_current_timestamp()
        
        if existing_repos['total'] > 0:
            # Update existing activated repository (replace with new one)
            existing_repo = existing_repos['documents'][0]
            repo_doc_id = existing_repo['$id']
            
            print(f"🔄 Updating activated repository for user {user_id}")
            updated_repo = databases.update_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=activated_repos_collection_id,
                document_id=repo_doc_id,
                data={
                    'installationId': request.installation_id,
                    'repoFullName': request.repo_name,
                    'defaultBranch': request.default_branch,
                    'isActive': True,
                    'activatedAt': current_time,
                    'lastSyncAt': None,
                    'updatedAt': current_time
                }
            )
            message = "Repository updated successfully"
        else:
            # Create new activated repository
            print(f"💾 Creating new activated repository for user {user_id}")
            updated_repo = databases.create_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=activated_repos_collection_id,
                document_id=ID.unique(),
                data={
                    'userId': user_id,
                    'installationId': request.installation_id,
                    'repoFullName': request.repo_name,
                    'defaultBranch': request.default_branch,
                    'isActive': True,
                    'activatedAt': current_time,
                    'lastSyncAt': None,
                    'updatedAt': current_time
                }
            )
            message = "Repository activated successfully"
        
        # Update user's Repo_activation to True
        databases.update_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=users_collection_id,
            document_id=user_id,
            data={
                'Repo_activation': True,
                'updatedAt': current_time
            }
        )
        print(f"✅ User Repo_activation updated to true")
        
        return RepoActivationResponse(
            success=True,
            message=message,
            email=email,
            repo_full_name=updated_repo['repoFullName'],
            default_branch=updated_repo['defaultBranch'],
            installation_id=updated_repo['installationId'],
            activated_at=updated_repo['activatedAt'],
            is_active=updated_repo['isActive']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to activate repository: {str(e)}"
        )

@app.delete("/api/repos/deactivate/{email}")
async def deactivate_repository(email: str):
    """
    Deactivate the currently activated repository for a user
    
    - **email**: User's email address
    """
    try:
        email = email.lower()
        user_id = email_to_id(email)
        
        # Get collection IDs
        users_collection_id = get_collection_id("users")
        activated_repos_collection_id = "694101df002d9f1c8ed3"
        
        # Check if user exists
        try:
            user_doc = databases.get_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=users_collection_id,
                document_id=user_id
            )
        except AppwriteException as e:
            if e.code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with email '{email}' not found"
                )
            raise
        
        # Find activated repository
        activated_repos = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=activated_repos_collection_id,
            queries=[Query.equal('userId', user_id)]
        )
        
        if activated_repos['total'] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No activated repository found for user '{email}'"
            )
        
        # Delete the activated repository record
        repo_doc = activated_repos['documents'][0]
        repo_doc_id = repo_doc['$id']
        repo_name = repo_doc['repoFullName']
        
        databases.delete_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=activated_repos_collection_id,
            document_id=repo_doc_id
        )
        print(f"🗑️  Deleted activated repository record for user {user_id}")
        
        # Update user's Repo_activation to False
        current_time = get_current_timestamp()
        databases.update_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=users_collection_id,
            document_id=user_id,
            data={
                'Repo_activation': False,
                'updatedAt': current_time
            }
        )
        print(f"✅ User Repo_activation updated to false")
        
        return {
            "success": True,
            "message": "Repository deactivated successfully",
            "email": email,
            "deactivated_repo": repo_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deactivate repository: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        collections = databases.list_collections(APPWRITE_DATABASE_ID)
        return {
            "status": "healthy",
            "database": "connected",
            "collections_count": len(collections.get('collections', [])),
            "timestamp": get_current_timestamp()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": get_current_timestamp()
        }

# ---- Appwrite Function Wrapper ----
def main(context):
    """Entry point for Appwrite Function - handles all HTTP requests"""
    try:
        # Parse incoming request
        path = context.req.path if context.req.path else "/"
        method = context.req.method.upper() if context.req.method else "GET"
        
        context.log(f"📥 Incoming request: {method} {path}")
        
        # Parse query parameters from path if present
        query_params = {}
        if "?" in path:
            path_parts = path.split("?", 1)
            path = path_parts[0]
            query_string = path_parts[1]
            for param in query_string.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    query_params[key] = value
        
        # Parse request body for POST/PUT/PATCH
        body_data = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                # Try to parse as JSON first
                if context.req.body_text:
                    body_data = json.loads(context.req.body_text)
                    context.log(f"📦 Request body: {body_data}")
            except (json.JSONDecodeError, AttributeError):
                context.log("⚠️  No valid JSON body found")
        
        # Route to appropriate handler
        if path == "/" and method == "GET":
            return context.res.json({
                "message": "LeetVault API is running",
                "version": "1.0.0",
                "status": "healthy"
            })
        
        elif path == "/health" and method == "GET":
            try:
                collections = databases.list_collections(APPWRITE_DATABASE_ID)
                return context.res.json({
                    "status": "healthy",
                    "database": "connected",
                    "collections_count": len(collections.get('collections', [])),
                    "timestamp": get_current_timestamp()
                })
            except Exception as e:
                return context.res.json({
                    "status": "unhealthy",
                    "database": "disconnected",
                    "error": str(e),
                    "timestamp": get_current_timestamp()
                }, 500)
        
        elif path == "/api/users/check" and method == "POST":
            if not body_data or "email" not in body_data:
                return context.res.json({"error": "Email is required"}, 400)
            
            # Import asyncio to run async function
            import asyncio
            request = UserCheckRequest(email=body_data["email"])
            result = asyncio.run(check_or_create_user(request))
            return context.res.json(result.dict())
        
        elif path.startswith("/api/users/") and method == "GET":
            email = path.split("/api/users/")[1]
            import asyncio
            result = asyncio.run(get_user_by_email(email))
            return context.res.json(result)
        
        elif path == "/api/leetcode/credentials" and method == "POST":
            if not body_data:
                return context.res.json({"error": "Request body is required"}, 400)
            
            import asyncio
            request = LeetCodeCredentialsRequest(**body_data)
            result = asyncio.run(store_leetcode_credentials(request))
            return context.res.json(result.dict(), 201)
        
        elif path.startswith("/api/leetcode/credentials/") and method == "GET":
            email = path.split("/api/leetcode/credentials/")[1]
            import asyncio
            result = asyncio.run(get_leetcode_credentials(email))
            return context.res.json(result.dict())
        
        elif path == "/api/auth/github/install" and method == "GET":
            email = query_params.get("email")
            if not email:
                return context.res.json({"error": "Email parameter is required"}, 400)
            
            import asyncio
            result = asyncio.run(get_installation_url(email))
            return context.res.json(result)
        
        elif path == "/api/auth/github/callback" and method == "GET":
            installation_id = query_params.get("installation_id")
            setup_action = query_params.get("setup_action")
            state = query_params.get("state")
            code = query_params.get("code")
            
            if not installation_id or not setup_action or not state:
                return context.res.json({"error": "Missing required parameters"}, 400)
            
            import asyncio
            result = asyncio.run(github_installation_callback(
                installation_id=installation_id,
                setup_action=setup_action,
                state=state,
                code=code
            ))
            
            # Handle redirect response
            if hasattr(result, 'headers') and 'location' in result.headers:
                return context.res.redirect(result.headers['location'])
            return result
        
        elif path.startswith("/api/github/installations/") and path.endswith("/repositories") and method == "GET":
            installation_id = path.split("/api/github/installations/")[1].split("/repositories")[0]
            import asyncio
            result = asyncio.run(get_installation_repositories(installation_id))
            return context.res.json(result)
        
        elif path == "/api/repos/activate" and method == "POST":
            if not body_data:
                return context.res.json({"error": "Request body is required"}, 400)
            
            import asyncio
            request = RepoActivationRequest(**body_data)
            result = asyncio.run(activate_repository(request))
            return context.res.json(result.dict(), 201)
        
        elif path.startswith("/api/repos/deactivate/") and method == "DELETE":
            email = path.split("/api/repos/deactivate/")[1]
            import asyncio
            result = asyncio.run(deactivate_repository(email))
            return context.res.json(result)
        
        else:
            return context.res.json({
                "error": "Not Found",
                "path": path,
                "method": method
            }, 404)
        
    except Exception as e:
        context.error(f"❌ Function Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return context.res.json({
            "error": str(e),
            "status": "error"
        }, 500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

