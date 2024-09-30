from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.done as done_cruds
from api.db import get_db
import api.schemas.done as done_schemas


router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=done_schemas.DoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    return await done_cruds.create_done(db, task_id)


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    return await done_cruds.delete_done(db, task_id)
