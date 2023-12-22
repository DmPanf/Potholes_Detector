from aiogram import Bot, Dispatcher, types  # pip install aiogram==2.11.2 (https://pypi.org/project/aiogram/)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
import logging
# import requests
import asyncio  # pip install asyncio (https://pypi.org/project/asyncio/)
import aiohttp  # pip install aiohttp (https://pypi.org/project/aiohttp/)
from aiohttp import ClientTimeout  # ClientSession,
import json
from dotenv import load_dotenv
from io import BytesIO  # pip install io (https://pypi.org/project/io/)
from datetime import datetime  # pip install datetime (https://pypi.org/project/datetime/)
from PIL import Image
import os
import requests
import cv2
import base64  # pip install base64 (https://pypi.org/project/base64/)
from tools import load_servers_list, update_env_variable  # load_available_modes,
from text_module import commands, help_text


NEW_ADMIN = 12345
MAX_FILE_SIZE_MB = 20  # Maximum file size in MB
# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
token = os.getenv("FastAPI_TOKEN")


#ACCESS_LIST = os.getenv("ACCESS_LIST")
#ACCESS_LIST = list(map(int, os.getenv("ACCESS_LIST", "").split(",")))
ACCESS_LIST = list(map(int, os.getenv("ACCESS_LIST").split(",")))
blocked_users = set()  # global set for storing the ID of blocked users and possible receipt of the phone

# print(f'... ACCESS_LIST: {ACCESS_LIST}')
log_folder = os.getenv("LOG_DIR")
log_file = os.getenv("LOG_FILE")


if not API_TOKEN:
    raise ValueError("TG_TOKEN is not set in the environment variables or .env file!")
if not os.path.exists(log_folder):  # Create log folder if it doesn't exist
    os.makedirs(log_folder)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{log_folder}/{log_file}"),
        logging.StreamHandler()
    ]
)

class AccessMiddleware(BaseMiddleware):  # BLOCKING USERS FOR ANY ACTIONS WITH THE BOT!!!
    def __init__(self, access_list):
        self.access_list = access_list
        super().__init__()
        #super(AccessMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        logging.info(f"msg from: {user_id} ({message.from_user.full_name})")
        # print(f' ----- {user_id}: {self.access_list}')

        if user_id not in self.access_list: ## or user_id != ADMIN_CHAT_ID:
            add_text = f"Dear, <b>{message.from_user.full_name}</b> [<code>{message.from_user.username}</code>]!\n"
            add_text += f"The bot is in development!\nAccess from your <b>ID</b> [<code>{user_id}</code>] is denied!"
            # add_text += "\nPlease send your phone number for registration:"
            await message.answer(f"{add_text}", parse_mode="HTML")
            blocked_users.add(user_id)  # Add ID of blocked user
            update_env_variable("BLOKED_LIST", ','.join(map(str, blocked_users)))
            print(f'... blocked_users: {blocked_users}')
            raise CancelHandler()  # Cancel current handler and continue to the next one in the chain
        return False  # Continue to the next handler in the chain

#logging.basicConfig(level=logging.DEBUG)  # DEBUG !!!
#logging.basicConfig(level=logging.INFO)  # INFO
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_LIST))

servers_list = load_servers_list(bot)
# available_modes = load_available_modes(bot)

async def on_startup(dp):
    bot_info = await dp.bot.get_me()
    bot_name = bot_info.username
    user_id = bot_info.id
    await dp.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'✴️ The @{bot_name} is online!\n🈲 Main Server: ciet')
    await dp.bot.send_message(chat_id=NEW_ADMIN, text=f'✴️ The @{bot_name} is online!\n🈲 Main Server: ciet')
    print(f'✴️  The {bot_name} is online!')
    if user_id not in ACCESS_LIST:
        await dp.bot.set_my_commands(commands)


