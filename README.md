# To-Do List Manager - Flask Application

A comprehensive web application for managing tasks with RESTful APIs, custom SQL queries (no ORM), and responsive templates built with Flask.

## Features

- ✅ Full CRUD operations for tasks
- 🎨 Beautiful, responsive web interface
- 🔌 RESTful API endpoints
- 📊 Task statistics and filtering
- 🗄️ Raw SQL queries (no ORM/SQLAlchemy)
- 📝 Comprehensive logging
- ⚠️ Exception handling
- ✨ Interactive UI with JavaScript
- 🧪 Complete test suite with pytest

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite3 with raw SQL queries
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Testing**: pytest with pytest-flask
- **Architecture**: Function-based views

## Project Structure

```
todo-flask-app/
├── app.py                 # Main Flask application
├── db_manager.py          # Database operations with raw SQL
├── templates/
│   ├── base.html          # Base template
│   ├── task_list.html     # Task list view
│   ├── add_task.html      # Add task form
│   └── error.html         # Error page
├── tests/
│   └── test_api.py        # Test suite
├── logs/
│   └── app.log            # Application logs
├── tasks.db               # SQLite database
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd todo-flask-app
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`

The database and logs directory are created automatically on first run.

## API Documentation

### Base URL
```
http://127.0.0.1:5000/api/
```

### Endpoints

#### 1. Create Task
- **URL**: `/api/tasks/create/`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
    "title": "Complete project documentation",
    "description": "Write comprehensive README",
    "due_date": "2025-12-31",
    "status": "pending"
}
```
- **Response** (201 Created):
```json
{
    "success": true,
    "message": "Task created successfully",
    "data": {
        "id": 1,
        "title": "Complete project documentation",
        "description": "Write comprehensive README",
        "due_date": "2025-12-31",
        "status": "pending",
        "created_at": "2025-12-30 10:30:00",
        "updated_at": "2025-12-30 10:30:00"
    }
}
```

#### 2. Get All Tasks
- **URL**: `/api/tasks/`
- **Method**: `GET`
- **Response** (200 OK):
```json
{
    "success": true,
    "count": 2,
    "data": [
        {
            "id": 1,
            "title": "Task 1",
            "description": "Description",
            "due_date": "2025-12-31",
            "status": "pending",
            "created_at": "2025-12-30 10:30:00",
            "updated_at": "2025-12-30 10:30:00"
        }
    ]
}
```

#### 3. Get Single Task
- **URL**: `/api/tasks/{task_id}/`
- **Method**: `GET`
- **Response** (200 OK):
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Task 1",
        "description": "Description",
        "due_date": "2025-12-31",
        "status": "pending",
        "created_at": "2025-12-30 10:30:00",
        "updated_at": "2025-12-30 10:30:00"
    }
}
```

#### 4. Update Task
- **URL**: `/api/tasks/{task_id}/update/`
- **Method**: `PUT` or `PATCH`
- **Content-Type**: `application/json`
- **Request Body** (all fields optional):
```json
{
    "title": "Updated title",
    "description": "Updated description",
    "due_date": "2026-01-15",
    "status": "completed"
}
```
- **Response** (200 OK):
```json
{
    "success": true,
    "message": "Task updated successfully",
    "data": {
        "id": 1,
        "title": "Updated title",
        "status": "completed",
        ...
    }
}
```

#### 5. Delete Task
- **URL**: `/api/tasks/{task_id}/delete/`
- **Method**: `DELETE`
- **Response** (200 OK):
```json
{
    "success": true,
    "message": "Task deleted successfully"
}
```

### Status Values
Valid status values for tasks:
- `pending`
- `in_progress`
- `completed`

### Error Responses

#### 400 Bad Request
```json
{
    "success": false,
    "error": "Title is required"
}
```

#### 404 Not Found
```json
{
    "success": false,
    "error": "Task not found"
}
```

#### 500 Internal Server Error
```json
{
    "success": false,
    "error": "Internal server error"
}
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Class

```bash
pytest tests/test_api.py::TestCreateTaskAPI -v
```

### Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### View Coverage Report

After running with coverage, open `htmlcov/index.html` in your browser.

### Test Coverage

The test suite includes:
- ✅ API endpoint testing (create, read, update, delete)
- ✅ Validation testing
- ✅ Error handling testing
- ✅ Database operations testing
- ✅ Template rendering tests
- ✅ Edge cases and boundary conditions

## Logging

Logs are stored in `logs/app.log` and include:
- INFO level: Successful operations
- WARNING level: Potential issues
- ERROR level: Errors and exceptions

Log entries include timestamp, module name, and message:
```
INFO 2025-12-30 10:30:00 db_manager: Task created successfully with ID: 1
```

The logging system uses a rotating file handler with a maximum file size of 10MB and keeps up to 10 backup files.

## Exception Handling

The application implements comprehensive exception handling:
- Database connection errors
- JSON parsing errors
- Validation errors
- HTTP method errors
- Network errors
- 404 and 500 error handlers

All exceptions are logged and return appropriate HTTP status codes with user-friendly error messages.

## Web Interface

### Pages

1. **Task List** (`/`)
   - View all tasks in a grid layout
   - Filter tasks by status (All, Pending, In Progress, Completed)
   - Real-time task statistics dashboard
   - Update task status with one click
   - Delete tasks with confirmation
   - Responsive design for mobile and desktop

2. **Add Task** (`/add/`)
   - Create new tasks with a user-friendly form
   - Client-side and server-side validation
   - Date picker for due dates (prevents past dates)
   - Status selection dropdown
   - Success/error message display

### Features

- **Real-time Updates**: All operations update the UI without page reload
- **Confirmation Dialogs**: Delete operations require confirmation
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on desktop, tablet, and mobile

## Database Schema

### Tasks Table

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Fields Description

- `id`: Auto-incrementing primary key
- `title`: Task title (required)
- `description`: Detailed task description (optional)
- `due_date`: Task deadline (optional)
- `status`: Current status (pending/in_progress/completed)
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last updated

## Key Implementation Details

### No ORM Usage
- All database operations use raw SQL queries
- Custom `TaskDBManager` class handles all database interactions
- Direct SQLite3 connections using the `sqlite3` module
- No SQLAlchemy or other ORM frameworks

### Raw SQL Query Examples

```python
# Create
cursor.execute('''
    INSERT INTO tasks (title, description, due_date, status)
    VALUES (?, ?, ?, ?)
''', (title, description, due_date, status))

