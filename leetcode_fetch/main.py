from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json
from typing import List, Dict, Optional
import html2text
import time
import asyncio
from datetime import datetime
import base64
import jwt
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# Environment variables
GRAPHQL_URL = os.getenv('GRAPHQL_URL', 'https://leetcode.com/graphql')

# Appwrite Configuration
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")
APPWRITE_DATABASE_ID = os.getenv("APPWRITE_DATABASE_ID")

# GitHub App Configuration
GITHUB_APP_ID = int(os.getenv("GITHUB_APP_ID", "0"))
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH", "")

# Email Configuration
GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Hardcoded collection IDs (from your Appwrite database)
COLLECTION_IDS = {
    "users": "694101bf003792f1a56b",
    "leetcode_credentials": "694101f900308ac95c21",
    "activated_repos": "694101df002d9f1c8ed3",
    "sync_logs": "6941020f001a701ab9ae",
    "github_installations": "694101cf003c5c9bba86"
}

# Initialize Appwrite client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)
databases = Databases(client)

# Language extension mapping
EXT_MAP = {
    "python": "py", "python3": "py", "cpp": "cpp", "java": "java", "c": "c",
    "csharp": "cs", "javascript": "js", "typescript": "ts", "kotlin": "kt",
    "swift": "swift", "golang": "go", "ruby": "rb", "scala": "scala",
    "rust": "rs", "mysql": "sql", "bash": "sh", "racket": "rkt", "erlang": "erl",
    "elixir": "ex", "dart": "dart", "php": "php", "perl": "pl", "haskell": "hs"
}

VALID_LANGUAGES = list(EXT_MAP.keys())

app = FastAPI(title="LeetCode Fetch Service", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class FetchRequest(BaseModel):
    output_dir: Optional[str] = "leetcode"
    languages: Optional[List[str]] = ["python3"]

# Removed SyncRequest - no longer needed as we always sync all active repos

class FetchStatus(BaseModel):
    status: str
    message: str
    last_fetch_time: Optional[str] = None
    problems_processed: Optional[int] = None
    submissions_downloaded: Optional[int] = None

# Global variable to track fetch status
fetch_status = {
    "status": "idle",
    "message": "No fetch in progress",
    "last_fetch_time": None,
    "problems_processed": None,
    "submissions_downloaded": None
}

def generate_jwt_token():
    """Generate JWT for GitHub App authentication"""
    try:
        # Parse private key
        if os.path.exists(GITHUB_PRIVATE_KEY_PATH):
            with open(GITHUB_PRIVATE_KEY_PATH, "r") as key_file:
                private_key = key_file.read()
        else:
            private_key = GITHUB_PRIVATE_KEY_PATH.replace('\\n', '\n')
            if '\n' not in private_key:
                private_key = private_key.replace(r'\n', '\n')
            private_key = private_key.strip().strip('"').strip("'")

        current_time = int(time.time())
        payload = {
            "iat": current_time,
            "exp": current_time + 600,
            "iss": GITHUB_APP_ID
        }

        token = jwt.encode(payload, private_key, algorithm="RS256")
        return token
    except Exception as e:
        print(f"❌ JWT generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate JWT: {str(e)}")

def get_installation_token(installation_id: str) -> str:
    """Get installation access token from GitHub"""
    jwt_token = generate_jwt_token()
    
    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    
    if not response.ok:
        raise HTTPException(status_code=response.status_code, 
                          detail=f"Failed to get installation token: {response.text}")
    
    return response.json()["token"]

def refresh_leetcode_session(csrf_token: str, old_session: str) -> Optional[str]:
    """
    Refresh LeetCode session cookie using CSRF token
    Returns new session cookie if successful, None otherwise
    """
    try:
        # Try to get a new session by making a request with the CSRF token
        response = requests.post(
            "https://leetcode.com/accounts/login/",
            headers={
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
                "Cookie": f"csrftoken={csrf_token}; LEETCODE_SESSION={old_session};",
                "Referer": "https://leetcode.com/accounts/login/"
            }
        )
        
        # Check if we got a new session cookie
        if 'Set-Cookie' in response.headers:
            cookies = response.headers.get('Set-Cookie', '')
            for cookie in cookies.split(';'):
                if 'LEETCODE_SESSION=' in cookie:
                    new_session = cookie.split('LEETCODE_SESSION=')[1].split(';')[0]
                    return new_session
        
        return None
    except Exception as e:
        print(f"❌ Failed to refresh session: {str(e)}")
        return None

def graphql_request(query: str, variables: dict, session_token: str, csrf_token: str = None) -> dict:
    """Make GraphQL request to LeetCode API"""
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={session_token};",
        "Referer": "https://leetcode.com/problemset/all/"
    }
    
    if csrf_token:
        headers["X-CSRFToken"] = csrf_token
        headers["Cookie"] += f" csrftoken={csrf_token};"
    
    r = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if not r.ok:
        print("GraphQL error:", r.text)
        r.raise_for_status()
    
    return r.json()

