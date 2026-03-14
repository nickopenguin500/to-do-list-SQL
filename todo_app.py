from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    # Added priority column
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            date_completed TEXT,
            priority TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Grab filters and sorting from the URL
    filter_status = request.args.get('filter_status', 'All')
    filter_priority = request.args.get('filter_priority', 'All')
    sort_by = request.args.get('sort', 'due_asc')
    
    conn = get_db_connection()
    
    # Base query
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    # 1. Apply Status Filter
    if filter_status in ['Pending', 'Completed']:
        query += " AND status = ?"
        params.append(filter_status)
        
    # 2. Apply Priority Filter
    if filter_priority in ['High', 'Medium', 'Low']:
        query += " AND priority = ?"
        params.append(filter_priority)
        
    # 3. Apply Sorting (including the custom CASE statement for priority)
    if sort_by == 'alpha':
        query += " ORDER BY task ASC"
    elif sort_by == 'due_desc':
        query += " ORDER BY due_date DESC"
    elif sort_by == 'comp_asc':
        query += " ORDER BY date_completed ASC"
    elif sort_by == 'comp_desc':
        query += " ORDER BY date_completed DESC"
    elif sort_by == 'pri_high_low':
        query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 ELSE 4 END ASC"
    elif sort_by == 'pri_low_high':
        query += " ORDER BY CASE priority WHEN 'Low' THEN 1 WHEN 'Medium' THEN 2 WHEN 'High' THEN 3 ELSE 4 END ASC"
    else:
        query += " ORDER BY due_date ASC" 
        
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('index.html', tasks=tasks, current_status=filter_status, current_priority=filter_priority, current_sort=sort_by)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    due_date = request.form['due_date']
    priority = request.form['priority']
    status = "Pending"
    date_completed = "" 
    
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (task, status, due_date, date_completed, priority) VALUES (?, ?, ?, ?, ?)',
                 (task_name, status, due_date, date_completed, priority))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    new_task_name = request.form['task_name']
    new_due_date = request.form['due_date']
    new_status = request.form['status']
    new_priority = request.form['priority']
    date_completed = ""
    
    if new_status == 'Completed':
        date_completed = date.today().strftime('%Y-%m-%d')
        
    conn = get_db_connection()
    conn.execute('''
        UPDATE tasks 
        SET task = ?, status = ?, due_date = ?, date_completed = ?, priority = ? 
        WHERE id = ?
    ''', (new_task_name, new_status, new_due_date, date_completed, new_priority, id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)