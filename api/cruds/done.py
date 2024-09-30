from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.models.task as task_model

async def create_done(db: AsyncSession, task_id: int) -> task_model.Done:
    done = task_model.Done(id=task_id)

    db.add(done)
    await db.commit()
    await db.refresh(done)

    return done


async def delete_done(db: AsyncSession, task_id: int) -> None:
    done = await db.get(task_model.Done, task_id)

    if done is None:
        raise HTTPException(status_code=404, detail="Done not found")

    await db.delete(done)
    await db.commit()
