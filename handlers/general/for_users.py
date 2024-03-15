import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from LEXICON.lexicon import LEXICON_user, LEXICON_keyboard, LEXICON
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from filters.filter import IsPrivate
from handlers.general.message_profile import profile
from keyboards.general_keyboards import questionnaire, keyboard_change_list, keyboard_new_list, keyboard_creator, \
    keyboard_user, keyboard_friend

router = Router()
router.message.filter(IsPrivate())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


@router.callback_query(F.data == LEXICON_keyboard["keyboard_start_2"][1], StateFilter(default_state))
async def for_new_user(callback: CallbackQuery):
    user = callback.from_user
    if await db_manager.get_user_by_id(user_id=user.id):
        await callback.message.edit_text(text=LEXICON_user["in_the_game"].format(name=user.first_name),
                                         reply_markup=questionnaire)
    else:
        await callback.message.edit_text(text=LEXICON_user["not_in_the_game"].format(name=user.first_name))


@router.message(F.text == LEXICON_keyboard["button"][2], StateFilter(default_state))
async def your_questionnaire(message: Message, bot: Bot):
    user = message.from_user
    data = await db_manager.get_questionnaire_by_id(user.id)
    logging.debug(f'Profile - {data}')
    if data:
        await profile(bot, data=data, id_user=user.id, text='')
    else:
        await message.answer(text=LEXICON_user["in_the_game"].format(name=user.first_name),
                             reply_markup=questionnaire)


@router.message(F.text == LEXICON_keyboard["button"][3], StateFilter(default_state))
async def gift_list(message: Message):
    data = await db_manager.get_gift_list(user_id=message.from_user.id)
    if not data:
        await message.answer(LEXICON["new_list"], reply_markup=keyboard_new_list)
    else:
        logging.debug(f'Gift_list - {[data.list]}')
        await message.answer(LEXICON["gift_list"].format(gift_list=data.list), reply_markup=keyboard_change_list)


@router.message(F.text == LEXICON["menu"], StateFilter(default_state))
async def gift_list_secret_friend(message: Message):
    if (await db_manager.get_user_by_id(user_id=message.from_user.id)).creator_id:
        await message.answer('Хоу-хоу-хоу🎅', reply_markup=keyboard_creator.as_markup(resize_keyboard=True))
    else:
        await message.answer('Хоу-хоу-хоу🎅', reply_markup=keyboard_user.as_markup(resize_keyboard=True))


@router.message(F.text == LEXICON_keyboard["button"][4], StateFilter(default_state))
async def secret_friend(message: Message):
    await message.answer(LEXICON_user["secret_friend"], reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
