# import asyncio
#
# from config_data.config import DATABASE_URL
# from database.requests import DatabaseManager
#
#
# async def main_db():
#     dsn = DATABASE_URL
#     db_manager = DatabaseManager(dsn)
#
#     # Создание таблиц, если они не существуют
#     await db_manager.create_tables()
