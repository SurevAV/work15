from sqlalchemy import select, update
from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from aiogram import types
from data import Config
from db.user import User


prices = [
    types.LabeledPrice(label='Working Time Machine', amount=5750),
]


ID = str(uuid.uuid4())[:5]

async def handler(call: CallbackQuery):
    #call.from_user.id)
    await call.bot.send_invoice(call.from_user.id, title='Пополнение баланса',
                           description='Пополните баланс для использования комментаторов и консультантов.',
                           provider_token=Config.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           photo_url='https://telegra.ph/file/2c1f7fc68ad31a7415a7c.jpg',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='replenish-the-balance',
                           payload='ОПЛАТА')


async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")



async def got_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()

    db = message.bot.get('db')
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(message.from_user.id)))
        user = user.fetchone()[0]

    async with db() as session:
        await session.execute(update(User).values({User.balance: payment_info['total_amount']+user.balance}).where(
            User.idTelegram == str(message.from_user.id)))
        await session.commit()

    await message.bot.send_message(message.chat.id,f"Ваш баланс пополнен на сумму - {payment_info['total_amount']/100} рублей.",
                                parse_mode='Markdown', reply_markup=make_keyboard([],'return_to_main_menu'))