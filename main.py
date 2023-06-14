from telethon import TelegramClient, events
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import db
import handlers
import openai
from db.commentator import Commentator
from sqlalchemy.future import select
from sqlalchemy import update
from telethon.sessions import StringSession
from datetime import datetime
import os
from data import Config
import uuid
from random import choice
import random

class orhestra():
    def __init__(self):

        self.dict_commentators = {}
        self.db = None

    async def main(self):
        logging.basicConfig(level=logging.INFO)
        bot = Bot(Config.BOT_TOKEN, validate_token=True)
        openai.api_key = Config.OPENAI_API_KEY
        bot["openai"] = openai

        bot["orhestra"] = self.dict_commentators
        bot["user_settings"] = {}

        bot['db'] = await db.setup()
        self.db = bot['db']

        dp = Dispatcher(bot, storage=MemoryStorage())

        handlers.user.setup(dp)

        await dp.start_polling(bot)

    def write_file(self, name_file, text):
        name_file = name_file.replace(':', '-')
        with open(os.path.join('replys', name_file), 'w', encoding='utf-8') as f:
            f.write(text)



    async def make_reply(self, event):
        try:
            commentator_client = await event.client.get_entity("me")
        except Exception as e:
            self.write_file(f'error_name-{str(datetime.now())[:19]}-{str(uuid.uuid4())}.txt', f'name error')

        try:
            async with self.db() as session:
                commentator = await session.execute(
                    select(Commentator).where(Commentator.name == commentator_client.username))
                commentator = commentator.fetchone()[0]


            if commentator.untilDate>=datetime.now():

                list_channels = commentator.channels#.split(',')
                if event.chat.username.lower() in list_channels.lower():
                    openai.api_key = Config.OPENAI_API_KEY
                    if commentator.is_humanity:
                        await asyncio.sleep(random.randint(1, 2))

                    completion = await openai.ChatCompletion.acreate(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": f'{commentator.promt} : {event.message.text}'}])
                    reply_item = completion.choices[0].message.content

                    if commentator.is_humanity:
                        reply_item = reply_item.replace(',','')
                        reply_item = reply_item.lower()

                        reply_item = list(reply_item)
                        for i in range(2):
                            reply_item[random.randint(0, len(reply_item) - 1)] = choice("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

                        reply_item = ''.join(reply_item)

                    await event.client.send_message(entity=event.message.peer_id, message=reply_item,
                                                        comment_to=event.message.id)

                    self.write_file( f'ok-{event.chat.username.lower()}-{commentator_client.username}-{str(datetime.now())[:19]}-{str(uuid.uuid4())}.txt',
                        f'{commentator_client.username} - {reply_item} - {event.message.text} - {str(event)}')

            # else:
            #
            #     name_file = f'no-{event.chat.username.lower()}-{str(datetime.now())[:19]}-{str(uuid.uuid4())}.txt'
            #     name_file = name_file.replace(':', '-')
            #     with open(os.path.join('replys', name_file), 'w', encoding='utf-8') as f:
            #         f.write(f'{event.chat.username.lower()} - {event.message.text} - {list_channels.lower()}')

        except Exception as e:
            try:
                self.write_file(f'error-{event.chat.username.lower()}-{commentator_client.username}-{str(datetime.now())[:19]}-{str(uuid.uuid4())}.txt',
                                f'{str(e)} - {event.message.text} - {str(event)}')
                print(str(e))

                if 'banned' in str(e):

                    try:
                        commentator_client = await event.client.get_entity("me")

                        async with self.db() as session:
                            commentator_row = await session.execute(select(Commentator).where(Commentator.name == commentator_client.username))
                            commentator_row = commentator_row.fetchone()[0]

                        commentator_row = commentator_row.channels.lower()
                        commentator_row = commentator_row.replace(event.chat.username.lower(), '')
                        commentator_row = commentator_row.replace('https://t.me/', '')

                        async with self.db() as session:
                            await session.execute(
                                update(Commentator).values({Commentator.channels: commentator_row}).where(
                                    Commentator.name == commentator_client.username))
                            await session.commit()
                    except Exception as e:
                        self.write_file(f'error_leave-{str(datetime.now())[:19]}-{str(uuid.uuid4())}.txt', f'leave error{str(e)}')

            except Exception as e2:

                self.write_file(f'error2-{commentator_client.username}-{str(datetime.now())[:19]}-{str(uuid.uuid4())}.txt',
                    f'{str(e)} - {str(e2)} - {str(event)}')




    async def run_client(self, commentator):

        proxy = {
             'proxy_type': commentator.proxyHttp,
             'addr': commentator.proxyIp,
             'port': commentator.proxyPort,
             'username': commentator.proxyUser,
             'password': commentator.proxyPass,
             'rdns': True
         }

        self.dict_commentators[commentator.phone] = await TelegramClient(StringSession(commentator.stringConnection),
                                                                         api_id=commentator.apiId,
                                                                         api_hash=commentator.apiHash,
                                                                         proxy = proxy,
                                                                         device_model = str(uuid.uuid4()),
                                                                         system_version = str(uuid.uuid4()),


                                                                         ).start('0',password="parol15") #proxy=(commentator.proxyHttp,commentator.proxyIp, commentator.proxyPort,commentator.proxyPass,commentator.proxyUser)
        #exist_user = await self.dict_commentators[commentator.phone].get_entity("me")

        await self.dict_commentators[commentator.phone].add_event_handler(self.make_reply, events.NewMessage())
        await self.dict_commentators[commentator.phone].run_until_disconnected()

    async def start_pool(self):
        connect = await db.setup()
        async with connect() as session:
            commentators = await session.execute(select(Commentator).where(Commentator.usage == True))
            commentators = commentators.fetchall()
        list_commentators = [commentator[0] for commentator in commentators]
        #print(list_commentators)


        loop = asyncio.get_event_loop()


        list_tasks = [loop.create_task(self.main())]
        for commentator in list_commentators:
            list_tasks.append(loop.create_task(self.run_client(commentator)))

        await asyncio.wait(list_tasks)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_pool())
        loop.close()


server = orhestra()
server.run()
