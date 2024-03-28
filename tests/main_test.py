from fastapi.testclient import TestClient
from main import app
from app.models.task import Task
from app.db.session import SessionLocal

client = TestClient(app)

# ------------------ test for create task

# mocking db, conftest.py --> fixtures
    
def test_create_task():

    task_data = {"task": "New Task"}

    response = client.post("/tasks/", json=task_data)

    assert response.status_code == 200
    assert response.json()["task"] == task_data["task"]

    db = SessionLocal()
    created_task = db.query(Task).filter(Task.task == task_data["task"]).first()
    db.delete(created_task)
    db.commit()
    db.close()

# ------------------  test read task

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ------------------  test for update
    
# def test_update_task():
#     new_task = Task(task="Task for updating")
#     db = SessionLocal()
#     db.add(new_task)
#     db.commit()
#     db.close()

#     updated_task_data = {"task": "Updated Task"}

#     response = client.put(f"/tasks/{new_task.id}", json=updated_task_data)

#     assert response.status_code == 200
#     assert response.json()["task"] == updated_task_data["task"]

#     db = SessionLocal()
#     updated_task = db.query(Task).filter(Task.id == new_task.id).first()
#     db.delete(updated_task)
#     db.commit()
#     db.close()


# ------------------ test for  delete
    
# def test_delete_task():
#     new_task = Task(task="Task for deletion")
#     db = SessionLocal()
#     db.add(new_task)
#     db.commit()
#     db.close()

#     response = client.delete(f"/tasks/{new_task.id}")

#     assert response.status_code == 204

#     db = SessionLocal()
#     deleted_task = db.query(Task).filter(Task.id == new_task.id).first()
#     assert deleted_task is None
#     db.close()
    
#  ------------------  Error/Invalid test
    
def test_invalid_task_id():

    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
