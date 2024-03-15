from aiogram.filters.callback_data import CallbackData


# Класс для создания callback_data
class CallbackFactory(CallbackData, prefix='gift', sep='-'):
    user_id: int
    index: int
    gift: str
