from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    await call.message.edit_text("Инструкция", reply_markup=make_keyboard([], 'return_to_main_menu'))
