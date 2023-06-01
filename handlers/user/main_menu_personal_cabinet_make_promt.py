from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from db.promt import Promt

import uuid

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]
ID_3 = str(uuid.uuid4())[:5]


class MakePromt(StatesGroup):
    name = State()
    text = State()


async def handler(
        call: CallbackQuery, state: FSMContext):
    # await MakePromt.name.set()
    await call.message.edit_text(f"Введите имя промта.")
    await state.set_state(MakePromt.name.state)


async def handler_2(
        message: types.Message, state: FSMContext):
    message.bot["user_settings"][str(message.from_user.id)] = message.text

    await state.set_state(MakePromt.text.state)
    await message.answer(f"Введите текст промта.")


async def handler_3(
        message: types.Message, state: FSMContext):
    await state.finish()
    name = message.bot["user_settings"][str(message.from_user.id)]

    db = message.bot.get('db')

    async with db() as session:
        session.add(Promt(name=name, text=message.text, user=str(message.from_user.id)))
        await session.commit()

    await message.answer(f"Добавлен промт - {name} с текстом {message.text}",
                         reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                             'return_to_main_menu'))
