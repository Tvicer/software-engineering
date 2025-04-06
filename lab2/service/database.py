import json
from pathlib import Path
from typing import List, Dict, Any

JIRA_DB_FILE = Path("JIRA_DB.json")


def load_data() -> Dict[str, List[Dict[str, Any]]]:
    if not JIRA_DB_FILE.exists():
        return {"projects": [], "tasks": []}
    try:
        with open(JIRA_DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "projects" not in data:
                data["projects"] = []
            if "tasks" not in data:
                data["tasks"] = []
            return data
    except json.JSONDecodeError:
        return {"projects": [], "tasks": []}
    except Exception as e:
        raise ValueError(f"Ошибка чтения файла JIRA_DB.json: {str(e)}")


def save_data(data: Dict[str, List[Dict[str, Any]]]):
    try:
        with open(JIRA_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise IOError(f"Ошибка сохранения файла JIRA_DB.json: {e}")


def create_project(project_data: Dict[str, Any]):
    try:
        data = load_data()

        if any(p["name"] == project_data["name"] for p in data["projects"]):
            return {"error": "Проект с таким именем уже существует"}

        project_id = len(data["projects"]) + 1
        project_data["id"] = project_id
        project_data["code"] = f"PROJ-{project_id}"

        data["projects"].append(project_data)
        save_data(data)
        return {"message": "Проект успешно создан", "project": project_data}
    except Exception as e:
        return {"error": f"Ошибка при создании проекта: {str(e)}"}


def search_projects_by_name(name: str) -> List[Dict[str, Any]]:
    data = load_data()
    return [p for p in data["projects"] if name.lower() in p["name"].lower()]


def get_all_projects() -> List[Dict[str, Any]]:
    data = load_data()
    return data["projects"]


def create_task(task_data: Dict[str, Any]):
    try:
        data = load_data()

        project = next((p for p in data["projects"] if p["id"] == task_data["project_id"]), None)
        if not project:
            return {"error": "Проект не найден"}

        project_tasks = [t for t in data["tasks"] if t["project_id"] == task_data["project_id"]]
        task_number = len(project_tasks) + 1
        task_code = f"{project['code']}-{task_number}"

        task_data["id"] = len(data["tasks"]) + 1
        task_data["code"] = task_code

        data["tasks"].append(task_data)
        save_data(data)
        return {"message": "Задача успешно создана", "task": task_data}
    except Exception as e:
        return {"error": f"Ошибка при создании задачи: {str(e)}"}


def get_all_tasks_in_project(project_id: int) -> List[Dict[str, Any]]:
    data = load_data()
    return [t for t in data["tasks"] if t["project_id"] == project_id]


def get_task_by_code(code: str) -> Dict[str, Any]:
    data = load_data()
    return next((t for t in data["tasks"] if t["code"] == code), None)
