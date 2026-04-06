from typing import Dict, Optional

USERS: Dict[str, Dict[str, str]] = {
    "guest": {"password": "", "role": "guest"},
    "admin": {"password": "1234", "role": "admin"},
}


def authenticate(username: str, password: str) -> Optional[Dict[str, str]]:
    user = USERS.get(username)
    if not user:
        return None
    if username == "guest":
        return {"username": "guest", "role": "guest"}
    if user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None
