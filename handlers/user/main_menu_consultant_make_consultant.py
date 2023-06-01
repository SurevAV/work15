from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from db.consultant import Consultant
from . import main_menu_consultant
import uuid

ID = str(uuid.uuid4())[:5]



class MakeConsultant(StatesGroup):
    channel = State()
    promt = State()


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
        session.add(Consultant(channel=channel, promt=message.text, owner=str(message.from_user.id)))
        await session.commit()

    await message.answer(f"Добавлен консультант для канала - {channel} с промтом - {message.text}",
                         reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                             main_menu_consultant.ID))