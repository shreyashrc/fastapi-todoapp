import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.task import Task

client = TestClient(app)

# Mocking the database session
@pytest.fixture
def db_session(monkeypatch): #monkeypatch is a fixture provided by the pytest testing framework
    monkeypatch.setattr("app.db.session", lambda: None)
    yield

# Mocking the Task model
@pytest.fixture
def task_model(monkeypatch):
    monkeypatch.setattr("app.models.task.Task", lambda task: task)
    yield Task

# Test Create Endpoint
def test_create_task(db_session, task_model):
    task_data = {"task": "New Task"}
    
    response = client.post("/tasks/", json=task_data)
    
    assert response.status_code == 200
    assert response.json()["task"] == task_data["task"]

# Test Read Endpoint
def test_read_tasks(db_session, task_model):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test Update Endpoint
# def test_update_task(db_session, task_model):
#     new_task = task_model(task="Task for updating")
    
#     response = client.put(f"/tasks/{new_task.id}", json={"task": "Updated Task"})
    
#     assert response.status_code == 200
#     assert response.json()["task"] == "Updated Task"

# # # Test Delete Endpoint
# def test_delete_task(db_session, task_model):
#     new_task = task_model(task="Task for deletion")
    
#     response = client.delete(f"/tasks/{new_task.id}")
    
#     assert response.status_code == 204

# Test Invalid Task ID
def test_invalid_task_id(db_session, task_model):
    response = client.get("/tasks/999999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
