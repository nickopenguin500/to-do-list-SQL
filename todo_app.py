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

# Run the setup function when the script starts
if __name__ == "__main__":
    setup_database()