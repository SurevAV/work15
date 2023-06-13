from datetime import timedelta
from sqlalchemy import select, update
from db import Consultant
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from data import Config
from db.user import User
from . import main_menu_consultant_my_consultants_consultant

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]
async def accept(call: CallbackQuery):
    channel = call.data.split('|')[1]

    db = call.bot.get('db')
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(call.from_user.id)))
        user = user.fetchone()[0]

    if user.balance >= Config.COST_CONSULTANT:
        string = f'Ваш баланс составляет - {str(user.balance / 100)} рублей. Стоимость одного комментатора {str(Config.COST_CONSULTANT  / 100)} рублей за {str(Config.PERIOD_CONSULTANT )} дней. Вы можете продлить подписку на {str(Config.PERIOD_CONSULTANT )} дней.'
        list_buttons = [(f'Продлить подписку на {str(Config.PERIOD_CONSULTANT )} дней за {str(Config.COST_CONSULTANT  / 100)} рублей', f'{ID_2}|{channel}')]
    else:
        string = f'Ваш баланс составляет - {str(user.balance / 100)} рублей. Стоимость одного комментатора {str(Config.COST_CONSULTANT  / 100)}  рублей за {str(Config.PERIOD_CONSULTANT )}  дней. Вы не можете продлить подписку.'
        list_buttons = []

    await call.message.edit_text(string, reply_markup=make_keyboard(list_buttons, f'{main_menu_consultant_my_consultants_consultant.ID}|{channel}'))


async def handler(call: CallbackQuery):
    channel = call.data.split('|')[1]

    db = call.bot.get('db')
    async with db() as session:
        consultant = await session.execute(select(Consultant).where((Consultant.channel == channel)&(Consultant.owner == str(call.from_user.id))))
        consultant = consultant.fetchone()[0]

    async with db() as session:
        await session.execute(update(Consultant).values({Consultant.untilDate: consultant.untilDate+timedelta(days=Config.PERIOD_CONSULTANT)})
                              .where((Consultant.channel == channel)&(Consultant.owner == str(call.from_user.id))))
        await session.commit()

    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(call.from_user.id)))
        user = user.fetchone()[0]

    async with db() as session:
        await session.execute(update(User).values({User.balance: user.balance-Config.COST_CONSULTANT }).where(
            User.idTelegram == str(call.from_user.id)))
        await session.commit()

    await call.message.edit_text(f'Консультант {channel} продлен на {str(Config.PERIOD_CONSULTANT )} дней.', reply_markup=make_keyboard([],
                                                                    f'{main_menu_consultant_my_consultants_consultant.ID}|{channel}'))

