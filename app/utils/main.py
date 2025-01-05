from jose import jwt
import requests
from fastapi import HTTPException
from app.core.config import get_settings

settings = get_settings()
def fetch_apple_public_keys():
	response = requests.get(settings.APPLE_PUBLIC_KEYS_URL)
	if response.status_code != 200:
		raise HTTPException(
			status_code=500,
			detail="Failed to fetch Apple public keys"
		)
	return response.json()["keys"]

def verify_apple_token(id_token: str) -> dict:
    keys = fetch_apple_public_keys()
    
    for key in keys:
        try:
            decoded = jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=settings.APPLE_BUNDLE_ID,
                issuer="https://appleid.apple.com"
            )
            return decoded
        except jwt.JWTError:
            continue
    
    raise HTTPException(
        status_code=401,
        detail="Invalid Apple ID token"
    ) 