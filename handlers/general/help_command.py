from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from LEXICON.lexicon import LEXICON

router = Router()


@router.message(Command('help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['help'])
