from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from LEXICON.lexicon import LEXICON_Creator, LEXICON_keyboard
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from filters.filter import IsPrivate, IsBot
from keyboards.general_keyboards import keyboard_creator

router = Router()
router.message.filter(~IsPrivate())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn)


@router.callback_query(F.data == LEXICON_keyboard["keyboard_start_1"][1])
async def new_creator(callback: CallbackQuery):
    # id_creator = callback.from_user.id
    await callback.message.edit_text(text=LEXICON_Creator["creator_start"])


# регистрируем администратора  __tableuser__
@router.message(F.content_type == 'new_chat_members', IsBot())
async def new_chat(message: Message, bot: Bot):
    chat_members = await bot.get_chat_administrators(message.chat.id)
    id_chat = message.chat.id
    for admin in chat_members:
        if admin.status == "creator":
            # добавляем user_id, id_chat, creator_id в __tableuser__
            user_data = {"user_id": admin.user.id, "chat_id": id_chat, "creator_id": admin.user.id}
            keyboard = keyboard_creator.as_markup(resize_keyboard=True)
            if not await db_manager.get_user_by_id(user_id=admin.user.id):
                await db_manager.add_user(user_data)
                await bot.send_message(admin.user.id, LEXICON_Creator["new_chat"],
                                       reply_markup=keyboard)
                break
            else:
                await bot.send_message(admin.user.id, text=LEXICON_Creator["chat_already_created"],
                                       reply_markup=keyboard)
