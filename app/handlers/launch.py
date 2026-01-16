from aiogram import Router, types
from aiogram.filters import Command

import asyncio
import configparser
import random
import logging

from app.database.db import save_cursor, load_cursor, check_post, add_post, create_connection
from app.utils.functions import search_posts, check_topic, comment_post, admin_only, generate_comment

launch_router = Router()

task = None

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='debug.log',  
    filemode='a'
) 

@launch_router.message(Command(commands=['launch']))
@admin_only()
async def handle_launch(msg: types.Message):
    global task

    if task and not task.done():
        await msg.answer("👀 Bot is already running!")
        return

    await msg.answer('✅ Bot started in the background!')

    task = asyncio.create_task(background_worker(msg))


@launch_router.message(Command(commands=['stop']))
@admin_only()
async def handle_stop(msg: types.Message):
    global task

    if task and not task.done():
        task.cancel()
        await msg.answer("🛑 Bot stopped")
    else:
        await msg.answer("ℹ️ Bot is not running")


async def background_worker(msg):
    config = configparser.ConfigParser(interpolation=None)
    config.read('app/constants/config.ini')

    while True:

        logging.info('Iteration started')

        conn = create_connection('data.db')

        end_cursor = load_cursor(conn)
        queries = config['Bot']['queries']
        queries_list = queries.split(',')
        query_choice = random.choice(queries_list)

        posts = search_posts(query=query_choice,
                             end_cursor=end_cursor, 
                             limit=10
        )

        if posts:
            edges = posts['data']['searchResults']['edges']

            for edge in edges:
                
                post = edge['node']['thread']['thread_items'][0]['post']
                pk = post['pk']
                caption = post['caption']

                if check_post(conn, pk):
                    continue

                add_post(conn, pk)

                topic = check_topic(caption)
                
                if topic and topic.strip().lower() != 'true':
                    continue
                
                generated_comment = generate_comment(caption)

                logging.info(generated_comment)

                try:
                    comment_post(post_pk=pk, text=generated_comment)                     
                except Exception as e:
                    await msg.answer("Can't publish comment.. probably it has too many words. For more info please reach out to the debug file")
                    logging.error(e)
                    continue

                await asyncio.sleep(random.randint(10, 15))
            
            end_cursor = posts['data']['searchResults']['page_info']['end_cursor']

            save_cursor(conn, end_cursor)

            logging.info("Cursor saved. Need to wait for a while..")

            conn.close()
            await asyncio.sleep(random.randint(900, 1200))
        else:
            await asyncio.sleep(90)