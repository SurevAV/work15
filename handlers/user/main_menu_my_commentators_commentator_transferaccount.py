from telethon.tl.functions.users import GetFullUserRequest
from aiogram.dispatcher import FSMContext
from query.make_user_if_not_exist import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from db.commentator import Commentator
from sqlalchemy import update
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from . import main_menu_my_commentators_commentator

ID = str(uuid.uuid4())[:5]


class TransferAccount(StatesGroup):
    name = State()


async def handler(
        call: CallbackQuery, state: FSMContext):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    await call.message.edit_text(f"Введите имя пользователя которому вы хотетие передать комментатора - {commentator}.")
    call.bot["user_settings"][str(call.from_user.id)] = f'{commentator}|{phone}'
    await state.set_state(TransferAccount.name.state)


async def handler_2(
        message: types.Message, state: FSMContext):
    await state.finish()

    user_settings = message.bot["user_settings"][str(message.from_user.id)].split('|')
    commentator = user_settings[0]
    phone = user_settings[1]
    try:
        orhestra = message.bot.get('orhestra')
        username = message.text
        client = orhestra[phone]
        user = await client(GetFullUserRequest(username))

        db = message.bot.get('db')
        await make_user(db, user.full_user.id, username)

        async with db() as session:
            await session.execute(update(Commentator).values({Commentator.owner: str(user.full_user.id)}).where(
                Commentator.phone == phone))
            await session.commit()

        await message.answer(f"Для комментатора {commentator} - установлен владелец - {username}",
                             reply_markup=make_keyboard([],
                                                        f'{main_menu_my_commentators_commentator.ID}|{commentator}|{phone}'))
    except Exception as e:
        await message.answer(f"{str(e)}",
                             reply_markup=make_keyboard([],
                                                        f'{main_menu_my_commentators_commentator.ID}|{commentator}|{phone}'))
