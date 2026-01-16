from aiogram import types, Router
from aiogram.filters import Command
from app.utils.functions import admin_only

help_router = Router()

@help_router.message(Command(commands=['help']))
@admin_only()
async def handle_help(msg: types.Message):
    await msg.answer(f"""📝 Available commands: \n/start – start the bot\n/launch – launch Threads commenting bot\n/stop – stop Threads commenting bot\n/change_topic_prompt [insert prompt] – change system prompt for topic detection if necessary\n/change_comment_prompt [insert prompt] – change system prompt for comment if necessary\n/change_queries [insert list of queries; use coma as separator] – these queries are used for Threads search. Hit this command if you'd like to change them\n/show – show current setup (the bot will show system prompts for AI and queries)""")

