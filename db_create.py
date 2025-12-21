"""
LeetVault Database Schema Setup Script
Creates all collections and attributes in Appwrite
"""

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.permission import Permission
from appwrite.role import Role
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configuration
ENDPOINT = "https://sgp.cloud.appwrite.io/v1"
PROJECT_ID = "693ed956000ee167b797"
API_KEY = "standard_87ae34ae3ce6d5ad62fd78896c7f3d49ed757cc2e0cd97be1d5e5dd2fb88aca83ea73e737ec11aa36b459cc04f5d8585059c7ff38b74df28672cd885878e2e6728199a9f5fbcb6e63132bec994e7ddfbed9d4725a34437607c2ed975ea953ed036ff548fd57015967778a44a351724fe1ead66e6332ebe887877915a896f51f2"  # Replace with your API key
DATABASE_ID = '693edb55001ee4882410'  # LeetVault_Storage database ID

# Initialize Appwrite client
client = Client()
client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)

databases = Databases(client)

def create_users_collection():
    """Create users collection"""
    try:
        print("Creating 'users' collection...")
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name='users',
            permissions=[
                Permission.read(Role.any()),
                Permission.create(Role.users()),
                Permission.update(Role.users()),
                Permission.delete(Role.users())
            ],
            document_security=True
        )
        collection_id = collection['$id']
        print(f"✓ Collection 'users' created with ID: {collection_id}")
        
        # Wait for collection to be ready
        time.sleep(2)
        
        # Create attributes
        print("  Creating attributes...")
        
        # email (unique, required)
        databases.create_email_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='email',
            required=True
        )
        time.sleep(1)
        
        # name (optional)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='name',
            size=255,
            required=False
        )
        time.sleep(1)
        
        # createdAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='createdAt',
            required=True
        )
        time.sleep(1)
        
        # updatedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='updatedAt',
            required=True
        )
        
        print("  ✓ All attributes created for 'users'")
        
        # Create indexes
        print("  Creating indexes...")
        time.sleep(2)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='email_unique',
            type='unique',
            attributes=['email']
        )
        print("  ✓ Indexes created for 'users'")
        
        return collection_id
        
    except Exception as e:
        print(f"✗ Error creating users collection: {e}")
        return None

def create_github_installations_collection():
    """Create github_installations collection"""
    try:
        print("\nCreating 'github_installations' collection...")
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name='github_installations',
            permissions=[
                Permission.read(Role.any()),
                Permission.create(Role.users()),
                Permission.update(Role.users()),
                Permission.delete(Role.users())
            ],
            document_security=True
        )
        collection_id = collection['$id']
        print(f"✓ Collection 'github_installations' created with ID: {collection_id}")
        
        time.sleep(2)
        
        # Create attributes
        print("  Creating attributes...")
        
        # userId (unique foreign key, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # githubInstallationId (unique, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='githubInstallationId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # isActive (optional with default true - will be set in app logic)
        databases.create_boolean_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='isActive',
            required=False,
            default=True
        )
        time.sleep(1)
        
        # installedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='installedAt',
            required=True
        )
        time.sleep(1)
        
        # updatedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='updatedAt',
            required=True
        )
        
        print("  ✓ All attributes created for 'github_installations'")
        
        # Create indexes
        print("  Creating indexes...")
        time.sleep(2)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId_unique',
            type='unique',
            attributes=['userId']
        )
        time.sleep(1)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='githubInstallationId_unique',
            type='unique',
            attributes=['githubInstallationId']
        )
        print("  ✓ Indexes created for 'github_installations'")
        
        return collection_id
        
    except Exception as e:
        print(f"✗ Error creating github_installations collection: {e}")
        return None

def create_activated_repos_collection():
    """Create activated_repos collection"""
    try:
        print("\nCreating 'activated_repos' collection...")
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name='activated_repos',
            permissions=[
                Permission.read(Role.any()),
                Permission.create(Role.users()),
                Permission.update(Role.users()),
                Permission.delete(Role.users())
            ],
            document_security=True
        )
        collection_id = collection['$id']
        print(f"✓ Collection 'activated_repos' created with ID: {collection_id}")
        
        time.sleep(2)
        
        # Create attributes
        print("  Creating attributes...")
        
        # userId (unique foreign key, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # installationId (foreign key, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='installationId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # repoFullName (required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='repoFullName',
            size=512,
            required=True
        )
        time.sleep(1)
        
        # defaultBranch (optional with default)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='defaultBranch',
            size=255,
            required=False,
            default='main'
        )
        time.sleep(1)
        
        # isActive (optional with default)
        databases.create_boolean_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='isActive',
            required=False,
            default=True
        )
        time.sleep(1)
        
        # activatedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='activatedAt',
            required=True
        )
        time.sleep(1)
        
        # lastSyncAt (optional)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='lastSyncAt',
            required=False
        )
        time.sleep(1)
        
        # updatedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='updatedAt',
            required=True
        )
        
        print("  ✓ All attributes created for 'activated_repos'")
        
        # Create indexes
        print("  Creating indexes...")
        time.sleep(2)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId_unique',
            type='unique',
            attributes=['userId']
        )
        time.sleep(1)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='installationId_idx',
            type='key',
            attributes=['installationId']
        )
        time.sleep(1)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='repoFullName_idx',
            type='key',
            attributes=['repoFullName']
        )
        print("  ✓ Indexes created for 'activated_repos'")
        
        return collection_id
        
    except Exception as e:
        print(f"✗ Error creating activated_repos collection: {e}")
        return None