#async def fetch(session, url):
async def fetch(session, url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.text()
                # return await response.json()
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")
    except Exception as e:
        print(f"fetch ------ Error occurred: {e}")
        raise e


@dp.message_handler(commands=['start','info'])
async def send_info(message: types.Message):
    API_URL = os.getenv("API_URL")  # API_URL = 'http://127.0.0.1:8000'
    print(f' ... API_URL/info: {API_URL}')
    timeout = ClientTimeout(total=35)  # 5 seconds timeout
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            info = await fetch(session, f'{API_URL}/info')
            data = json.loads(info)["Project 2023"]
            await message.answer(f"🔰 <b>Project Info:</b>\n<pre>{data}</pre>", parse_mode="HTML", reply_markup=keyboard)
        except Exception as e:
            print(f"info ------ Error occurred: {e}")
            await message.answer(f"⛔️ Server <b>FastAPI</b> is not available!\n{e}", parse_mode="HTML", reply_markup=keyboard)

# ++++++++++++++++++++ SQLite Summary ++++++++++++++++
@dp.message_handler(commands=['dbsum'])
async def send_database_summary(message: types.Message):
    API_URL = os.getenv("API_URL")  # API_URL = 'http://127.0.0.1:8000'
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/database_summary") as response:
            if response.status != 200:
                await message.reply("An error occurred while retrieving data from the database.")
                return

            data = await response.json()

            summary_message = (
                f"📊 <b>Database Summary:</b>\n"
                f"Total Records: <b>{data['total_records']}</b>\n"
                f"Last Record Time: <b>{data['last_record_time']}</b>\n"
                f"Max Box Width: <b>{data['max_box_width']}</b>\n"
                f"Max Confidence: <b>{data['max_confidence']}</b>\n"
                f"Max Inference: <b>{data['max_inference']}</b>"
            )

            await message.reply(summary_message, parse_mode="HTML")

# ++++++++++++++++++++ SQLite CSV Download ++++++++++++++++
@dp.message_handler(commands=['csv'])
async def send_csv_file(message: types.Message):
    API_URL = os.getenv("API_URL")  # API_URL = 'http://127.0.0.1:8000'
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/download_csv") as response:
            if response.status != 200:
                await message.reply("Error loading CSV file.")
                return

            # Read the CSV content from the response
            csv_content = await response.read()

            # Save the CSV content to a temporary file
            temp_file_path = 'last_10_records.csv'
            with open(temp_file_path, 'wb') as f:
                f.write(csv_content)

            # Send the CSV file to the user
            with open(temp_file_path, 'rb') as f:
                await message.reply_document(f)

            os.remove(temp_file_path)  # Clean up the temporary file

# ++++++++++++++++++++ Main KeyBoard ++++++++++++++++
# 
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(KeyboardButton('📡Server'), KeyboardButton('⚙️ Mode'), KeyboardButton('⚖️Model'), KeyboardButton('💡HELP'))

#
@dp.message_handler(lambda message: message.text == '⚖️Model')
async def handle_model(message: types.Message):
    await send_models(message)

@dp.message_handler(lambda message: message.text == '⚙️ Mode')
async def handle_mode(message: types.Message):
    await set_mode(message)

@dp.message_handler(lambda message: message.text == '💡HELP')
async def handle_help(message: types.Message):
    #await send_help(message)
    await message.reply(help_text, parse_mode="Markdown")


# ++++++++++ ACTIVE MODE [Basic, Grid, HQ-SAM, YOLOv8] ++++++++++++++
async def get_active_mode(session, api_url):  # API_URL = 'http://app:8001'
    try:
        response = json.loads(await fetch(session, f'{api_url}/modes'))
        print(f"get_active_mode ------ response: {response}")
        ACTIVE_MODE = response['Active_Mode']
        AVAILABLE_MODES = response['Modes_List']
        return ACTIVE_MODE, AVAILABLE_MODES
    except Exception as e:
        print(f"get_active_mode ------ Error occurred: {e}")
        return None, None

async def set_active_mode(session, api_url, mode):  # API_URL = 'http://app:8001'
    try:
        #await fetch(session, f'{api_url}/modes/{mode}')
	# Must be POST (not GET)
        await session.post(f'{api_url}/modes/{mode}')
    except Exception as e:
        print(f"set_active_mode ------ Error occurred: {e}")


@dp.message_handler(commands=['mode'])
async def set_mode(message: types.Message):
    API_URL = os.getenv("API_URL")
    print(f"\nset_mode ------ API_URL: {API_URL}\n")
    timeout = ClientTimeout(total=30)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            active_mode, available_modes = await get_active_mode(session, API_URL)
            print(f"set_mode ------ result: {active_mode} of [{available_modes}]")

            if active_mode is not None or available_modes is not None:
                markup = InlineKeyboardMarkup()  #available_modes = ['Basic', 'Grid', 'HQ-SAM', 'YOLOv8']
                for mode in available_modes:
                    mprefix = "🔘 " if mode == active_mode else "⚪️ "
                    markup.add(InlineKeyboardButton(f"{mprefix}{mode}", callback_data=f"mode_{mode}"))
                kbtxt = f"⚙️ Active Mode:<b>{active_mode}</b>\n<b>Available Modes:</b>"
                await message.answer(kbtxt, parse_mode="HTML", reply_markup=markup)
            else:
                await message.answer(f"🆘 Server <b>FastAPI</b> is not available!\n{active_mode} of [{available_modes}]", parse_mode="HTML")

    except Exception as e:
        print(f"set_mode ------ Error occurred: {e}")
        await message.answer(f"🆘 Server <b>FastAPI</b> is not available!\n{e}", parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data.startswith("mode_"))
async def mode_callback_inline(call: CallbackQuery):
    selected_mode = call.data.split("_")[1]
    API_URL = os.getenv("API_URL")
    current_time = datetime.now().strftime("%H:%M:%S")
    try:
        timeout = ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            await set_active_mode(session, API_URL, selected_mode)  # Устанавливаем выбранный режим
            active_mode, available_modes = await get_active_mode(session, API_URL)  # Получаем актуальный список режимов

            markup = InlineKeyboardMarkup()
            for mode in available_modes:
                mprefix = "🔘 " if mode == active_mode else "⚪️ "
                markup.add(InlineKeyboardButton(f"{mprefix}{mode}", callback_data=f"mode_{mode}"))

            kbtxt = f"⚙️ [{current_time}]\nActive Mode: <b>{active_mode}</b>\n<b>Available Modes:</b>"
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=kbtxt, reply_markup=markup, parse_mode="HTML")
            await call.answer(f"🔘 Mode {selected_mode} is selected!")
    except Exception as e:
        print(f"mode_callback_inline ------ Error occurred: {e}")
        await call.answer(f"Error: {e}", show_alert=True)


