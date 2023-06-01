from sqlalchemy.future import select
from db.user import User

async def user_is_admin(db, user_id):
    async with db() as session:
        user = await session.execute(select(User).where(User.idTelegram == str(user_id)))
        user = user.fetchone()
    return user[0].is_admin