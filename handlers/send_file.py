import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# A set to keep track of users who have already received the reply
replied_users = set()

async def reply_forward(user_id: int):
    if user_id not in replied_users:
        try:
            print(f"Sending reply to user_id: {user_id}")  # Debugging line
            await bot.send_message(
                chat_id=user_id,
                text="Files will be deleted in 30 minutes to avoid copyright issues. Please forward and save them.",
                disable_web_page_preview=True
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
    
    # Send the reply text after all files are sent
    await reply_forward(user_id)

    # Schedule deletion of all sent messages
    for message in sent_messages:
        asyncio.create_task(delete_after_delay(message, 1800))

async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()
