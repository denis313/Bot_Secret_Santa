import logging
from aiogram import F, Bot, Router
from aiogram.fsm.state import StatesGroup, State

from config_data.config import DATABASE_URL
from database.requests import DatabaseManager

router = Router()
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


class Stock(StatesGroup):
    stock = State()


@router.callback_query(and_f(or_f(F.data == LEXICON_keyboard["questionnaire"][1],
                                  F.data == LEXICON_keyboard["change_b"][1]), StateFilter(default_state)))
async def add_questionnaire(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await state.set_state(Questionnaire.name)
    await callback.message.answer(text=LEXICON_FSM["name"][0])


@router.message(StateFilter(Questionnaire.name))
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Questionnaire.sex)
    await message.answer(text=LEXICON_FSM["sex"][0], reply_markup=sex)