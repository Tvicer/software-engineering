from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user
from database import (
    create_project, search_projects_by_name, get_all_projects,
    create_task, get_all_tasks_in_project, get_task_by_code
)
from models import ProjectCreate, TaskCreate

router = APIRouter()


@router.get("/api/v1/user/login", tags=["Страница пользователя"])
def user_hello(user: dict = Depends(get_current_user)):
    return {"message": f"Привет, {user['email']}! Это страница для пользователей."}


@router.post("/api/v1/project/create", tags=["Проекты"])
def create_project_route(project: ProjectCreate):
    """Создает новый проект"""
    result = create_project(project.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Проект успешно создан", "project": result["project"]}


@router.get("/api/v1/project/search", tags=["Проекты"])
def search_project_by_name_route(name: str):
    """Ищет проекты по имени"""
    projects = search_projects_by_name(name)
    return {"projects": projects}


@router.get("/api/v1/projects", tags=["Проекты"])
def get_all_projects_route():
    """Возвращает список всех проектов"""
    projects = get_all_projects()
    return {"projects": projects}


@router.post("/api/v1/task/create", tags=["Задачи"])
def create_task_route(task: TaskCreate):
    """Создает новую задачу в проекте"""
    result = create_task(task.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Задача успешно создана", "task": result["task"]}


@router.get("/api/v1/tasks", tags=["Задачи"])
def get_all_tasks_in_project_route(project_id: int):
    """Возвращает список всех задач в проекте"""
    tasks = get_all_tasks_in_project(project_id)
    return {"tasks": tasks}


@router.get("/api/v1/task", tags=["Задачи"])
def get_task_by_code_route(code: str):
    """Возвращает задачу по коду"""
    task = get_task_by_code(code)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"task": task}
