from keyboards.keyboards import *
from aiogram.types import CallbackQuery
from . import main_menu_my_commentators_commentator_settings
from . import main_menu_my_commentators_commentator_settings_settings_account_change_photo
from . import main_menu_my_commentators_commentator_settings_settings_account_change_description_account
from . import main_menu_my_commentators_commentator_settings_settings_account_change_username
from . import main_menu_my_commentators_commentator_settings_settings_account_change_name
from . import main_menu_my_commentators_commentator_settings_settings_account_change_surname
import uuid

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    commentator = call.data.split('|')[1]
    phone = call.data.split('|')[2]

    list_buttons = [('Изменить фото аккаунта',
                     f'{main_menu_my_commentators_commentator_settings_settings_account_change_photo.ID}|{commentator}|{phone}'),
                    ('Изменить описание аккаунта',
                     f'{main_menu_my_commentators_commentator_settings_settings_account_change_description_account.ID}|{commentator}|{phone}'),
                    ('Изменить username',
                     f'{main_menu_my_commentators_commentator_settings_settings_account_change_username.ID}|{commentator}|{phone}'),
                    ('Изменить имя',
                     f'{main_menu_my_commentators_commentator_settings_settings_account_change_name.ID}|{commentator}|{phone}'),
                    ('Изменить фамилию',
                     f'{main_menu_my_commentators_commentator_settings_settings_account_change_surname.ID}|{commentator}|{phone}')]

    await call.message.edit_text(f"Настройки аккаунта - {commentator}",
                                 reply_markup=make_keyboard(list_buttons,
                                                            f'{main_menu_my_commentators_commentator_settings.ID}|{commentator}|{phone}'))
