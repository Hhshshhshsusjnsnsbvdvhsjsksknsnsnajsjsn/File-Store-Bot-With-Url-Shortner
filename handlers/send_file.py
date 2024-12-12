import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# A set to keep track of users who have already received the reply
replied_users = set()

# Variable to store the last sent message
last_sent_message = None

async def reply_forward(user_id: int):
    global replied_users, last_sent_message
    # Check if the last sent message exists
    if last_sent_message and user_id not in replied_users:
        try:
            print(f"Sending reply to user_id: {user_id}")  # Debugging line
            await last_sent_message.reply_text(
                f"Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
                disable_web_page_preview=True,
                quote=True
            )
            replied_users.add(user_id)  # Mark this user as having received the reply
            print(f"Reply sent to user_id: {user_id}")  # Debugging line
        except FloodWait as e:
            print(f"FloodWait encountered: {e.x} seconds")  # Debugging line
            await asyncio.sleep(e.x)
            await reply_forward(user_id)  # Retry if FloodWait occurs
        except Exception as e:
            print(f"Error while sending reply: {e}")  # Catch all other exceptions

async def media_forward(bot: Client, user_id: int, file_id: int):
    global last_sent_message  # Declare it as global to modify
    try:
        if Config.FORWARD_AS_COPY is True:
            last_sent_message = await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                          message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            last_sent_message = await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await media_forward(bot, user_id, file_id)

async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    await media_forward(bot, user_id, file_id)
    await reply_forward(user_id)  # Now passing only user_id

async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()
