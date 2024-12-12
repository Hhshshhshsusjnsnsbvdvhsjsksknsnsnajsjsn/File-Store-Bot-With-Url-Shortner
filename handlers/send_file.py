import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

async def media_forward(bot: Client, user_id: int, file_id: int):
    """
    Forwards or copies a media message to a user.
    """
    try:
        if Config.FORWARD_AS_COPY:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        else:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media(bot: Client, user_id: int, file_id: int):
    """
    Forwards media and schedules it for deletion after 30 minutes.
    """
    # Forward the media
    sent_message = await media_forward(bot, user_id, file_id)

    # Schedule the message for deletion after 30 minutes
    asyncio.create_task(delete_after_delay(sent_message, 1800))

async def delete_after_delay(message: Message, delay: int):
    """
    Deletes a message after a specified delay (in seconds).
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
