import db
from db.commentator import Commentator
from telethon import TelegramClient
from sqlalchemy.future import select
import asyncio
from telethon.sessions import StringSession

#uk3030220:RO52gHRJbm@77.83.1.129:7953
api_id = 28942694

api_hash = '1dfb2e23e32bf557c49f4ba300278804'

phone = '447506039259'

user_name = 'pirat10005000'

proxyHttp = 'Http'

proxyIp =  '77.83.1.244'

proxyPort = 7953

proxyPass = 'RO52gHRJbm'

proxyUser = 'uk3030220'

proxy = {
    'proxy_type': proxyHttp,
    'addr': proxyIp,
    'port': proxyPort,
    'username': proxyUser,
    'password': proxyPass,
    'rdns': False
}
async def main():
    app = TelegramClient(phone,  api_id=api_id, api_hash=api_hash, proxy=proxy) #proxy=(proxyHttp, proxyIp, proxyPort, proxyPass, proxyUser)
    await app.start(phone = phone,password="parol15") #password="parol15"

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
                                     stringConnection = StringSession.save(app.session)))
             await session.commit()


    #app.add_event_handler(make_reply,events.NewMessage())

    await app.run_until_disconnected()

asyncio.run(main())
