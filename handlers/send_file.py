import asyncio
import requests
import string
import random
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

sent_messages = []

async def send_direct_message(bot: Client, user_id: int):
    """This sends a direct message instead of a reply."""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "🎬 𝙁𝙞𝙡𝙚𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙙𝙚𝙡𝙚𝙩𝙚𝙙 𝙞𝙣 60 𝙢𝙞𝙣𝙪𝙩𝙚𝙨 𝙩𝙤 𝙖𝙫𝙤𝙞𝙙 𝙘𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙞𝙨𝙨𝙪𝙚𝙨..."
            ),
            disable_web_page_preview=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await send_direct_message(bot, user_id)

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                          message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, user_id, file_id)
        await message.delete()

async def send_media_and_reply(bot: Client, user_id: int, file_id: int, is_last: bool = False):
    global sent_messages
    sent_message = await media_forward(bot, user_id, file_id)
    if sent_message:
        sent_messages.append(sent_message.id)
    if is_last:
        await send_direct_message(bot, user_id)
        asyncio.create_task(delete_after_delay(bot, user_id, sent_messages, 10))
        
async def delete_after_delay(bot: Client, chat_id: int, message_ids: list, delay: int):
    await asyncio.sleep(delay)

    try:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
        print(f"Deleted messages: {message_ids}")
    except Exception as e:
        print(f"Failed to delete messages: {e}")
