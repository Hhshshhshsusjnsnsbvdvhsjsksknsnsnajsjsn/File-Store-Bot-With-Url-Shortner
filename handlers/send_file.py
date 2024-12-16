import asyncio
import requests
import string
import random
from configs import Config
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

sent_messages = []

async def send_direct_message(bot: Client, user_id: int):
    """This sends a direct message with an inline button for the link."""
    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💯 Earning Money 🤑", url="https://t.me/+MxH5jcG5cek5OWNl")]
        ])
        
        message = await bot.send_message(
            chat_id=user_id,
            text=(
                "🎬 𝙁𝙞𝙡𝙚𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙙𝙚𝙡𝙚𝙩𝙚𝙙 𝙞𝙣 1 𝙢𝙞𝙣𝙪𝙩𝙚 𝙩𝙤 𝙖𝙫𝙤𝙞𝙙 𝙘𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙞𝙨𝙨𝙪𝙚𝙨..\n<b>Best Colour Tranding Platform for Fast deposit and Withdrawl Since 5 Year old ☠️</b>"
            ),
            reply_markup=keyboard,  
            disable_web_page_preview=True  
        )
        
        return message  # Return the message object to track its ID

    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_direct_message(bot, user_id)

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            sent_message = await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            sent_message = await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)

        return sent_message

    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await media_forward(bot, user_id, file_id)
    except Exception as e:
        print(f"Error in media_forward: {e}")
        return None

async def send_media_and_reply(bot: Client, user_id: int, file_id: int, is_last: bool = False):
    global sent_messages
    sent_message = await media_forward(bot, user_id, file_id)

    if sent_message:
        sent_messages.append(sent_message.id)  # Track forwarded message IDs

    if is_last:
        direct_message = await send_direct_message(bot, user_id)  # Send direct message
        if direct_message:
            asyncio.create_task(delete_after_delay(bot, user_id, [direct_message.id], 1800))  # Delete after 30 minutes
        asyncio.create_task(delete_after_delay(bot, user_id, sent_messages, 3600))  # Delete media messages after 1 hour

async def delete_after_delay(bot: Client, chat_id: int, message_ids: list, delay: int):
    await asyncio.sleep(delay)
    try:
        if message_ids:  
            await bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
            print(f"Deleted messages: {message_ids}")
        else:
            print("No messages to delete.")
    except Exception as e:
        print(f"Failed to delete messages: {e}")
