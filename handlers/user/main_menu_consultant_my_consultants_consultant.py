from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from query.check_user import *
from db.consultant import Consultant
from . import main_menu_consultant_my_consultants_consultant_edit
from . import main_menu_consultant_my_consultants
from . import main_menu_consultant_my_consultants_consultant_prolong
ID = str(uuid.uuid4())[:5]

async def handler(call: CallbackQuery):
    item = call.data.split('|')
    channel = item[1]

    list_buttons = [
        ("Редактировать промт", f'{main_menu_consultant_my_consultants_consultant_edit.ID}|{channel}'),
        ("Продлить подписку", f'{main_menu_consultant_my_consultants_consultant_prolong.ID}|{channel}')
    ]
    db = call.bot.get('db')

    async with db() as session:
        consultant = await session.execute(
            select(Consultant).where(Consultant.channel == channel))
        consultant = consultant.fetchone()



    await call.message.edit_text(f"Для канала - {consultant[0].channel} сейчас утсановлен промт {consultant[0].promt}. Консультант доступен до {str(consultant[0].untilDate)[:10]}.", reply_markup=make_keyboard(list_buttons,main_menu_consultant_my_consultants.ID))