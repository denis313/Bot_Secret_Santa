from aiogram.filters import BaseFilter
from aiogram.types import Message
import re

from config_data.config import DATABASE_URL
from database.requests import DatabaseManager

dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)

# delete characters in string
def keep_letters_and_spaces(input_string):
    # Используем регулярное выражение для удаления символов, кроме букв и пробелов
    cleaned_string = re.sub(r'[^a-zA-Z\s]', '', str(input_string))
    return cleaned_string


class IsPrivate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == 'private'


class IsBot(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.new_chat_members[0].is_bot


class IsAlpha(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return all([i.isalpha() for i in keep_letters_and_spaces(message.text).split()])


class IsDigit(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return all([i.isdigit() for i in message.text.split()])


class IsCreator(BaseFilter):
    async def __call__(self, message: Message):
        user = await db_manager.get_user_by_id(user_id=message.from_user.id)
        return user.creator_id


class InGame(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = await db_manager.get_user_by_id(user_id=message.from_user.id)
        return user.game_status
        # if user.game_status:
        #     return True
        # else:
        #      False
