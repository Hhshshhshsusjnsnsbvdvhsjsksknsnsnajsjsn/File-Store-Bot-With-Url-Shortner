import os

class Config(object):
  API_ID = int(os.environ.get("API_ID", "9619481"))
  API_HASH = os.environ.get("API_HASH", "10effb30531c66d27b90f1e07f6bd071")
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "6423120715:")
  BOT_USERNAME = os.environ.get("BOT_USERNAME", "Fgggffd_bot")
  DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002036697162"))
  SHORTLINK_URL = os.environ.get('SHORTLINK_URL', "api.shareus.io")
  SHORTLINK_API = os.environ.get('SHORTLINK_API', "X8KgVEykIqhQIXefXcmrJb9aSPt2")
  BOT_OWNER = int(os.environ.get("BOT_OWNER", "6624919731"))
  DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://fffworld57:Or97XLuv6P6GvtFZ@cluster0.u34tcer.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
  LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002135831842"))
  BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
  FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
  BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
  BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "").split()))
  OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
  ABOUT_BOT_TEXT = f"""
This is a Permanent 𝙥𝙧𝙞𝙫𝙖𝙩𝙚 𝘽𝙤𝙩. 
𝙳𝚘 𝙽𝚘𝚝 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝, 𝙸𝚏 𝚢𝚘𝚞 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝙱𝚎 𝙱𝚊𝚗𝚗𝚎𝚍 𝙱𝚎𝚌𝚊𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚒𝚜 𝚊 𝙿𝚛𝚒𝚟𝚊𝚝𝚎 𝙱𝚘𝚝 , 𝚗𝚘𝚝 𝚊 𝚙𝚞𝚋𝚕𝚒𝚌 𝙱𝚘𝚝. About Bot. 

╭────[ 🔅FɪʟᴇSᴛᴏʀᴇBᴏᴛ🔅]────⍟
│
├🔸 My Name: [FileStore Bot](https://t.me/{BOT_USERNAME})
│
├🔸 Language: [Python 3](https://www.python.org)
│
├🔹 Library: [Pyrogram](https://docs.pyrogram.org)
│
╰──────[ 😎 ]───────────⍟
"""
  ABOUT_DEV_TEXT = f"""
🧑🏻‍💻 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: [qt](https://telegram.me/qtmovie)
 
 I am Super noob Please Support My Hard Work.

[dev](https://t.me/0)
"""
  HOME_TEXT = """
Hello, [{}](tg://user?id={})\n\nThis is a Permanent **FileStore Bot**.

This is a Permanent 𝙥𝙧𝙞𝙫𝙖𝙩𝙚 𝘽𝙤𝙩. 
𝙳𝚘 𝙽𝚘𝚝 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝, 𝙸𝚏 𝚢𝚘𝚞 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝙱𝚎 𝙱𝚊𝚗𝚗𝚎𝚍 𝙱𝚎𝚌𝚊𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚒𝚜 𝚊 𝙿𝚛𝚒𝚟𝚊𝚝𝚎 𝙱𝚘𝚝 , 𝚗𝚘𝚝 𝚊 𝚙𝚞𝚋𝚕𝚒𝚌 𝙱𝚘𝚝. About Bot. **About Bot**.
"""
