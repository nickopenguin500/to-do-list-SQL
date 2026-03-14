My app tracks tasks that the user inputs in the form a to-do list. I chose this because I feel like most of the commonly used to-do lists don't have enough filters.

The app uses a table named "tasks" with the following columns: 
"id" (INTEGER), "task" (TEXT), "status" (TEXT), "due_date" (TEXT), "date_completed" (TEXT), "priority" (TEXT)

How to run this app: (May be different for windows)
Open terminal and run "pip3 install flask"
Run the command "python3 todo_app.py"
Open your browser and go to "http://127.0.0.1:5001"

CRUD Operations:
Create: Users can create a new task at the top by entering a name, selecting a priority, and selecting a date
Read: All tasks are displayed in a table on the screen. There is sorting by due date, completion date, priority, and alphabetical. There is also filtering by priority and completion status
Update: Everything in the table can be updated except for the completion date. After editing the data, click the update button to save these changes to the database
Delete: Clicking the delete button for any task will delete it