# ++++++++++ MODELS ++++++++++++++
@dp.message_handler(commands=['model'])
async def send_models(message: types.Message):
    API_URL = os.getenv("API_URL")  #
    BEST_MODEL = os.getenv("mdl_name")  #
    # models_list = os.getenv("models_list")  #
    timeout = ClientTimeout(total=30)  #

    async with aiohttp.ClientSession(timeout=timeout) as session:  #
        try:
            # print(f'1. ... API_URL/models: {API_URL}/models')
            Models = json.loads(await fetch(session, f'{API_URL}/models'))  #
            #Models = json.loads(await fetch(session, f'{API_URL}/models', token))  #
            # print(f'2. ... Models: {Models}')
            models_list = Models['Models']
            markup = InlineKeyboardMarkup()  #
            #print(f"3. ===> models_list: {models_list}")

            if models_list:
                if BEST_MODEL in models_list:
                    mdl_name = BEST_MODEL
                    # print(f'4a. .... Best Model: {mdl_name}')
                else:
                    mdl_name = models_list[-1]
                    # print(f'4b. .... Best Model: {mdl_name}')

                for model in models_list:  #
                    prefix = "🟢 " if model == mdl_name else "⚪️ "
                    markup.add(InlineKeyboardButton(f"{prefix}{model}", callback_data=model))  #

                update_env_variable("mdl_name", mdl_name)  #
                # update_env_variable("models_list", models_list)  #
                update_env_variable("models_list", ','.join(models_list))  #
                # print(f"5. ......... Models: {','.join(models_list)}")
                current_time = datetime.now().strftime("%H:%M:%S")
                msg = f"🪩 Models List ...\nCurrent Time: <b>[{current_time}</b>]"
                await message.answer(msg, parse_mode="HTML", reply_markup=markup)  #

            else:
                await message.answer("⭕️ Models List <b>is empty</b>.", parse_mode="HTML")
        except Exception as e:
            await message.answer(f"⛔ Server <b>FastAPI</b> is not available.\n{e}", parse_mode="HTML")


