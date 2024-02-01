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
            f"𝙁𝙞𝙡𝙚𝙨 𝙒𝙞𝙡𝙡 𝘽𝙚 𝘿𝙚𝙡𝙚𝙩𝙚𝙙 𝙄𝙣 𝟲 𝙃𝙤𝙪𝙧'𝙨⌛ 𝙏𝙤 𝘼𝙫𝙤𝙞𝙙 𝘾𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙄𝙨𝙨𝙪𝙚.𝙋𝙡𝙚𝙖𝙨𝙚 𝙁𝙤𝙧𝙬𝙖𝙧𝙙 𝘼𝙣𝙙 𝙎𝙖𝙫𝙚 𝙏𝙝𝙚𝙢
कॉपीराइट समस्याओं से बचने के लिए फ़ाइलें 𝟲 घंटे  में हटा दी जाएंगी। कृपया Movie को  सेव करें या डाउनलोड कर ले या किसी को भेज दे।.",
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
    asyncio.create_task(delete_after_delay(sent_message, 21600))

async def delete_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()
