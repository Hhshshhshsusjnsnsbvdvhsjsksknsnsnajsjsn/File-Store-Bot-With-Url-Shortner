import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config

async def reply_forward(bot: Client, user_id: int):
    """
    Send a reply text to the user.
    """
    try:
        reply_message = await bot.send_message(
            chat_id=user_id,
            text="Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
            disable_web_page_preview=True
        )
        return reply_message
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await reply_forward(bot, user_id)

async def media_forward(bot: Client, user_id: int, file_id: int):
    """
    Forward or copy a single media file.
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
    Send all media files and a single reply text, deleting both after 30 minutes.
    """
    # Ensure file_ids is a list
    if not isinstance(file_ids, list):
        file_ids = [file_ids]

    # Track messages to delete
    messages_to_delete = []

    # Forward all media files
    for file_id in file_ids:
        sent_message = await media_forward(bot, user_id, file_id)
        if isinstance(sent_message, Message):
            messages_to_delete.append(sent_message)

    # Send the reply text only once
    if messages_to_delete:
        reply_message = await reply_forward(bot, user_id)
        messages_to_delete.append(reply_message)

    # Schedule all messages for deletion after 30 minutes
    for message in messages_to_delete:
        asyncio.create_task(delete_after_delay(message, 1800))

async def delete_after_delay(message: Message, delay: int):
    """
    Deletes a message after a specified delay.
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
