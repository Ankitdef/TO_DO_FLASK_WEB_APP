# tests/test_api.py
import pytest
import json
import os
from app import app
from db_manager import TaskDBManager

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_manager():
    """Create database manager instance for testing"""
    test_db = 'test_tasks.db'
    manager = TaskDBManager(test_db)
    yield manager
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)

@pytest.fixture
def sample_task(db_manager):
    """Create a sample task for testing"""
    task = db_manager.create_task(
        title="Test Task",
        description="This is a test task",
        due_date="2025-12-31",
        status="pending"
    )
    yield task
    # Cleanup
    db_manager.delete_task(task['id'])

class TestCreateTaskAPI:
    """Tests for task creation API"""
    
    def test_create_task_success(self, client):
        """Test successful task creation"""
        data = {
            "title": "New Task",
            "description": "Task description",
            "due_date": "2025-12-31",
            "status": "pending"
        }
        
        response = client.post(
            '/api/tasks/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        result = json.loads(response.data)
        assert result['success'] == True
        assert result['data']['title'] == "New Task"
    
    def test_create_task_missing_title(self, client):
        """Test task creation with missing title"""
        data = {
            "description": "Task without title"
        }
        
        response = client.post(
            '/api/tasks/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        assert 'Title is required' in result['error']
    
    def test_create_task_empty_title(self, client):
        """Test task creation with empty title"""
        data = {
            "title": "   ",
            "description": "Task with empty title"
        }
        
        response = client.post(
            '/api/tasks/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
    
    def test_create_task_invalid_status(self, client):
        """Test task creation with invalid status"""
        data = {
            "title": "Task with invalid status",
            "status": "invalid_status"
        }
        
        response = client.post(
            '/api/tasks/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False
        assert 'Invalid status' in result['error']
    
    def test_create_task_no_data(self, client):
        """Test task creation with no data"""
        response = client.post(
            '/api/tasks/create/',
            data='',
            content_type='application/json'
        )
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False

class TestGetTasksAPI:
    """Tests for retrieving tasks"""
    
    def test_get_all_tasks(self, client):
        """Test retrieving all tasks"""
        response = client.get('/api/tasks/')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] == True
        assert 'count' in result
        assert isinstance(result['data'], list)
    
    def test_get_single_task_not_found(self, client):
        """Test retrieving non-existent task"""
        response = client.get('/api/tasks/99999/')
        
        assert response.status_code == 404
        result = json.loads(response.data)
        assert result['success'] == False
        assert 'not found' in result['error'].lower()

class TestUpdateTaskAPI:
    """Tests for updating tasks"""
    
    def test_update_task_title(self, client):
        """Test updating task title"""
        # First create a task
        create_data = {
            "title": "Original Title",
            "status": "pending"
        }
        create_response = client.post(
            '/api/tasks/create/',
            data=json.dumps(create_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        # Update the task
        update_data = {"title": "Updated Title"}
        response = client.put(
            f'/api/tasks/{task_id}/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] == True
        assert result['data']['title'] == "Updated Title"
    
    def test_update_task_status(self, client):
        """Test updating task status"""
        # First create a task
        create_data = {
            "title": "Task to Update",
            "status": "pending"
        }
        create_response = client.post(
            '/api/tasks/create/',
            data=json.dumps(create_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        # Update the status
        update_data = {"status": "completed"}
        response = client.put(
            f'/api/tasks/{task_id}/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] == True
        assert result['data']['status'] == "completed"
    
    def test_update_task_not_found(self, client):
        """Test updating non-existent task"""
        data = {"title": "Updated"}
        
        response = client.put(
            '/api/tasks/99999/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        result = json.loads(response.data)
        assert result['success'] == False
    
    def test_update_task_invalid_status(self, client):
        """Test updating with invalid status"""
        # First create a task
        create_data = {
            "title": "Task to Update",
            "status": "pending"
        }
        create_response = client.post(
            '/api/tasks/create/',
            data=json.dumps(create_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        # Try to update with invalid status
        update_data = {"status": "invalid"}
        response = client.put(
            f'/api/tasks/{task_id}/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] == False

class TestDeleteTaskAPI:
    """Tests for deleting tasks"""
    
    def test_delete_task_success(self, client):
        """Test successful task deletion"""
        # First create a task
        create_data = {
            "title": "Task to Delete",
            "status": "pending"
        }
        create_response = client.post(
            '/api/tasks/create/',
            data=json.dumps(create_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        # Delete the task
        response = client.delete(f'/api/tasks/{task_id}/delete/')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] == True
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}/')
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self, client):
        """Test deleting non-existent task"""
        response = client.delete('/api/tasks/99999/delete/')
        
        assert response.status_code == 404
        result = json.loads(response.data)
        assert result['success'] == False

class TestDatabaseManager:
    """Tests for database manager"""
    
    def test_create_and_retrieve_task(self, db_manager):
        """Test creating and retrieving a task"""
        task = db_manager.create_task(
            "DB Test Task",
            "Testing database",
            "2025-12-31",
            "pending"
        )
        
        assert task is not None
        assert task['title'] == "DB Test Task"
        
        # Cleanup
        db_manager.delete_task(task['id'])
    
    def test_update_task(self, db_manager):
        """Test updating a task"""
        task = db_manager.create_task("Original", "Desc", None, "pending")
        
        updated = db_manager.update_task(
            task['id'],
            title="Updated",
            status="completed"
        )
        
        assert updated['title'] == "Updated"
        assert updated['status'] == "completed"
        
        # Cleanup
        db_manager.delete_task(task['id'])
    
    def test_delete_task(self, db_manager):
        """Test deleting a task"""
        task = db_manager.create_task("To Delete", "", None, "pending")
        
        deleted = db_manager.delete_task(task['id'])
        assert deleted == True
        
        # Verify deletion
        retrieved = db_manager.get_task_by_id(task['id'])
        assert retrieved is None
    
    def test_get_all_tasks(self, db_manager):
        """Test retrieving all tasks"""
        # Create some tasks
        task1 = db_manager.create_task("Task 1", "", None, "pending")
        task2 = db_manager.create_task("Task 2", "", None, "completed")
        
        tasks = db_manager.get_all_tasks()
        assert len(tasks) >= 2
        
        # Cleanup
        db_manager.delete_task(task1['id'])
        db_manager.delete_task(task2['id'])

class TestTemplateViews:
    """Tests for template rendering views"""
    
    def test_task_list_view(self, client):
        """Test task list view renders"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'To-Do List Manager' in response.data
    
    def test_add_task_view(self, client):
        """Test add task view renders"""
        response = client.get('/add/')
        assert response.status_code == 200
        assert b'Add New Task' in response.data