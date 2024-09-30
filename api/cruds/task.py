from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model
import api.schemas.task as task_schema


async def get_tasks_with_done(db: AsyncSession) -> List[task_schema.Task]:
    stmt = (
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )

    result = await db.execute(stmt)

    rows = result.fetchall()
    tasks = [
        task_schema.Task(id=row.id, title=row.title, done=row.done)
        for row in rows
    ]
    
    return tasks



async def create_task(db: AsyncSession, task_create: task_schema.TaskCreate) -> task_model.Task:
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession, task_update: task_schema.TaskCreateResponse) -> task_model.Task:
    target_task = await db.get(task_model.Task, task_update.id)

    if target_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    target_task.title = task_update.title

    await db.commit()
    await db.refresh(target_task)
    
    return target_task


async def delete_task(db: AsyncSession, id: int) -> None:
    target_task = await db.get(task_model.Task, id)

    if target_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(target_task)
    await db.commit()
