import logging
from aiogram import executor
from sqlalchemy.util import asyncio

from bot.handlers import *
from db import db


async def create_all():
    await db.create_all()





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_all())
    executor.start_polling(dp, skip_updates=True)