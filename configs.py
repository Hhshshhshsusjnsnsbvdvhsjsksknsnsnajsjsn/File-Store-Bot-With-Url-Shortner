import os

class Config(object):
  API_ID = int(os.environ.get("API_ID", "9619481"))
  API_HASH = os.environ.get("API_HASH", "10effb30531c66d27b90f1e07f6bd071")
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "6423120715:AAHxlrO2Bj1T7QaJfjdpJGV-uhlyFwUT1FQ")
  BOT_USERNAME = os.environ.get("BOT_USERNAME", "Fgggffd_bot")
  DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002036697162"))
  SHORTLINK_URL = os.environ.get('SHORTLINK_URL', "ziplinker.net")
  SHORTLINK_API = os.environ.get('SHORTLINK_API', "8ea1e29d79de76acacdae5625f19fe8703c97f68")
  BOT_OWNER = int(os.environ.get("BOT_OWNER", "6624919731"))
  DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://groggajaj:A9bSxyuxPkw2MIg1@cluster0.6nr3zop.mongodb.net/?retryWrites=true&w=majority")
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
  LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002135831842"))
  BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
  FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
  BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
  BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "").split()))
  OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
  ABOUT_BOT_TEXT = f"""
This is a Permanent 𝙥𝙧𝙞𝙫𝙖𝙩𝙚 𝘽𝙤𝙩. 
𝙳𝚘 𝙽𝚘𝚝 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝, 𝙸𝚏 𝚢𝚘𝚞 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝙱𝚎 𝙱𝚊𝚗𝚗𝚎𝚍 𝙱𝚎𝚌𝚊𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚒𝚜 𝚊 𝙿𝚛𝚒𝚟𝚊𝚝𝚎 𝙱𝚘𝚝 , 𝚗𝚘𝚝 𝚊 𝚙𝚞𝚋𝚕𝚒𝚌 𝙱𝚘𝚝.
╭────[ 🔅FɪʟᴇSᴛᴏʀᴇBᴏᴛ🔅]────⍟
│
├🔸 My Name: [private Bot](https://t.me/{BOT_USERNAME})
│
├🔸 Language: [Python 3](https://www.python.org)
│
├🔹 Library: [Pyrogram](https://docs.pyrogram.org)
│
╰──────[  ]───────────⍟
"""
  ABOUT_DEV_TEXT = f"""
🧑🏻‍💻 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: [VJ](https://telegram.me/paidby99)
 
 I am Super noob Please Support My Hard Work.

[repo](https://t.me/paidby99)
"""
  HOME_TEXT = """
Hello, [{}](tg://user?id={})\n\n
This is a Permanent 𝙥𝙧𝙞𝙫𝙖𝙩𝙚 𝘽𝙤𝙩. 
𝙳𝚘 𝙽𝚘𝚝 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝, 𝙸𝚏 𝚢𝚘𝚞 𝚄𝚜𝚎 𝚝𝚑𝚒𝚜 𝙱𝚘𝚝 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝙱𝚎 𝙱𝚊𝚗𝚗𝚎𝚍 𝙱𝚎𝚌𝚊𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚒𝚜 𝚊 𝙿𝚛𝚒𝚟𝚊𝚝𝚎 𝙱𝚘𝚝 , 𝚗𝚘𝚝 𝚊 𝚙𝚞𝚋𝚕𝚒𝚌 𝙱𝚘𝚝. **About Bot**.
"""