async def get_user_leetcode_credentials(user_id: str) -> Optional[Dict]:
    """
    Get user's LeetCode credentials from database
    Returns dict with sessionCookie, csrfToken, and credential document ID
    """
    try:
        result = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=COLLECTION_IDS["leetcode_credentials"],
            queries=[Query.equal("userId", user_id)]
        )
        
        if not result["documents"]:
            print(f"⚠️ No LeetCode credentials found for user {user_id}")
            return None
        
        cred = result["documents"][0]
        return {
            "sessionCookie": cred.get("sessionCookie"),
            "csrfToken": cred.get("csrfToken"),
            "leetcodeUsername": cred.get("leetcodeUsername"),
            "credentialId": cred["$id"]
        }
    except Exception as e:
        print(f"❌ Failed to get credentials for {user_id}: {str(e)}")
        return None

async def update_user_session_cookie(credential_id: str, new_session_cookie: str):
    """Update user's session cookie in the database"""
    try:
        databases.update_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=COLLECTION_IDS["leetcode_credentials"],
            document_id=credential_id,
            data={"sessionCookie": new_session_cookie}
        )
        print(f"✅ Updated session cookie for credential {credential_id}")
    except Exception as e:
        print(f"❌ Failed to update session cookie: {str(e)}")

def get_all_submissions(session_token: str, csrf_token: str = None) -> List[Dict]:
    """Fetch all accepted submissions"""
    subs = []
    offset = 0
    limit = 20

    while True:
        data = graphql_request(
            """
            query subs($offset: Int!, $limit: Int!) {
              submissionList(offset: $offset, limit: $limit) {
                submissions {
                  id titleSlug lang statusDisplay timestamp
                }
                hasNext
              }
            }
            """,
            {"offset": offset, "limit": limit},
            session_token,
            csrf_token
        )
        s = data["data"]["submissionList"]

        accepted_subs = [
            sub for sub in s["submissions"]
            if sub["statusDisplay"] == "Accepted"
        ]
        subs.extend(accepted_subs)

        if not s["hasNext"]:
            break
        offset += limit

    return subs

def get_submission_code(submission_id: int, session_token: str, csrf_token: str = None) -> str:
    """Fetch code for a specific submission"""
    data = graphql_request(
        """
        query details($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
          }
        }
        """,
        {"submissionId": submission_id},
        session_token,
        csrf_token
    )
    return data["data"]["submissionDetails"]["code"]

def html_to_md(html: str) -> str:
    """Convert HTML to Markdown"""
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.body_width = 0
    return h.handle(html)

def get_problem_data(slug: str, session_token: str, csrf_token: str = None) -> dict:
    """Fetch problem data including title, content, and code snippets"""
    q = """
    query q($slug: String!) {
      question(titleSlug: $slug) {
        title content difficulty codeSnippets { lang code }
      }
    }"""
    return graphql_request(q, {"slug": slug}, session_token, csrf_token)["data"]["question"]

