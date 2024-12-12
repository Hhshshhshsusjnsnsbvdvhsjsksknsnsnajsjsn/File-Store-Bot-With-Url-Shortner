import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# A set to keep track of users who have already received the reply
replied_users = set()

async def reply_forward(message: Message, file_id: int):
    global replied_users
    user_id = message.from_user.id  # Get the user ID from the message

    # Check if the user has already received the reply for this file
    if user_id not in replied_users:
        try:
            await message.reply_text(
                f"Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
                disable_web_page_preview=True,
                quote=True
            )
            replied_users.add(user_id)  # Mark this user as having received the reply
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await reply_forward(message, file_id)  # Retry if FloodWait occurs

async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                          message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
    asyncio.create_task(delete_after_delay(sent_message, 1800))

async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()
