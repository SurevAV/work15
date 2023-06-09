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
    channel = State()
    promt = State()

async def handler(
        call: CallbackQuery, state: FSMContext):
    call.bot["user_settings"][str(call.from_user.id)] = call.data.split('|')[1]

    await call.message.edit_text(f"Введите новое имя канала для консультанта.")
    await state.set_state(EditConsultant.channel.state)

async def handler_2(
        message: types.Message, state: FSMContext):
    message.bot["user_settings"][str(message.from_user.id)] += '|'
    message.bot["user_settings"][str(message.from_user.id)] += message.text

    await state.set_state(EditConsultant.promt.state)
    await message.answer(f"Введите текст промта.")


async def handler_3(
        message: types.Message, state: FSMContext):
    await state.finish()

    item = message.bot["user_settings"][str(message.from_user.id)].split('|')
    channel = item[0]
    new_name = item[1]
    promt = message.text

    db = message.bot.get('db')

    async with db() as session:
         await session.execute(update(Consultant).values({Consultant.promt: promt, Consultant.channel: new_name}).where(Consultant.channel == channel))
         await session.commit()


    await message.answer(f"Для консультанта - {channel} установлено новое имя - {new_name} и новый промт- {message.text}",
                         reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
                                                             main_menu_consultant.ID))
