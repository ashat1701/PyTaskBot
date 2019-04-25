import telegram
import database
import gauth
import gcalendar


def get_menu():
    buttons = [["/plan", "/get_today_tasks"], ["/logout"]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    return reply_markup


# TODO: delete this after debug
def echo_callback(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def logout_callback(update, context):
    db = database.Database()
    chat_id = update.message.chat_id
    db.delete_cred(chat_id)
    start_callback(update, context)


def get_today_tasks(update, context):
    chat_id = update.message.chat_id
    db = database.Database()
    if db.is_auth(chat_id):
        response = gcalendar.get_today_tasks_list(chat_id)
        if response is str:
            context.bot.send_message(chat_id=chat_id, text=response, reply_markup=get_menu())
        else:
            text = "Events for today: \n"
            counter = 1
            for event in response:
                text = text + str(counter) + ". " + event["start"].get("dateTime", event['start'].get('date')) + "\n"
                text = text + event["summary"] + "\n"
            context.bot.send_message(chat_id=chat_id, text=text, reply_markup=get_menu())
    else:
        reply_markup = telegram.ReplyKeyboardMarkup([["/login"]], resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="Вам необходимо войти в аккаунт. Используйте /login",
                                 reply_markup=reply_markup)


def login_callback(update, context):
    db = database.Database()
    chat_id = update.message.chat_id
    if db.is_auth(chat_id):
        context.bot.send_message(chat_id=chat_id, text="Вы уже вошли в свой аккаунт.", reply_markup=get_menu())
    else:
        googleAuth = gauth.GoogleAuth(chat_id)
        context.bot.send_message(chat_id=chat_id, text=googleAuth.generate_url())


def start_callback(update, context):
    args = "".join(context.args)
    if args == "":
        reply_markup = telegram.ReplyKeyboardMarkup([["/login"]], resize_keyboard=True)
        context.bot.send_message(chat_id=int(update.message.chat_id), text="Здравствуйте! Вам нужно войти в свой аккаунт Google для использования этого бота", reply_markup=reply_markup)
    else:
        db = database.Database()
        chat_id = args
        if db.is_auth(chat_id):
            context.bot.send_message(chat_id=int(chat_id), text="Вы успешно вошли в аккаунт", reply_markup=get_menu())
        else:
            reply_markup = telegram.ReplyKeyboardMarkup([["/login"]], resize_keyboard=True)
            context.bot.send_message(chat_id=int(chat_id), text="Вам необходимо войти в аккаунт. Используйте /login", reply_markup=reply_markup)
