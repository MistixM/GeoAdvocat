from aiogram import types, Router
from aiogram.filters import Command
from app.utils.functions import admin_only

import configparser

change_queries_router = Router()

@change_queries_router.message(Command(commands=['change_queries']))
@admin_only()
async def handle_topic_change(msg: types.Message):
    parts = msg.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await msg.answer("Please provide a query/queries as an argument.")
        return
    
    prompt = parts[1].strip()

    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    config['Bot']['queries'] = prompt

    with open('app/constants/config.ini', 'w') as configfile:
        config.write(configfile)

    await msg.answer("✅ Queries has been changed!")