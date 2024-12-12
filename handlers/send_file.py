import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_ids: list):
    # List to hold sent messages
    sent_messages = []
    
    # Send all files
    for file_id in file_ids:
        sent_message = await media_forward(bot, user_id, file_id)
        sent_messages.append(sent_message)
        # Schedule deletion of each message
        asyncio.create_task(delete_after_delay(sent_message, 1800))

    # Send the final important message after all files have been sent
    try:
        await bot.send_message(
            chat_id=user_id,
            text="Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
            disable_web_page_preview=True
        )
    except FloodWait as e:
        print(f"FloodWait encountered while sending important message: {e.x} seconds")
        await asyncio.sleep(e.x)
        await send_media_and_reply(bot, user_id, file_ids)  # Retry if FloodWait occurs

async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()
