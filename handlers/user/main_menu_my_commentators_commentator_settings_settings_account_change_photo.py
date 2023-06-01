from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from aiogram.dispatcher import FSMContext
from telethon.tl.functions.photos import DeletePhotosRequest
import uuid
from . import main_menu_my_commentators_commentator_settings_settings_account

ID = str(uuid.uuid4())[:5]


class GetPhotoState(StatesGroup):
    photo = State()


async def handler(call: CallbackQuery,
                  state: FSMContext):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]
    call.bot["user_settings"][str(call.from_user.id)] = f'{commentator}|{phone}'

    await call.message.edit_text(f"Загрузите фото для коментатора - {commentator}")
    await state.set_state(GetPhotoState.photo.state)


async def handler_2(message: types.Message, state: FSMContext):
    user = str(message.from_user.id)
    await state.finish()

    user_settings = message.bot["user_settings"][user].split('|')
    # print(3)
    commentator = user_settings[0]
    # print(4)
    phone = user_settings[1]

    try:
        #print(1)
        video = False
        if message.content_type == 'photo':
            await message.photo[-1].download(f'{user}')
        elif message.content_type == 'document':
            await message.document.download(f'{user}')
        elif message.content_type == 'video':
            file_id = message.video.file_id
            file = await message.bot.get_file(file_id)
            await message.bot.download_file(file.file_path, f'{user}')
            video = True
        elif message.content_type == 'animation':
            file_id = message.animation.file_id
            file = await message.bot.get_file(file_id)
            await message.bot.download_file(file.file_path, f'{user}')
            video = True
        #print(2)

        #print(5)
        orhestra = message.bot.get('orhestra')
        #print(6)
        client = orhestra[phone]
        #print(7)

        await client(DeletePhotosRequest(await client.get_profile_photos("me", limit=5)))

        #print(8)
        file = await client.upload_file(f'{user}')
        #print(9)
        if not video:
            upload = UploadProfilePhotoRequest(file=file)
        else:
            upload = UploadProfilePhotoRequest(video=file)
        #print(10)
        await client(upload)
        #print(11)

        await message.answer(f"Фото загружено.",
                             reply_markup=make_keyboard([],
                                                        f'{main_menu_my_commentators_commentator_settings_settings_account.ID}|{commentator}|{phone}'))
    except Exception as e:

        await message.answer(f"Не получилось загрузить фото. {str(e)}",
                             reply_markup=make_keyboard([],
                                                        f'{main_menu_my_commentators_commentator_settings_settings_account.ID}|{commentator}|{phone}'))
