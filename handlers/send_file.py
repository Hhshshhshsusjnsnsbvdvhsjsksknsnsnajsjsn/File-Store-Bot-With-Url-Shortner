import asyncio
import requests
import string
import random
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"𝙵𝚒𝚕𝚕 𝚠𝚒𝚕𝚕 𝚋𝚎 𝙳𝚎𝚕𝚎𝚝𝚎𝚍 𝚒𝚗 𝟭 𝗛𝗼𝘂𝗿'𝘀⌛ 𝚝𝚘 𝚊𝚟𝚘𝚒𝚍 𝚌𝚘𝚙𝚢𝚛𝚒𝚐𝚑𝚝 𝚒𝚜𝚜𝚞𝚎𝚜. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗙𝗼𝗿𝘄𝗮𝗿𝗱 𝚊𝚗𝚍 𝚜𝚊𝚟𝚎 𝚝𝚑𝚎𝚖. ㅤ ㅤ𝙅𝙤𝙞𝙣 👉 @qtmovie.",
            disable_web_page_preview=True,
            quote=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await reply_forward(message, file_id)

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

async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
    asyncio.create_task(delete_after_delay(sent_message, 3600))

async def delete_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()
