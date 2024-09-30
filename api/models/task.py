from typing import List
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(1024))

    done: Mapped["Done"] = relationship("Done", back_populates="task", cascade="all, delete-orphan", uselist=False)


class Done(Base):
    __tablename__ = "dones"

    id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), primary_key=True)

    task: Mapped["Task"] = relationship("Task", back_populates="done")
