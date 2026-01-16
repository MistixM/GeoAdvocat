from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from app.utils.functions import admin_only

import configparser

start_router = Router()


@start_router.message(CommandStart())
@admin_only()
async def handle_start(msg: types.Message):
    full_name = msg.from_user.full_name

    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    await msg.answer(f"<b>Hello, {full_name}!</b> 👋🏻\n\nI'm here to help you with the threads automation 🙂 Before you start please read carefully about available commands with using /help command.")

