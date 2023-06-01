from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from query.check_user import user_is_admin
from . import main_menu_my_commentators_commentator_run_stop
from . import main_menu_my_commentators_commentator_settings
from . import main_menu_my_commentators_commentator_transferaccount
from . import main_menu_my_commentators

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]

    list_buttons = [
        ('Запустить/Остановить', f'{main_menu_my_commentators_commentator_run_stop.ID}|{commentator}|{phone}'),
        ('Настройки', f'{main_menu_my_commentators_commentator_settings.ID}|{commentator}|{phone}'), ]

    if await user_is_admin(call.bot.get('db'), call.from_user.id):
        list_buttons.append(
            ("Передать аккаунт",
             f'{main_menu_my_commentators_commentator_transferaccount.ID}|{commentator}|{phone}'))

    await call.message.edit_text(f"Меню действий для {commentator}",
                                 reply_markup=make_keyboard(list_buttons, f'{main_menu_my_commentators.ID}'))
