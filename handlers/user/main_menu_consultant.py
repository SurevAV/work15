from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from . import main_menu_consultant_my_consultants
from . import main_menu_consultant_make_consultant
from . import main_menu_consultant_delete_consultant
from query.check_user import *

ID = str(uuid.uuid4())[:5]

async def handler(call: CallbackQuery):
    list_buttons = [
        ("Мои консультанты", f'{main_menu_consultant_my_consultants.ID}'),
        ("Добавить консультанта", f'{main_menu_consultant_make_consultant.ID}'),
        ("Удалить консультанта", f'{main_menu_consultant_delete_consultant.ID}')
    ]

    #if await user_is_admin(call.bot.get('db'), call.from_user.id):
     #   list_buttons.insert(1, ("Добавить консультанта", f'{main_menu_consultant_make_consultant.ID}'))

    await call.message.edit_text(f"Выберете раздел консультанта", reply_markup=make_keyboard(list_buttons,'return_to_main_menu'))