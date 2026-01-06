from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.base import Task, User
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut, status_code=201)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task()
    new_task.description = task.description
    new_task.title = task.title
    new_task.owner_id = current_user.id
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskOut], status_code=200)
async def get_user_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Task).where(Task.owner_id == current_user.id)
    result = await db.scalars(query)
    return result.all()


@router.patch("/{task_id}", response_model=TaskOut, status_code=200)
async def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Task).where(
        (Task.owner_id == current_user.id) & (Task.id == task_id)
    )
    result = await db.scalar(query)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task is found with this id!",
        )
    update_data = updated_task.model_dump(exclude_unset=True)
    for updated_data_key, updated_data_value in update_data.items():
        setattr(result, updated_data_key, updated_data_value)

    await db.commit()
    await db.refresh(result)
    return result


@router.get("/{task_id}", response_model=TaskOut, status_code=200)
async def search_for_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Task).where(
        (Task.owner_id == current_user.id) & (Task.id == task_id)
    )
    result = await db.scalar(query)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task is found with this id!",
        )
    return result


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Task).where(
        (Task.owner_id == current_user.id) & (Task.id == task_id)
    )
    result = await db.scalar(query)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task is found with this id!",
        )
    await db.delete(result)
    await db.commit()
