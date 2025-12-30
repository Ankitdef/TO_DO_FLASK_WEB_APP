from flask import Flask, render_template, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os
from db_manager import TaskDBManager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database manager
db_manager = TaskDBManager()

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(levelname)s %(asctime)s %(module)s: %(message)s'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('To-Do List application startup')

# ==================== API ROUTES ====================

@app.route('/api/tasks/create/', methods=['POST'])
def create_task_api():
    """API endpoint to create a new task"""
    try:
        data = request.get_json()
        
        if not data:
            app.logger.warning("No JSON data provided")
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        if 'title' not in data or not data['title'].strip():
            app.logger.warning("Task creation failed: Missing title")
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        title = data['title']
        description = data.get('description', '')
        due_date = data.get('due_date', None)
        status = data.get('status', 'pending')
        
        # Validate status
        valid_statuses = ['pending', 'in_progress', 'completed']
        if status not in valid_statuses:
            app.logger.warning(f"Invalid status provided: {status}")
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400
        
        task = db_manager.create_task(title, description, due_date, status)
        
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': task
        }), 201
        
    except Exception as e:
        app.logger.error(f"Error creating task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/tasks/', methods=['GET'])
def get_tasks_api():
    """API endpoint to retrieve all tasks"""
    try:
        tasks = db_manager.get_all_tasks()
        
        return jsonify({
            'success': True,
            'count': len(tasks),
            'data': tasks
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error retrieving tasks: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/tasks/<int:task_id>/', methods=['GET'])
def get_task_api(task_id):
    """API endpoint to retrieve a single task"""
    try:
        task = db_manager.get_task_by_id(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': task
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error retrieving task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/tasks/<int:task_id>/update/', methods=['PUT', 'PATCH'])
def update_task_api(task_id):
    """API endpoint to update a task"""
    try:
        data = request.get_json()
        
        if not data:
            app.logger.warning("No JSON data provided")
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')
        status = data.get('status')
        
        # Validate status if provided
        if status:
            valid_statuses = ['pending', 'in_progress', 'completed']
            if status not in valid_statuses:
                app.logger.warning(f"Invalid status provided: {status}")
                return jsonify({
                    'success': False,
                    'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }), 400
        
        task = db_manager.update_task(task_id, title, description, due_date, status)
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': task
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error updating task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/tasks/<int:task_id>/delete/', methods=['DELETE'])
def delete_task_api(task_id):
    """API endpoint to delete a task"""
    try:
        deleted = db_manager.delete_task(task_id)
        
        if not deleted:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error deleting task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


# ==================== TEMPLATE ROUTES ====================

@app.route('/')
def task_list_view():
    """View to display list of tasks"""
    try:
        tasks = db_manager.get_all_tasks()
        return render_template('task_list.html', tasks=tasks)
    except Exception as e:
        app.logger.error(f"Error in task list view: {str(e)}")
        return render_template('error.html', error='Unable to load tasks'), 500


@app.route('/add/')
def add_task_view():
    """View to display add task form"""
    return render_template('add_task.html')


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)