import aiosqlite

database_path = "data/bot_tasks.db"  # Path to db file

init_db_tasks_sql_script = """
CREATE TABLE IF NOT EXISTS bot_tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
description TEXT,
priority INTEGER,
status INTEGER,
deadline TEXT,
user_id INTEGER,
created_at TEXT DEFAULT CURRENT_TIMESTAMP,
updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""


async def init_tasks_database() -> bool:  # Init database
    async with aiosqlite.connect(database_path) as db:
        try:
            await db.execute(init_db_tasks_sql_script)
            await db.execute("CREATE INDEX IF NOT EXISTS idx_bot_tasks_user_id ON bot_tasks(user_id)")  # Execute script
            await db.commit()  # Save
            return True
        except aiosqlite.Error as e:
            print(f"database init error: {e}")
            return False


async def create_task(task: list) -> bool:  # Create task func
    async with aiosqlite.connect(database_path) as db:
        try:
            await db.execute(
                "INSERT INTO bot_tasks (title, description, priority, status, deadline, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                task)  # Exec script
            await db.commit()  # Save
            return True
        except aiosqlite.Error as e:
            print(f"create task error: {e}")
            return False


async def get_tasks_for_user(user_id):  # Tasks users func
    async with aiosqlite.connect(database_path) as db:
        try:
            async with db.execute("SELECT * FROM bot_tasks WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchall()
                return result
        except aiosqlite.Error as e:
            print(f"get tasks error: {e}")
            return 0
