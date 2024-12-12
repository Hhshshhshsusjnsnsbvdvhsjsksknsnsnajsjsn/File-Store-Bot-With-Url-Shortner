import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config

async def reply_forward(message: Message):
    try:
        reply_message = await message.reply_text(
            "Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
            disable_web_page_preview=True,
            quote=True
        )
        return reply_message
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await reply_forward(message)

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        else:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    # Send media
    sent_message = await media_forward(bot, user_id, file_id)
    if isinstance(sent_message, Message):
        # Send reply to the media
        reply_message = await reply_forward(message=sent_message)
        # Schedule both messages for deletion after 30 minutes
        asyncio.create_task(delete_after_delay(sent_message, 1800))
        asyncio.create_task(delete_after_delay(reply_message, 1800))

async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
