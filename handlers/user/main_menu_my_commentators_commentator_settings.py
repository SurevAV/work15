from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from . import main_menu_my_commentators_commentator_settings_choose_character_commentators
from . import main_menu_my_commentators_commentator_settings_add_list_channels
from . import main_menu_my_commentators_commentator_settings_leave_channel
from . import main_menu_my_commentators_commentator_settings_settings_account
from . import main_menu_my_commentators_commentator


ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]

    list_buttons = [('Выбрать характер комментатора',
                     f'{main_menu_my_commentators_commentator_settings_choose_character_commentators.ID}|{commentator}|{phone}'),
                    ('Добавить список каналов',
                     f'{main_menu_my_commentators_commentator_settings_add_list_channels.ID}|{commentator}|{phone}'),
                    ('Покинуть канал',
                     f'{main_menu_my_commentators_commentator_settings_leave_channel.ID}|{commentator}|{phone}'),
                    ('Настройки аккаунта',
                     f'{main_menu_my_commentators_commentator_settings_settings_account.ID}|{commentator}|{phone}'),
                    ('Комментинг от Канала',
                     f'{str(None)}|{commentator}|{phone}'),
                    ('Отчётность',
                     f'{str(None)}|{commentator}|{phone}'), ]

    await call.message.edit_text(f"Настройки для - {commentator}",
                                 reply_markup=make_keyboard(list_buttons,
                                                            f'{main_menu_my_commentators_commentator.ID}|{commentator}|{phone}'))
