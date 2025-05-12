###task routes using fast api

from fastapi import APIRouter, HTTPException
import schemas
from Task_Manager_.src.db.task_queries import TaskQueries
from Task_Manager_.src.db.connection import DataBase

route = APIRouter(prefix = "/v1/taskmanager")

@route.get('/{user_name}')
def list_tasks(user_name: str):
    db = DataBase()
    tasks = TaskQueries(db.conn, db.cur)
    try:
        data = tasks.list_tasks(user_name)
        if not data:
            raise HTTPException(status_code=404, detail="No task found.")
        db.close_database()
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        db.close_database()