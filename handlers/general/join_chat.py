from aiogram import Router, F, Bot
from aiogram.types import Message

from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from filters.filter import IsPrivate, IsBot
from LEXICON.lexicon import LEXICON_user, LEXICON_Creator

router = Router()
router.message.filter(~IsPrivate())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


# добавление user в базу
@router.message(F.content_type == 'new_chat_members', ~IsBot())
async def on_user_joined(message: Message, bot: Bot):
    new_user = message.new_chat_members[0]
    new_user_db = {'user_id': new_user.id, 'chat_id': message.chat.id, "subscription": 'zero'}
    users = await db_manager.get_all_users(id_chat=new_user_db["chat_id"])
    if len(users) >= 15:
        await bot.send_message(chat_id=users[0][1], text=LEXICON_Creator["many_players"])
    else:
        await db_manager.add_user(new_user_db)

        if new_user.username:
            await message.answer(LEXICON_user["user_start"].format(name=f'@{new_user.username}'))
        else:
            await message.answer(LEXICON_user["user_start"].format(name=new_user.first_name))


# удаляем юзера
@router.message(F.content_type == 'left_chat_member')
async def on_user_joined(message: Message, bot: Bot):
    # print(message.left_chat_member.id)
    user = message.left_chat_member.id
    if user != 6704403824:
        await db_manager.delete_user(user_id=user)
        await bot.send_message(chat_id=user, text=LEXICON_Creator["delete"])
