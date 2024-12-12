import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# Variable to store the last sent message
last_sent_message = None

async def reply_forward():
    global last_sent_message
    if last_sent_message is not None:
        try:
            await last_sent_message.reply_text(
                f"Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
                disable_web_page_preview=True,
                quote=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await reply_forward()  # Retry if FloodWait occurs
        except Exception as e:
            print(f"Error while sending reply: {e}")  # Catch all other exceptions

async def media_forward(bot: Client, user_id: int, file_id: int):
    global last_sent_message  # Declare it as global to modify
    try:
        if Config.FORWARD_AS_COPY is True:
            last_sent_message = await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            last_sent_message = await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL, message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_ids: list):
    # Send all files
    for file_id in file_ids:
        await media_forward(bot, user_id, file_id)

    # Send reply text to the last sent message
    await reply_forward()

    # Schedule deletion of the last sent message
    if last_sent_message:
        asyncio.create_task(delete_after_delay(last_sent_message, 1800))

async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()
