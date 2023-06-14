from sqlalchemy import select
from db import Commentator
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from query.check_user import user_is_admin
from . import main_menu_my_commentators_commentator_run_stop
from . import main_menu_my_commentators_commentator_settings
from . import main_menu_my_commentators_commentator_transferaccount
from . import main_menu_my_commentators
from . import main_menu_my_commentators_commentator_prolong

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    item = call.data.split('|')
    commentator =item[1]
    phone = item[2]

    list_buttons = [
        ('Запустить/Остановить', f'{main_menu_my_commentators_commentator_run_stop.ID}|{commentator}|{phone}'),
        ('Настройки', f'{main_menu_my_commentators_commentator_settings.ID}|{commentator}|{phone}'),
        ('Продлить срок действия', f'{main_menu_my_commentators_commentator_prolong.ID}|{commentator}|{phone}'),]

    if await user_is_admin(call.bot.get('db'), call.from_user.id):
        list_buttons.append(
            ("Передать аккаунт",
             f'{main_menu_my_commentators_commentator_transferaccount.ID}|{commentator}|{phone}'))

    db = call.bot.get('db')

    async with db() as session:
        commentator_row = await session.execute(select(Commentator).where(Commentator.name == commentator))
        commentator_row = commentator_row.fetchone()[0]



    await call.message.edit_text(f"Меню действий для {commentator}. Комментатор доступен до {str(commentator_row.untilDate)[:10]}.",
                                 reply_markup=make_keyboard(list_buttons, f'{main_menu_my_commentators.ID}'))
