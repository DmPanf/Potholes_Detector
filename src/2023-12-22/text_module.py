# text_module.py
from aiogram import types

# Register bot commands
commands = [
    types.BotCommand(command="/start", description="♻️ Get Started"),
    types.BotCommand(command="/help", description="💡 Help"),
    types.BotCommand(command="/mode", description="⚙️ Set Mode"),
    types.BotCommand(command="/info", description="ℹ️  Information"),
    types.BotCommand(command="/model", description="🪩 Available Models"),
    types.BotCommand(command="/alarm", description="💢 Pothole Size Limit"),
    types.BotCommand(command="/conf", description="🔭 Confidence"),
    types.BotCommand(command="/sky", description="📶 Set SkyLine"),
    types.BotCommand(command="/dbsum", description="📊 Database Summary"),
    types.BotCommand(command="/csv", description="🛄 CSV Download"),
    types.BotCommand(command="/id", description="🪪 Your ID"),
    types.BotCommand(command="/list", description="📝 User List"),
    types.BotCommand(command="/add", description="🛂 Add User"),
    types.BotCommand(command="/del", description="🚫 Delete User"),
]


help_text = """
🤖 *Welcome to the Potholes AI Detection Project!*
👇 Here's how you can interact with the bot:

/start - ♻️ *Get Started*
/help - 💡 *Help*
/info - ℹ️  *Information*
/mode - ⚙️ *Set Mode*
/model - 🪩 *Available Models*
/alarm - 💢 *Set Pothole Size*
/conf - 🔭 *Set Confidence*
/sky - 📶 *Set SkyLine*
/dbsum - 📊 *Database Summary*
/csv - 🛄 *CSV Download*
/id - 🪪  *Your ID*
/list - 📝 *User List*
/add - 🛂 *Add User*
/del - 🚫 *Delete User*

📸  *Image Processing*;
📽  *Video Processing*
"""
