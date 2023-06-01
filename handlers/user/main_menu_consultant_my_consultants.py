from db.consultant import Consultant
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from query.check_user import *
import uuid
from . import main_menu_consultant
from . import main_menu_consultant_my_consultants_consultant
ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    db = call.bot.get('db')

    if await user_is_admin(db, call.from_user.id):
        async with db() as session:
            consultants = await session.execute(select(Consultant))
            consultants = consultants.fetchall()
    else:
        async with db() as session:
            consultants = await session.execute(select(Consultant).where(Consultant.owner == str(call.from_user.id)))
            consultants = consultants.fetchall()

    list_consultants = [(consultant[0].channel,
                          f'{main_menu_consultant_my_consultants_consultant.ID}|{consultant[0].channel}')
                         for consultant in consultants]

    await call.message.edit_text("Список консультантов",
                                 reply_markup=make_keyboard(list_consultants, main_menu_consultant.ID))