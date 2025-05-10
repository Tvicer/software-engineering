from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "systemDesign"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

projects_collection = db["projects"]
tasks_collection = db["tasks"]

# Создаем индексы
projects_collection.create_index("name", unique=True)
projects_collection.create_index("code", unique=True)
tasks_collection.create_index("code", unique=True)


def create_project(project_data: Dict[str, Any]):
    """Создает новый проект"""
    try:
        project_data.setdefault("code", None)
        result = projects_collection.insert_one(project_data)

        if not project_data["code"]:
            code = f"PROJ-{result.inserted_id}"
            projects_collection.update_one(
                {"_id": result.inserted_id},
                {"$set": {"code": code}}
            )
            project_data["code"] = code

        project_data["_id"] = str(result.inserted_id)
        return {"message": "Проект успешно создан", "project": project_data}
    except DuplicateKeyError:
        return {"error": "Проект с таким именем или кодом уже существует"}
    except Exception as e:
        return {"error": f"Ошибка при создании проекта: {str(e)}"}


def search_projects_by_name(name: str) -> List[Dict[str, Any]]:
    """Ищет проекты по имени"""
    projects = []
    for project in projects_collection.find({"name": {"$regex": name, "$options": "i"}}):
        project["_id"] = str(project["_id"])
        projects.append(project)
    return projects


def get_all_projects() -> List[Dict[str, Any]]:
    """Возвращает все проекты"""
    projects = []
    for project in projects_collection.find():
        project["_id"] = str(project["_id"])
        projects.append(project)
    return projects


def create_task(task_data: Dict[str, Any]):
    """Создает новую задачу"""
    try:
        project = projects_collection.find_one({"_id": ObjectId(task_data["project_id"])})
        if not project:
            return {"error": "Проект не найден"}

        task_count = tasks_collection.count_documents({"project_id": task_data["project_id"]})
        task_code = f"{project['code']}-{task_count + 1}"

        task_data["code"] = task_code
        result = tasks_collection.insert_one(task_data)

        task_data["_id"] = str(result.inserted_id)
        return {"message": "Задача успешно создана", "task": task_data}
    except Exception as e:
        return {"error": f"Ошибка при создании задачи: {str(e)}"}


def get_all_tasks_in_project(project_id: str) -> List[Dict[str, Any]]:
    """Возвращает все задачи в проекте"""
    tasks = []
    for task in tasks_collection.find({"project_id": project_id}):
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks


def get_task_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Находит задачу по коду"""
    task = tasks_collection.find_one({"code": code})
    if task:
        task["_id"] = str(task["_id"])
    return task