#@dp.callback_query_handler(lambda call: not call.data.startswith("server_"))   # !! Add callback_data !!
@dp.callback_query_handler(lambda call: call.data.endswith(".pt"))
async def models_callback_inline(call: CallbackQuery):
    BEST_MODEL = os.getenv("mdl_name")  #
    current_time = datetime.now().strftime("%H:%M:%S")
    if call.data == BEST_MODEL:
        await call.answer(f"[{current_time}] The Model {BEST_MODEL} is selected!")
    else:
        print(type(call.data), call.data)
        await change_model(call, call.data)


async def change_model(call: CallbackQuery, new_model: str):
    mdl_name = new_model
    #print(f'X1 ..... New Model: {mdl_name}')
    update_env_variable("mdl_name", mdl_name)  #
    models_list = os.getenv("models_list").split(',')  #
    print(f' ......... New Model: {mdl_name}')
    #print(f' ....... models_list: {models_list}')

    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f'🪩 Models List ...\nCurrent Time: <b>{current_time}</b>'

    markup = InlineKeyboardMarkup()
    #for model in models_list['Models']:  #
    for model in models_list:
        prefix = "🟢 " if model == mdl_name else "⚪️ "
        markup.add(InlineKeyboardButton(f"{prefix}{model}", callback_data=model))

    # await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text = msg,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await call.answer(f"🟢 The Model {mdl_name} is selected!")


# ++++++++++++++ Skyline ++++++++++++++
def set_skyline_on_server(value):
    API_URL = os.getenv("API_URL")
    url = f"{API_URL}/skyline?skyline={value}"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"🅾️  Error: {response.status_code}, {response.text}")


@dp.message_handler(commands=['sky'])
async def set_skyline_command(message: types.Message):
    try:
        args = message.get_args()
        if not args:
            await message.reply("🔍 Please provide a value.")
            return
        value = int(args)
        if value in range(5,50):
            result = set_skyline_on_server(value)
            await message.reply(f"📶 Skyline is set <b>{result['Skyline']} %</b> below the Top", parse_mode="HTML")
        else:
            await message.reply("🔍 Please provide a valid value (between 5 and 50).")

    except Exception as e:
        await message.reply(f"🅾️  Failed to set Skyline. <b>Error</b>:\n<code>{e}</code>", parse_mode="HTML")

# ++++++++++++++ Confidence ++++++++++++++
def set_confidence_on_server(value):
    API_URL = os.getenv("API_URL")
    url = f"{API_URL}/confidence?confidence={value}"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"🅾️  Error: {response.status_code}, {response.text}")


@dp.message_handler(commands=['conf'])
async def set_confidence_command(message: types.Message):
    try:
        args = message.get_args()
        if not args:
            await message.reply("🔍 Please provide a value.")
            return
        value = float(args)
        if 0.1 <= value <= 1.0:
            result = set_confidence_on_server(value)
            await message.reply(f"🔭 Confidence is set to <b>{result['Confidence']}</b>", parse_mode="HTML")
        else:
            await message.reply("🔍 Please provide a valid value (between 0.1 and 1.0).")

    except Exception as e:
        await message.reply(f"🅾️  Failed to set Confidence. <b>Error</b>:\n<code>{e}</code>", parse_mode="HTML")


# ++++++++++++++ Alarm Size Limit ++++++++++++++
def set_alarm_size_on_server(value):
    API_URL = os.getenv("API_URL")
    url = f"{API_URL}/alarm_size?alarm_size={value}"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"🅾️  Error: {response.status_code}, {response.text}")


@dp.message_handler(commands=['alarm'])
async def set_alarm_size_command(message: types.Message):
    try:
        args = message.get_args()
        if not args:
            await message.reply("🔍 Please provide a value.")
            return
        value = float(args)
        if 10.0 <= value <= 500.0:
            result = set_alarm_size_on_server(value)
            await message.reply(f"💢 Pothole Size Limit is set to <b>{result['Alarm_Size']}</b>", parse_mode="HTML")
        else:
            await message.reply("🔍 Please provide a valid value (between 10.0 and 500.0).")

    except Exception as e:
        await message.reply(f"🅾️  Failed to set Pothole Size Limit. <b>Error</b>:\n<code>{e}</code>", parse_mode="HTML")

