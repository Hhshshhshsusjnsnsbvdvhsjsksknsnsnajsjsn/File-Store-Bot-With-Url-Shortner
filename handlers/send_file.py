import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config

async def send_file(bot: Client, user_id: int, file_ids: list):
    """
    Sends multiple files to the user, then sends a final message indicating deletion.
    """
    try:
        sent_messages = []  # To keep track of all sent messages

        # Forward or copy each file
        for file_id in file_ids:
            if Config.FORWARD_AS_COPY:
                sent_message = await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=Config.DB_CHANNEL,
                    message_id=file_id
                )
            else:
                sent_message = await bot.forward_messages(
                    chat_id=user_id,
                    from_chat_id=Config.DB_CHANNEL,
                    message_ids=file_id
                )
            sent_messages.append(sent_message)

        # After sending all messages, send the final important message
        await asyncio.sleep(1)  # Small delay to separate the final message
        final_message = await bot.send_message(
            chat_id=user_id,
            text="All files have been sent. These files will be deleted in 30 minutes to avoid copyright issues. Please save them.",
            disable_web_page_preview=True
        )

        # Schedule deletion for all sent messages and the final message
        asyncio.create_task(delete_after_delay(sent_messages + [final_message], 1800))

    except FloodWait as e:
        await asyncio.sleep(e.value)
        await send_file(bot, user_id, file_ids)

async def delete_after_delay(messages: list, delay: int):
    """
    Deletes all messages in the list after the specified delay (in seconds).
    """
    await asyncio.sleep(delay)
    for message in messages:
        try:
            await message.delete()
        except Exception as e:
            print(f"Error while deleting message {message.message_id}: {e}")
