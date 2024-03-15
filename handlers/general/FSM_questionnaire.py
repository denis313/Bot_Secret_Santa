import logging

from aiogram import F, Bot, Router
from aiogram.filters import StateFilter, and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, UserProfilePhotos

from LEXICON.lexicon import LEXICON_FSM, LEXICON_keyboard, LEXICON
from config_data.config import DATABASE_URL
from database.requests import DatabaseManager
from filters.filter import IsAlpha
from handlers.general.message_profile import profile
from keyboards.general_keyboards import sex, sizes, keyboard_start, keyboard_creator, keyboard_user
from services.parsing import gift_list_generation

router = Router()
router.message.filter(IsAlpha())
dsn = DATABASE_URL
db_manager = DatabaseManager(dsn=dsn)


class Questionnaire(StatesGroup):
    name = State()  # user name
    sex = State()  # user sex
    clothing_brand = State()  # favorite clothing brand
    color_palette = State()  # favorite color palette
    sizes = State()  # user sizes
    fashion_style = State()  # favorite fashion style
    hobby = State()  # user hobby
    allergy = State()  # user allergy
    salty_or_sweet = State()  # favorite food
    dream = State()  # dream
    stock = State()


@router.message(F.text == LEXICON_keyboard["stop"], ~StateFilter(default_state))
async def process_gender_press(message: Message, state: FSMContext):
    await message.answer(LEXICON_keyboard["stop"], reply_markup=keyboard_start)
    await state.clear()


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


@router.message(StateFilter(Questionnaire.name))
async def add_not_name(message: Message):
    await message.answer(LEXICON_FSM["name"][1])


