import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "TaskList", "description": "Operations for TaskList entities"},
        {"name": "TaskList Relationships", "description": "Manage TaskList relationships"},
        {"name": "Task", "description": "Operations for Task entities"},
        {"name": "Task Relationships", "description": "Manage Task relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")
    
    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error", 
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["tasklist_count"] = database.query(TaskList).count()
    stats["task_count"] = database.query(Task).count()
    stats["total_entities"] = sum(stats.values())
    return stats

############################################
#
#   TaskList functions
#
############################################
 
 

@app.get("/tasklist/", response_model=None, tags=["TaskList"])
def get_all_tasklist(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload
    
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(TaskList)
        tasklist_list = query.all()
        
        # Serialize with relationships included
        result = []
        for tasklist_item in tasklist_list:
            item_dict = tasklist_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)
            
            # Add many-to-one relationships (foreign keys for lookup columns)
            
            # Add many-to-many and one-to-many relationship objects (full details)
            task_list = database.query(Task).filter(Task.tasklist_id == tasklist_item.id).all()
            item_dict['contains'] = []
            for task_obj in task_list:
                task_dict = task_obj.__dict__.copy()
                task_dict.pop('_sa_instance_state', None)
                item_dict['contains'].append(task_dict)
            
            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(TaskList).all()


@app.get("/tasklist/count/", response_model=None, tags=["TaskList"])
def get_count_tasklist(database: Session = Depends(get_db)) -> dict:
    """Get the total count of TaskList entities"""
    count = database.query(TaskList).count()
    return {"count": count}


@app.get("/tasklist/paginated/", response_model=None, tags=["TaskList"])
def get_paginated_tasklist(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of TaskList entities"""
    total = database.query(TaskList).count()
    tasklist_list = database.query(TaskList).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": tasklist_list
        }
    
    result = []
    for tasklist_item in tasklist_list:
        contains_ids = database.query(Task.id).filter(Task.tasklist_id == tasklist_item.id).all()
        item_data = {
            "tasklist": tasklist_item,
            "contains_ids": [x[0] for x in contains_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/tasklist/search/", response_model=None, tags=["TaskList"])
def search_tasklist(
    database: Session = Depends(get_db)
) -> list:
    """Search TaskList entities by attributes"""
    query = database.query(TaskList)
    
    
    results = query.all()
    return results


@app.get("/tasklist/{tasklist_id}/", response_model=None, tags=["TaskList"])
async def get_tasklist(tasklist_id: int, database: Session = Depends(get_db)) -> TaskList:
    db_tasklist = database.query(TaskList).filter(TaskList.id == tasklist_id).first()
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")

    contains_ids = database.query(Task.id).filter(Task.tasklist_id == db_tasklist.id).all()
    response_data = {
        "tasklist": db_tasklist,
        "contains_ids": [x[0] for x in contains_ids]}
    return response_data



@app.post("/tasklist/", response_model=None, tags=["TaskList"])
async def create_tasklist(tasklist_data: TaskListCreate, database: Session = Depends(get_db)) -> TaskList:


    db_tasklist = TaskList(
        listId=tasklist_data.listId,        name=tasklist_data.name,        createdDate=tasklist_data.createdDate        )

    database.add(db_tasklist)
    database.commit()
    database.refresh(db_tasklist)

    if tasklist_data.contains:
        # Validate that all Task IDs exist
        for task_id in tasklist_data.contains:
            db_task = database.query(Task).filter(Task.id == task_id).first()
            if not db_task:
                raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")
        
        # Update the related entities with the new foreign key
        database.query(Task).filter(Task.id.in_(tasklist_data.contains)).update(
            {Task.tasklist_id: db_tasklist.id}, synchronize_session=False
        )
        database.commit()


    
    contains_ids = database.query(Task.id).filter(Task.tasklist_id == db_tasklist.id).all()
    response_data = {
        "tasklist": db_tasklist,
        "contains_ids": [x[0] for x in contains_ids]    }
    return response_data


@app.post("/tasklist/bulk/", response_model=None, tags=["TaskList"])
async def bulk_create_tasklist(items: list[TaskListCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple TaskList entities at once"""
    created_items = []
    errors = []
    
    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            
            db_tasklist = TaskList(
                listId=item_data.listId,                name=item_data.name,                createdDate=item_data.createdDate            )
            database.add(db_tasklist)
            database.flush()  # Get ID without committing
            created_items.append(db_tasklist.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})
    
    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})
    
    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} TaskList entities"
    }


