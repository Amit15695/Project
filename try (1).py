# import json
# import os
# import telebot
# from telebot import types
# from PIL import Image
# from io import BytesIO
#
# TOKEN = '6531156662:AAFUwyas9FqJTFoRICmFB55j3l9-4asoXH4'
# bot = telebot.TeleBot(TOKEN)
# SAVE_FOLDER = '/C:/Users/User/PycharmProjects/Project/Images'
#
# METADATA_FILE = 'metadata.json'
#
# user_states = {}
#
# @bot.message_handler(commands=['start', 'hello', 'hey'])
# def send_welcome(message):
#     user_name = message.from_user.first_name
#     # bot.reply_to(message, "Hello" + name )
#     bot.reply_to(message, "Hello! I'm your chatbot. please upload a picture of a dog")
#
# # @bot.message_handler(func=lambda message: True)
# # def echo_message(message):
# #     bot.reply_to(message, "I'm here to create a data set from the pictures I'm collecting! ")
# #
# # @bot.message_handler(func=lambda message: True)
# # # //maybe add here more options for us
# # def handle_responses(message):
# #     try:
# #         user_response = message.text.lower()
# #
# #         if user_response == 'hello':
# #             bot.reply_to(message, "Hey there! How are you?")
# #         elif user_response == 'how are you?':
# #             bot.reply_to(message, "I'm just a bot, but thanks for asking!")
# #         else:
# #             bot.reply_to(message, "I'm here to recieve your dog image! Feel free to ask me anything else.")
# #     except Exception as e:
# #         # Handle the error gracefully
# #         bot.reply_to(message, "Oops! Something went wrong. Please try again later.")
#
# # old one
# # @bot.message_handler(content_types=['photo'])
# # def handle_images(message):
# #     # Handle the image
# #     bot.reply_to(message, "Thank you for sharing this image with me, it's a cute dog! 🐶")
# #     bot.send_message(message.chat.id, "What type of dog is it?")
# #     user_states[message.chat.id] = 'awaiting_type'
# #
# # @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_type')
# # def handle_dog_type(message):
# #     bot.reply_to(message, "Got it! And what color is the dog?")
# #     user_states[message.chat.id] = 'awaiting_color'
# #
# # @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_color')
# # def handle_dog_color(message):
# #     bot.reply_to(message, "Thank you for providing the information about the dog!")
# #     user_states[message.chat.id] = 'start'
#
# # new one
# # @bot.message_handler(content_types=['photo'])
# # def handle_images(message):
# #     # Handle the image
# #     bot.reply_to(message, "Thank you for sharing this image with me, it's a cute dog! 🐶")
# #     bot.send_message(message.chat.id, "What type of dog is it?")
# #     user_states[message.chat.id] = 'awaiting_type'
#
#
# @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_type')
# def handle_dog_type(message):
#     dog_type = message.text
#     bot.reply_to(message, "Got it! And what color is the dog?")
#     user_states[message.chat.id] = 'awaiting_color'
#
# @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_color')
# def handle_dog_color(message):
#     dog_color = message.text
#     bot.reply_to(message, "Thank you for providing the information about the dog!")
#     user_states[message.chat.id] = 'start'
#
#
#
# @bot.message_handler(content_types=['photo'])
# def handle_images(message):
#     try:
#         # Get the photo's file_id and file_path
#         photo = message.photo[-1]
#         file_id = photo.file_id
#         file_info = bot.get_file(file_id)
#         file_path = file_info.file_path
#
#         # Download the image
#         image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
#         image_filename = f"image_{message.chat.id}_{file_id}.jpg"
#         full_path = os.path.join(SAVE_FOLDER, image_filename)
#         with open(full_path, 'wb') as image_file:
#             image_file.write(bot.download_file(image_url))
#
#         # Save metadata to JSON
#         metadata = {
#             'file_id': file_id,
#             'type': None,
#             'color': None,
#         }
#         save_metadata(metadata)
#
#         bot.reply_to(message, "Image and metadata saved successfully!")
#     except Exception as e:
#         bot.reply_to(message, "Oops! An error occurred while saving the image and metadata. Please try again later.")
#
#
# def save_metadata(metadata):
#     with open(METADATA_FILE, 'w') as json_file:
#         json.dump(metadata, json_file, indent=4)
#
#
#
#
# # @bot.message_handler(content_types=['photo'])
# # def handle_images(message):
# #     # Get the photo's file_id and file_path
# #     photo = message.photo[-1]  # Get the largest available photo
# #     file_id = photo.file_id
# #     file_info = bot.get_file(file_id)
# #     file_path = file_info.file_path
# #
# #     # Download the image
# #     image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
# #     image_filename = f"image_{message.chat.id}_{file_id}.jpg"  # Customize the filename
# #     full_path = os.path.join(SAVE_FOLDER, image_filename)  # Combine folder and filename
# #
# #     with open(full_path, 'wb') as image_file:
# #         image_file.write(bot.download_file(image_url))
# #
# #     bot.reply_to(message, "Image received and saved! Thank you!")
# #     bot.send_message(message.chat.id, "Oh, it's a cute dog! 🐶")
#
#
# bot.infinity_polling()
# # bot.polling()
#
#