@router.message(StateFilter(Questionnaire.sex), F.text.in_({'М', 'Ж'}))
async def add_sex(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(Questionnaire.clothing_brand)
    await message.answer(LEXICON_FSM["clothing_brand"][0], reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(Questionnaire.sex))
async def add_not_sex(message: Message):
    await message.answer(LEXICON_FSM["sex"][1])


@router.message(StateFilter(Questionnaire.clothing_brand))
async def add_clothing_brand(message: Message, state: FSMContext):
    await state.update_data(clothing_brand=message.text)
    await state.set_state(Questionnaire.color_palette)
    await message.answer(LEXICON_FSM["color_palette"][0])


@router.message(StateFilter(Questionnaire.clothing_brand))
async def add_not_clothing_brand(message: Message):
    await message.answer(LEXICON_FSM["clothing_brand"][1])


@router.message(StateFilter(Questionnaire.color_palette))
async def add_color_palette(message: Message, state: FSMContext):
    await state.update_data(color_palette=message.text)
    await state.set_state(Questionnaire.sizes)
    await message.answer(LEXICON_FSM["sizes"][0], reply_markup=sizes)


@router.message(StateFilter(Questionnaire.color_palette))
async def add_not_color_palette(message: Message):
    await message.answer(LEXICON_FSM["color_palette"][1])


@router.message(StateFilter(Questionnaire.sizes), F.text.in_({'M', 'S', 'L', 'XL'}))
async def add_sizes(message: Message, state: FSMContext):
    await state.update_data(sizes=message.text)
    await state.set_state(Questionnaire.fashion_style)
    await message.answer(LEXICON_FSM["fashion_style"][0], reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(Questionnaire.sizes))
async def add_not_sizes(message: Message):
    await message.answer(LEXICON_FSM["sizes"][1])


@router.message(StateFilter(Questionnaire.fashion_style))
async def add_fashion_style(message: Message, state: FSMContext):
    await state.update_data(fashion_style=message.text)
    await state.set_state(Questionnaire.hobby)
    await message.answer(LEXICON_FSM["hobby"][0])


@router.message(StateFilter(Questionnaire.fashion_style))
async def add_not_fashion_style(message: Message):
    await message.answer(LEXICON_FSM["fashion_style"][1])


@router.message(StateFilter(Questionnaire.hobby))
async def add_hobby(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    await state.set_state(Questionnaire.allergy)
    await message.answer(LEXICON_FSM["allergy"][0])


@router.message(StateFilter(Questionnaire.hobby))
async def add_not_hobby(message: Message):
    await message.answer(LEXICON_FSM["hobby"][1])


@router.message(StateFilter(Questionnaire.allergy))
async def add_allergy(message: Message, state: FSMContext):
    await state.update_data(allergy=message.text)
    await state.set_state(Questionnaire.salty_or_sweet)
    await message.answer(LEXICON_FSM["salty_or_sweet"][0])


@router.message(StateFilter(Questionnaire.allergy))
async def add_not_allergy(message: Message):
    await message.answer(LEXICON_FSM["allergy"][1])


@router.message(StateFilter(Questionnaire.salty_or_sweet))
async def add_salty_or_sweet(message: Message, state: FSMContext):
    await state.update_data(salty_or_sweet=message.text)
    await state.set_state(Questionnaire.dream)
    await message.answer(LEXICON_FSM["trips"][0])


@router.message(StateFilter(Questionnaire.salty_or_sweet))
async def add_not_salty_or_sweet(message: Message):
    await message.answer(LEXICON_FSM["salty_or_sweet"][1])


@router.message(StateFilter(Questionnaire.dream))
async def add_trips(message: Message, state: FSMContext):
    await state.update_data(dream=message.text)
    await state.set_state(Questionnaire.stock)
    await message.answer(LEXICON_FSM["stock"][0])


@router.message(StateFilter(Questionnaire.dream))
async def add_not_trips(message: Message):
    await message.answer(LEXICON_FSM["dream"][1])


@router.message(StateFilter(Questionnaire.stock), F.text.isdigit())
async def add_trips(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(stock=int(message.text))
    result: UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
    id_user, data, data["user_id"], data["photo"] = (message.from_user.id, await state.get_data(), message.from_user.id,
                                                     result.photos[0][0].file_id)
    await state.clear()
    user_data = await db_manager.get_questionnaire_by_id(user_id=id_user)
    secret_friend = await db_manager.get_user_by_id(user_id=id_user)
    if not user_data:
        # New questionnaire
        await db_manager.add_questionnaire(data)
    else:
        # Update questionnaire
        await db_manager.update_questionnaire(user_id=id_user, questionnaire_data=data)
        await profile(bot, data=user_data, id_user=secret_friend.id_secret_friend, text=LEXICON["change_profile"],
                      keyboard=None)
    if secret_friend.creator_id:
        keyboard = keyboard_creator.as_markup(resize_keyboard=True)
    else:
        keyboard = keyboard_user.as_markup(resize_keyboard=True)
    await message.answer(LEXICON_FSM["end"], reply_markup=keyboard)


@router.message(StateFilter(Questionnaire.stock))
async def add_not_trips(message: Message):
    await message.answer(LEXICON_FSM["stock"][1])


class GiftList(StatesGroup):  # gift list for user
    user_id = State()  # user name
    list = State()  # user sex


@router.callback_query(or_f(F.data == LEXICON_keyboard["new_list"][1], F.data == LEXICON_keyboard["change_list"][1]),
                             StateFilter(default_state))
async def add_gift_list(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GiftList.user_id)
    await state.set_state(GiftList.list)
    await callback.message.answer(LEXICON["normal_list"])


@router.message(StateFilter(GiftList.list))
async def add_list(message: Message, state: FSMContext):
    id_user = message.from_user.id
    await state.update_data(user_id=id_user)
    await state.update_data(list=message.text)
    data = await state.get_data()
    await state.clear()
    if not await db_manager.get_gift_list(user_id=id_user):
        # New list
        logging.debug(f'New list: {data}')
        await db_manager.add_gift_list(data)
    else:
        # Update list
        logging.debug(f'Update list: {data}')
        await db_manager.update_gift_list(user_id=id_user, list_data=data)
        await db_manager.delete_gifts(user_id=id_user)
    logging.debug(f'Generate list: {message.text}')
    await gift_list_generation(gifts=message.text, user_id=id_user)
        # user = await db_manager.get_user_by_id(user_id=id_user)
        # if user.id_secret_friend:
        #     await bot.send_message(chat_id=user.id_secret_friend,
        #                            text=LEXICON_keyboard["change_gift_list_friend"].format(gift_list=data))

    await message.answer(LEXICON_FSM["end_list"])


@router.message(StateFilter(GiftList.list))
async def add_not_list(message: Message):
    await message.answer(LEXICON["normal_list"])
