import telebot
from telebot import types
from PIL import Image
from io import BytesIO
import pymongo

TOKEN = '6531156662:AAFUwyas9FqJTFoRICmFB55j3l9-4asoXH4'

bot = telebot.TeleBot(TOKEN)

# check if need to use this for saving the pictures
# client = pymongo.MongoClient('YOUR_CONNECTION_STRING')
# db = client['image_database']
# images_collection = db['images']


@bot.message_handler(commands=['start', 'hello', 'hey'])
def send_welcome(message):
    # user_name = message.from_user.first_name
    # bot.reply_to(message, "Hello" + name )
    bot.reply_to(message, "Hello! I'm your chatbot. I'd like you to upload a picture of a dog")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "I'm here to create a data set from the pictures I'm collecting! Please send me a dog picture")

@bot.message_handler(func=lambda message: True)
def handle_responses(message):
    try:
        user_response = message.text.lower()

        if user_response == 'hello':
            bot.reply_to(message, "Hey there! How are you?")
        elif user_response == 'how are you?':
            bot.reply_to(message, "I'm just a bot, but thanks for asking!")
        else:
            bot.reply_to(message, "I'm here to receive your dog image! Feel free to ask me anything else.")
    except Exception as e:
        # Handle the error gracefully
        bot.reply_to(message, "Oops! Something went wrong. Please try again later.")


# @bot.message_handler(content_types=['photo'])
# def handle_images(message):
#     image_file_id = message.photo[-1].file_id
#
#     image_data = bot.download_file(bot.get_file(image_file_id).file_path)
#
#     image = Image.open(BytesIO(image_data))
#
#     image_filename = f'image_{message.from_user.id}.jpg'
#     image.save(image_filename)
#
#     images_collection.insert_one({
#         'user_id': message.from_user.id,
#         'file_id': image_file_id,
#         'file_name': image_filename
#     })
#     bot.reply_to(message, "Image received and saved! Thank you!")


bot.polling()

