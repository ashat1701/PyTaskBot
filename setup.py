import telegram.ext
import os
import webserver
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
webserver.init()


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


TOKEN = os.environ["TOKEN"]
PORT = int(os.environ.get('PORT', '8443'))
updater = telegram.ext.Updater(token=TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, echo))
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://yet-another-task-bot.herokuapp.com/" + TOKEN)

updater.idle()