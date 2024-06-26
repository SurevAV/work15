from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from sqlalchemy import select, update
from db import User
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from db.commentator import Commentator
from query.check_user import get_user, change_user_balance
from . import main_menu_my_commentators
from datetime import datetime, timedelta
import uuid
from data import Config
from . import main_menu_my_commentators

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]

async def accept(call: CallbackQuery):


    user = await get_user(call.bot.get('db'), call.from_user.id)

    if user.balance >= Config.COST_COMMENTATOR  :
        string = f'Ваш баланс составляет - {str(user.balance/100)} рублей. Стоимость одного комментатора {str(Config.COST_COMMENTATOR /100)} рублей в {str(Config.PERIOD_COMMENTATOR )} дней. Вы можете купить комментатора.'
        list_buttons = [('Купить комментатора', f'{ID_2}')]
    else:
        string = f'Ваш баланс составляет - {str(user.balance / 100)} рублей. Стоимость одного комментатора {str(Config.COST_COMMENTATOR /100)}  рублей в {str(Config.PERIOD_COMMENTATOR )}  дней. Вы не можете купить комментатора.'
        list_buttons = []


    await call.message.edit_text(string, reply_markup=make_keyboard(list_buttons, ID_2))


async def handler(call: CallbackQuery):




    db = call.bot.get('db')

    async with db() as session:
        commentator = await session.execute(select(Commentator).where((Commentator.owner == 'n')|(Commentator.untilDate < datetime.now())))
        commentator = commentator.fetchone()[0]




    async with db() as session:
        await session.execute(update(Commentator).values({Commentator.owner: str(call.from_user.id), Commentator.untilDate:  datetime.now()+timedelta(days=Config.PERIOD_CONSULTANT)})
                              .where((Commentator.id == commentator.id)))
        await session.commit()


    await change_user_balance(db, call.from_user.id, Config.COST_COMMENTATOR)

    await call.message.edit_text(f"Вы преобрели комментатора.",
                                 reply_markup=make_keyboard([], f'{main_menu_my_commentators.ID}'))


