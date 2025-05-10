from typing import List, Dict, Optional

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.auth import verify_password
from api.cache import set_to_cache, get_from_cache, invalidate_cache

DATABASE_URL = "postgresql://postgres:123@localhost:5432/systemDesign"

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    password = Column(String(255))
    role = Column(String(50))

    def to_dict(self) -> Dict:
        """Преобразует объект User в словарь"""
        return {
            'email': self.email,
            'name': self.name,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, user_dict: Dict) -> 'User':
        return User(
            email=user_dict.get('email'),
            name=user_dict.get('name'),
            password=user_dict.get('password'),
            role=user_dict.get('role')
        )


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Создает таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Генератор сессий для зависимостей"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_users() -> List[Dict]:
    """Загружает всех пользователей из базы данных (без паролей)"""
    cache_key = "users:all"
    cached_data = get_from_cache(cache_key)
    if cached_data is not None:
        return cached_data

    create_tables()
    db = SessionLocal()
    try:
        users = db.query(User).all()
        result = [user.to_dict() for user in users]
        set_to_cache(cache_key, result)
        return result
    finally:
        db.close()


def save_users(users: List[Dict]):
    """Сохраняет всех пользователей в базу данных (перезаписывает существующих)"""
    create_tables()
    db = SessionLocal()
    try:
        db.query(User).delete()

        for user_dict in users:
            user = User.from_dict(user_dict)
            db.add(user)

        db.commit()

        set_to_cache("users:all", [user.to_dict() for user in db.query(User).all()])

    finally:
        db.close()


def find_user_by_email(email: str) -> Optional[Dict]:
    """Находит пользователя по email и возвращает данные для аутентификации"""
    cache_key = f"user:email:{email}"
    cached_data = get_from_cache(cache_key)
    if cached_data is not None:
        return cached_data

    create_tables()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None

        result = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "password": user.password
        }

        set_to_cache(cache_key, result)

        return result
    finally:
        db.close()


def delete_user_by_email(email: str) -> bool:
    """Удаляет пользователя по email"""
    create_tables()
    db = SessionLocal()
    try:
        result = db.query(User).filter(User.email == email).delete()
        db.commit()

        if result > 0:
            invalidate_cache(f"user:email:{email}")
            invalidate_cache("users:all")

        return result > 0
    finally:
        db.close()


def authenticate_user(email: str, password: str) -> Optional[User]:
    """Аутентифицирует пользователя"""
    db = SessionLocal()
    try:
        user = find_user_by_email(email)
        if not user or not verify_password(password, user["password"]):
            return None
        return user
    finally:
        db.close()
