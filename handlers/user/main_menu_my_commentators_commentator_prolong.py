from datetime import timedelta
from sqlalchemy import update
from db import  Commentator
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from data import Config
from query.check_user import get_user
from . import main_menu_my_commentators_commentator

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]

async def accept(call: CallbackQuery):

    item =  call.data.split('|')
    commentator = item[1]
    phone = item[2]

    user = await get_user(call.bot.get('db'), call.from_user.id)

    if user.balance >= Config.COST_COMMENTATOR:
        string = f'sВаш баланс составляет - {str(user.balance / 100)} рублей. Стоимость одного комментатора {str(Config.COST_COMMENTATOR  / 100)} рублей за {str(Config.PERIOD_COMMENTATOR )} дней. Вы можете продлить подписку на {str(Config.PERIOD_COMMENTATOR )} дней.'
        list_buttons = [(f'Продлить подписку на {str(Config.PERIOD_COMMENTATOR)} дней за {str(Config.COST_COMMENTATOR/ 100)} рублей',
                         f'{ID_2}|{commentator}|{phone}')]
    else:
        string = f'Ваш баланс составляет - {str(user.balance / 100)} рублей. Стоимость одного комментатора {str(Config.COST_COMMENTATOR/ 100)}  рублей за {str(Config.PERIOD_COMMENTATOR)}  дней. Вы не можете продлить подписку.'
        list_buttons = []

    await call.message.edit_text(string, reply_markup=make_keyboard(list_buttons, f'{main_menu_my_commentators_commentator.ID}|{commentator}|{phone}'))


async def handler(call: CallbackQuery):
    item = call.data.split('|')
    commentator = item[1]
    phone = item[2]

    db = call.bot.get('db')
    async with db() as session:
        await session.execute(update(Commentator).values({Commentator.untilDate: Commentator.untilDate+timedelta(days=Config.PERIOD_COMMENTATOR)})
                              .where((Commentator.phone == phone)))
        await session.commit()

    await call.message.edit_text(f'Комментатор {commentator} продлен на {str(Config.PERIOD_COMMENTATOR)} дней.', reply_markup=make_keyboard([],
                                                                    f'{main_menu_my_commentators_commentator.ID}|{commentator}|{phone}'))

