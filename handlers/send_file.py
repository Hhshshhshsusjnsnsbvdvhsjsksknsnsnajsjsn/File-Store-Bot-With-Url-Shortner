import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

async def media_forward(bot: Client, user_id: int, file_id: int):
    """
    Forward or copy a media message to a user.
    """
    try:
        if Config.FORWARD_AS_COPY:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        else:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_ids: list[int], important_message: str):
    """
    Forward all media files, then send a single important message at the end, 
    and schedule deletion of all messages after 30 minutes.
    """
    sent_messages = []  # Keep track of all sent messages

    # Forward all media files to the user
    for file_id in file_ids:
        sent_message = await media_forward(bot, user_id, file_id)
        if isinstance(sent_message, Message):
            sent_messages.append(sent_message)

    # Send the important message after all media has been sent
    important_message_sent = await bot.send_message(chat_id=user_id, text=important_message)
    sent_messages.append(important_message_sent)  # Add the important message to the list

    # Schedule deletion of all messages after 30 minutes
    for message in sent_messages:
        asyncio.create_task(delete_after_delay(message, 1800))

async def delete_after_delay(message: Message, delay: int):
    """
    Deletes a message after a specified delay (in seconds).
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
