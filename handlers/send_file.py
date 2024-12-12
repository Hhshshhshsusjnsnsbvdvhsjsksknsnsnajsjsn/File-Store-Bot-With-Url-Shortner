import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config

async def reply_forward(message: Message):
    """
    Sends a reply message and informs about the 30-minute deletion policy.
    """
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

async def send_media_and_reply(bot: Client, user_id: int, file_ids: list[int]):
    """
    Forwards all media files, sends a reply to the last media, and schedules both for deletion after 30 minutes.
    """
    last_sent_message = None  # To track the last forwarded message

    # Forward the media files
    for file_id in file_ids:
        sent_message = await media_forward(bot, user_id, file_id)
        if isinstance(sent_message, Message):
            last_sent_message = sent_message  # Keep track of the last sent message

    # Send reply to the last forwarded message
    if last_sent_message:
        await reply_forward(message=last_sent_message)

    # Schedule both the media and the reply for deletion after 30 minutes
    if last_sent_message:
        asyncio.create_task(delete_after_delay(last_sent_message, 1800))

async def delete_after_delay(message: Message, delay: int):
    """
    Deletes a message after a specified delay (in seconds).
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
