from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message
from aiogram.dispatcher.filters import Regexp
import openai
from . import bot_start
from . import bot_start_again
from . import main_menu_delete_commentator
from . import main_menu_instruction
from . import main_menu_my_commentators
from . import main_menu_my_commentators_commentator
from . import main_menu_my_commentators_commentator_run_stop
from . import main_menu_my_commentators_commentator_settings
from . import main_menu_my_commentators_commentator_settings_add_list_channels
from . import main_menu_my_commentators_commentator_settings_choose_character_commentators
from . import main_menu_my_commentators_commentator_settings_leave_channel
from . import main_menu_my_commentators_commentator_settings_settings_account
from . import main_menu_my_commentators_commentator_settings_settings_account_change_description_account
from . import main_menu_my_commentators_commentator_settings_settings_account_change_name
from . import main_menu_my_commentators_commentator_settings_settings_account_change_photo
from . import main_menu_my_commentators_commentator_settings_settings_account_change_surname
from . import main_menu_my_commentators_commentator_settings_settings_account_change_username
from . import main_menu_my_commentators_commentator_transferaccount
from . import main_menu_personal_cabinet
from . import main_menu_personal_cabinet_delete_promt
from . import main_menu_personal_cabinet_make_promt
from . import main_menu_consultant
from . import main_menu_consultant_my_consultants
from . import main_menu_consultant_make_consultant
from . import main_menu_consultant_delete_consultant
from . import main_menu_consultant_my_consultants_consultant
from . import main_menu_consultant_my_consultants_consultant_edit
from . import main_menu_replenish_the_balance
from aiogram.types.message import ContentTypes
from sqlalchemy.future import select
from db.consultant import Consultant
from sqlalchemy import or_
def setup(db: Dispatcher):
    db.register_message_handler(bot_start.handler, CommandStart(), state='*')

    db.register_callback_query_handler(bot_start_again.handler, text='return_to_main_menu')

    db.register_callback_query_handler(main_menu_personal_cabinet.handler,
                                       Regexp(regexp=f'{main_menu_personal_cabinet.ID}.*'))

    db.register_callback_query_handler(main_menu_my_commentators.handler,
                                       Regexp(regexp=f'{main_menu_my_commentators.ID}.*'))

    db.register_callback_query_handler(main_menu_instruction.handler,
                                       Regexp(regexp=f'{main_menu_instruction.ID}.*'))

    db.register_callback_query_handler(main_menu_my_commentators_commentator.handler,
                                       Regexp(regexp=f'{main_menu_my_commentators_commentator.ID}.*'))

    db.register_callback_query_handler(main_menu_my_commentators_commentator_run_stop.handler,
                                       Regexp(regexp=f'{main_menu_my_commentators_commentator_run_stop.ID}.*'))

    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings.handler,
                                       Regexp(regexp=f'{main_menu_my_commentators_commentator_settings.ID}.*'))
    # ----------------------------------
    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_add_list_channels.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_add_list_channels.ID}.*'))

    db.register_message_handler(main_menu_my_commentators_commentator_settings_add_list_channels.handler_2,
                                state=main_menu_my_commentators_commentator_settings_add_list_channels.ChannelList.channels_names)

    # ----------------------------------

    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_settings_account.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_settings_account.ID}.*'))

    # ----------------------------------

    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_settings_account_change_photo.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_settings_account_change_photo.ID}.*'))

    db.register_message_handler(main_menu_my_commentators_commentator_settings_settings_account_change_photo.handler_2,
                                state=main_menu_my_commentators_commentator_settings_settings_account_change_photo.GetPhotoState.photo,
                                content_types=["document", "photo", "video",'animation'])
    # ----------------------------------
    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_choose_character_commentators.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_choose_character_commentators.ID}.*'))

    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_choose_character_commentators.handler_2,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_choose_character_commentators.ID_2}.*'))
    # ----------------------------------

    db.register_callback_query_handler(
        main_menu_my_commentators_commentator_settings_settings_account_change_description_account.handler,
        Regexp(
            regexp=f'{main_menu_my_commentators_commentator_settings_settings_account_change_description_account.ID}.*'))

    db.register_message_handler(
        main_menu_my_commentators_commentator_settings_settings_account_change_description_account.handler_2,
        state=main_menu_my_commentators_commentator_settings_settings_account_change_description_account.ChangeDescription.description)

    # ----------------------------------

    db.register_callback_query_handler(
        main_menu_my_commentators_commentator_settings_settings_account_change_name.handler,
        Regexp(
            regexp=f'{main_menu_my_commentators_commentator_settings_settings_account_change_name.ID}.*'))

    db.register_message_handler(
        main_menu_my_commentators_commentator_settings_settings_account_change_name.handler_2,
        state=main_menu_my_commentators_commentator_settings_settings_account_change_name.ChangeName.name)

    # ----------------------------------

    db.register_callback_query_handler(
        main_menu_my_commentators_commentator_settings_settings_account_change_surname.handler,
        Regexp(
            regexp=f'{main_menu_my_commentators_commentator_settings_settings_account_change_surname.ID}.*'))

    db.register_message_handler(
        main_menu_my_commentators_commentator_settings_settings_account_change_surname.handler_2,
        state=main_menu_my_commentators_commentator_settings_settings_account_change_surname.ChangeSurname.surname)

    # ----------------------------------
    db.register_callback_query_handler(
        main_menu_personal_cabinet_make_promt.handler,
        Regexp(
            regexp=f'{main_menu_personal_cabinet_make_promt.ID}.*'))

    db.register_message_handler(
        main_menu_personal_cabinet_make_promt.handler_2,
        state=main_menu_personal_cabinet_make_promt.MakePromt.name)

    db.register_message_handler(
        main_menu_personal_cabinet_make_promt.handler_3,
        state=main_menu_personal_cabinet_make_promt.MakePromt.text)

    # --------------------------------
    db.register_callback_query_handler(
        main_menu_personal_cabinet_delete_promt.handler,
        Regexp(
            regexp=f'{main_menu_personal_cabinet_delete_promt.ID}.*'))

    db.register_callback_query_handler(
        main_menu_personal_cabinet_delete_promt.handler_2,
        Regexp(
            regexp=f'{main_menu_personal_cabinet_delete_promt.ID_2}.*'))

    # --------------------------------

    db.register_callback_query_handler(
        main_menu_delete_commentator.handler,
        Regexp(
            regexp=f'{main_menu_delete_commentator.ID}.*'))

    db.register_callback_query_handler(
        main_menu_delete_commentator.handler_2,
        Regexp(
            regexp=f'{main_menu_delete_commentator.ID_2}.*'))

    # ----------------------------------

    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_settings_account_change_username.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_settings_account_change_username.ID}.*'))

    db.register_message_handler(main_menu_my_commentators_commentator_settings_settings_account_change_username.handler_2,
                                state=main_menu_my_commentators_commentator_settings_settings_account_change_username.ChangeUserName.username)

    # ----------------------------------
    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_leave_channel.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_leave_channel.ID}.*'))
    db.register_callback_query_handler(main_menu_my_commentators_commentator_settings_leave_channel.handler_2,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_settings_leave_channel.ID_2}.*'))
    # ------------------------------------------------
    # ------------------------------------------------

    #db.register_channel_post_handler(channel_work)
    # ------------------------------------------------
    db.register_message_handler(channel_work_chat)#, commands=['say']

    # ------------------------------------------------
    db.register_callback_query_handler(main_menu_my_commentators_commentator_transferaccount.handler,
                                       Regexp(
                                           regexp=f'{main_menu_my_commentators_commentator_transferaccount.ID}.*'))

    db.register_message_handler(main_menu_my_commentators_commentator_transferaccount.handler_2,
                                state=main_menu_my_commentators_commentator_transferaccount.TransferAccount.name)
    #-------------------------------------------------
    db.register_callback_query_handler(main_menu_consultant.handler,
                                       Regexp(
                                           regexp=f'{main_menu_consultant.ID}.*'))

    #main_menu_consultant_my_consultants
    db.register_callback_query_handler(main_menu_consultant_my_consultants.handler,
                                       Regexp(
                                           regexp=f'{main_menu_consultant_my_consultants.ID}.*'))
    #--------------------------------------------------
    db.register_callback_query_handler(
        main_menu_consultant_make_consultant.accept,
        Regexp(
            regexp=f'{main_menu_consultant_make_consultant.ID}.*'))

    db.register_callback_query_handler(
        main_menu_consultant_make_consultant.handler,
        Regexp(
            regexp=f'{main_menu_consultant_make_consultant.ID_2}.*'))

    db.register_message_handler(
        main_menu_consultant_make_consultant.handler_2,
        state=main_menu_consultant_make_consultant.MakeConsultant.channel)

    db.register_message_handler(
        main_menu_consultant_make_consultant.handler_3,
        state=main_menu_consultant_make_consultant.MakeConsultant.promt)
    #-------------------------------------------------------------------

    db.register_callback_query_handler(
        main_menu_consultant_delete_consultant.handler,
        Regexp(
            regexp=f'{main_menu_consultant_delete_consultant.ID}.*'))

    db.register_callback_query_handler(
        main_menu_consultant_delete_consultant.handler_2,
        Regexp(
            regexp=f'{main_menu_consultant_delete_consultant.ID_2}.*'))

    # -------------------------------------------------------------------
    db.register_callback_query_handler(
        main_menu_consultant_my_consultants_consultant.handler,
        Regexp(
            regexp=f'{main_menu_consultant_my_consultants_consultant.ID}.*'))

    # -------------------------------------------------------------------
    db.register_callback_query_handler(
        main_menu_consultant_my_consultants_consultant_edit.handler,
        Regexp(
            regexp=f'{main_menu_consultant_my_consultants_consultant_edit.ID}.*'))

    db.register_message_handler(
        main_menu_consultant_my_consultants_consultant_edit.handler_2,
        state=main_menu_consultant_my_consultants_consultant_edit.EditConsultant.promt)

    # -------------------------------------------------------------------

    db.register_callback_query_handler(
        main_menu_replenish_the_balance.handler,
        Regexp(
            regexp=f'{main_menu_replenish_the_balance.ID}.*'))

    db.register_pre_checkout_query_handler(
        main_menu_replenish_the_balance.checkout,lambda query: True)

    db.register_message_handler(
        main_menu_replenish_the_balance.got_payment,
        content_types=ContentTypes.SUCCESSFUL_PAYMENT)

    # -------------------------------------------------------------------


async def channel_work(message: Message):
    await message.bot.send_message(message.chat.id, f"Привет")


async def channel_work_chat(message: Message):
    if message.text[:4]=='/say' or '?' in message.text:
        #print(message.chat)

        db = message.bot.get('db')

        async with db() as session:
            consultant = await session.execute(
                select(Consultant).where(or_(Consultant.channel == message.chat.username, Consultant.channel == str(message.chat.id))))
            consultant = consultant.fetchone()

        item = message.text.replace('/say','')


        if consultant:

            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": consultant[0].promt},
                          {"role": "user", "content": f'{item}'}])
            reply_item = completion.choices[0].message.content
            await message.reply(reply_item)
