from telethon import functions
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from db.commentator import Commentator
from sqlalchemy.future import select
from sqlalchemy import update
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
import uuid
from . import main_menu_my_commentators_commentator_settings

ID = str(uuid.uuid4())[:5]


class ChannelList(StatesGroup):
    channels_names = State()


async def handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Добавте список каналов через запятую.")
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    call.bot["user_settings"][str(call.from_user.id)] = f'{commentator}|{phone}'
    await state.set_state(ChannelList.channels_names.state)


async def handler_2(message: types.Message, state: FSMContext):
    channel = message.text

    await state.finish()

    user_settings = message.bot["user_settings"][str(message.from_user.id)].split('|')

    commentator = user_settings[0]
    phone = user_settings[1]

    db = message.bot.get('db')
    orhestra = message.bot.get('orhestra')

    channel = channel.replace(' ', '')
    channel = channel.replace('https://t.me/', '')

    if ',' in channel:
        channel_list = channel.split(',')
    else:
        channel_list = [channel]

    client = orhestra[phone]

    for channel in channel_list:
        try:
            async with db() as session:
                commentator_row = await session.execute(select(Commentator).where(Commentator.phone == phone))
                commentator_row = commentator_row.fetchone()[0]

            if commentator_row.channels:
                channels = commentator_row.channels
            else:
                channels = ''

            if channel != '':
                await client(functions.channels.JoinChannelRequest(channel=channel))

                channels += f',{channel}'

                async with db() as session:
                    await session.execute(update(Commentator).values({Commentator.channels: channels}).where(
                        Commentator.phone == phone))
                    await session.commit()
                    # ------------------------------
                await message.answer(f"{commentator} был добавлен в каннал {channel}.")

        except Exception as e:
            await message.answer(
                f"Не удалось добавить комментатор - {commentator} в канал - {channel}. {str(e)}")

    await message.answer(f"Вы можете вернуться назад.",
                         reply_markup=make_keyboard([],
                                                    f'{main_menu_my_commentators_commentator_settings.ID}|{commentator}|{phone}'))