# +++++++++++++++ PHOTO +++++++++++++++
# handler for receiving images and making POST requests to FastAPI
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    API_URL = os.getenv("API_URL")  # Remote server URL for FastAPI (for local Bot: http://app:8001)
    mdl_name = os.getenv("mdl_name")  #
    file_id = message.photo[-1].file_id  #
    file = await bot.get_file(file_id)  #
    file_path = file.file_path  #

    image_data = await bot.download_file(file_path)  #

    url = f'{API_URL}/predict'  #

    timeout = ClientTimeout(total=30)  #
    async with aiohttp.ClientSession(timeout=timeout) as session:  #
    # async with ClientSession() as session:  #
        form = aiohttp.FormData()  #
        form.add_field('file', image_data, filename='input_image.jpg', content_type='image/jpg')  #
        form.add_field('mdl_name', mdl_name)
        try:
            # async with session.post(url, data=form, timeout=30) as response:
            async with session.post(url, data=form) as response:
                if response.status == 200:
                    """
                    # GOOD only for the Image with no dictionary!!!
                    # Read the response content as bytes and create a BytesIO object from it
                    output_image_data = BytesIO(await response.read())
                    output_image_data.seek(0)
                    msg = f"✅ Processed image\n<b>Model:</b>: <b>{mdl_name}</b>"
                    await message.reply_photo(photo=output_image_data, caption=msg, parse_mode="HTML")
                    """
                    response_json = await response.json()  #
                    img_str = response_json['image']
                    results = response_json['results']  #

                    # Create additional information string with additional data
                    add_info = f"\n<b>💾 Image Size:</b> {results['image_size']}" \
                               f"\n<b>⏳ Processing Time:</b> {results['processing_time']}s" \
                               f"\n<b>⚖️ Model:</b> <code>{results['model_name']}</code>" \
                               f"\n<b>🔭 Confidence Level:</b> {results['conf']}" \
                               f"\n<b>📸 View Mode:</b> {results['mode']}" \
                               f"\n<b>💢 Pothole Size Limit:</b> {results['alarm_size']}" \
                               f"\n<b>🔍 Object Count:</b> {results['object_count']}" \
                               f"\n<b>📐 Max Object Width:</b> {results['max_box_width']}" \
                               f"\n<b>💎 Object Confidence:</b> {results['confidence']}" \
                               f"\n<b>⏱ Inference:</b> {results['inference']}ms" \
                               f"\n<b>🌐 Geo [Lat, Long]:</b> <code>{results['latitude']}, {results['longitude']}</code>" \
                               f"\n<b>🖥 GPU Info:</b> {results['gpu_info']}"

                    # Read the response content as bytes and create a BytesIO object from it
                    # output_image_data = BytesIO(base64.b64decode(response_json['image']))

                    output_image_data = BytesIO(base64.b64decode(img_str))
                    output_image_data.seek(0)
                    await message.reply_photo(photo=output_image_data, caption=add_info, parse_mode="HTML")
        except KeyError as key_error:
            print(f"Key error: {key_error}")
            await message.answer(f"predict ------ {key_error}")
        except Exception as e:
            print(f"predict ------ ⛔️ Server FastAPI [{API_URL}] is not available!\n: {e}")
            await message.answer(f"⛔️ Server <b>FastAPI [{API_URL}]</b> is not available!\n⌛️ Timeout=<b>{timeout} s</b>\n{e}", parse_mode="HTML")


