import logging

from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, CallbackQuery

from LEXICON.lexicon import LEXICON_Creator, LEXICON_keyboard, LEXICON_FSM
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from filters.filter import IsPrivate, IsCreator
from handlers.general.message_profile import profile
from keyboards.general_keyboards import keyboard_stock, keyboard_change_stock
from services.services import random_assignment

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(IsPrivate(), IsCreator())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


@router.message(F.text == LEXICON_keyboard["button"][1])
async def start_the_game(message: Message, bot: Bot):
    user = await db_manager.get_user_by_id(user_id=message.from_user.id)
    all_users = await db_manager.get_all_users(id_chat=user.chat_id)
    if len(all_users) > 1:
        if all_users[0][4] == 1:
            await message.answer(LEXICON_Creator["already_game"])
        else:
            logger.debug('Debug Information - STARTING THE GAME')
            for your_id, friend_id in random_assignment(all_users):
                user_data = await db_manager.get_questionnaire_by_id(user_id=friend_id)
                await db_manager.update_user(user_id=your_id,
                                             user_data={"id_secret_friend": friend_id, "game_status": 1})
                if user_data:
                    await bot.send_message(chat_id=your_id, text=LEXICON_Creator["start_game"])
                    await profile(bot, data=user_data, id_user=your_id, text='', keyboard=None)
    else:
        await message.answer(LEXICON_Creator["few_players"])


@router.message(F.text == LEXICON_keyboard["button"][0])
async def stop_the_game(message: Message, bot: Bot):
    data = {"game_status": None, "id_secret_friend": None}
    user = await db_manager.get_user_by_id(user_id=message.from_user.id)
    if user.game_status == 1:
        await db_manager.update_user(chat_id=user.chat_id, user_data=data)
        await bot.send_message(chat_id=user.chat_id, text=LEXICON_Creator["stop_game"])
    else:
        await message.answer('Игра еще не началась')


@router.message(F.text == LEXICON_keyboard["button"][5])
async def buying_places_play(message: Message):
    print(message.from_user.id)


@router.message(F.text == LEXICON_keyboard["button"][6])
async def stock_gifts(message: Message):
    await message.answer(LEXICON_Creator["stock"], reply_markup=keyboard_stock.as_markup())


@router.callback_query(F.data == LEXICON_keyboard["stock"]["Бюджет игроков"], StateFilter(default_state))
async def for_new_user(callback: CallbackQuery):
    user = callback.from_user
    i = await db_manager.get_user_by_id(user_id=user.id)
    users = await db_manager.get_all_users(id_chat=i.chat_id)
    for user in users:
        questionnaire = await db_manager.get_questionnaire_by_id(user_id=user[1])
        await callback.message.answer(f'{questionnaire.name} бюджет: {questionnaire.stock}')


@router.callback_query(F.data == LEXICON_keyboard["stock"]["Подсчитать бюджет"], StateFilter(default_state))
async def all_stock(callback: CallbackQuery):
    user = callback.from_user
    stock = 0
    i = await db_manager.get_user_by_id(user_id=user.id)
    users = await db_manager.get_all_users(id_chat=i.chat_id)
    print(users)
    for user in users:
        stocks = await db_manager.get_questionnaire_by_id(user_id=user[1])
        if stocks:
            stock += stocks.stock
    await callback.message.answer(f'Средний бюджет: {stock / len(users)}')


@router.callback_query(F.data == LEXICON_keyboard["stock"]["Обсудить в Группе"], StateFilter(default_state))
async def for_new_user(callback: CallbackQuery, bot: Bot):
    user = callback.from_user
    data = await db_manager.get_user_by_id(user_id=user.id)
    await callback.message.answer(text=LEXICON_Creator["stock_answer"],  reply_markup=keyboard_change_stock)
    await bot.send_message(chat_id=data.chat_id, text=LEXICON_Creator['stock_chat'])


class Stock(StatesGroup):
    stock = State()


@router.callback_query(F.data == LEXICON_keyboard['Бюджет'], StateFilter(default_state))
async def change_stock(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Stock.stock)
    await callback.message.answer('Введите бюджет на подарки')


@router.message(StateFilter(Stock.stock), F.text.isdigit())
async def stock(message: Message, state: FSMContext):
    await state.update_data(stock=int(message.text))
    data = await state.get_data()
    await state.clear()
    i = await db_manager.get_user_by_id(user_id=message.from_user.id)
    users = await db_manager.get_all_users(id_chat=i.chat_id)
    for user in users:
        await db_manager.update_questionnaire(user_id=user[1], questionnaire_data=data)
    await message.answer('Успешно сохранено✅')


@router.message(StateFilter(Stock.stock))
async def add_not_trips(message: Message):
    await message.answer(LEXICON_FSM["stock"][1])