def check_file_exists_in_repo(token: str, repo_full_name: str, file_path: str, branch: str) -> bool:
    """Check if a file exists in the GitHub repository"""
    response = requests.get(
        f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        },
        params={"ref": branch}
    )
    return response.status_code == 200

def get_file_sha(token: str, repo_full_name: str, file_path: str, branch: str) -> Optional[str]:
    """Get the SHA of a file in the repository"""
    response = requests.get(
        f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        },
        params={"ref": branch}
    )
    
    if response.status_code == 200:
        return response.json().get("sha")
    return None

def create_or_update_file(token: str, repo_full_name: str, file_path: str, content: str, 
                          message: str, branch: str, sha: Optional[str] = None):
    """Create or update a file in the GitHub repository"""
    encoded_content = base64.b64encode(content.encode()).decode()
    
    data = {
        "message": message,
        "content": encoded_content,
        "branch": branch
    }
    
    if sha:
        data["sha"] = sha
    
    response = requests.put(
        f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        },
        json=data
    )
    
    if not response.ok:
        print(f"❌ Failed to create/update {file_path}: {response.text}")
        raise Exception(f"Failed to create/update file: {response.text}")
    
    return response.json()

def generate_problem_files_content(summary: List[Dict], languages: List[str]) -> Dict[str, str]:
    """Generate content for difficulty-based problem files"""
    files_content = {}

    # Group problems by difficulty
    problems_by_difficulty = {"Easy": [], "Medium": [], "Hard": []}
    for item in summary:
        problems_by_difficulty[item["difficulty"]].append(item)

    # Generate content for each difficulty
    for difficulty, problems in problems_by_difficulty.items():
        if problems:
            content = f"# {difficulty} Problems\n\n"
            content += f"## Solutions in {', '.join(languages)}\n\n"
            content += f"Total {difficulty} problems: {len(problems)}\n\n"
            content += "| No | Title | Source Code |\n"
            content += "|----|-------|-------------|\n"

            for i, item in enumerate(sorted(problems, key=lambda x: x["title"]), 1):
                slug = item["slug"]
                title = item["title"]
                url = f"./leetcode/{slug}"
                content += f"| {i} | {title} | [Link]({url}) |\n"
            
            content += "\n---\n\n*Back to [LeetCode Progress](./LeetcodeProgress.md)*\n"
            files_content[f"{difficulty.lower()}-problems.md"] = content
    
    return files_content

