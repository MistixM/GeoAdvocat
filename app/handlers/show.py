from aiogram import types, Router
from aiogram.filters import Command
from app.utils.functions import admin_only

import configparser

show_router = Router()

@show_router.message(Command(commands=['show']))
@admin_only()
async def handle_show(msg: types.Message):
    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    statistic = ("✍🏻 Here's the current configuration: \n\n"
                  f"<b>System topic prompt:</b> <code>{config['Bot']['system_topic_prompt']}</code>\n\n"
                  f"<b>System comment prompt:</b> <code>{config['Bot']['system_comment_prompt']}</code>\n\n"
                  f"<b>Current queries:</b> <code>{config['Bot']['queries']}</code>\n"
                )

    await msg.answer(statistic)