import json
import os
import telebot


TOKEN = '6531156662:AAFUwyas9FqJTFoRICmFB55j3l9-4asoXH4'
bot = telebot.TeleBot(TOKEN)
# SAVE_FOLDER = '/C:/Users/User/PycharmProjects/Project/Images'
SAVE_FOLDER = 'images'
METADATA_FILE = 'metadata.json'

user_states = {}
user_data = {}


@bot.message_handler(commands=['start', 'hello', 'hey'])
def send_welcome(message):
    user_name = message.from_user.first_name
    # bot.reply_to(message, "Hello" + name )
    bot.reply_to(message, "Hello! I'm your chatbot. please upload a picture of a dog")


def save_metadata(user_id, metadata):
    user_metadata = {}

    # Load existing metadata if available
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as json_file:
            user_metadata = json.load(json_file)

    # Update metadata for the specific user
    user_metadata[user_id] = metadata

    # Save updated metadata to JSON
    with open(METADATA_FILE, 'w') as json_file:
        json.dump(user_metadata, json_file, indent=4)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_type')
def handle_dog_type(message):
    dog_type = message.text
    bot.reply_to(message, "Got it! What color is the dog?")
    user_states[message.chat.id] = 'awaiting_color'
    user_data[message.chat.id] = {'type': dog_type}


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_color')
def handle_dog_color(message):
    dog_color = message.text
    bot.reply_to(message, "Thank you for providing the information about the dog!")

    # Retrieve the stored type from user_data
    dog_type = user_data.get(message.chat.id, {}).get('type', None)

    # Save metadata to JSON
    metadata = {
        'type': dog_type,
        'color': dog_color,
    }
    save_metadata(message.chat.id, metadata)

    user_states[message.chat.id] = 'start'


@bot.message_handler(content_types=['photo'])
def handle_images(message):
    try:
        # Get the photo's file_id and file_path
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Download the image
        image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        image_filename = f"image_{message.chat.id}_{file_id}.jpg"
        full_path = os.path.join(SAVE_FOLDER, image_filename)
        with open(full_path, 'wb') as image_file:
            image_file.write(bot.download_file(image_url))

        bot.reply_to(message, "Image and metadata saved successfully!")
    except Exception as e:
        bot.reply_to(message, "Oops! An error occurred while saving the image and metadata. Please try again later.")


bot.infinity_polling()