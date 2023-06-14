from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from query.make_user_if_not_exist import *
import uuid
from . import main_menu_personal_cabinet
from . import main_menu_my_commentators
from query.check_user import *
from . import main_menu_instruction
from . import main_menu_consultant
from . import main_menu_replenish_the_balance

ID = str(uuid.uuid4())[:5]

async def handler(call: CallbackQuery):
    db = call.bot.get('db')

    await make_user(db, call.from_user.id,call.from_user.username)

    list_buttons = (
        ("Личный кабинет", f'{main_menu_personal_cabinet.ID}'),
        ("Мои комментаторы", f'{main_menu_my_commentators.ID}'),
        ("Консультант", f'{main_menu_consultant.ID}'),
        ("Пополнить баланс", f'{main_menu_replenish_the_balance.ID}'),
        ("Инструкция", f'{main_menu_instruction.ID}')
    )#("Удалить комментатора", f'{main_menu_delete_commentator.ID}'),


    user = await get_user(call.bot.get('db'), call.from_user.id)
    await call.message.edit_text(f"Приветсвую выберете раздел. Ваш баланс {str(user.balance/100)} рублей", reply_markup=make_keyboard(list_buttons))