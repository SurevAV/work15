from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from db.consultant import Consultant
from . import main_menu_consultant
import uuid
from sqlalchemy import update

ID = str(uuid.uuid4())[:5]


class EditConsultant(StatesGroup):
    promt = State()


async def handler(
        call: CallbackQuery, state: FSMContext):
    call.bot["user_settings"][str(call.from_user.id)] = call.data.split('|')[1]

    await call.message.edit_text(f"Введите промт для консультанта.")
    await state.set_state(EditConsultant.promt.state)


async def handler_2(
        message: types.Message, state: FSMContext):
    await state.set_state(EditConsultant.promt.state)
    channel = message.bot["user_settings"][str(message.from_user.id)]

    await state.finish()
    db = message.bot.get('db')

    async with db() as session:
        await session.execute(update(Consultant).values({Consultant.promt: message.text}).where(
            Consultant.channel == channel))
        await session.commit()

    await message.answer(f"Добавлен консультанта - {channel} установлен - {message.text}",
                         reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                             main_menu_consultant.ID))
