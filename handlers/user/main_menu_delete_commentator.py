from db.commentator import Commentator
from db.user import User
from sqlalchemy.future import select
from sqlalchemy import delete
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    db = call.bot.get('db')

    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(call.from_user.id)))
        user = user.fetchone()

    if user[0].is_admin:
        async with db() as session:
            commentators = await session.execute(select(Commentator))
            commentators = commentators.fetchall()
    else:
        async with db() as session:
            commentators = await session.execute(select(Commentator).where(Commentator.owner == str(call.from_user.id)))
            commentators = commentators.fetchall()

    list_commentators = [
        (commentator[0].name, f'{ID_2}|{commentator[0].name}|{commentator[0].phone}') for
        commentator in commentators]

    await call.message.edit_text("Список комментаторов для удаления",
                                 reply_markup=make_keyboard(list_commentators, 'return_to_main_menu'))


async def handler_2(call: CallbackQuery):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    db = call.bot.get('db')
    async with db() as session:
        await session.execute(delete(Commentator).where(Commentator.phone == phone))
        await session.commit()

    await call.message.edit_text(f"Комментатор {commentator} удален.",
                                 reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                                     'return_to_main_menu'))
