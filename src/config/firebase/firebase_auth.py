import os
#import firebase_admin
#from firebase_admin import auth, credentials
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_PATH = BASE_DIR / "firebase" / "service-account.json"


# if not firebase_admin._apps:
#     cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
#     firebase_admin.initialize_app(cred)

auth_scheme = HTTPBearer()

# def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
#     """Verify Firebase ID Token"""
#     try:
#         decoded_token = auth.verify_id_token(credentials.credentials)
#         return decoded_token
#     except Exception as e:
#         raise HTTPException(
#             status_code=401,
#             detail=f"Invalid authentication token: {str(e)}"
#         )

def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
    """Temporarily disabled Firebase ID Token verification"""
    return {"uid": "test_user"}  # Mock user data for testing
