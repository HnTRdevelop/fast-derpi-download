import telebot
import requests


BOT_TOKEN = "6183217757:AAHmq_mJFKGAl72oZAD8VjcX-ncUglHQNKs"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=["photo"])
def give_image(message):
    print(f"image from: {message.chat.username}")

    link = message.caption.split(" ")[0]
    print(f"photo page link: {link}")
    photo_page = requests.get(link).text
    
    start_index = photo_page.find("download") - 25
    end_index = 0
    for i in range(start_index, len(photo_page)):
        if photo_page[i] == "\"":
            end_index = i
            break
    download_link = photo_page[start_index:end_index]
    print(f"photo download link: {download_link}")

    print(f"downloading image...")
    image = requests.get(download_link).content
    print(f"image ready!")

    print(f"sending image to: {message.chat.username}...")
    filename = download_link[download_link.rfind("/") + 1:]
    bot.send_document(chat_id=message.chat.id, document=image, reply_to_message_id=message.id, visible_file_name=filename)

    print(f"DONE!!!")


bot.infinity_polling()