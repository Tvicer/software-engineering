from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., example="Новый проект")
    description: str = Field(..., example="Описание нового проекта")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Обновленное название проекта")
    description: Optional[str] = Field(None, example="Обновленное описание проекта")


class TaskCreate(BaseModel):
    project_id: int = Field(..., example=1)
    title: str = Field(..., example="Новая задача")
    description: str = Field(..., example="Описание новой задачи")
    status: str = Field(..., example="open")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Обновленное название задачи")
    description: Optional[str] = Field(None, example="Обновленное описание задачи")
    status: Optional[str] = Field(None, example="in_progress")
