from sqlalchemy import select, update

from keyboards.keyboards import *
from aiogram.types import CallbackQuery
import uuid
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor
from data import Config
from db.user import User



# Setup prices
prices = [
    types.LabeledPrice(label='Working Time Machine', amount=5750),
    types.LabeledPrice(label='Gift wrapping', amount=500),
]

# Setup shipping options
shipping_options = [
    types.ShippingOption(id='instant', title='WorldWide Teleporter').add(types.LabeledPrice('Teleporter', 1000)),
    types.ShippingOption(id='pickup', title='Local pickup').add(types.LabeledPrice('Pickup', 300)),
]

ID = str(uuid.uuid4())[:5]


async def handler(call: CallbackQuery):
    #call.from_user.id)
    await call.bot.send_invoice(call.from_user.id, title='Working Time Machine',
                           description='Want to visit your great-great-great-grandparents?'
                                       ' Make a fortune at the races?'
                                       ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
                                       ' Order our Working Time Machine today!',
                           provider_token=Config.PAYMENTS_PROVIDER_TOKEN,
                           currency='usd',
                           photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')

    #await call.message.answer("Для возврата в главное меню нажмите - назад", reply_markup=make_keyboard([], 'return_to_main_menu'))



#@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


#@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()
    print(payment_info['total_amount'])

    db = message.bot.get('db')
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(message.from_user.id)))
        user = user.fetchone()[0]

    async with db() as session:
        await session.execute(update(User).values({User.balance: payment_info['total_amount']+user.balance}).where(
            User.idTelegram == str(message.from_user.id)))
        await session.commit()

 


    await message.bot.send_message(message.chat.id,
                           'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                           ' as fast as possible! Stay in touch.'
                           '\n\nUse /buy again to get a Time Machine for your friend!'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment.currency),
                           parse_mode='Markdown')