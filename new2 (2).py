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

user_data_file = 'user_data.json'
if not os.path.exists(user_data_file):
    with open(user_data_file, 'w') as f:
        json.dump({}, f)

# Dictionary to store user states (waiting for image, dog type, dog color)
user_states = {}
# Directory to save images
images_dir = 'dog_images'

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I'm your chatbot. Please upload a picture of a dog.")

# @bot.message_handler(content_types=['photo'])
# def get_photo(message):
    # Save the photo sent by the user
    # photo = message.photo[-1]  # Get the largest available photo
    # file_id = photo.file_id
    # file_info = bot.get_file(file_id)
    # downloaded_file = bot.download_file(file_info.file_path)
    #
    # # Save the photo as PNG
    # photo_path = f"{images_dir}/{file_id}.png"
    # with open(photo_path, 'wb') as new_file:
    #     new_file.write(downloaded_file)
    #
    # # Update user state and ask for dog type
    # user_states[message.chat.id] = {'photo_path': photo_path}
    # ask_dog_type(message.chat.id)
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

        # Update user state and ask for user's name
        user_states[message.chat.id] = {'photo_path': photo_path}
        bot.send_message(message.chat.id, "Thanks for the photo! What's your name?")
        bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    # Get the user's name and store it in the user's state
    user_states[message.chat.id]['user_name'] = message.text

    # Ask for the dog type
    ask_dog_type(message.chat.id)
def ask_dog_type(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Golden Retriever', callback_data='type_golden'),
               types.InlineKeyboardButton('German Shepherd', callback_data='type_german shepherd'))
    markup.row(types.InlineKeyboardButton('Bulldog', callback_data='type_bulldog'),
               types.InlineKeyboardButton('Beagle', callback_data='type_beagle'),
               types.InlineKeyboardButton('Poodle', callback_data='type_poodle'))
    markup.row(types.InlineKeyboardButton('Australian Shepherd', callback_data='type_australian shepherd'),
               types.InlineKeyboardButton('Maltese', callback_data='type_maltese'),
               types.InlineKeyboardButton('Labrador', callback_data='type_labrador'))
    markup.row(types.InlineKeyboardButton('Other', callback_data='type_other'))

    bot.send_message(chat_id, "What type of dog is this?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))
def dog_type_callback(call):
    dog_type = call.data.replace('type_', '')
    user_states[call.message.chat.id]['dog_type'] = dog_type
    ask_dog_color(call.message.chat.id)

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
    # user_states[call.message.chat.id]['dog_color'] = dog_color
    # save_user_data(call.message.chat.id)
    bot.send_message(call.message.chat.id, "Thank you for providing the information! You can share now another picture")
#

def save_user_data(chat_id):
    # Get user data from the state
    user_data = user_states.get(chat_id, {})

    # Create a dictionary to store user information
    user_info = {
        'name': user_data.get('user_name', 'Unknown'),
        'dog_type': user_data.get('dog_type', 'Unknown'),
        'dog_color': user_data.get('dog_color', 'Unknown'),
    }

    # Load existing user data
    with open(user_data_file, 'r') as f:
        all_user_data = json.load(f)

    # Add the new user information
    all_user_data[chat_id] = user_info

    # Save the updated user data to the JSON file
    with open(user_data_file, 'w') as f:
        json.dump(all_user_data, f, indent=4)

# def save_user_states():
#     with open(json_file_path, 'w') as json_file:
#         json.dump(user_states, json_file, indent=4)
#

# Start the bot
# bot.polling()
bot.infinity_polling()
