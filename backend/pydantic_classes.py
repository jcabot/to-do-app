from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

############################################
# Classes are defined here
############################################
class TaskListCreate(BaseModel):
    listId: int
    name: str
    createdDate: date
    contains: Optional[List[int]] = None  # 1:N Relationship


class TaskCreate(BaseModel):
    dueDate: date
    status: str
    taskId: int
    title: str
    important: bool
    description: str
    urgent: bool
    completionDate: date
    tasklist: int  # N:1 Relationship (mandatory)


