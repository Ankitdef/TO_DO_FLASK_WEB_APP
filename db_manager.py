
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskDBManager:
    """Database manager for tasks using raw SQL queries"""
    
    def __init__(self, db_path='tasks.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
    
    def init_db(self):
        """Initialize database and create tasks table"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date DATE,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise
    
    def create_task(self, title, description, due_date, status='pending'):
        """Create a new task"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO tasks (title, description, due_date, status)
                VALUES (?, ?, ?, ?)
            ''', (title, description, due_date, status))
            
            task_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Task created successfully with ID: {task_id}")
            return self.get_task_by_id(task_id)
        except sqlite3.Error as e:
            logger.error(f"Error creating task: {str(e)}")
            raise
    
    def get_all_tasks(self):
        """Retrieve all tasks"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            tasks = [dict(row) for row in rows]
            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
        except sqlite3.Error as e:
            logger.error(f"Error retrieving tasks: {str(e)}")
            raise
    
    def get_task_by_id(self, task_id):
        """Retrieve a task by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.info(f"Task retrieved with ID: {task_id}")
                return dict(row)
            else:
                logger.warning(f"Task not found with ID: {task_id}")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving task: {str(e)}")
            raise
    
    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        """Update a task"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            params = []
            
            if title is not None:
                update_fields.append("title = ?")
                params.append(title)
            if description is not None:
                update_fields.append("description = ?")
                params.append(description)
            if due_date is not None:
                update_fields.append("due_date = ?")
                params.append(due_date)
            if status is not None:
                update_fields.append("status = ?")
                params.append(status)
            
            if not update_fields:
                conn.close()
                logger.warning("No fields to update")
                return self.get_task_by_id(task_id)
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            params.append(task_id)
            
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount == 0:
                conn.close()
                logger.warning(f"No task found to update with ID: {task_id}")
                return None
            
            conn.close()
            logger.info(f"Task updated successfully with ID: {task_id}")
            return self.get_task_by_id(task_id)
        except sqlite3.Error as e:
            logger.error(f"Error updating task: {str(e)}")
            raise
    
    def delete_task(self, task_id):
        """Delete a task"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            
            deleted = cursor.rowcount > 0
            conn.close()
            
            if deleted:
                logger.info(f"Task deleted successfully with ID: {task_id}")
            else:
                logger.warning(f"No task found to delete with ID: {task_id}")
            
            return deleted
        except sqlite3.Error as e:
            logger.error(f"Error deleting task: {str(e)}")
            raise
    
    def close(self):
        """Close database connection (cleanup method)"""
        logger.info("Database manager cleanup completed")