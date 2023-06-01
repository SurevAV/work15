from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from . import main_menu_personal_cabinet_make_promt
from . import main_menu_personal_cabinet_delete_promt

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    list_butons = (
        ("Партнерская программа", '1'),
        ("Выбрать тариф", '1'),
        ("Добавить свой промт", f'{main_menu_personal_cabinet_make_promt.ID}'),
        ("Удалить свой промт", f'{main_menu_personal_cabinet_delete_promt.ID}'),)
    await call.message.edit_text("Персональный кабинет", reply_markup=make_keyboard(list_butons, 'return_to_main_menu'))
