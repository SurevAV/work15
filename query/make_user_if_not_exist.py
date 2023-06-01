from sqlalchemy.future import select
from db.user import User

async def make_user(db, user_id, username = 'None'):
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(user_id)))
        if not user.fetchone():
            session.add(User(name=username,
                             idTelegram=str(user_id),
                             phone='0',
                             is_admin=False,
                             balance=1000))
            await session.commit()