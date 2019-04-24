import telegram.ext
import os
import logging
import database
import auth

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# TODO: delete this after debug
def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def login(update, context):
    db = database.Database()
    chat_id = update.message.chat_id
    if db.is_auth(chat_id):
        context.bot.send_message(chat_id=chat_id, text="Вы уже вошли в свой аккаунт.")
    else:
        googleAuth = auth.GoogleAuth(chat_id)
        context.bot.send_message(chat_id=chat_id, text=googleAuth.generate_url())


def start_callback(update, context):
    args = "".join(context.args)
    if args == "":
        reply_markup = telegram.ReplyKeyboardMarkup(["Login"])
        context.bot.send_message(chat_id=int(update.message.chat_id), text="Здравствуйте! Вам нужно войти в свой аккаунт Google для использования этого бота", reply_markup=reply_markup)
    else:
        db = database.Database()
        chat_id = args
        if db.is_auth(chat_id):
            context.bot.send_message(chat_id=int(chat_id), text="Вы успешно вошли в аккаунт")
        else:
            context.bot.send_message(chat_id=int(chat_id), text="Вам необходимо войти в аккаунт. Используйте /login")



TOKEN = os.environ["TOKEN"]
PORT = int(os.environ.get('PORT', '8443'))
updater = telegram.ext.Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, echo))
dispatcher.add_handler(telegram.ext.CommandHandler('login', login))
dispatcher.add_handler(telegram.ext.CommandHandler("start", start_callback, pass_args=True))
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://yet-another-task-bot.herokuapp.com/" + TOKEN)

updater.idle()