# Read All
cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')

# Read One
cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))

# Update
cursor.execute('''
    UPDATE tasks 
    SET title = ?, status = ?, updated_at = CURRENT_TIMESTAMP 
    WHERE id = ?
''', (title, status, task_id))

# Delete
cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
```

### Function-Based Views
- No Flask-RESTful or other extensions
- Custom route decorators for HTTP methods
- Manual JSON parsing and response creation
- Explicit error handling in each view

## API Testing Examples

### Using cURL

```bash
# Create a task
curl -X POST http://127.0.0.1:5000/api/tasks/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","status":"pending"}'

# Get all tasks
curl http://127.0.0.1:5000/api/tasks/

# Get single task
curl http://127.0.0.1:5000/api/tasks/1/

# Update task
curl -X PUT http://127.0.0.1:5000/api/tasks/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Delete task
curl -X DELETE http://127.0.0.1:5000/api/tasks/1/delete/
```

### Using Python requests

```python
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# Create task
response = requests.post(
    f"{BASE_URL}/tasks/create/",
    json={
        "title": "New Task",
        "description": "Task description",
        "status": "pending"
    }
)
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks/")
print(response.json())

# Update task
response = requests.put(
    f"{BASE_URL}/tasks/1/update/",
    json={"status": "completed"}
)
print(response.json())

# Delete task
response = requests.delete(f"{BASE_URL}/tasks/1/delete/")
print(response.json())
```

### Using JavaScript (from browser console)

```javascript
// Create task
fetch('http://127.0.0.1:5000/api/tasks/create/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        title: 'New Task',
        status: 'pending'
    })
})
.then(r => r.json())
.then(data => console.log(data));

// Get all tasks
fetch('http://127.0.0.1:5000/api/tasks/')
    .then(r => r.json())
    .then(data => console.log(data));
```

## Development Notes

### Application Structure

- **app.py**: Main Flask application with all route handlers
- **db_manager.py**: Database operations layer (raw SQL only)
- **templates/**: Jinja2 templates for web interface
- **tests/**: Comprehensive test suite

### Configuration

- Debug mode is enabled by default (set `debug=False` in production)
- Server runs on `0.0.0.0:5000` (accessible from network)
- Logging level set to INFO
- Rotating file handler with 10MB max file size

### Best Practices Implemented

1. **Separation of Concerns**: Database logic separated from route handlers
2. **Error Handling**: Try-except blocks in all database operations
3. **Logging**: Comprehensive logging at all levels
4. **Validation**: Input validation for all user data
5. **Consistent API**: Uniform response format for all endpoints
6. **Testing**: High test coverage with pytest
7. **Documentation**: Detailed inline comments and docstrings

## Troubleshooting

### Issue: Database locked
**Solution**: Ensure no other process is accessing the database. The application creates a new connection for each operation and closes it properly.

### Issue: Module not found
**Solution**: Activate virtual environment and reinstall requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution**: Change the port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Tests failing
**Solution**: Make sure you're in the project root directory and the virtual environment is activated:
```bash
cd /path/to/project
source venv/bin/activate
pytest tests/ -v
```

## Production Deployment

For production deployment:

1. **Disable Debug Mode**:
```python
app.run(debug=False)
```

2. **Use Production WSGI Server** (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Set Environment Variables**:
```bash
export FLASK_ENV=production
export SECRET_KEY='your-secure-secret-key'
```

4. **Use PostgreSQL** (instead of SQLite for better concurrency):
- Modify `db_manager.py` to use PostgreSQL connection
- Update connection string in configuration

5. **Configure Reverse Proxy** (Nginx):
```nginx
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Future Enhancements

- [ ] User authentication and authorization (Flask-Login)
- [ ] Task categories and tags
- [ ] Search and advanced filtering
- [ ] Pagination for large datasets
- [ ] Export tasks (CSV, JSON, PDF)
- [ ] Email reminders for due tasks
- [ ] API rate limiting
- [ ] Swagger/OpenAPI documentation
- [ ] WebSocket for real-time updates
- [ ] Task sharing and collaboration

## Contributors

- Your Name

## License

MIT License

## Support

For issues or questions, please create an issue in the GitHub repository.

---

 47f553fa22c37b46f6c4314198e7327aa4232299
