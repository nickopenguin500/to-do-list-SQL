from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date # Added to automatically get today's date

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    # Added date_completed column
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            date_completed TEXT 
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Grab both the filter and the sort choices from the URL
    filter_status = request.args.get('filter', 'All')
    sort_by = request.args.get('sort', 'due_asc')
    
    conn = get_db_connection()
    
    # We build the SQL query dynamically based on user choices
    query = "SELECT * FROM tasks"
    params = []
    
    # 1. Apply Filtering
    if filter_status in ['Pending', 'Completed']:
        query += " WHERE status = ?"
        params.append(filter_status)
        
    # 2. Apply Sorting
    if sort_by == 'alpha':
        query += " ORDER BY task ASC"
    elif sort_by == 'due_desc':
        query += " ORDER BY due_date DESC"
    elif sort_by == 'comp_asc':
        query += " ORDER BY date_completed ASC"
    elif sort_by == 'comp_desc':
        query += " ORDER BY date_completed DESC"
    else:
        query += " ORDER BY due_date ASC" # Default sorting
        
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('index.html', tasks=tasks, current_filter=filter_status, current_sort=sort_by)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    due_date = request.form['due_date']
    status = "Pending"
    date_completed = "" # Empty by default
    
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (task, status, due_date, date_completed) VALUES (?, ?, ?, ?)',
                 (task_name, status, due_date, date_completed))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    new_status = request.form['status']
    date_completed = ""
    
    # If the user marks it completed, stamp it with today's date!
    if new_status == 'Completed':
        date_completed = date.today().strftime('%Y-%m-%d')
        
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = ?, date_completed = ? WHERE id = ?', 
                 (new_status, date_completed, id))
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
    app.run(debug=True)