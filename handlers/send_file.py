import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config

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

async def send_media_and_reply(bot: Client, user_id: int, file_ids: list[int]):
    """
    Forward all media files, send a single reply to one message, and delete all after 30 minutes.
    """
    sent_messages = []  # Keep track of all sent messages
    reply_sent = False  # Track if the reply has already been sent

    for file_id in file_ids:
        sent_message = await media_forward(bot, user_id, file_id)
        if isinstance(sent_message, Message):
            sent_messages.append(sent_message)

            # Send the reply only for the first message
            if not reply_sent:
                try:
                    await sent_message.reply_text(
                        "Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
                        disable_web_page_preview=True,
                        quote=True
                    )
                    reply_sent = True
                except FloodWait as e:
                    await asyncio.sleep(e.value)

    # Schedule all messages for deletion after 30 minutes
    for message in sent_messages:
        asyncio.create_task(delete_after_delay(message, 1800))

async def delete_after_delay(message: Message, delay: int):
    """
    Deletes a message after a specified delay (in seconds).
    """
    await asyncio.sleep(d
