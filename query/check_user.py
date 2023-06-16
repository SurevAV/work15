from sqlalchemy import update
from sqlalchemy.future import select
from db.user import User

async def user_is_admin(db, user_id):
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(user_id)))
        user = user.fetchone()
    return user[0].is_admin

async def get_user(db, user_id):
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(user_id)))
        user = user.fetchone()
    return user[0]

async def change_user_balance(db, user_id, cost):
    user = await get_user(db, user_id)
    async with db() as session:
        await session.execute(update(User).values({User.balance: user.balance - cost}).where(
            User.idTelegram == str(user_id)))
        await session.commit()