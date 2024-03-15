from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from LEXICON.lexicon import LEXICON
from keyboards.general_keyboards import read


router = Router()


@router.message(Command('rules'), StateFilter(default_state))
async def start(message: Message, bot: Bot):
    await message.answer(LEXICON["rules"], reply_markup=read)
    await bot.delete_message(message.chat.id, message.message_id)


@router.callback_query(F.data == 'read', StateFilter(default_state))
async def new_creator(callback: CallbackQuery):
    await callback.message.delete()
