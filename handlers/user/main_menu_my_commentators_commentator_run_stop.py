import uuid
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from . import main_menu_my_commentators_commentator

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    await call.message.edit_text(f"{commentator} запущен/остановлен",
                                 reply_markup=make_keyboard([],
                                                            f'{main_menu_my_commentators_commentator.ID}|{commentator}|{phone}'))
