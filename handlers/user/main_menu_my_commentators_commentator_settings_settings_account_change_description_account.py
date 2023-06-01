from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from telethon.tl.functions.account import UpdateProfileRequest
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from . import main_menu_my_commentators_commentator_settings_settings_account
import uuid

ID = str(uuid.uuid4())[:5]


class ChangeDescription(StatesGroup):
    description = State()


async def handler(
        call: CallbackQuery, state: FSMContext):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    await call.message.edit_text(f"Введите описание для аккаунта - {commentator}.")
    call.bot["user_settings"][str(call.from_user.id)] = f'{commentator}|{phone}'
    await state.set_state(ChangeDescription.description.state)


async def handler_2(
        message: types.Message, state: FSMContext):
    await state.finish()

    user_settings = message.bot["user_settings"][str(message.from_user.id)].split('|')
    commentator = user_settings[0]
    phone = user_settings[1]
    try:
        orhestra = message.bot.get('orhestra')
        description = message.text

        client = orhestra[phone]
        await client(UpdateProfileRequest(about=description))

        await message.answer(f"Для комментатора {commentator} было установлено описание {description}",
                             reply_markup=make_keyboard([],
                                                        f'{main_menu_my_commentators_commentator_settings_settings_account.ID}|{commentator}|{phone}'))
    except Exception as e:
        await message.answer(f"{str(e)}",
                             reply_markup=make_keyboard([],
                                                        f'{main_menu_my_commentators_commentator_settings_settings_account.ID}|{commentator}|{phone}'))
