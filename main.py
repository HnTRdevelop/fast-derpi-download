import telebot
import requests


BOT_TOKEN = "6183217757:AAHmq_mJFKGAl72oZAD8VjcX-ncUglHQNKs"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=["photo"])
def give_image(message):
    print("-"*15)
    print(f"Image from: {message.chat.username}")
    print(f"Chat ID: {message.chat.id}\tMessage ID: {message.id}\n")

    tries = 15
    for t in range(tries):
        link = message.caption.split(" ")[0]
        print(f"Image page link: {link}")
        photo_page = requests.get(link).text

        start_index = photo_page.find("download") - 25
        end_index = 0
        for i in range(start_index, len(photo_page)):
            if photo_page[i] == "\"":
                end_index = i
                break
        download_link = photo_page[start_index:end_index]
        print(f"Image download link: {download_link}")

        print(f"Downloading image...")
        response = requests.get(download_link)
        image = response.content
        if response.status_code != 200:
            print(f"Failed to download image! Retrying... {'' if t == 0 else t}")
            continue
        print(f"Image ready!")

        print(f"Sending image to: {message.chat.username}...")
        filename = download_link[download_link.rfind("/") + 1:]
        bot.send_document(chat_id=message.chat.id,
                          document=image,
                          reply_to_message_id=message.id,
                          visible_file_name=filename)

        break
    else:
        print(f"Failed to download image for {message.chat.username}")
    print(f"Image for {message.chat.username} done!")
    print("-"*15, end="\n\n")


print("Bot ready!")
bot.infinity_polling()
