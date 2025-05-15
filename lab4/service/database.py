import uuid
from typing import List, Dict, Any, Optional

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "projects_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

projects_collection = db["projects"]
tasks_collection = db["tasks"]

projects_collection.create_index("name", unique=True)
projects_collection.create_index("code", unique=True)
tasks_collection.create_index("code", unique=True)


def create_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Создает новый проект в MongoDB"""
    try:
        project_id = str(uuid.uuid4())
        project_data["_id"] = project_id

        if not project_data.get("code"):
            project_data["code"] = f"PROJ-{project_id[:8]}"

        result = projects_collection.insert_one(project_data)

        if result.inserted_id:
            project_data["id"] = project_data.pop("_id")
            return {"message": "Проект успешно создан", "project": project_data}
        else:
            return {"error": "Не удалось создать проект"}

    except DuplicateKeyError:
        return {"error": "Проект с таким именем или кодом уже существует"}
    except Exception as e:
        return {"error": f"Ошибка при создании проекта: {str(e)}"}


def search_projects_by_name(name: str) -> List[Dict[str, Any]]:
    """Ищет проекты по имени (регистронезависимо)"""
    try:
        projects = list(projects_collection.find(
            {"name": {"$regex": name, "$options": "i"}},
            {"_id": 0, "id": "$_id"}
        ))
        return projects
    except Exception as e:
        print(f"Ошибка при поиске проектов: {str(e)}")
        return []


def get_all_projects() -> List[Dict[str, Any]]:
    """Возвращает все проекты"""
    try:
        projects = list(projects_collection.find(
            {},
            {"_id": 0, "id": "$_id"}
        ))
        return projects
    except Exception as e:
        print(f"Ошибка при получении проектов: {str(e)}")
        return []


def create_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Создает новую задачу в MongoDB"""
    try:
        project = projects_collection.find_one({"_id": task_data["project_id"]})
        if not project:
            return {"error": "Проект не найден"}

        task_id = str(uuid.uuid4())
        task_data["_id"] = task_id

        task_count = tasks_collection.count_documents({"project_id": task_data["project_id"]})
        task_data["code"] = f"{project['code']}-{task_count + 1}"

        result = tasks_collection.insert_one(task_data)

        if result.inserted_id:
            task_data["id"] = task_data.pop("_id")
            return {"message": "Задача успешно создана", "task": task_data}
        else:
            return {"error": "Не удалось создать задачу"}

    except Exception as e:
        return {"error": f"Ошибка при создании задачи: {str(e)}"}


def get_all_tasks_in_project(project_id: str) -> List[Dict[str, Any]]:
    """Возвращает все задачи в проекте"""
    try:
        tasks = list(tasks_collection.find(
            {"project_id": project_id},
            {"_id": 0, "id": "$_id"}
        ))
        return tasks
    except Exception as e:
        print(f"Ошибка при получении задач: {str(e)}")
        return []


def get_task_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Находит задачу по коду"""
    try:
        task = tasks_collection.find_one(
            {"code": code},
            {"_id": 0, "id": "$_id"}
        )
        return task
    except Exception as e:
        print(f"Ошибка при поиске задачи: {str(e)}")
        return None
