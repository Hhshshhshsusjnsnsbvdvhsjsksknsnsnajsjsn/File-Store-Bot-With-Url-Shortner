import asyncio
import logging
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from configs import Config

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sent_messages = []


async def send_direct_message(bot: Client, user_id: int):
    """Sends a direct message with an inline button."""
    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💯 Earning Money 🤑", url="https://t.me/+MxH5jcG5cek5OWNl")]
        ])
        await bot.send_message(
            chat_id=user_id,
            text=(
                "🎬 𝙁𝙞𝙡𝙚𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙙𝙚𝙡𝙚𝙩𝙚𝙙 𝙞𝙣 1 𝙢𝙞𝙣𝙪𝙩𝙚 𝙩𝙤 𝙖𝙫𝙤𝙞𝙙 𝙘𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙞𝙨𝙨𝙪𝙚𝙨..\n"
                "<b>Best Colour Tranding Platform for Fast deposit and Withdrawl Since 5 Year old ☠️</b>"
            ),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    except FloodWait as e:
        logger.warning(f"FloodWait encountered: sleeping for {e.x} seconds.")
        await asyncio.sleep(e.x)
        await send_direct_message(bot, user_id)
    except Exception as e:
        logger.error(f"Error sending direct message: {e}")


async def media_forward(bot: Client, user_id: int, file_id: int):
    """Forwards or copies a message to the user."""
    try:
        if Config.FORWARD_AS_COPY:
            sent_message = await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        else:
            sent_message = await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)

        return sent_message
    except FloodWait as e:
        logger.warning(f"FloodWait during forwarding: sleeping for {e.x} seconds.")
        await asyncio.sleep(e.x)
        return await media_forward(bot, user_id, file_id)
    except Exception as e:
        logger.error(f"Error in media_forward: {e}")
        return None


async def send_media_and_reply(bot: Client, user_id: int, file_id: int, is_last: bool = False):
    """Sends media to a user and replies with a direct message."""
    global sent_messages
    sent_message = await media_forward(bot, user_id, file_id)

    if sent_message:
        sent_messages.append(sent_message.id)

    if is_last:
        await send_direct_message(bot, user_id)
        asyncio.create_task(delete_after_delay(bot, user_id, sent_messages, 10))


async def delete_after_delay(bot: Client, chat_id: int, message_ids: list, delay: int):
    """Deletes messages after a specified delay."""
    await asyncio.sleep(delay)

    try:
        if message_ids:
            await bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
            logger.info(f"Deleted messages: {message_ids}")
        else:
            logger.info("No messages to delete.")
    except Exception as e:
        logger.error(f"Failed to delete messages: {e}")
