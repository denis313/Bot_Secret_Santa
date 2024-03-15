from LEXICON.lexicon import LEXICON
from keyboards.general_keyboards import keyboard_change


async def profile(bot, data, id_user: int, text: str, keyboard=keyboard_change):
    try:
        return await bot.send_photo(photo=data.photo, chat_id=id_user,
                                    caption=text + LEXICON["profile"].format(name=data.name,
                                                                             sex=data.sex,
                                                                             clothing_brand=data.clothing_brand,
                                                                             color_palette=data.color_palette,
                                                                             sizes=data.sizes,
                                                                             fashion_style=data.fashion_style,
                                                                             hobby=data.hobby,
                                                                             allergy=data.allergy,
                                                                             salty_or_sweet=data.salty_or_sweet,
                                                                             dream=data.dream),
                                    reply_markup=keyboard)
    except AttributeError:
        print('error')
