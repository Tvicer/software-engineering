from fastapi import APIRouter, HTTPException
from database import load_users, save_users, find_user_by_email, delete_user_by_email
from auth import hash_password, verify_password, create_access_token
from models import UserCreate, UserLogin, UserUpdate

router = APIRouter()

def register_user(user: UserCreate, role: str):
    users = load_users()

    if find_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "password_hash": hash_password(user.password),
        "role": role,
    }

    users.append(new_user)
    save_users(users)

    return {"message": "Вы зарегистрированы"}

@router.post("/api/v1/user/create", tags=["Регистрация пользователя"])
def register_regular_user(user: UserCreate):
    return register_user(user, role="user")

@router.post("/api/v1/login", tags=["Авторизация пользователя (получение токена)"])
def login_user(user: UserLogin):
    db_user = find_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    token = create_access_token(db_user["email"], db_user["role"], db_user["id"])
    return {"access_token": token, "token_type": "Bearer"}

@router.delete("/api/v1/user/delete", tags=["Пользователь"])
def delete_user(email: str):
    db_user = find_user_by_email(email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не cуществует")
    if delete_user_by_email(email):
        return {"message": "Пользователь удален"}
    return {"message": "Ошибка удаления"}
    

@router.put("/api/v1/user/update", tags=["Пользователь"])
def update_user(user: UserUpdate):
    db_user = find_user_by_email(str(user.email))   
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не cуществует")
    
    if user.new_name:
        db_user["name"] = user.new_name
    if user.new_email:
        db_user["email"] = user.new_email
    if user.new_password:
        db_user["password_hash"] = hash_password(user.new_password)
        
    delete_user_by_email(str(user.email))
    users = load_users()
    users.append(db_user)
    save_users(users)
    return {"message": "Данные пользователя обновлены"}


@router.get("/api/v1/user/get_all", tags=["Пользователь"])
def get_all_users():
    users = load_users()
    if not users:
        raise HTTPException(status_code=401, detail="Ошибка. Нет пользователей или ошибка загрузки") 
    return {"users": users}
