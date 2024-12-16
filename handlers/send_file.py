import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait
from configs import Config

async def send_file(bot: Client, user_id: int, file_ids: list):
    """
    Sends multiple files to the user, then sends a final message indicating deletion.
    """
    try:
        sent_messages = []  # Track all sent messages

        # Send each file
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

        # Send the final important message
        final_message = await bot.send_message(
            chat_id=user_id,
            text="✅ All files have been sent successfully.\n\n⚠️ **Note:** These files will be deleted in 30 minutes. Please save them before then.",
            disable_web_page_preview=True
        )

        # Add the final message to the list of messages to delete
        sent_messages.append(final_message)

        # Schedule deletion of all messages after 30 minutes
        asyncio.create_task(delete_after_delay(sent_messages, 1800))

    except FloodWait as e:
        # Handle rate limits
        await asyncio.sleep(e.value)
        await send_media_and_reply(bot, user_id, file_ids)

async def delete_after_delay(messages: list, delay: int):
    """
    Deletes all messages in the list after the specified delay (in seconds).
    """
    await asyncio.sleep(delay)
    for message in messages:
        try:
            await message.delete()
        except Exception as e:
            print(f"Error deleting message {message.message_id}: {e}")
