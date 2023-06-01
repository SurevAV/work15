from db.consultant import Consultant
from . import main_menu_consultant
from sqlalchemy import delete
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from query.check_user import *

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]


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

    list_consultants = [
        (consultant[0].channel, f'{ID_2}|{consultant[0].channel}|{str(consultant[0].id)}') for
        consultant in consultants] #TODO change callbackdata on id in all cases



    await call.message.edit_text("Список косультантов для удаления",
                                 reply_markup=make_keyboard(list_consultants, main_menu_consultant.ID))


async def handler_2(call: CallbackQuery):
    call_back_item = call.data.split('|')
    channel, consultant_id = call_back_item[1], call_back_item[2]

    db = call.bot.get('db')
    async with db() as session:
        await session.execute(delete(Consultant).where(Consultant.id == int(consultant_id)))
        await session.commit()

    await call.message.edit_text(f"Консультант {channel} удален.",
                                 reply_markup=add_inline_back_button(InlineKeyboardMarkup(),ID))

