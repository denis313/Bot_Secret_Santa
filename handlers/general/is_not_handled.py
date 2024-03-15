from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from LEXICON.lexicon import LEXICON, LEXICON_keyboard
from filters.filter import IsPrivate

router = Router()


@router.message(StateFilter(default_state), IsPrivate())
async def other_text(message: Message):
    if message.text in LEXICON_keyboard["friend_button"]:
        await message.answer('Игра еще не началась и эти кнопки не доступны')
    else:
        await message.answer(text="Я тебя не понимаю( Используй кнопки")
