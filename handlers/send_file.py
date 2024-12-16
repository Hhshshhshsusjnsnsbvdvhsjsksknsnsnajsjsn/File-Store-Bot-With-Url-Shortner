import asyncio
import requests
import string
import random
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

async def send_reply_text(bot: Client, user_id: int):
    try:
        await bot.send_message(
            chat_id=user_id,
            text="Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
            disable_web_page_preview=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await send_reply_text(bot, user_id)

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        else:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    # Forward the media message
    sent_message = await media_forward(bot, user_id, file_id)

    # Schedule deletion for the forwarded media
    asyncio.create_task(delete_after_delay(sent_message, 1800))

    # Wait 5 seconds before sending the reply text
    await asyncio.sleep(5)
    await send_reply_text(bot, user_id)

async def delete_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()
