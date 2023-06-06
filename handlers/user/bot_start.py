import uuid
from keyboards.keyboards import *
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from query.make_user_if_not_exist import *
from . import main_menu_personal_cabinet
from . import main_menu_my_commentators
from . import main_menu_delete_commentator
from . import main_menu_instruction
from . import main_menu_consultant
from . import main_menu_replenish_the_balance

ID = str(uuid.uuid4())[:5]

async def handler(msg: Message, state: FSMContext):
    await state.finish()

    db = msg.bot.get('db')

    await make_user(db, msg.from_user.id, msg.from_user.username)

    list_buttons = (
        ("Личный кабинет", f'{main_menu_personal_cabinet.ID}'),
        ("Мои комментаторы", f'{main_menu_my_commentators.ID}'),
        ("Консультант", f'{main_menu_consultant.ID}'),
        ("Пополнить баланс", f'{main_menu_replenish_the_balance.ID}'),
        ("Инструкция", f'{main_menu_instruction.ID}')
    )#("Удалить комментатора", f'{main_menu_delete_commentator.ID}'),

    db = msg.bot.get('db')
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(msg.from_user.id)))
        user = user.fetchone()[0]

    await msg.answer(f"Приветсвую выберете раздел. Ваш баланс {str(user.balance/100)} рублей", reply_markup=make_keyboard(list_buttons))