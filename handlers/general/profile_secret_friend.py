from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from LEXICON.lexicon import LEXICON_keyboard, LEXICON_user, LEXICON
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from filters.filter import IsPrivate, InGame
from handlers.general.message_profile import profile
from keyboards.callback_data_classes import CallbackFactory
from keyboards.general_keyboards import keyboard_friend, keyboard_user, keyboard_creator, keyboard_list

# from services.parsing import read_json

router = Router()
router.message.filter(IsPrivate(), InGame())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


@router.message(F.text == LEXICON_keyboard["friend_button"][0], StateFilter(default_state))
async def profile_secret_friend(message: Message, bot: Bot):
    id_user = message.from_user.id
    id_friend = await db_manager.get_user_by_id(user_id=id_user)
    data = await db_manager.get_questionnaire_by_id(id_friend.id_secret_friend)
    await profile(bot, data=data, id_user=id_user, text='', keyboard=None)


@router.message(F.text == LEXICON_keyboard["friend_button"][1], StateFilter(default_state))
async def gift_list_secret_friend(message: Message):
    id_user = message.from_user.id
    id_friend = await db_manager.get_user_by_id(user_id=id_user)
    data = await db_manager.get_gift_list(user_id=id_friend.id_secret_friend)
    if data.list == "СЮРПРИЗ":
        await message.answer(LEXICON["surprise"].format(gift_list=data.list))
    else:
        await message.answer(LEXICON_keyboard["gift_list_friend"].format(gift_list=data.list))


@router.message(F.text == LEXICON_keyboard["friend_button"][2], StateFilter(default_state))
async def generate_gift_list(message: Message):
    id_user = message.from_user.id
    id_friend = await db_manager.get_user_by_id(user_id=id_user)
    data = await db_manager.get_gift_list(user_id=id_friend.id_secret_friend)
    if data.list == "СЮРПРИЗ":
        await message.answer(LEXICON["surprise"].format(gift_list=data.list))
    else:
        await message.reply(LEXICON["gifts"], reply_markup=keyboard_list(user_id=id_friend.id_secret_friend,
                                                                         gifts=data.list))


@router.callback_query(CallbackFactory.filter())
async def gift_details(callback: CallbackQuery, callback_data: CallbackFactory):
    id_user = callback_data.user_id
    gifts = await db_manager.get_generate_gift(user_id=id_user, name_gift=callback_data.gift)
    for gift in gifts:
        await callback.message.reply(text=f"Подробности о подарке {gift.name}:\n"
                                     f"{gift.status} вариант: \n" +
                                     LEXICON["general_list"].format(id=gift.id_gift,
                                                                    brand=gift.brand,
                                                                    name=gift.name,
                                                                    price=gift.price,
                                                                    supplierRating=gift.supplierRating,
                                                                    feedbacks=gift.feedbacks))
