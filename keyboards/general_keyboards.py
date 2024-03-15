from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from LEXICON.lexicon import LEXICON_keyboard, LEXICON
from keyboards.callback_data_classes import CallbackFactory

btn_1 = InlineKeyboardButton(text=LEXICON_keyboard["keyboard_start_1"][0],
                             callback_data=LEXICON_keyboard["keyboard_start_1"][1])
btn_2 = InlineKeyboardButton(text=LEXICON_keyboard["keyboard_start_2"][0],
                             callback_data=LEXICON_keyboard["keyboard_start_2"][1])
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[[btn_1, btn_2]])

# keyboard for read rules
read = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=LEXICON_keyboard["read"][0],
                                                                   callback_data=LEXICON_keyboard["read"][1])]])

# keyboard for user questionnaire
questionnaire = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text=LEXICON_keyboard["questionnaire"][0],
    callback_data=LEXICON_keyboard["questionnaire"][1])]])

next_questionnaire = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Следующий вопрос',
    callback_data='next')]])

# keyboard for sex
sex = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='М'),
                                     KeyboardButton(text='Ж')]],
                          resize_keyboard=True)

# keyboard for sizes
sizes = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='S'),
                                       KeyboardButton(text='M'),
                                       KeyboardButton(text='L'),
                                       KeyboardButton(text='XL')]],
                            resize_keyboard=True)

# keyboard for user
keyboard_user = (ReplyKeyboardBuilder())
keyboard_user.row(*[KeyboardButton(text=bt) for bt in LEXICON_keyboard["button"][2:5]], width=2)

# keyboard for creator
keyboard_creator = (ReplyKeyboardBuilder())
keyboard_creator.row(*[KeyboardButton(text=bt) for bt in LEXICON_keyboard["button"]], width=2)

# keyboard for change questionnaire
keyboard_change = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text=LEXICON_keyboard["change_b"][0],
    callback_data=LEXICON_keyboard["change_b"][1])]])

# keyboard for stop FSM
keyboard_stop_FSM = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=LEXICON_keyboard["stop"])]],
                                        resize_keyboard=True)

# keyboard for new list
keyboard_new_list = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text=LEXICON_keyboard["new_list"][0],
    callback_data=LEXICON_keyboard["new_list"][1])]])

# keyboard for change list
keyboard_change_list = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text=LEXICON_keyboard["change_list"][0],
    callback_data=LEXICON_keyboard["change_list"][1])]])

# keyboard for secret friend
keyboard_friend = (ReplyKeyboardBuilder())
(keyboard_friend.row(*[KeyboardButton(text=bt) for bt in LEXICON_keyboard["friend_button"]], width=2)).row(
    KeyboardButton(text=LEXICON["menu"]))


# keyboard for gift list
def keyboard_list(user_id, gifts):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[(InlineKeyboardButton(text=gift,
                                           callback_data=(CallbackFactory(user_id=user_id, index=index, gift=gift).pack())))
                     for index, gift in enumerate(gifts.split(','))], width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# keyboard for stock
keyboard_stock = InlineKeyboardBuilder()
keyboard_stock.row(*[(InlineKeyboardButton(
    text=key,
    callback_data=name)) for key, name in LEXICON_keyboard["stock"].items()], width=1)
