from sqlalchemy.future import select
from sqlalchemy import delete
from db.promt import Promt
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from . import main_menu_personal_cabinet

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    db = call.bot.get('db')

    async with db() as session:
        promts = await session.execute(select(Promt).where(Promt.user == str(call.from_user.id)))
        promts = promts.fetchall()

    list_buttons = [(promt[0].name, f'{ID_2}|{str(promt[0].id)}') for promt in promts]

    await call.message.edit_text(f"Выберети промт для удаления.",
                                 reply_markup=make_keyboard(list_buttons,
                                                            f'{main_menu_personal_cabinet.ID}.'))


async def handler_2(call: CallbackQuery):
    promt = call.data.split('|')[1]
    db = call.bot.get('db')
    async with db() as session:
        await session.execute(delete(Promt).where(Promt.id == int(promt)))
        await session.commit()

    await call.message.answer(f"Промт удален.",
                              reply_markup=make_keyboard([], f'{main_menu_personal_cabinet.ID}.'))
