import json
from aiogram import Bot
from dotenv import load_dotenv
import os


load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")

# Load servers list from config.json file 
def load_servers_list(bot: Bot):
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            servers_list = config_data.get("servers", [])

        if servers_list is None:  # key 'servers' not found in config.json file 
            bot.send_message(chat_id=CHAT_ID, text="⛔ Error: key 'servers' not found in config.json file.")
            return None

        # Проверим, является ли servers_list списком
        if not isinstance(servers_list, list):  # Check if servers_list is a list of servers 
            bot.send_message(chat_id=CHAT_ID, text="⛔ Error: 'servers' must be a list.")
            return None

        return servers_list

    except json.JSONDecodeError:  # config.json is not valid JSON file 
        bot.send_message(chat_id=CHAT_ID, text="⛔ Error: config.json is not valid JSON file.")
        return None

"""
# Function for Loading available modes from config.json file
def load_available_modes(bot: Bot):  # Load available modes from config.json file 
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            available_modes = config_data.get("Modes_List", [])
        return available_modes
    except json.JSONDecodeError:  # config.json is not valid JSON file 
        bot.send_message(chat_id=CHAT_ID, text="⛔ Error: config.json is not valid JSON file.")
        return None
"""


def update_env_variable(key, new_value):  # Update environment variable in .env file 
    env_variables = {}
    with open('.env', 'r') as f:
        for line in f.readlines():
            k, v = line.strip().split('=', 1)
            env_variables[k] = v

    env_variables[key] = new_value  # Update value of the key in env_variables dictionary 

    # Save updated environment variables to .env file 
    with open('.env', 'w') as f:
        for k, v in env_variables.items():
            f.write(f"{k}={v}\n")

    os.environ[key] = new_value  # Update value of the key in os.environ dictionary
