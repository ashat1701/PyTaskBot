import datetime
import logging

import google.oauth2.credentials
import googleapiclient.discovery
import pytz

import database


def get_today_tasks_list(chat_id):
    db = database.Database()
    creds_dict = db.get_cred(chat_id)
    del creds_dict["chat_id"]
    logging.info("Get new task list request{}".format(creds_dict))
    credentials = google.oauth2.credentials.Credentials(**creds_dict)
    calendar = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)
    # TODO: fix this for other UTC
    date = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    today = datetime.datetime.combine(datetime.date(date.year, date.month, date.day), datetime.datetime.min.time())
    start_of_day = today.isoformat() + '+03:00'
    end = datetime.datetime.combine(datetime.date(date.year, date.month, date.day), datetime.datetime.max.time())
    end_of_day = end.isoformat() + '+03:00'
    events_result = calendar.events().list(calendarId="primary", singleEvents=True, orderBy='startTime',
                                           timeMin=start_of_day, timeMax=end_of_day).execute()
    events = events_result.get('items', [])
    if not events:
        return False
    else:
        return events


def set_new_task(chat_id, time, date, summary):
    db = database.Database()
    creds_dict = db.get_cred(chat_id)
    del creds_dict["chat_id"]
    credentials = google.oauth2.credentials.Credentials(**creds_dict)
    calendar = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)
    event = {
        'summary': summary,
        'start': {
            'dateTime': date + "T" + time + ":00+03:00",
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': date + "T" + time + ":00+03:00",
            'timeZone': 'Europe/Moscow',
        },
    }
    calendar.events().insert(calendarId="primary", body=event).execute()