# ++++++++++++++++++ VIDEO ++++++++
#@dp.message_handler(content_types=['video'])
@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    API_URL = os.getenv("API_URL")  # Remote server URL for FastAPI (for local Bot: http://app:8001)
    mdl_name = os.getenv("mdl_name")  #

    file_id = message.video.file_id
    try:
        file = await bot.get_file(file_id)
        file_size_MB = file.file_size / (1024 * 1024)  # Convert to MB
    except Exception as e:
        await message.reply("Error receiving the file: {}".format(str(e)))
        return
    
    # Check if the file size exceeds the limit
    if file_size_MB > MAX_FILE_SIZE_MB:
        await message.reply(f"Sorry, the file size is too large. Maximum size: {MAX_FILE_SIZE_MB} MB.")
        return
    
    # Download the video file
    file_path = file.file_path
    video_data = await bot.download_file(file_path)

    # ============== File Size ======================
    # Process the video locally to get its properties
    """
    temp_video_path = 'temp_video.mp4'
    with open(temp_video_path, 'wb') as f:
        f.write(video_data.read())  # Read bytes from BytesIO object

    cap = cv2.VideoCapture(temp_video_path)
    if not cap.isOpened():
        await message.reply("Could not open the video file for analysis.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps if fps else 0

    cap.release()
    os.remove(temp_video_path)  # Clean up the temporary file

    # Inform the client about the video properties
    processing_time_estimate = frame_count * 0.1
    await message.reply(
        f"Video file size: {file_size_MB:.2f} MB\n"
        f"Frame count: {frame_count}\n"
        f"Duration: {duration:.2f} seconds\n"
        f"Estimated processing time: {processing_time_estimate:.2f} seconds."
    )
    # -----------------------------------------------
    """
    await message.reply(f"Video file size: {file_size_MB:.2f} MB\nEstimated processing time: 30-90 seconds.")
    # Send the video file to FastAPI server for processing
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file', video_data, filename='video.mp4', content_type='video/mp4')
        data.add_field('mdl_name', mdl_name)

        response = await session.post(f'{API_URL}/predict_video', data=data)
        if response.status != 200:
            await message.reply("Video processing error")
            return

        # Assuming the server returns the processed video file
        processed_video = await response.read()

    # Save the processed video to a temporary file
    temp_file_path = 'processed_video.mp4'
    with open(temp_file_path, 'wb') as f:
        f.write(processed_video)

    # Send the processed video back to the user
    with open(temp_file_path, 'rb') as f:
        await message.reply_video(f)

    os.remove(temp_file_path)  # Clean up the temporary file

# ++++++++++++ SERVERS +++++++++++++++++
@dp.message_handler(lambda message: message.text == '📡Server')
async def choose_server(message: types.Message):
    API_URL = os.getenv("API_URL")  #

    markup = InlineKeyboardMarkup()  #
    if servers_list:  #
        for server in servers_list:
            server_name = server['name']
            server_url = server['url']
            prefix = "🟩 " if server_url == API_URL else "⬜️ "
            markup.add(InlineKeyboardButton(f"{prefix}{server_name}", callback_data=f"server_{server_url}"))

        update_env_variable("API_URL", API_URL)  #
        print(f' ......... Server: {API_URL}')
        current_time = datetime.now().strftime("%H:%M:%S")
        msg = f"📡 Choosing servers ...\nCurrent time: <b>[{current_time}</b>]"
        await message.answer(msg, parse_mode="HTML", reply_markup=markup)
    else:
        await message.answer("⭕️ Server list <b>is empty</b>.", parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data.startswith("server_"))  #
async def servers_callback_inline(call: CallbackQuery):
    API_URL = os.getenv("API_URL")  #
    current_time = datetime.now().strftime("%H:%M:%S")
    if call.data.startswith("server_"):
        server_url = call.data[7:]
        server_name = [s['name'] for s in servers_list if s['url'] == server_url]
        if server_url == API_URL:
            await call.answer(f"[{current_time}] The Server {server_name} is selected!", show_alert=True)
        else:
            await change_server(call, server_url)


async def change_server(call: CallbackQuery, new_server_url: str):
    API_URL = new_server_url
    update_env_variable("API_URL", API_URL)  #
    print(f' ..... New Server: {API_URL}')

    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f'📡 Choosing servers ...\nCurrent Time: <b>{current_time}</b>'

    markup = InlineKeyboardMarkup()
    for server in servers_list:
        prefix = "🟩 " if server['url'] == API_URL else "⬜️ "
        markup.add(InlineKeyboardButton(f"{prefix}{server['name']}", callback_data=f"server_{server['url']}"))

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text = msg,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await call.answer(f"🟩 The Server {new_server_url} is selected!")


