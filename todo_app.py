import sqlite3

def setup_database():
    # Connect to a database file (this creates the file if it doesn't exist)
    con = sqlite3.connect('todo.db')
    cur = con.cursor()

    # Create the 'tasks' table if it isn't already there
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT
        )
    ''')
    
    # Save the changes and close the connection for now
    con.commit()
    con.close()
    print("Database setup complete! 'todo.db' is ready.")

def add_task():
    # Get input from the user
    task_name = input("Enter the task description: ")
    due_date = input("Enter the due date (YYYY-MM-DD) or leave blank: ")
    
    # We default the status to 'Pending' for all new tasks
    status = "Pending"
    
    # Connect to the database
    con = sqlite3.connect('todo.db')
    cur = con.cursor()
    
    # Use parameterized queries (?) to safely insert the data
    cur.execute('''
        INSERT INTO tasks (task, status, due_date)
        VALUES (?, ?, ?)
    ''', (task_name, status, due_date))
    
    # Save the changes and close the connection
    con.commit()
    con.close()
    
    print(f"\nSuccess! '{task_name}' has been added to your to-do list.")

if __name__ == "__main__":
    # setup_database()  <-- You can comment this out now since the DB is already made
    add_task()