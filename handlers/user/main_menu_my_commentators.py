from db.commentator import Commentator
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from query.check_user import *
from . import main_menu_my_commentators_commentator
import uuid

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    db = call.bot.get('db')

    if await user_is_admin(db, call.from_user.id):
        async with db() as session:
            commentators = await session.execute(select(Commentator))
            commentators = commentators.fetchall()
    else:
        async with db() as session:
            commentators = await session.execute(select(Commentator).where(Commentator.owner == str(call.from_user.id)))
            commentators = commentators.fetchall()

    list_commentators = [(commentator[0].name,
                          f'{main_menu_my_commentators_commentator.ID}|{commentator[0].name}|{commentator[0].phone}')
                         for commentator in commentators]

    await call.message.edit_text("Список комментаторов",
                                 reply_markup=make_keyboard(list_commentators, 'return_to_main_menu'))
