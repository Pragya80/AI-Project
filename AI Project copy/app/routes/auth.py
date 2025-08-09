from fastapi import APIRouter, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/auth", tags=["Auth"])

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")


@router.get("/login")
def login_with_linkedin():
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={LINKEDIN_REDIRECT_URI}"
        "&scope=w_member_social%20r_liteprofile%20r_emailaddress"
    )
    return {"auth_url": auth_url}


@router.get("/callback")
def linkedin_callback(code: str):
    # Step 1 — Exchange code for access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    token_data = response.json()

    if "access_token" in token_data:
        access_token = token_data["access_token"]
        return {"message": "LinkedIn Auth successful", "access_token": access_token}
    else:
        return {"error": "Failed to get access token", "details": token_data}
