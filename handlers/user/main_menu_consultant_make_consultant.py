from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from sqlalchemy import select, update
from db import User
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from db.consultant import Consultant
from . import main_menu_consultant
from datetime import datetime, timedelta
import uuid
from data import Config

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]


class MakeConsultant(StatesGroup):
    channel = State()
    promt = State()


async def accept(call: CallbackQuery):
    db = call.bot.get('db')
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(call.from_user.id)))
        user = user.fetchone()[0]


    if user.balance >= Config.COST_CONSULTANT :
        string = f'Ваш баланс составляет - {str(user.balance/100)} рублей. Стоимость одного консультанта {str(Config.COST_CONSULTANT /100)} рублей в {str(Config.PERIOD_CONSULTANT )} дней. Вы можете купить консультанта.'
        list_buttons = [('Купить консульанта', f'{ID_2}')]
    else:
        string = f'Ваш баланс составляет - {str(user.balance / 100)} рублей. Стоимость одного консультанта {str(Config.COST_CONSULTANT /100)}  рублей в {str(Config.PERIOD_CONSULTANT)}  дней. Вы не можете купить консультанта.'
        list_buttons = []



    await call.message.edit_text(string, reply_markup=make_keyboard(list_buttons, main_menu_consultant.ID))


async def handler(
        call: CallbackQuery, state: FSMContext):

    await call.message.edit_text(f"Введите имя канала для консультанта.")
    await state.set_state(MakeConsultant.channel.state)


async def handler_2(
        message: types.Message, state: FSMContext):
    message.bot["user_settings"][str(message.from_user.id)] = message.text

    await state.set_state(MakeConsultant.promt.state)
    await message.answer(f"Введите текст промта.")


async def handler_3(
        message: types.Message, state: FSMContext):
    await state.finish()
    channel = message.bot["user_settings"][str(message.from_user.id)]


    db = message.bot.get('db')

    async with db() as session:
        consultant = await session.execute(select(Consultant).where(Consultant.channel == channel))

    if not consultant.fetchone():


        async with db() as session:
            session.add(Consultant(channel=channel, promt=message.text, owner=str(message.from_user.id), untilDate = datetime.now()+timedelta(days=Config.PERIOD_CONSULTANT)))
            await session.commit()

        async with db() as session:
            user = await session.execute(select(User).where(User.idTelegram == str(message.from_user.id)))
            user = user.fetchone()[0]

        balance = user.balance - Config.COST_CONSULTANT

        async with db() as session:
            await session.execute(update(User).values({User.balance: balance}).where(
                User.idTelegram == str(message.from_user.id)))
            await session.commit()

        await message.answer(f"Добавлен консультант для канала - {channel} с промтом - {message.text}. Ваш баланс {str((user.balance - Config.COST_CONSULTANT )/100)} рублей",
                             reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                                 main_menu_consultant.ID))
    else:
        await message.answer(
            f"Для канала - {channel} уже есть консультант.",
            reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                main_menu_consultant.ID))