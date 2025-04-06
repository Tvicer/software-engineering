import json
from pathlib import Path

USER_DB_FILE = Path("USERS_DB.json")

def load_users():
    if not USER_DB_FILE.exists() or USER_DB_FILE.stat().st_size == 0:
        return []
    with open(USER_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def find_user_by_email(email):
    users = load_users()
    if not users:
        return None
    
    for user in users:
        if user["email"] == email:
            return user
    return None

def delete_user_by_email(email):
    users = load_users()
    new_users = []
    for user in users:
        if user["email"] != email:
            new_users.append(user)
    if len(new_users) == len(users):
        return False
    save_users(new_users)
    return True

