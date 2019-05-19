import datetime

import dateutil.parser
import pytz
import telegram

import database
import gauth
import gcalendar


def get_menu():
    buttons = [["/plan", "/get_today_tasks"], ["/logout"]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    return reply_markup


def text_callback(update, context):
    reply_markup = telegram.ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True)
    if "state" in context.user_data:
        if context.user_data["state"] == "summary":
            context.user_data["state"] = "date"
            context.user_data["summary"] = update.message.text
            context.bot.send_message(chat_id=update.message.chat_id, text="Введите дату в формате ГГГГ-ММ-ДД",
                                     reply_markup=reply_markup)
        elif context.user_data["state"] == "date":
            context.user_data["state"] = "time"
            # TODO: check if it is correct date
            context.user_data["date"] = update.message.text
            context.bot.send_message(chat_id=update.message.chat_id, text="Введите время события",
                                     reply_markup=reply_markup)
        elif context.user_data["state"] == "time":
            gcalendar.set_new_task(update.message.chat_id, update.message.text, context.user_data["date"],
                                   context.user_data["summary"])
            context.bot.send_message(chat_id=update.message.chat_id, text="Задача успешно добавлена",
                                     reply_markup=get_menu())
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Команда не распознана", reply_markup=get_menu())


def plan_callback(update, context):
    context.user_data["state"] = "summary"
    reply_markup = telegram.ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text="Введите текст для задачи.",
                             reply_markup=reply_markup)


def back_callback(update, context):
    pass


def cancel_callback(update, context):
    context.user_data.clear()
    context.bot.send_message(chat_id=update.message.chat_id, text="Выберете команду", reply_markup=get_menu())


def logout_callback(update, context):
    db = database.Database()
    chat_id = update.message.chat_id
    db.delete_cred(chat_id)
    start_callback(update, context)


def get_today_tasks_callback(update, context):
    chat_id = update.message.chat_id
    db = database.Database()
    if db.is_auth(chat_id):
        response = gcalendar.get_today_tasks_list(chat_id)
        if not response:
            context.bot.send_message(chat_id=chat_id, text="Ваш день сегодня свободен. Везет же)",
                                     reply_markup=get_menu())
        else:
            text = "События на сегодня: \n"
            counter = 1
            for event in response:
                text = text + str(counter) + ". " + event["start"].get("dateTime", event['start'].get('date')) + "\n"
                text = text + event["summary"] + "\n"
                counter += 1
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
        reply_markup = telegram.ReplyKeyboardMarkup([["/login"]], resize_keyboard=True)
        # TODO : strange behavior with /login twice
        context.bot.send_message(chat_id=chat_id, text=googleAuth.generate_url(), reply_markup=reply_markup)


def start_callback(update, context):
    args = "".join(context.args)
    if args == "":
        reply_markup = telegram.ReplyKeyboardMarkup([["/login"]], resize_keyboard=True)
        context.bot.send_message(chat_id=int(update.message.chat_id),
                                 text="Здравствуйте! Вам нужно войти в свой аккаунт Google для использования этого бота",
                                 reply_markup=reply_markup)
    else:
        db = database.Database()
        chat_id = args
        if db.is_auth(chat_id):
            context.bot.send_message(chat_id=int(chat_id), text="Вы успешно вошли в аккаунт", reply_markup=get_menu())
            context.job_queue.run_daily(daily_announce, datetime.time(hour=8, minute=0, second=0,
                                                                      tzinfo=pytz.timezone("Europe/Moscow")))
        else:
            reply_markup = telegram.ReplyKeyboardMarkup([["/login"]], resize_keyboard=True)
            context.bot.send_message(chat_id=int(chat_id), text="Вам необходимо войти в аккаунт. Используйте /login",
                                     reply_markup=reply_markup)


def daily_announce(bot, job):
    # TODO: Repeating code
    chat_id = job.context
    db = database.Database()
    if db.is_auth(chat_id):
        bot.send_message(chat_id=chat_id, text="Доброе утро!")
        response = gcalendar.get_today_tasks_list(chat_id)
        if not response:
            bot.send_message(chat_id=chat_id, text="Ваш день сегодня свободен. Везет же)",
                             reply_markup=get_menu())
        else:
            text = "События на сегодня: \n"
            counter = 1
            # TODO: add enumerate
            for event in response:
                date = dateutil.parser.parse(event["start"].get("dateTime", event['start'].get('date')))
                text = text + str(counter) + ". {}:{}".format(date.time().hour, date.time().minute) + + "\n"
                text = text + event["summary"] + "\n"
                counter += 1
            bot.send_message(chat_id=chat_id, text=text, reply_markup=get_menu())
