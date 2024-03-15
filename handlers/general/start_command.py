from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from LEXICON.lexicon import LEXICON
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from keyboards.general_keyboards import keyboard_start, read
from filters.filter import IsPrivate


router = Router()
router.message.filter(IsPrivate())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


@router.message(CommandStart(), StateFilter(default_state))
async def start(message: Message):
    # await db_manager.create_tables()
    await message.answer(text=LEXICON["start"], reply_markup=keyboard_start)


# @router.message(Command('rules'))
# async def start(message: Message, bot: Bot):
#     await message.answer(LEXICON["rules"], reply_markup=read)
#     await bot.delete_message(message.chat.id, message.message_id)
#
#
# @router.callback_query(F.data == 'read')
# async def new_creator(callback: CallbackQuery):
#     await callback.message.delete()
