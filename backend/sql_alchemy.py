import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships

# Tables definition
class TaskList(Base):
    __tablename__ = "tasklist"
    id: Mapped[int] = mapped_column(primary_key=True)
    listId: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(100))
    createdDate: Mapped[dt_date] = mapped_column(Date)

class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    taskId: Mapped[int] = mapped_column(Integer)
    urgent: Mapped[bool] = mapped_column(Boolean)
    important: Mapped[bool] = mapped_column(Boolean)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    dueDate: Mapped[dt_date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(100))
    completionDate: Mapped[dt_date] = mapped_column(Date)
    tasklist_id: Mapped[int] = mapped_column(ForeignKey("tasklist.id"))


#--- Relationships of the tasklist table
TaskList.contains: Mapped[List["Task"]] = relationship("Task", back_populates="tasklist", foreign_keys=[Task.tasklist_id])

#--- Relationships of the task table
Task.tasklist: Mapped["TaskList"] = relationship("TaskList", back_populates="contains", foreign_keys=[Task.tasklist_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)