from sqlalchemy.future import select
from db.promt import Promt
from db.commentator import Commentator
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from sqlalchemy import update
from . import main_menu_my_commentators_commentator_settings
import uuid

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    db = call.bot.get('db')
    commentator_name = call.data.split('|')[1]
    commentator_phone = call.data.split('|')[2]

    async with db() as session:
        commentator = await session.execute(select(Commentator).where(Commentator.phone == commentator_phone))
        commentator = commentator.fetchone()[0]

    async with db() as session:
        promts = await session.execute(select(Promt).where(Promt.user.in_(['any', str(call.from_user.id)])))
        promts = promts.fetchall()

    list_buttons = [(promt[0].name,
                     f'{ID_2}|{commentator_name}|{commentator_phone}|{promt[0].name}')
                    for promt in promts]

    await call.message.edit_text(
        f"Для комментатора {commentator_name} сейчас установлен промт: {commentator.promt}. Выберите промт из списка.",
        reply_markup=make_keyboard(list_buttons,
                                   f'{main_menu_my_commentators_commentator_settings.ID}|{commentator_name}|{commentator_phone}'))


async def handler_2(call: CallbackQuery):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    promt_name = call.data.split('|')[3]

    db = call.bot.get('db')
    async with db() as session:
        promt = await session.execute(select(Promt).where(Promt.name == promt_name))
        promt = promt.fetchone()[0]

    async with db() as session:
        await session.execute(
            update(Commentator).values({Commentator.promt: promt.text}).where(Commentator.phone == phone))
        await session.commit()

    await call.message.edit_text(
        f"Для комментатора {commentator} установлен промт {promt.name} звучащий так : {promt.text}",
        reply_markup=make_keyboard([],
                                   f'{main_menu_my_commentators_commentator_settings.ID}|{commentator}|{phone}'))
