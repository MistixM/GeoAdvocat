from aiogram import types, Router
from aiogram.filters import Command
from app.utils.functions import admin_only

import configparser

change_topic = Router()

@change_topic.message(Command(commands=['change_topic_prompt']))
@admin_only()
async def handle_topic_change(msg: types.Message):
    parts = msg.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await msg.answer("Please provide a prompt as an argument.")
        return
    
    prompt = parts[1].strip()

    if '"' not in prompt:
        await msg.answer('Please include " at the start and end of the text prompt. For quotes inside use single quotes.')
        return
    
    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    config['Bot']['system_topic_prompt'] = prompt

    with open('app/constants/config.ini', 'w') as configfile:
        config.write(configfile)

    await msg.answer("✅ Topic system prompt has been changed!")