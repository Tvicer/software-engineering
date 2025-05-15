from typing import List, Dict, Any, Optional

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql://postgres:123@localhost:5432/postgres"

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    code = Column(String(50), unique=True)

    tasks = relationship("Task", back_populates="project")

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект Project в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'code': self.code
        }

    @classmethod
    def from_dict(cls, project_dict: Dict[str, Any]) -> 'Project':
        """Создает объект Project из словаря"""
        return Project(
            name=project_dict.get('name'),
            description=project_dict.get('description'),
            code=project_dict.get('code')
        )


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50))
    code = Column(String(50), unique=True)
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship("Project", back_populates="tasks")

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект Task в словарь"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'code': self.code,
            'project_id': self.project_id
        }

    @classmethod
    def from_dict(cls, task_dict: Dict[str, Any]) -> 'Task':
        """Создает объект Task из словаря"""
        return Task(
            title=task_dict.get('title'),
            description=task_dict.get('description'),
            status=task_dict.get('status'),
            code=task_dict.get('code'),
            project_id=task_dict.get('project_id')
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


def create_project(project_data: Dict[str, Any]):
    """Создает новый проект"""
    db = SessionLocal()
    try:
        existing_project = db.query(Project).filter(Project.name == project_data["name"]).first()
        if existing_project:
            return {"error": "Проект с таким именем уже существует"}

        project = Project.from_dict(project_data)
        project.code = f"PROJ-{project.id}" if not project_data.get("code") else project_data.get("code")

        db.add(project)
        db.commit()
        db.refresh(project)

        if not project_data.get("code"):
            project.code = f"PROJ-{project.id}"
            db.commit()
            db.refresh(project)

        return {"message": "Проект успешно создан", "project": project.to_dict()}
    except Exception as e:
        db.rollback()
        return {"error": f"Ошибка при создании проекта: {str(e)}"}
    finally:
        db.close()


def search_projects_by_name(name: str) -> List[Dict[str, Any]]:
    """Ищет проекты по имени"""
    db = SessionLocal()
    try:
        projects = db.query(Project).filter(Project.name.ilike(f"%{name}%")).all()
        return [project.to_dict() for project in projects]
    finally:
        db.close()


def get_all_projects() -> List[Dict[str, Any]]:
    """Возвращает все проекты"""
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        return [project.to_dict() for project in projects]
    finally:
        db.close()


def create_task(task_data: Dict[str, Any]):
    """Создает новую задачу"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == task_data["project_id"]).first()
        if not project:
            return {"error": "Проект не найден"}

        task_count = db.query(Task).filter(Task.project_id == task_data["project_id"]).count()
        task_code = f"{project.code}-{task_count + 1}"

        task = Task.from_dict(task_data)
        task.code = task_code

        db.add(task)
        db.commit()
        db.refresh(task)

        return {"message": "Задача успешно создана", "task": task.to_dict()}
    except Exception as e:
        db.rollback()
        return {"error": f"Ошибка при создании задачи: {str(e)}"}
    finally:
        db.close()


def get_all_tasks_in_project(project_id: int) -> List[Dict[str, Any]]:
    """Возвращает все задачи в проекте"""
    db = SessionLocal()
    try:
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        return [task.to_dict() for task in tasks]
    finally:
        db.close()


def get_task_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Находит задачу по коду"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.code == code).first()
        return task.to_dict() if task else None
    finally:
        db.close()


create_tables()
