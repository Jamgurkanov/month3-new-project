 # C-R-U-D
# C - Create, R - Read, U - Update, D - Delete

CREATE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
"""

INSERT_TASKS = 'INSERT INTO tasks (task) VALUES (?)'

SELECT_TASKS = "SELECT id, task FROM tasks"

UPDATE_TASKS = "UPDATE tasks SET task = ? WHERE id = ?"

DELETE_TASKS = 'DELETE FROM tasks WHERE id = ?'

