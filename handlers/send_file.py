import asyncio
import requests
import string
import random
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

async def reply_forward(message: Message):
    try:
        await message.reply_text(
            "Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
            disable_web_page_preview=True,
            quote=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await reply_forward(message)

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        else:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    # Forward all media messages first
    sent_messages = []
    for file_id in file_ids:
        sent_message = await media_forward(bot, user_id, file_id)
        sent_messages.append(sent_message)

    # Reply to the last sent message
    if sent_messages:
        await reply_forward(sent_messages[-1])

    # Schedule deletion for all sent messages
    for message in sent_messages:
        asyncio.create_task(delete_after_delay(message, 1800))

async def delete_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()
