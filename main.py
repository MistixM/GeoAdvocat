import asyncio
import configparser
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.handlers import routers

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='debug.log',  
    filemode='a'
) 

async def main():
    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    bot = Bot(token=config['Bot']['TOKEN'], default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info('Bot started.')
    asyncio.run(main())
    logging.info('Bot stopped.')