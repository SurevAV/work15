from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from telethon.tl.functions.account import UpdateProfileRequest
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from . import main_menu_my_commentators_commentator_settings_settings_account
import uuid

ID = str(uuid.uuid4())[:5]


class ChangeName(StatesGroup):
    name = State()


async def handler(
        call: CallbackQuery, state: FSMContext):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    await call.message.edit_text(f"Введите имя для аккаунта - {commentator}.")
    call.bot["user_settings"][str(call.from_user.id)] = f'{commentator}|{phone}'
    await state.set_state(ChangeName.name.state)


async def handler_2(
        message: types.Message, state: FSMContext):
    await state.finish()
    # try:
    orhestra = message.bot.get('orhestra')
    name_client = message.text

    user_settings = message.bot["user_settings"][str(message.from_user.id)].split('|')
    commentator = user_settings[0]
    phone = user_settings[1]
    client = orhestra[phone]

    await client(UpdateProfileRequest(first_name=name_client))

    await message.answer(f"Для комментатора {commentator} было установлено имя {name_client}",
                         reply_markup=make_keyboard([],
                                                    f'{main_menu_my_commentators_commentator_settings_settings_account.ID}|{commentator}|{phone}'))
    # except Exception as e:
    # await message.answer(f"{str(e)}",
    # reply_markup=add_inline_back_button(InlineKeyboardMarkup(),
    # 'return_to_main_menu'))
