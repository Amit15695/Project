import os
import telebot
import json
from telebot import types
from io import BytesIO
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# Set up Telegram bot
bot_token = '6629293167:AAGJmZjz6JLspgWXngbB3sZFTSU59Q67Ccc'
bot = telebot.TeleBot(bot_token)

user_data_file = 'user_data2.json'
if not os.path.exists(user_data_file):
    with open(user_data_file, 'w') as f:
        json.dump({}, f)

user_states = {}
images_dir = 'dog_images'

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I'm your chatbot. Please upload a picture of a dog.")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    # Save the photo sent by the user
    photo = message.photo[-1]  # Get the largest available photo
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Save the photo as PNG
    photo_path = f"{images_dir}/{file_id}.png"
    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Update user state and add the photo path with type and color information
    user_id = message.chat.id
    if user_id not in user_states:
        user_states[user_id] = {'photos': []}

    # Ask for dog type
    user_states[user_id]['current_photo'] = {
        'photo_path': photo_path,
        'type': None,
        'color': None
    }

    user_states[user_id]['photos'].append(user_states[user_id]['current_photo'])
    ask_dog_type(user_id)

def ask_dog_type(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Golden Retriever', callback_data='type_golden'),
               types.InlineKeyboardButton('German Shepherd', callback_data='type_german_shepherd'))
    markup.row(types.InlineKeyboardButton('Bulldog', callback_data='type_bulldog'),
               types.InlineKeyboardButton('Beagle', callback_data='type_beagle'),
               types.InlineKeyboardButton('Poodle', callback_data='type_poodle'))
    markup.row(types.InlineKeyboardButton('Australian Shepherd', callback_data='type_australian_shepherd'),
               types.InlineKeyboardButton('Maltese', callback_data='type_maltese'),
               types.InlineKeyboardButton('Labrador', callback_data='type_labrador'))
    markup.row(types.InlineKeyboardButton('Other', callback_data='type_other'))

    bot.send_message(chat_id, "What type of dog is this?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))
def dog_type_callback(call):
    dog_type = call.data.replace('type_', '')
    user_id = call.message.chat.id
    user_states[user_id]['current_photo']['type'] = dog_type
    ask_dog_color(user_id)

def ask_dog_color(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Brown', callback_data='color_brown'),
               types.InlineKeyboardButton('Black', callback_data='color_black'))
    markup.row(types.InlineKeyboardButton('White', callback_data='color_white'),
               types.InlineKeyboardButton('Other', callback_data='color_other'))

    bot.send_message(chat_id, "What is the color of the dog?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('color_'))
def dog_color_callback(call):
    dog_color = call.data.replace('color_', '')
    user_id = call.message.chat.id
    user_states[user_id]['current_photo']['color'] = dog_color
    save_user_data(user_id)
    bot.send_message(user_id, "Thank you for providing the information! You can share another picture now")

@bot.message_handler(commands=['showinfo'])
def show_dog_info(message):
    user_id = message.chat.id
    user_info = get_user_info(user_id)
    if user_info:
        for photo_info in reversed(user_info.get('photos', [])):
            photo_path = photo_info.get('photo_path')
            with open(photo_path, 'rb') as photo_file:
                bot.send_photo(user_id, photo_file)
            info_message = f"Dog Type: {photo_info.get('type')}\n"
            info_message += f"Dog Color: {photo_info.get('color')}\n"
            bot.send_message(user_id, info_message)
    else:
        bot.send_message(user_id, "No dog information found.")

def save_user_data(chat_id):
    user_info = user_states[chat_id]
    with open(user_data_file, 'r') as f:
        data = json.load(f)

    user_id = str(chat_id)
    if user_id not in data:
        data[user_id] = {}

    if 'photos' not in data[user_id]:
        data[user_id]['photos'] = []

    data[user_id]['photos'].extend(user_info['photos'])

    with open(user_data_file, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_info(user_id):
    with open(user_data_file, 'r') as f:
        data = json.load(f)
        return data.get(str(user_id))

# Start the bot
bot.infinity_polling()