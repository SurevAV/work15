from sqlalchemy.future import select
from db.commentator import Commentator
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from telethon import functions
from sqlalchemy import update
from . import main_menu_my_commentators_commentator_settings
import uuid

ID = str(uuid.uuid4())[:5]
ID_2 = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    item = call.data.split('|')
    commentator = item[1]
    phone = item[2]

    orhestra = call.bot.get('orhestra')
    client = orhestra[phone]

    db = call.bot.get('db')
    async with db() as session:
        commentator_row = await session.execute(select(Commentator).where(Commentator.phone == phone))
        commentator_row = commentator_row.fetchone()[0]



    commentator_channels = await client.get_dialogs()



    list_buttons = []
    for commentator_channel in commentator_channels:

        if not commentator_channel.is_group and commentator_channel.is_channel:

            name_channel = str(commentator_channel.entity.username)

            if name_channel not in commentator_row.channels:
                name_channel += ' - not in list'
            #print(commentator_channel )
            #try:

            #    await client(functions.channels.LeaveChannelRequest(channel=str(commentator_channel.entity.username)))
            #except Exception as e:
              #  print(f"{str(e)}", )

            list_buttons.append([name_channel,
                                 f'{ID_2}|{commentator}|{phone}|{str(commentator_channel.entity.username)}'])

    await call.message.edit_text(f"Выберете какой канал должен покинуть комментатор {commentator}.",
                                 reply_markup=make_keyboard(list_buttons[:20],
                                                            f'{main_menu_my_commentators_commentator_settings.ID}|{commentator}|{phone}'))


async def handler_2(call: CallbackQuery):
    item = call.data.split('|')
    commentator = item[1]
    phone = item[2]
    channel = item[3]

    orhestra = call.bot.get('orhestra')
    client = orhestra[phone]

    try:
        await client(functions.channels.LeaveChannelRequest(channel=channel))
    except Exception as e:
        await call.message.answer(f"{str(e)}", )

    db = call.bot.get('db')
    async with db() as session:
        commentator_row = await session.execute(select(Commentator).where(Commentator.phone == phone))
        commentator_row = commentator_row.fetchone()[0]

    commentator_row = commentator_row.channels.replace(channel, '')
    commentator_row = commentator_row.replace('https://t.me/', '')

    async with db() as session:
        await session.execute(
            update(Commentator).values({Commentator.channels: commentator_row}).where(Commentator.phone == phone))
        await session.commit()

    await call.message.edit_text(f"{commentator} покинул канал {channel}.",
                                 reply_markup=make_keyboard([],
                                                            f'{ID}|{commentator}|{phone}'))