@app.delete("/tasklist/bulk/", response_model=None, tags=["TaskList"])
async def bulk_delete_tasklist(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple TaskList entities at once"""
    deleted_count = 0
    not_found = []
    
    for item_id in ids:
        db_tasklist = database.query(TaskList).filter(TaskList.id == item_id).first()
        if db_tasklist:
            database.delete(db_tasklist)
            deleted_count += 1
        else:
            not_found.append(item_id)
    
    database.commit()
    
    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} TaskList entities"
    }

@app.put("/tasklist/{tasklist_id}/", response_model=None, tags=["TaskList"])
async def update_tasklist(tasklist_id: int, tasklist_data: TaskListCreate, database: Session = Depends(get_db)) -> TaskList:
    db_tasklist = database.query(TaskList).filter(TaskList.id == tasklist_id).first()
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")

    setattr(db_tasklist, 'listId', tasklist_data.listId)
    setattr(db_tasklist, 'name', tasklist_data.name)
    setattr(db_tasklist, 'createdDate', tasklist_data.createdDate)
    if tasklist_data.contains is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Task).filter(Task.tasklist_id == db_tasklist.id).update(
            {Task.tasklist_id: None}, synchronize_session=False
        )
        
        # Set new relationships if list is not empty
        if tasklist_data.contains:
            # Validate that all IDs exist
            for task_id in tasklist_data.contains:
                db_task = database.query(Task).filter(Task.id == task_id).first()
                if not db_task:
                    raise HTTPException(status_code=400, detail=f"Task with id {task_id} not found")
            
            # Update the related entities with the new foreign key
            database.query(Task).filter(Task.id.in_(tasklist_data.contains)).update(
                {Task.tasklist_id: db_tasklist.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_tasklist)
    
    contains_ids = database.query(Task.id).filter(Task.tasklist_id == db_tasklist.id).all()
    response_data = {
        "tasklist": db_tasklist,
        "contains_ids": [x[0] for x in contains_ids]    }
    return response_data


@app.delete("/tasklist/{tasklist_id}/", response_model=None, tags=["TaskList"])
async def delete_tasklist(tasklist_id: int, database: Session = Depends(get_db)):
    db_tasklist = database.query(TaskList).filter(TaskList.id == tasklist_id).first()
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    database.delete(db_tasklist)
    database.commit()
    return db_tasklist





############################################
#
#   Task functions
#
############################################
 
 

@app.get("/task/", response_model=None, tags=["Task"])
def get_all_task(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload
    
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Task)
        query = query.options(joinedload(Task.tasklist))
        task_list = query.all()
        
        # Serialize with relationships included
        result = []
        for task_item in task_list:
            item_dict = task_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)
            
            # Add many-to-one relationships (foreign keys for lookup columns)
            if task_item.tasklist:
                related_obj = task_item.tasklist
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['tasklist'] = related_dict
            else:
                item_dict['tasklist'] = None
            
            
            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Task).all()


@app.get("/task/count/", response_model=None, tags=["Task"])
def get_count_task(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Task entities"""
    count = database.query(Task).count()
    return {"count": count}


@app.get("/task/paginated/", response_model=None, tags=["Task"])
def get_paginated_task(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Task entities"""
    total = database.query(Task).count()
    task_list = database.query(Task).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": task_list
    }


@app.get("/task/search/", response_model=None, tags=["Task"])
def search_task(
    database: Session = Depends(get_db)
) -> list:
    """Search Task entities by attributes"""
    query = database.query(Task)
    
    
    results = query.all()
    return results


@app.get("/task/{task_id}/", response_model=None, tags=["Task"])
async def get_task(task_id: int, database: Session = Depends(get_db)) -> Task:
    db_task = database.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    response_data = {
        "task": db_task,
}
    return response_data



@app.post("/task/", response_model=None, tags=["Task"])
async def create_task(task_data: TaskCreate, database: Session = Depends(get_db)) -> Task:

    if task_data.tasklist is not None:
        db_tasklist = database.query(TaskList).filter(TaskList.id == task_data.tasklist).first()
        if not db_tasklist:
            raise HTTPException(status_code=400, detail="TaskList not found")
    else:
        raise HTTPException(status_code=400, detail="TaskList ID is required")

    db_task = Task(
        dueDate=task_data.dueDate,        status=task_data.status,        taskId=task_data.taskId,        title=task_data.title,        important=task_data.important,        description=task_data.description,        urgent=task_data.urgent,        completionDate=task_data.completionDate,        tasklist_id=task_data.tasklist        )

    database.add(db_task)
    database.commit()
    database.refresh(db_task)



    
    return db_task


@app.post("/task/bulk/", response_model=None, tags=["Task"])
async def bulk_create_task(items: list[TaskCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Task entities at once"""
    created_items = []
    errors = []
    
    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.tasklist:
                raise ValueError("TaskList ID is required")
            
            db_task = Task(
                dueDate=item_data.dueDate,                status=item_data.status,                taskId=item_data.taskId,                title=item_data.title,                important=item_data.important,                description=item_data.description,                urgent=item_data.urgent,                completionDate=item_data.completionDate,                tasklist_id=item_data.tasklist            )
            database.add(db_task)
            database.flush()  # Get ID without committing
            created_items.append(db_task.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})
    
    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})
    
    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Task entities"
    }


@app.delete("/task/bulk/", response_model=None, tags=["Task"])
async def bulk_delete_task(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Task entities at once"""
    deleted_count = 0
    not_found = []
    
    for item_id in ids:
        db_task = database.query(Task).filter(Task.id == item_id).first()
        if db_task:
            database.delete(db_task)
            deleted_count += 1
        else:
            not_found.append(item_id)
    
    database.commit()
    
    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Task entities"
    }

@app.put("/task/{task_id}/", response_model=None, tags=["Task"])
async def update_task(task_id: int, task_data: TaskCreate, database: Session = Depends(get_db)) -> Task:
    db_task = database.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    setattr(db_task, 'dueDate', task_data.dueDate)
    setattr(db_task, 'status', task_data.status)
    setattr(db_task, 'taskId', task_data.taskId)
    setattr(db_task, 'title', task_data.title)
    setattr(db_task, 'important', task_data.important)
    setattr(db_task, 'description', task_data.description)
    setattr(db_task, 'urgent', task_data.urgent)
    setattr(db_task, 'completionDate', task_data.completionDate)
    if task_data.tasklist is not None:
        db_tasklist = database.query(TaskList).filter(TaskList.id == task_data.tasklist).first()
        if not db_tasklist:
            raise HTTPException(status_code=400, detail="TaskList not found")
        setattr(db_task, 'tasklist_id', task_data.tasklist)
    database.commit()
    database.refresh(db_task)
    
    return db_task


@app.delete("/task/{task_id}/", response_model=None, tags=["Task"])
async def delete_task(task_id: int, database: Session = Depends(get_db)):
    db_task = database.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    database.delete(db_task)
    database.commit()
    return db_task







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



