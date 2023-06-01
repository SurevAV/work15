import db
from db.commentator import Commentator
from telethon import TelegramClient
from sqlalchemy.future import select
import asyncio
from telethon.sessions import StringSession



api_id = 22134742

api_hash = '454f6c39f163cc03915b3a2c8140413c'

phone = '79952176761'

user_name = 'username2user5'

proxyHttp = 'Http'

proxyIp =  '194.169.161.79'

proxyPort = 8148

proxyPass = '7l16r3'

proxyUser = 'user109441'

stringConnection =''
async def main():


    connect = await db.setup()

    async with connect() as session:
        commentator = await session.execute(select(Commentator).where(Commentator.phone == phone))
        if not commentator.fetchone():
             session.add(Commentator(name=user_name,
                                     phone=phone,
                                     usage = True,
                                     promt = '-',
                                     channels = ',',
                                     owner = '773281550',
                                     apiId = api_id,
                                     apiHash= api_hash,
                                     proxyHttp=proxyHttp,
                                     proxyIp = proxyIp,
                                     proxyPort = proxyPort,
                                     proxyPass = proxyPass,
                                     proxyUser = proxyUser,
                                     stringConnection = stringConnection))
             await session.commit()



asyncio.run(main())