def create_leetcode_credentials_collection():
    """Create leetcode_credentials collection"""
    try:
        print("\nCreating 'leetcode_credentials' collection...")
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name='leetcode_credentials',
            permissions=[
                Permission.read(Role.any()),
                Permission.create(Role.users()),
                Permission.update(Role.users()),
                Permission.delete(Role.users())
            ],
            document_security=True
        )
        collection_id = collection['$id']
        print(f"✓ Collection 'leetcode_credentials' created with ID: {collection_id}")
        
        time.sleep(2)
        
        # Create attributes
        print("  Creating attributes...")
        
        # userId (unique foreign key, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # sessionCookie (required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='sessionCookie',
            size=2048,
            required=True
        )
        time.sleep(1)
        
        # csrfToken (required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='csrfToken',
            size=512,
            required=True
        )
        time.sleep(1)
        
        # leetcodeUsername (optional)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='leetcodeUsername',
            size=255,
            required=False
        )
        time.sleep(1)
        
        # isValid (optional with default)
        databases.create_boolean_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='isValid',
            required=False,
            default=True
        )
        time.sleep(1)
        
        # lastValidatedAt (optional)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='lastValidatedAt',
            required=False
        )
        time.sleep(1)
        
        # createdAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='createdAt',
            required=True
        )
        time.sleep(1)
        
        # updatedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='updatedAt',
            required=True
        )
        
        print("  ✓ All attributes created for 'leetcode_credentials'")
        
        # Create indexes
        print("  Creating indexes...")
        time.sleep(2)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId_unique',
            type='unique',
            attributes=['userId']
        )
        print("  ✓ Indexes created for 'leetcode_credentials'")
        
        return collection_id
        
    except Exception as e:
        print(f"✗ Error creating leetcode_credentials collection: {e}")
        return None

def create_sync_logs_collection():
    """Create sync_logs collection"""
    try:
        print("\nCreating 'sync_logs' collection...")
        collection = databases.create_collection(
            database_id=DATABASE_ID,
            collection_id=ID.unique(),
            name='sync_logs',
            permissions=[
                Permission.read(Role.any()),
                Permission.create(Role.users()),
                Permission.update(Role.users()),
                Permission.delete(Role.users())
            ],
            document_security=True
        )
        collection_id = collection['$id']
        print(f"✓ Collection 'sync_logs' created with ID: {collection_id}")
        
        time.sleep(2)
        
        # Create attributes
        print("  Creating attributes...")
        
        # userId (foreign key, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # repoId (foreign key, required)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='repoId',
            size=255,
            required=True
        )
        time.sleep(1)
        
        # syncType (optional with default)
        databases.create_enum_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='syncType',
            elements=['scheduled', 'manual', 'webhook'],
            required=False,
            default='scheduled'
        )
        time.sleep(1)
        
        # status (optional with default)
        databases.create_enum_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='status',
            elements=['pending', 'success', 'failed', 'partial'],
            required=False,
            default='pending'
        )
        time.sleep(1)
        
        # submissionsCount (optional with default)
        databases.create_integer_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='submissionsCount',
            required=False,
            default=0
        )
        time.sleep(1)
        
        # errorMessage (optional)
        databases.create_string_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='errorMessage',
            size=2048,
            required=False
        )
        time.sleep(1)
        
        # startedAt (required)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='startedAt',
            required=True
        )
        time.sleep(1)
        
        # completedAt (optional)
        databases.create_datetime_attribute(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='completedAt',
            required=False
        )
        
        print("  ✓ All attributes created for 'sync_logs'")
        
        # Create indexes
        print("  Creating indexes...")
        time.sleep(2)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='userId_idx',
            type='key',
            attributes=['userId']
        )
        time.sleep(1)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='repoId_idx',
            type='key',
            attributes=['repoId']
        )
        time.sleep(1)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='status_idx',
            type='key',
            attributes=['status']
        )
        time.sleep(1)
        databases.create_index(
            database_id=DATABASE_ID,
            collection_id=collection_id,
            key='startedAt_idx',
            type='key',
            attributes=['startedAt']
        )
        print("  ✓ Indexes created for 'sync_logs'")
        
        return collection_id
        
    except Exception as e:
        print(f"✗ Error creating sync_logs collection: {e}")
        return None

def main():
    """Main function to create all collections"""
    print("=" * 60)
    print("LeetVault Database Schema Setup")
    print("=" * 60)
    print(f"Database ID: {DATABASE_ID}")
    print(f"Database Name: LeetVault_Storage")
    print("=" * 60)
    
    # Create collections in order
    users_id = create_users_collection()
    github_installations_id = create_github_installations_collection()
    activated_repos_id = create_activated_repos_collection()
    leetcode_credentials_id = create_leetcode_credentials_collection()
    sync_logs_id = create_sync_logs_collection()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"users: {users_id if users_id else 'Failed'}")
    print(f"github_installations: {github_installations_id if github_installations_id else 'Failed'}")
    print(f"activated_repos: {activated_repos_id if activated_repos_id else 'Failed'}")
    print(f"leetcode_credentials: {leetcode_credentials_id if leetcode_credentials_id else 'Failed'}")
    print(f"sync_logs: {sync_logs_id if sync_logs_id else 'Failed'}")
    print("=" * 60)
    print("\n✓ Database schema setup complete!")

if __name__ == "__main__":
    main()
