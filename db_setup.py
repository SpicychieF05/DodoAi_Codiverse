import aiosqlite
import asyncio

async def init_db():
    async with aiosqlite.connect('api_stats.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT,
                success INTEGER,
                session_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                response_time REAL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                chat_id TEXT PRIMARY KEY,
                last_provider TEXT,
                switch_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                last_used DATETIME
            )
        ''')
        await db.commit()
        print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