def generate_email_html(user_email: str, summary: List[Dict], repo_name: str) -> str:
    """Generate HTML email content for sync notification"""
    total = len(summary)
    count = {"Easy": 0, "Medium": 0, "Hard": 0}
    for item in summary:
        count[item["difficulty"]] += 1

    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Times New Roman', Times, serif;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background-color: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 2px;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            color: #333;
            margin-bottom: 20px;
        }}
        .stats-container {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
            border-left: 4px solid #667eea;
        }}
        .stat-title {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }}
        .stat-row {{
            display: table;
            width: 100%;
            margin-bottom: 15px;
        }}
        .stat-label {{
            display: table-cell;
            font-size: 16px;
            color: #555;
            padding: 8px 0;
        }}
        .stat-value {{
            display: table-cell;
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
            text-align: right;
            padding: 8px 0;
        }}
        .difficulty-stats {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }}
        .difficulty-row {{
            display: table;
            width: 100%;
            margin-bottom: 12px;
        }}
        .difficulty-label {{
            display: table-cell;
            font-size: 15px;
            color: #666;
            padding: 5px 0;
        }}
        .difficulty-value {{
            display: table-cell;
            font-size: 16px;
            font-weight: bold;
            text-align: right;
            padding: 5px 0;
        }}
        .easy {{ color: #00b894; }}
        .medium {{ color: #fdcb6e; }}
        .hard {{ color: #d63031; }}
        .repo-info {{
            background-color: #e8f4f8;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            text-align: center;
        }}
        .repo-info p {{
            margin: 5px 0;
            color: #555;
            font-size: 14px;
        }}
        .repo-name {{
            font-weight: bold;
            color: #667eea;
            font-size: 16px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 25px 30px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }}
        .footer p {{
            margin: 5px 0;
            color: #666;
            font-size: 13px;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
            font-style: italic;
            margin-top: 15px;
        }}
        .divider {{
            height: 1px;
            background-color: #e0e0e0;
            margin: 25px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>LEETVAULT</h1>
            <p>Your LeetCode Progress Sync Report</p>
        </div>
        
        <div class="content">
            <p class="greeting">Hello,</p>
            <p class="greeting">Your LeetCode progress has been successfully synced to your GitHub repository!</p>
            
            <div class="stats-container">
                <div class="stat-title">📊 Sync Summary</div>
                
                <div class="stat-row">
                    <span class="stat-label">Total Problems Synced</span>
                    <span class="stat-value">{total}</span>
                </div>
                
                <div class="difficulty-stats">
                    <div class="difficulty-row">
                        <span class="difficulty-label">✅ Easy Problems</span>
                        <span class="difficulty-value easy">{count['Easy']}</span>
                    </div>
                    <div class="difficulty-row">
                        <span class="difficulty-label">⚡ Medium Problems</span>
                        <span class="difficulty-value medium">{count['Medium']}</span>
                    </div>
                    <div class="difficulty-row">
                        <span class="difficulty-label">🔥 Hard Problems</span>
                        <span class="difficulty-value hard">{count['Hard']}</span>
                    </div>
                </div>
            </div>
            
            <div class="repo-info">
                <p>Synced to Repository:</p>
                <p class="repo-name">{repo_name}</p>
            </div>
            
            <div class="divider"></div>
            
            <p style="color: #666; font-size: 14px; text-align: center;">
                All your LeetCode solutions have been organized and pushed to your GitHub repository. 
                Check your repository for detailed problem descriptions, solutions, and progress reports.
            </p>
            
            <p class="timestamp">Synced on {current_time}</p>
        </div>
        
        <div class="footer">
            <p><strong>LeetVault</strong> - Automate Your LeetCode Progress Tracking</p>
            <p>Keep coding, keep growing! 🚀</p>
        </div>
    </div>
</body>
</html>
"""
    return html

def send_email(to_email: str, subject: str, html_content: str):
    """Send email using Gmail SMTP"""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("⚠️ Email credentials not configured, skipping email notification")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return False

def generate_leetcode_progress_content(summary: List[Dict], languages: List[str]) -> str:
    """Generate content for LeetcodeProgress.md"""
    total = len(summary)
    count = {"Easy": 0, "Medium": 0, "Hard": 0}
    for item in summary:
        count[item["difficulty"]] += 1

    content = """<div align="center">

# <span style="background-color: #000066; color: white; padding: 10px 40px; border-radius: 5px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">LeetCode Solutions</span>

### <span style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Code present here: **""" + str(total) + """** problems (Easy: **""" + str(count['Easy']) + """** | Medium: **""" + str(count['Medium']) + """** | Hard: **""" + str(count['Hard']) + """**)</span>

---

### 📚 Problem Collections
- **[Easy Problems](./leetcode/easy-problems.md)** - """ + str(count['Easy']) + """ problem""" + ("s" if count['Easy'] != 1 else "") + """
- **[Medium Problems](./leetcode/medium-problems.md)** - """ + str(count['Medium']) + """ problem""" + ("s" if count['Medium'] != 1 else "") + """
- **[Hard Problems](./leetcode/hard-problems.md)** - """ + str(count['Hard']) + """ problem""" + ("s" if count['Hard'] != 1 else "") + """

---

*Solutions to LeetCode problems in """ + ", ".join(languages) + """*

*Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + """*

</div>
"""
    return content

async def sync_repo_with_leetcode(repo_data: dict, credentials: dict, languages: List[str]):
    """Sync a single repository with LeetCode data"""
    repo_full_name = repo_data["repoFullName"]
    installation_id = repo_data["installationId"]
    branch = repo_data["defaultBranch"]
    user_id = repo_data["userId"]
    
    session_cookie = credentials["sessionCookie"]
    csrf_token = credentials["csrfToken"]
    credential_id = credentials["credentialId"]
    
    print(f"🔄 Syncing {repo_full_name}...")
    
    try:
        # Get installation token
        token = get_installation_token(installation_id)
        
        # Fetch LeetCode submissions
        print(f"  📥 Fetching submissions from LeetCode...")
        
        try:
            all_subs = get_all_submissions(session_cookie, csrf_token)
            print(f"  ✓ Retrieved {len(all_subs)} submissions")
        except Exception as e:
            # If request fails, try to refresh the session cookie
            print(f"  ⚠️ Session may be expired, attempting to refresh...")
            new_session = refresh_leetcode_session(csrf_token, session_cookie)
            
            if new_session:
                print(f"  ✅ Session refreshed successfully")
                session_cookie = new_session
                await update_user_session_cookie(credential_id, new_session)
                
                # Retry with new session
                all_subs = get_all_submissions(session_cookie, csrf_token)
                print(f"  ✓ Retrieved {len(all_subs)} submissions")
            else:
                raise Exception("Failed to refresh session cookie. Please update your LeetCode credentials.")
        
        if not all_subs:
            print(f"  ⚠️ No recent submissions found")
            return {"repo": repo_full_name, "status": "no_submissions", "problems": 0}
        
        # Group submissions by problem
        by_slug = {}
        for s in all_subs:
            by_slug.setdefault(s["titleSlug"], []).append(s)

        slugs = list(by_slug.keys())
        print(f"  📝 Processing {len(slugs)} problems...")

        summary = []
        problems_created = 0

        for slug in slugs:
            try:
                # Get problem data
                pd = get_problem_data(slug, session_cookie, csrf_token)
                subs = by_slug[slug]
                
                # Create problem README
                problem_readme_path = f"leetcode/{slug}/README.md"
                readme_content = f"# {pd['title']}\n\n{html_to_md(pd.get('content',''))}\n"
                
                sha = get_file_sha(token, repo_full_name, problem_readme_path, branch)
                create_or_update_file(
                    token, repo_full_name, problem_readme_path, readme_content,
                    f"Add problem: {pd['title']}", branch, sha
                )
                
                # Save solution template
                for snippet in pd.get("codeSnippets", []):
                    if snippet["lang"].lower() in languages:
                        ext = EXT_MAP.get(snippet['lang'].lower(), snippet['lang'].lower())
                        template_path = f"leetcode/{slug}/solutiontemplate.{ext}"
                        
                        sha = get_file_sha(token, repo_full_name, template_path, branch)
                        create_or_update_file(
                            token, repo_full_name, template_path, snippet["code"],
                            f"Add solution template for {pd['title']}", branch, sha
                        )
                        break
                
                # Save submissions
                for sub in subs:
                    lang = sub["lang"].lower()
                    if lang not in languages:
                        continue
                    
                    ext = EXT_MAP.get(lang, lang)
                    timestamp = sub["timestamp"]
                    filename = f"{timestamp}_approach_{sub['id']}.{ext}"
                    submission_path = f"leetcode/{slug}/submissions/{lang}/{filename}"
                    
                    # Check if submission already exists
                    if check_file_exists_in_repo(token, repo_full_name, submission_path, branch):
                        continue
                    
                    code = get_submission_code(int(sub["id"]), session_cookie, csrf_token)
                    create_or_update_file(
                        token, repo_full_name, submission_path, code,
                        f"Add {lang} solution for {pd['title']}", branch
                    )
                
                summary.append({"slug": slug, "title": pd["title"], "difficulty": pd["difficulty"]})
                problems_created += 1
                print(f"  ✓ {pd['title']} ({pd['difficulty']})")
                
            except Exception as e:
                print(f"  ❌ Failed to process {slug}: {str(e)}")
        
        # Generate and update LeetcodeProgress.md
        if summary:
            progress_content = generate_leetcode_progress_content(summary, languages)
            sha = get_file_sha(token, repo_full_name, "LeetcodeProgress.md", branch)
            create_or_update_file(
                token, repo_full_name, "LeetcodeProgress.md", progress_content,
                f"Update LeetCode progress: {len(summary)} problems", branch, sha
            )
            
            # Generate and update difficulty-based problem files
            problem_files = generate_problem_files_content(summary, languages)
            for filename, content in problem_files.items():
                # These files go in the root directory, not inside leetcode/
                file_path = filename
                sha = get_file_sha(token, repo_full_name, file_path, branch)
                create_or_update_file(
                    token, repo_full_name, file_path, content,
                    f"Update {filename}", branch, sha
                )
        
        # Update lastSyncAt in database
        databases.update_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=COLLECTION_IDS["activated_repos"],
            document_id=repo_data["$id"],
            data={"lastSyncAt": datetime.now().isoformat()}
        )
        
        print(f"  ✅ Successfully synced {problems_created} problems to {repo_full_name}")
        
        # Send email notification to user
        try:
            # Get user email from userId
            user_email = user_id.replace("_", "@", 1).replace("_", ".")
            
            # Generate email HTML
            email_html = generate_email_html(user_email, summary, repo_full_name)
            
            # Send email
            send_email(
                to_email=user_email,
                subject=f"🎉 LeetVault Sync Complete - {problems_created} Problems Synced",
                html_content=email_html
            )
        except Exception as email_error:
            print(f"  ⚠️ Failed to send email notification: {str(email_error)}")
        
        return {
            "repo": repo_full_name, 
            "status": "success", 
            "problems": problems_created,
            "user_email": user_email
        }
        
    except Exception as e:
        print(f"  ❌ Failed to sync {repo_full_name}: {str(e)}")
        return {"repo": repo_full_name, "status": "failed", "error": str(e)}

async def sync_all_active_repos(user_email: Optional[str] = None):
    """Sync all active repositories with LeetCode data in parallel"""
    global fetch_status
    
    try:
        fetch_status.update({
            "status": "running",
            "message": "Syncing active repositories...",
            "last_fetch_time": datetime.now().isoformat()
        })
        
        # Get active repositories (optionally filtered by user email)
        queries = [Query.equal("isActive", True)]
        
        # If user_email is provided, convert to userId format and filter
        if user_email:
            user_id = user_email.replace("@", "_").replace(".", "_")
            queries.append(Query.equal("userId", user_id))
        
        result = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=COLLECTION_IDS["activated_repos"],
            queries=queries
        )
        
        active_repos = result["documents"]
        user_filter_msg = f" for user {user_email}" if user_email else ""
        print(f"📊 Found {len(active_repos)} active repositories{user_filter_msg}")
        
        if not active_repos:
            fetch_status.update({
                "status": "completed",
                "message": f"No active repositories found{user_filter_msg}"
            })
            return []
        
        # Prepare tasks for parallel execution
        tasks = []
        
        for repo in active_repos:
            # Get user's LeetCode credentials
            user_id = repo["userId"]
            credentials = await get_user_leetcode_credentials(user_id)
            
            if not credentials:
                print(f"⚠️ No LeetCode credentials found for user {user_id}")
                continue
            
            # Create task for parallel execution
            task = sync_repo_with_leetcode(
                repo,
                credentials,
                ["python3"]  # Default language, can be made configurable
            )
            tasks.append(task)
        
        # Execute all syncs in parallel
        print(f"🚀 Starting parallel sync for {len(tasks)} repositories...")
        sync_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle exceptions
        processed_results = []
        for i, result in enumerate(sync_results):
            if isinstance(result, Exception):
                print(f"❌ Task {i} failed with exception: {str(result)}")
                processed_results.append({
                    "status": "failed",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        total_problems = sum(r.get("problems", 0) for r in processed_results if isinstance(r, dict) and r.get("status") == "success")
        successful_syncs = sum(1 for r in processed_results if isinstance(r, dict) and r.get("status") == "success")

        fetch_status.update({
            "status": "completed",
            "message": f"Synced {successful_syncs}/{len(active_repos)} repositories with {total_problems} problems",
            "problems_processed": total_problems
        })

        print(f"✅ Parallel sync completed: {successful_syncs}/{len(active_repos)} successful")
        return processed_results

    except Exception as e:
        fetch_status.update({
            "status": "failed",
            "message": f"Sync failed: {str(e)}"
        })
        print(f"❌ Sync failed: {str(e)}")
        raise

class SyncRequest(BaseModel):
    user_email: Optional[str] = None

@app.post("/sync")
async def trigger_sync(background_tasks: BackgroundTasks, request: SyncRequest = None):
    """
    Trigger parallel sync for active repositories
    
    Args:
        user_email (optional): If provided, syncs only this user's repositories
                              If omitted, syncs all active repositories
    
    This will process repos simultaneously for maximum efficiency
    """
    global fetch_status

    if fetch_status["status"] == "running":
        raise HTTPException(status_code=409, detail="Sync already in progress")

    user_email = request.user_email if request else None
    background_tasks.add_task(sync_all_active_repos, user_email)

    if user_email:
        message = f"Sync started for user {user_email}"
    else:
        message = "Parallel sync started for all active repositories"

    return {
        "message": message,
        "status": "running",
        "user_email": user_email
    }

@app.get("/status")
async def get_fetch_status():
    """Get the current status of the sync process"""
    return FetchStatus(**fetch_status)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "LeetCode Fetch Service"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "LeetCode Fetch Service",
        "version": "1.0.0",
        "endpoints": {
            "POST /sync": "Trigger sync (optionally with user_email)",
            "GET /status": "Get sync status",
            "GET /health": "Health check"
        }
    }

# ---- Appwrite Function Wrapper ----
async def main(context):
    """Entry point for Appwrite Function"""
    try:
        req = context.req
        path = req.path if hasattr(req, 'path') and req.path else "/"
        method = (req.method if hasattr(req, 'method') and req.method else "GET").upper()
        headers = dict(req.headers) if hasattr(req, 'headers') and req.headers else {}
        query_params = {}
        if hasattr(req, 'query') and req.query:
            query_params = dict(req.query)
        
        # Get request body - only for methods that typically have bodies
        body = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                # Try body_json first (parsed JSON, recommended by Appwrite)
                if hasattr(req, 'body_json') and req.body_json is not None:
                    body = req.body_json
                # Fallback to body_text for text data
                elif hasattr(req, 'body_text') and req.body_text:
                    try:
                        body = json.loads(req.body_text)
                    except (json.JSONDecodeError, ValueError):
                        body = req.body_text
                # For binary data
                elif hasattr(req, 'body_binary') and req.body_binary:
                    body = req.body_binary
            except Exception:
                pass
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        if method == "GET":
            response = client.get(path, params=query_params, headers=headers)
        elif method == "POST":
            if isinstance(body, bytes):
                response = client.post(path, content=body, params=query_params, headers=headers)
            else:
                response = client.post(path, json=body, params=query_params, headers=headers)
        elif method == "PUT":
            if isinstance(body, bytes):
                response = client.put(path, content=body, params=query_params, headers=headers)
            else:
                response = client.put(path, json=body, params=query_params, headers=headers)
        elif method == "DELETE":
            response = client.delete(path, params=query_params, headers=headers)
        else:
            if isinstance(body, bytes):
                response = client.request(method, path, content=body, params=query_params, headers=headers)
            else:
                response = client.request(method, path, json=body, params=query_params, headers=headers)
        
        status_code = response.status_code
        response_headers = dict(response.headers)
        content_type = response.headers.get("content-type", "")
        
        if "application/json" in content_type:
            return context.res.json(response.json(), status_code, response_headers)
        else:
            return context.res.text(response.text, status_code, response_headers)
        
    except Exception as e:
        print(f"❌ Appwrite Function Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return context.res.json({"error": str(e), "status": "error"}, 500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
