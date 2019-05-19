import logging
import os

import telegram.ext

from callbacks import text_callback, login_callback, start_callback, logout_callback, get_today_tasks_callback, \
    plan_callback, cancel_callback

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = os.environ["TOKEN"]
SECRET_CLIENT = os.environ["SECRET_TOKEN"]
with open("client_secret.json", "w") as f:
    print(SECRET_CLIENT, file=f)

PORT = int(os.environ.get('PORT', '8443'))
updater = telegram.ext.Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, text_callback))
dispatcher.add_handler(telegram.ext.CommandHandler('login', login_callback))
dispatcher.add_handler(telegram.ext.CommandHandler("start", start_callback, pass_args=True))
dispatcher.add_handler(telegram.ext.CommandHandler("logout", logout_callback))
dispatcher.add_handler(telegram.ext.CommandHandler("get_today_tasks", get_today_tasks_callback))
dispatcher.add_handler(telegram.ext.CommandHandler("plan", plan_callback))
dispatcher.add_handler(telegram.ext.CommandHandler("cancel", cancel_callback))
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://yet-another-task-bot.herokuapp.com/" + TOKEN)
updater.idle()