# +++++++++++++++ TOOLS [/id, /list, /add, /help] +++++++++++++++
@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    my_str = (f"👤 {message.from_user.full_name} [<code>{message.from_user.username}</code>] ->\n"
              f"🆔 <b>User ID:</b> <code>{message.from_user.id}</code>\n"
              f"👥 <b>Chat ID:</b> <code>{message.chat.id}</code>")
    await message.reply(my_str, parse_mode="HTML")


@dp.message_handler(lambda message: message.forward_from)
async def handle_forwarded_message(message: types.Message):
    original_user_id = message.forward_from.id
    chat_id = message.chat.id
    u_name = message.forward_from.username
    f_name = message.forward_from.full_name

    response_str = (f"👤 <b>{f_name}</b> [<code>@{u_name}</code>]  ->\n"
                    f"🆔 <b>Forwarded User ID:</b> <code>{original_user_id}</code>\n"
                    f"👥 <b>Chat ID:</b> <code>{chat_id}</code>")
    await message.reply(response_str, parse_mode="HTML")

@dp.message_handler(commands=['list'])
async def send_access_list(message: types.Message):
    ACCESS_LIST = os.getenv("ACCESS_LIST")
    if ACCESS_LIST:
        access_list = ACCESS_LIST.split(',')
        formatted_list = ' '.join([f"<code>{x.strip()}</code>" for x in access_list])
        await message.answer(f"❇️ <b>ACCESS_LIST</b>:\n{formatted_list}", parse_mode="HTML")
    else:
        await message.answer("⚠️ ACCESS_LIST is empty.", parse_mode="HTML")


@dp.message_handler(lambda message: message.text.startswith('/add'))
async def add_to_access_list(message: types.Message):
    user_command = message.text.split()
    if len(user_command) != 2:
        await message.answer("⚠️ Invalid format. Use /add [ID] command.")
        return

    try:
        new_id = int(user_command[1])  # 
    except ValueError:
        await message.answer("⚠️ ID must be an integer.")
        return

    ACCESS_LIST = os.getenv("ACCESS_LIST")  #

    if ACCESS_LIST:
        access_list = list(map(int, ACCESS_LIST.split(',')))  #
    else:
        access_list = []

    if new_id not in access_list:  #
        access_list.append(new_id)
        new_access_list = ','.join(map(str, access_list))
        update_env_variable('ACCESS_LIST', new_access_list)  #
        await message.answer("✅ Your ID has been added to ACCESS_LIST.")
    else:
        await message.answer("⚠️ Your ID is already in ACCESS_LIST.")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_from_access_list(message: types.Message):
    user_command = message.text.split()[1:]  #

    if len(user_command) < 1:
        await message.answer("⚠️ Invalid format. Use /del [ID1] [ID2] ... command.")
        return

    ACCESS_LIST = os.getenv("ACCESS_LIST")  # 
    if ACCESS_LIST:
        access_list = list(map(int, ACCESS_LIST.split(',')))  # 
    else:
        await message.answer("⚠️ ACCESS_LIST is empty.")
        return

    deleted_ids = []
    not_found_ids = []

    for str_id in user_command:
        try:
            del_id = int(str_id)  # 
        except ValueError:
            await message.answer(f"⚠️ ID {str_id} must be a number. Skip it.")
            continue

        if del_id in access_list:  #
            access_list.remove(del_id)
            deleted_ids.append(str(del_id))
        else:
            not_found_ids.append(str(del_id))

    if deleted_ids:
        new_access_list = ','.join(map(str, access_list))
        update_env_variable('ACCESS_LIST', new_access_list)  # 
        await message.answer(f"❎ ID {', '.join(deleted_ids)} successfully removed from ACCESS_LIST.")

    if not_found_ids:
        await message.answer(f"⚠️ ID {', '.join(not_found_ids)} is not in ACCESS_LIST.")


@dp.message_handler(commands=['help'])  # Help command 
async def send_help(message: types.Message):
    await message.answer(help_text, parse_mode="Markdown")


# +++++++++++++ MAIN +++++++++++++
async def main():  # Main function
    await on_startup(dp)  # Call on_startup function 
    await dp.start_polling()  # Start polling 

if __name__ == '__main__':  # Start the bot when the script is run 
    asyncio.run(main())  # Call the main function
